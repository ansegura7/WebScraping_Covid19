# -*- coding: utf-8 -*-
"""
    Created By: Andres Segura Tinoco
    Created On: Apr 10, 2020
    Description: Web scraping to obtain daily data on confirmed cases and deaths of Covid-19
    Source: https://www.worldometers.info/coronavirus/
"""

# Import custom libraries
import util_lib as ul

# Import util libraries
import logging
import pytz
from pytz import timezone
from datetime import datetime

# Email libraries
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Database libraries
import pyodbc

# Import Web Scraping libraries
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

# DB function - Get email server credentials
def get_email_credentials():
    yaml_path = 'config\email.yml'
    email_login = ul.get_dict_from_yaml(yaml_path)
    return email_login

# Util function - Generic function that sends an email via SMTP
def smtp_send_email(msg):
    result = False
    
    try:
        # Read SMTP server credentials
        email_login = get_email_credentials()
        server_name = email_login['server']
        port = email_login['port']
        sent_from = email_login['account']
        password = email_login['password']
        context = ssl.create_default_context()

        # Send SMTP email        
        with smtplib.SMTP_SSL(server_name, port, context=context) as server:
            server.login(sent_from, password)
            server.send_message(msg)
            result = True
        
    except smtplib.SMTPException as e:
        print(' - Error sending SMTP email: ' + str(e))
        logging.error(' - Error sending SMTP email: ' + str(e))
    
    except Exception:
        print(' - Generic SMTP error')
        logging.error(' - Generic SMTP error')
    
    return result

# DB function - Get database credentials
def get_db_credentials():
    yaml_path = 'config\database.yml'
    db_login = ul.get_dict_from_yaml(yaml_path)
    return db_login

# DB function - Returns the country list
def get_country_list(db_login):
    country_list = []
    
    # Get database connection
    cnxn = pyodbc.connect(driver=db_login['driver'], server=db_login['server'], database=db_login['database'], trusted_connection=db_login['trusted_connection'])
    
    try:
        cursor = cnxn.cursor()
        
        # Countries with more daily data 
        query = '''
                SELECT [name]
                  FROM [dbo].[country_info]
                 ORDER BY [name];
                '''
        
        dt = cursor.execute(query).fetchall()
        for row in dt:
            country = row[0]
            country_list.append(country)
        
    except pyodbc.DatabaseError as e:
        logging.error(' - Pyodbc error: ' + str(e))
    finally:
        cursor.close()
    
    return country_list

# DB function - Merge a list records in the MS SQL Server table
def merge_data(db_login, record_list):
    result = False
    
    if len(record_list) == 0:
        logging.info(' - No data to save')
        return result
    else:
        logging.info(' - Total data: ' + str(len(record_list)))
    
    # Get database connection
    cnxn = pyodbc.connect(driver=db_login['driver'], server=db_login['server'], database=db_login['database'], trusted_connection=db_login['trusted_connection'])
    
    try:
        cursor = cnxn.cursor()
        
        # Initial number of records 
        query = 'SELECT COUNT(*) AS [count] FROM [dbo].[covid19_data];'
        n_init = cursor.execute(query).fetchone()
        n_init = int(n_init[0])
        
        # Merge many rows
        query = '''
                   MERGE [dbo].[covid19_data] AS a USING (
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ) AS vals ([country],[total_cases],[total_deaths],[total_recovered],[active_cases],
                              [serious_critical],[tot_cases_1m_pop],[deaths_1m_pop],[total_tests],[tests_1m_pop],[datestamp])
                   ON a.[country] = vals.[country] AND
                      a.[total_cases] = vals.[total_cases] AND
                      a.[total_deaths] = vals.[total_deaths] AND
                      a.[total_recovered] = vals.[total_recovered] AND
                      a.[active_cases] = vals.[active_cases] AND
                      a.[serious_critical] = vals.[serious_critical] AND
                      a.[tot_cases_1m_pop] = vals.[tot_cases_1m_pop] AND
                      a.[deaths_1m_pop] = vals.[deaths_1m_pop] AND
                      a.[total_tests] = vals.[total_tests] AND
                      a.[tests_1m_pop] = vals.[tests_1m_pop]
                   WHEN NOT MATCHED THEN
                       INSERT ([country],[datestamp],[total_cases],[total_deaths],[total_recovered],[active_cases],
                               [serious_critical],[tot_cases_1m_pop],[deaths_1m_pop],[total_tests],[tests_1m_pop])
                       VALUES (vals.[country],vals.[datestamp],vals.[total_cases],vals.[total_deaths],vals.[total_recovered],vals.[active_cases],
                               vals.[serious_critical],vals.[tot_cases_1m_pop],vals.[deaths_1m_pop],vals.[total_tests],vals.[tests_1m_pop]);
                '''
        
        cnxn.autocommit = False
        cursor.fast_executemany = True
        cursor.executemany(query, record_list)
        
    except pyodbc.DatabaseError as e:
        cnxn.rollback()
        logging.error(' - Pyodbc error: ' + str(e))
    else:
        cnxn.commit()
        
        # Final number of records
        query = 'SELECT COUNT(*) AS [count] FROM [dbo].[covid19_data];'
        n_final = cursor.execute(query).fetchone()
        n_final = int(n_final[0])
        
        logging.info(' - Data stored in the database: ' + str(n_final - n_init))
        result = (n_final > n_init)
    finally:
        cnxn.autocommit = True
        cursor.close()
    
    return result

# DB function - Generate current data as a CSV file
def generate_current_data(db_login):
    result = False
    
    # Get database connection
    cnxn = pyodbc.connect(driver=db_login['driver'], server=db_login['server'], database=db_login['database'], trusted_connection=db_login['trusted_connection'])
    
    try:
        cursor = cnxn.cursor()
        
        # Current data by country sorted by total_deaths
        query = '''
                SELECT ROW_NUMBER() OVER(ORDER BY total_deaths DESC, total_cases DESC) AS [row_index], country, CONVERT(varchar, [date], 101) AS [date], total_cases, 
                	   total_deaths, total_recovered, active_cases, serious_critical, tot_cases_1m_pop, deaths_1m_pop, total_tests, tests_1m_pop, [datestamp]
                  FROM [dbo].[v_current_covid19_data];
                '''
        
        dt = cursor.execute(query).fetchall()
        
    except pyodbc.DatabaseError as e:
        logging.error(' - Pyodbc error: ' + str(e))
    else:
        
        # Save data table (list format) to CSV file
        filename = '../data/current_data.csv'
        header = [column[0] for column in cursor.description]
        result = ul.save_data_to_csv(dt, filename, header)
        
        if result:
            logging.info(' - Current data saved in CSV file')
        else:
            logging.info(' - Current data CSV file not created')
        
    finally:
        cursor.close()
        
    return result

# DB function - Generate historical data as a CSV file
def generate_historical_data(db_login):
    result = False
    
    # Get database connection
    cnxn = pyodbc.connect(driver=db_login['driver'], server=db_login['server'], database=db_login['database'], trusted_connection=db_login['trusted_connection'])
    
    try:
        cursor = cnxn.cursor()
        
        # Historical data by country sorted by total_deaths
        query = '''
                WITH [c19_data] AS (
                	SELECT [country], [region], [subregion], [total_cases], [total_deaths], ISNULL([total_recovered], 0) AS [total_recovered], [active_cases], ISNULL([serious_critical], 0) AS [serious_critical], 
                           ISNULL([tot_cases_1m_pop], 0) AS [tot_cases_1m_pop], ISNULL([deaths_1m_pop], 0) AS [deaths_1m_pop], ISNULL([total_tests], 0) AS [total_tests], 
                           ISNULL([tests_1m_pop], 0) AS [tests_1m_pop], CONVERT(varchar, [date], 101) AS [date], 
                           CAST((CASE WHEN total_cases > 0 THEN 100.0 * total_deaths / total_cases ELSE 0 END) AS numeric(5, 2)) AS [perc_deaths],
                           CAST((CASE WHEN total_tests > 0 THEN 100.0 * total_cases / total_tests ELSE 0 END) AS numeric(5, 2)) AS [perc_infection],
                		   CAST((CASE WHEN total_cases > 0 THEN 100.0 * ISNULL(total_recovered, 0) / total_cases ELSE 0 END) AS numeric(5, 2)) AS [perc_recovered],
                           ISNULL([diff_total_cases], 0) AS [diff_total_cases],
                           ISNULL([diff_total_deaths], 0) AS [diff_total_deaths],
                           ISNULL([diff_total_recovered], 0) AS [diff_total_recovered]
                	  FROM [dbo].[v_daily_covid19_data] AS cd
                	 INNER JOIN
                		   [dbo].[country_info] AS ci
                	    ON cd.[country] = ci.[name]
                )
                SELECT [country], [region], [subregion], [date], ROW_NUMBER() OVER(PARTITION BY [date] ORDER BY [total_deaths] DESC) AS [row_index],
                	   [total_cases], [total_deaths], [total_recovered], [active_cases], [serious_critical], [total_tests], [tot_cases_1m_pop], [deaths_1m_pop],
                	   [tests_1m_pop], [perc_deaths], [perc_infection], [perc_recovered], [diff_total_cases], [diff_total_deaths], [diff_total_recovered]
                  FROM [c19_data]
                 ORDER BY [date], [country];
                '''
        
        dt = cursor.execute(query).fetchall()
        
    except pyodbc.DatabaseError as e:
        logging.error(' - Pyodbc error: ' + str(e))
    else:
        # Save data table (list format) to CSV file
        filename = '../data/historical_data.csv'
        header = [column[0] for column in cursor.description]
        result = ul.save_data_to_csv(dt, filename, header)
        
        if result:
            logging.info(' - Historical data saved in CSV file')
        else:
            logging.info(' - Historical data CSV file not created')
            
    finally:
        cursor.close()
        
    return result

# Send notification email function
def send_notification_email(country_list):
    
    # Create a message
    msg = MIMEMultipart()
    
    # Setup the parameters of the message
    msg['From'] = 'DevOps <ansegura.col@gmail.com>'
    msg['To'] = 'Segura Andres <seguraandres7@gmail.com>'
    msg['Subject'] = 'DevOps - New Country'
    
    # Add in the message body
    message = 'Daily data was saved for new countries.\nBasic information for the following countries should be added: %s' % ', '.join(country_list)
    msg.attach(MIMEText(message, 'plain'))
    
    # Sending email
    result = smtp_send_email(msg)
    
    return result

curr_table = None

# Find the index of the variables in the table header
def get_variables_index(header):
    vars_ix = {
        'country': 1, 
        'total_cases': 2, 
        'total_deaths': 4,
        'total_recovered': 6,
        'active_cases': 7,
        'serious_critical': 8,
        'tot_cases_1m_pop': 9,
        'deaths_1m_pop': 10,
        'total_tests': 11,
        'tests_1m_pop': 12
    }
    vars_name = {
        'country': 'country,other', 
        'total_cases': 'totalcases', 
        'total_deaths': 'totaldeaths',
        'total_recovered': 'totalrecovered',
        'active_cases': 'activecases',
        'serious_critical': 'serious,critical',
        'tot_cases_1m_pop': 'totcases/1m pop',
        'deaths_1m_pop': 'deaths/1m pop',
        'total_tests': 'totaltests',
        'tests_1m_pop': 'tests/1m pop'
    }
    
    cols = header.findAll('th')
    if len(cols):
        vars_list = [ul.dq_clean_html_text(col.text).lower() for col in cols]
        
        for k, v in vars_name.items():
            if v in vars_list:
                ix = vars_list.index(v)
                vars_ix[k] = ix
            else:
                logging.info(' - Warning: variable %s was not found in the header' % k)
    
    return vars_ix

# Web Scraping function
def web_scraping_data(db_login):
    record_list = []
    
    # Datetime with local TimeZone
    local_tz = timezone(pytz.country_timezones['co'][0])
    
    # Web data vars
    url = 'https://www.worldometers.info/coronavirus/'
    doc_format = 'lxml'
    id_main_table = 'main_table_countries_today'
    
    # Get country list
    country_list = get_country_list(db_login)
    new_country_list = []
    
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url, headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, doc_format)
        logging.info(' - The document was read')
        
    except HTTPError as e:
        logging.error(' - Error: ' + str(e))
        
    except URLError:
        logging.error(' - Server down or incorrect domain')
        
    else:
        # Find today main table
        curr_table = soup.find('table', {'id': id_main_table})
        
        # Get data
        if curr_table != None:
            logging.info(' - Getting data')
            rows = curr_table.findAll('tr')
            
            if len(rows):
                vars_ix = get_variables_index(rows[0])
                
                for row in rows:
                    cols = row.findAll('td')
                    
                    # Validation to make sure it is a row with country data
                    if len(cols) >= 13 and 'country' in str(cols[vars_ix['country']].a):                            
                        curr_country = cols[vars_ix['country']].a.text.strip()
                        
                        # Create country data
                        record = { 'country': curr_country }
                        for name, ix in vars_ix.items():
                            if name != 'country':
                                record[name] = ul.dq_parse_num(cols[ix].text)
                        record['datestamp'] = local_tz.localize(datetime.now()).isoformat()
                        
                        # Save country data
                        record_list.append(list(record.values()))
                        
                        # If it's a new country...
                        if curr_country not in country_list:
                            new_country_list.append(curr_country)
                
                logging.info(' - The data was found')
            else:
                logging.info(' - The data was not found')
        
        # Log new country list
        if len(new_country_list):
            country_string = ', '.join(new_country_list)
            send_notification_email(new_country_list)
            logging.info(' - Data was saved for new countries: ' + country_string)
    
    # Return data
    return record_list

#####################
### Start Program ###
#####################
logging.basicConfig(filename="log/log_file.log", level=logging.INFO)
logging.info(">> START PROGRAM: " + str(datetime.now()))

# 1. Get database credentials
db_login = get_db_credentials()

# 2. Get last data
data = web_scraping_data(db_login)

# 3. Store data
result = merge_data(db_login, data)

# 4. Generate derived data
if result:
    generate_current_data(db_login)
    generate_historical_data(db_login)

logging.info(">> END PROGRAM: " + str(datetime.now()))
logging.shutdown()
#####################
#### End Program ####
#####################
