# -*- coding: utf-8 -*-
"""
    Created By: Andres Segura Tinoco
    Created On: Apr 10, 2020
    Description: Web scraping to obtain daily data on confirmed cases and deaths of Covid-19
    Source: https://www.worldometers.info/coronavirus/
"""

# Import util libraries
import logging
import yaml
import csv
from datetime import datetime

# Database libraries
import pyodbc

# Import Web Scraping libraries
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

# Util function - Converts a string to a number (int or float) 
def parse_num(n):
    v = 0
    
    if n == 'N/A':
        v = -1
    else:
        n = n.replace(',', '').replace('+', '').strip()
        
        if '.' in n:
            v = float(n)
        elif n != '':
            v = int(n)
    
    return v

# Util function - Save datatable (list format) to CSV file
def save_dt_to_csv(dt, filename, header):
    result = False

    # Validating data
    if dt and len(dt):
        
        # Saving data in CSV file
        with open(filename, 'w', encoding='utf8', newline='') as f:
            wr = csv.writer(f, delimiter=',')
            wr.writerow(header)
            for row in dt:
                wr.writerow(row)
            result = True
    
    return result

# DB function - Get database credentials
def get_db_credentials():
    db_login = dict()
    yaml_path = 'config\database.yml'
    
    with open(yaml_path) as f:
        yaml_file = f.read()
        db_login = yaml.load(yaml_file, Loader=yaml.FullLoader)
    
    return db_login

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
                SELECT ROW_NUMBER() OVER(ORDER BY total_deaths DESC, country) AS [row_number], country, total_cases, total_deaths, total_recovered, 
                       active_cases, serious_critical, tot_cases_1m_pop, deaths_1m_pop, total_tests, tests_1m_pop, CONVERT(varchar, [date], 101) AS [date]
                  FROM [dbo].[v_current_covid19_data];
                '''
        
        dt = cursor.execute(query).fetchall()
        
    except pyodbc.DatabaseError as e:
        logging.error(' - Pyodbc error: ' + str(e))
    else:
        
        # Save data table (list format) to CSV file
        filename = '../data/current_data.csv'
        header = [column[0] for column in cursor.description]
        result = save_dt_to_csv(dt, filename, header)
            
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
                	SELECT [country], [total_cases], [total_deaths], ISNULL([total_recovered], 0) AS [total_recovered], [active_cases], ISNULL([serious_critical], 0) AS [serious_critical], 
                		   ISNULL([tot_cases_1m_pop], 0) AS [tot_cases_1m_pop], ISNULL([deaths_1m_pop], 0) AS [deaths_1m_pop], ISNULL([total_tests], 0) AS [total_tests], 
                		   ISNULL([tests_1m_pop], 0) AS [tests_1m_pop], CONVERT(varchar, [date], 101) AS [date], 
                		   CAST(CASE WHEN total_cases > 0 THEN 100.0 * total_deaths / total_cases ELSE 0 END AS decimal(5, 2)) AS [perc_deaths],
                		   CAST(CASE WHEN total_tests > 0 THEN 100.0 * total_cases / total_tests ELSE 0 END AS decimal(5, 2)) AS [perc_infection],
                		   [region]
                	  FROM [dbo].[v_daily_covid19_data] AS cd
                	 INNER JOIN
                	       [dbo].[country_info] AS ci
                		ON cd.[country] = ci.[name]
                )
                SELECT [country], [total_cases], [total_deaths], [total_recovered], [active_cases], [serious_critical], [tot_cases_1m_pop], [deaths_1m_pop], [total_tests],  
                       [tests_1m_pop], [date], [perc_deaths], [perc_infection], ROW_NUMBER() OVER(PARTITION BY [date] ORDER BY [total_deaths] DESC) AS [row_index], [region]
                  FROM [c19_data]
                 ORDER BY [date] ASC;
                '''
        
        dt = cursor.execute(query).fetchall()
        
    except pyodbc.DatabaseError as e:
        logging.error(' - Pyodbc error: ' + str(e))
    else:
        # Save data table (list format) to CSV file
        filename = '../data/historical_data.csv'
        header = [column[0] for column in cursor.description]
        result = save_dt_to_csv(dt, filename, header)
                
        if result:
            logging.info(' - Historical data saved in CSV file')
        else:
            logging.info(' - Historical data CSV file not created')
            
    finally:
        cursor.close()
        
    return result

# Web Scraping function
def web_scraping_data():
    record_list = []
    
    # Web data vars
    url = 'https://www.worldometers.info/coronavirus/'
    doc_format = 'lxml'
    id_main_table = 'main_table_countries_today'
    
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
                for row in rows:
                    cols = row.findAll('td')
                    if len(cols) == 13:
                        if 'country' in str(cols[0].a):
                            # print(cols[0].a.text, ',', cols[0].a.get('href'))
                            
                            record = {
                                'country': cols[0].a.text,
                                'total_cases': parse_num(cols[1].text),
                                'total_deaths': parse_num(cols[3].text),
                                'total_recovered': parse_num(cols[5].text),
                                'active_cases': parse_num(cols[6].text),
                                'serious_critical': parse_num(cols[7].text),
                                'tot_cases_1m_pop': parse_num(cols[8].text),
                                'deaths_1m_pop': parse_num(cols[9].text),
                                'total_tests': parse_num(cols[10].text),
                                'tests_1m_pop': parse_num(cols[11].text),
                                'datestamp': datetime.now()
                            }
                            record_list.append(list(record.values()))
                
                logging.info(' - The data was found')
            else:
                logging.info(' - The data was not found')
    
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
data = web_scraping_data()

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
