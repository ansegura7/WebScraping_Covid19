# -*- coding: utf-8 -*-
"""
    Created By: Andres Segura Tinoco
    Created On: Apr 10, 2020
    Description: Web scraping to obtain data on infections and deaths from Covid-19
    Source: https://www.worldometers.info/coronavirus/
"""

# Import util libraries
import logging
from datetime import datetime

# Import Web Scraping libraries
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

# Database libraries
import pyodbc

# Converts a string to a number (int or float) 
def parse_num(n):
    v = 0
    n = n.replace(',', '').replace('+', '').strip()
    
    if '.' in n:
        v = float(n)
    elif n != '':
        v = int(n)
    
    return v

# DB function: merge a list records in the MS SQL Server table
def merge_data(record_list):
    result = False
    
    if len(record_list) == 0:
        logging.info(' - No data to save')
        return result
    else:
        logging.info(' - Total data: ' + str(len(record_list)))
    
    # Get database connection
    cnxn = pyodbc.connect(driver='{SQL Server}', server='.\SQLExpress01', database='OVS_DEVOPS_WFS', trusted_connection='yes')
    
    try:
        cursor = cnxn.cursor()
        
        # Initial number of records 
        query = 'SELECT COUNT(*) AS [count] FROM [dbo].[covid_19];'
        n_init = cursor.execute(query).fetchone()
        n_init = int(n_init[0])
        
        # Merge many rows
        query = '''MERGE [dbo].[covid_19] USING (
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ) AS vals ([country],[total_cases],[new_cases],[total_deaths],[new_deaths],[total_recovered],[active_cases],
                              [serious_critical],[tot_cases_1m_pop],[deaths_1m_pop],[total_tests],[tests_1m_pop],[datestamp])
                   ON covid_19.[country] = vals.[country] AND
                      covid_19.[total_cases] = vals.[total_cases] AND
                      covid_19.[new_cases] = vals.[new_cases] AND
                      covid_19.[total_deaths] = vals.[total_deaths] AND
                      covid_19.[new_deaths] = vals.[new_deaths] AND
                      covid_19.[total_recovered] = vals.[total_recovered] AND
                      covid_19.[active_cases] = vals.[active_cases] AND
                      covid_19.[serious_critical] = vals.[serious_critical] AND
                      covid_19.[tot_cases_1m_pop] = vals.[tot_cases_1m_pop] AND
                      covid_19.[deaths_1m_pop] = vals.[deaths_1m_pop] AND
                      covid_19.[total_tests] = vals.[total_tests] AND
                      covid_19.[tests_1m_pop] = vals.[tests_1m_pop]
                   WHEN NOT MATCHED THEN
                       INSERT ([country],[total_cases],[new_cases],[total_deaths],[new_deaths],[total_recovered],[active_cases],
                               [serious_critical],[tot_cases_1m_pop],[deaths_1m_pop],[total_tests],[tests_1m_pop],[datestamp])
                       VALUES (vals.[country],vals.[total_cases],vals.[new_cases],vals.[total_deaths],vals.[new_deaths],vals.[total_recovered],vals.[active_cases],
                            vals.[serious_critical],vals.[tot_cases_1m_pop],vals.[deaths_1m_pop],vals.[total_tests],vals.[tests_1m_pop],vals.[datestamp]);
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
        query = 'SELECT COUNT(*) AS [count] FROM [dbo].[covid_19];'
        n_final = cursor.execute(query).fetchone()
        n_final = int(n_final[0])
        
        logging.info(' - Saved data: ' + str(n_final - n_init))
        result = True
    finally:
        cnxn.autocommit = True
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
            
            for row in curr_table.findAll('tr'):
                cols = row.findAll('td')
                if len(cols) == 13:
                    if 'country' in str(cols[0].a):
                        
                        record = {
                            'country': cols[0].a.text,
                            'total_cases': parse_num(cols[1].text),
                            'new_cases': parse_num(cols[2].text),
                            'total_deaths': parse_num(cols[3].text),
                            'new_deaths': parse_num(cols[4].text),
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
    
    # Return data
    return record_list

#####################
### Start Program ###
#####################
logging.basicConfig(filename="../log/log_file.log", level=logging.INFO)
logging.info(">> START PROGRAM: " + str(datetime.now()))

# Get data
data = web_scraping_data();

# Save data
merge_data(data)

logging.info(">> END PROGRAM: " + str(datetime.now()))
#####################
#### End Program ####
#####################
