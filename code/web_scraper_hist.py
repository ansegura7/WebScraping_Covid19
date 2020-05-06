# -*- coding: utf-8 -*-
"""
    Created By: Andres Segura Tinoco
    Created On: Apr 21, 2020
    Description: Web scraping to obtain history data on confirmed cases and deaths of Covid-19
    Source: https://www.worldometers.info/coronavirus/country/
"""

# Import custom libraries
import util_lib as ul

# Import util libraries
import logging
import pytz
from pytz import timezone
from datetime import datetime

# Database libraries
import pyodbc

# Import Web Scraping libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Util function - Apply data quality before saving data
def data_quality(data, top_date):
    new_data = dict()
    
    if len(data) == 2:
        x_data = data['x_data']
        y_data = data['y_data']
        
        for x, y in zip(x_data, y_data):
            x = datetime.strptime((x + ' 2020'), '%b %d %Y')
            if x < top_date:
                new_data[x] = y
    
    return new_data

# Util function - Read the country data from the CSV file and save it in a dictionary
def get_country_data(key_name, val_name):
    country_list = dict()
    
    # CSV file variables
    filename = '../data/country_info.csv'
    ix_key_name = -1
    ix_val_name = -1
    
    # Read country data csv file
    csv_data = ul.read_csv_file(filename)
    
    if len(csv_data):
        for row in csv_data:
            # Get variables index
            if ix_key_name == -1 and ix_val_name == -1:
                if key_name in row:
                    ix_key_name = row.index(key_name)
                if val_name in row:
                    ix_val_name = row.index(val_name)
                
            elif ix_key_name != -1 and ix_val_name != -1:
                # Get data
                k = row[ix_key_name]
                v = row[ix_val_name]
                country_list[k] = v
    
    return country_list

# DB function - Get database credentials
def get_db_credentials():
    yaml_path = 'config\database.yml'
    db_login = ul.get_dict_from_yaml(yaml_path)
    return db_login

# DB function - Get countries with more daily data 
def get_country_data_count(db_login):
    result = dict()
    
    # Get database connection
    cnxn = pyodbc.connect(driver=db_login['driver'], server=db_login['server'], database=db_login['database'], trusted_connection=db_login['trusted_connection'])
    
    try:
        cursor = cnxn.cursor()
        
        # Countries with more daily data 
        query = '''
                SELECT [country], COUNT(*) AS [count], MIN([date]) AS [min_data]
                  FROM [dbo].[v_daily_covid19_data]
                 GROUP BY [country]
                 ORDER BY [count] DESC;
                '''
        
        dt = cursor.execute(query).fetchall()
        for row in dt:
            country = row[0]
            count = row[1]
            min_date = datetime.strptime(row[2], '%Y-%m-%d')
            result[country] = {'count': count, 'min_date': min_date}
        
    except pyodbc.DatabaseError as e:
        logging.error(' - Pyodbc error: ' + str(e))
    finally:
        cursor.close()
    
    return result

# DB function - Bulk insertion of historical data by country
def bulk_save_data(db_login, record_list):
    
    if len(record_list) == 0:
        logging.info(' - No data to save')
        return
    else:
        logging.info(" - Start of bulk insert for " + str(len(record_list)) + " countries: " + str(datetime.now()))
    
    # Get database connection
    cnxn = pyodbc.connect(driver=db_login['driver'], server=db_login['server'], database=db_login['database'], trusted_connection=db_login['trusted_connection'])
    
    for country, data in record_list.items():
        try:
            cursor = cnxn.cursor()
            
            # Insert many rows
            query = '''
                       INSERT INTO [dbo].[covid19_data]
                           ([country],[datestamp],[total_cases],[total_deaths],[active_cases])
                       VALUES (?, ?, ?, ?, ?);
                    '''
            
            cnxn.autocommit = False
            cursor.fast_executemany = True
            cursor.executemany(query, data)
            
        except pyodbc.DatabaseError as e:
            cnxn.rollback()
            logging.error(' - Pyodbc error: ' + str(e))
        else:
            cnxn.commit()
            logging.info(' - Data stored in the database for ' + country + ', n: ' + str(len(data)))
        finally:
            cnxn.autocommit = True
            cursor.close()
    
    logging.info(" - End of bulk insert: " + str(datetime.now()))

# Web Scraping function
def web_scraping_hist(db_login, batch_size, threshold):
    record_list = dict()
    
    # Datetime with local TimeZone
    local_tz = timezone(pytz.country_timezones['co'][0])
    
    # Web data vars    
    drive_path = '../driver/chromedriver.exe'
    home_url = 'https://www.worldometers.info/coronavirus/'
    data_cols = ['total_cases', 'total_deaths', 'active_cases']
    chart_list = {data_cols[0]: 'coronavirus-cases-linear',
                  data_cols[1]: 'coronavirus-deaths-linear', 
                  data_cols[2]: 'graph-active-cases-total'}
    
    # Get country url dict
    country_url = get_country_data(key_name='country', val_name='url')
    
    # Get country count dict
    country_count = get_country_data_count(db_login)
    
    # Init validation
    if len(country_url) == 0 or len(country_count) == 0:
        logging.info(' - Country data were not found')
        return record_list
    
    try:
        # Chrome browser setup
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1024x1400")
        
        # Create Chrome browser
        browser = webdriver.Chrome(options=chrome_options, executable_path=drive_path)
        logging.info(' - The browser was created')
        
    except Exception as e:
        print(' - Error: ' + str(e))
        logging.error(' - Error: ' + str(e))
        
    else:
        # For each country search the data
        for name, url in country_url.items():
            count = country_count[name]['count']
            min_date = country_count[name]['min_date']
            
            # Country min date validation
            if count < threshold:
                
                # Get page in Chrome browser
                browser.get(home_url + url)
                logging.info(' - The document was read for: ' + name)
                
                # Get country hist data
                country_data = {}
                for chart_name, chart_id in chart_list.items():
                    
                    # Run scraping script
                    tmp_script = """
                        		let chart = $('#%s').highcharts()
                        		let chart_data = chart ? {'x_data': chart.xAxis[0].categories, 'y_data': chart.series[0].yData} : {}
                                return chart_data
                        		""" % chart_id
                    chart_data = browser.execute_script(tmp_script)
                    
                    if chart_data and len(chart_data) == 2:
                        country_data[chart_name] = data_quality(chart_data, min_date)
                        logging.info(' - The data was found for: ' + chart_name)
                    else:
                        logging.info(' - The data was not found for: ' + chart_name)
                
                # Temp save country hist data
                if len(country_data):
                    
                    # Merge data into a list (with default value)
                    dict1 = country_data.get(data_cols[0], {})
                    dict2 = country_data.get(data_cols[1], {})
                    dict3 = country_data.get(data_cols[2], {})
                    
                    country_list = []
                    for k, v in dict1.items():
                        d = local_tz.localize(k).isoformat()
                        row = (name, d, dict1.get(k, 0), dict2.get(k, 0), dict3.get(k, 0))
                        country_list.append(row)
                    
                    # Temporary saved
                    record_list[name] = country_list
                else:
                    logging.info(' - Incomplete country data')
            
            # Exit validation
            if len(record_list) == batch_size:
                break
    
    # Return data
    return record_list

#####################
### Start Program ###
#####################
logging.basicConfig(filename="log/log_file_hist.log", level=logging.INFO)
logging.info(">> START PROGRAM: " + str(datetime.now()))

# 1. Get database credentials
db_login = get_db_credentials()

# 2. Declaration of the execution variables
batch_size = 25
threshold = 10

# 3. Get historical data
data = web_scraping_hist(db_login, batch_size, threshold)

# 4. Store data
bulk_save_data(db_login, data)

logging.info(">> END PROGRAM: " + str(datetime.now()))
logging.shutdown()
#####################
#### End Program ####
#####################
