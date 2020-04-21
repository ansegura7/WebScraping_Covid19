# -*- coding: utf-8 -*-
"""
    Created By: Andres Segura Tinoco
    Created On: Apr 21, 2020
    Description: Web scraping to obtain history data on confirmed cases and deaths of Covid-19
    Source: https://www.worldometers.info/coronavirus/
"""

# Import util libraries
#import logging
import yaml
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Database libraries
import pyodbc

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
        #logging.info(' - No data to save')
        return result
    #else:
        #logging.info(' - Total data: ' + str(len(record_list)))
    
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
        #logging.error(' - Pyodbc error: ' + str(e))
    else:
        cnxn.commit()
        
        # Final number of records
        query = 'SELECT COUNT(*) AS [count] FROM [dbo].[covid19_data];'
        n_final = cursor.execute(query).fetchone()
        n_final = int(n_final[0])
        
        #logging.info(' - Data stored in the database: ' + str(n_final - n_init))
        result = (n_final > n_init)
    finally:
        cnxn.autocommit = True
        cursor.close()
    
    return result

# Web Scraping function
def web_scraping_hist():
    record_list = []
    
    # Web data vars    
    path = 'C:/Users/Andres/Documents/GitHub/WebScraping_Covid19/drive/chromedriver.exe'
    url = 'https://www.worldometers.info/coronavirus/country/us/'
    
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1024x1400")
    
        browser = webdriver.Chrome(options=chrome_options, executable_path=path)
        browser.get(url)
        #logging.info(' - The document was read')
        
    except Exception as e:
        print(' - Error: ' + str(e))
        #logging.error(' - Error: ' + str(e))
        
    else:        
        # Find all scripts
        chart_id = {'total_cases': 'coronavirus-cases-linear',
                    'total_deaths': 'coronavirus-deaths-linear', 
                    'active_cases': 'graph-active-cases-total'}
        
        # Get data
        for k, v in chart_id.items():    
            tmp_script = """
                		var chart = $('#%s').highcharts()
                		return {'x_data': chart.xAxis[0].categories, 'y_data': chart.series[0].yData}
                		""" % v
            
            chart_data = browser.execute_script(tmp_script)
            if len(chart_data) == 2:
                print(chart_data)
                #logging.info(' - The data was found')
            #else:
                    #logging.info(' - The data was not found')
                        
    print('n2:', len(record_list))
    #print(record_list)
    
    # Return data
    return record_list

#####################
### Start Program ###
#####################
#logging.basicConfig(filename="log/log_file.log", level=logging.INFO)
#logging.info(">> START PROGRAM: " + str(datetime.now()))

# 1. Get data
data = web_scraping_hist()

# 2. Get database credentials
#db_login = get_db_credentials()

# 3. Store data
#merge_data(db_login, data)

#logging.info(">> END PROGRAM: " + str(datetime.now()))
#logging.shutdown()
#####################
#### End Program ####
#####################
