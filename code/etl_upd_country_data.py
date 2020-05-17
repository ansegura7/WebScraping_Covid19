# -*- coding: utf-8 -*-
"""
    Created By: Andres Segura Tinoco
    Created On: May 17, 2020
    Description: Service that consults a Rest API to update the information of the countries
    Source: https://restcountries.eu/
"""

# Import custom libraries
import util_lib as ul

# Import util libraries
from datetime import datetime

# API Rest libraries
import requests

# Database libraries
import pyodbc

# DB function - Get database credentials
def get_db_credentials():
    yaml_path = 'config\database.yml'
    db_login = ul.get_dict_from_yaml(yaml_path)
    return db_login

# DB function - Get the complete list of stored countries
def get_country_list(db_login):
    country_list = []
    
    # Get database connection
    cnxn = pyodbc.connect(driver=db_login['driver'], server=db_login['server'], database=db_login['database'], trusted_connection=db_login['trusted_connection'])
    
    try:
        cursor = cnxn.cursor()
        
        # Countries with more daily data 
        query = '''
                SELECT [name], [fullname]
                  FROM [dbo].[country_info]
                 ORDER BY [name] ASC;
                '''
        
        dt = cursor.execute(query).fetchall()
        for row in dt:
            country_name = row[1]
            country_list.append(country_name)
        
    except pyodbc.DatabaseError as e:
        print(' - Pyodbc error: ' + str(e))
        
    finally:
        cursor.close()
    
    return country_list

# DB function - Update the data for a specific country
def update_country_data(db_login, row):
    result = False
    
    # Get database connection
    cnxn = pyodbc.connect(driver=db_login['driver'], server=db_login['server'], database=db_login['database'], trusted_connection=db_login['trusted_connection'])
    country_name = row['name']
    
    try:
        cursor = cnxn.cursor()
        
        # Country query
        query = '''
                UPDATE [dbo].[country_info]
                   SET [top_level_domain] = ?
                      ,[alpha2_dode] = ?
                      ,[alpha3_code] = ?
                      ,[calling_codes] = ?
                      ,[capital] = ?
                      ,[alt_spellings] = ?
                      ,[region] = ?
                      ,[subregion] = ?
                      ,[lat] = ?
                      ,[long] = ?
                      ,[demonym] = ?
                      ,[area] = ?
                      ,[gini] = ?
                      ,[timezones] = ?
                      ,[borders] = ?
                      ,[native_name] = ?
                      ,[numeric_code] = ?
                      ,[flag] = ?
                      ,[cioc] = ?
                 WHERE [fullname] = ?
               '''
        
        # Country data
        country_data = [', '.join(row['topLevelDomain']),
                        row['alpha2Code'],
                        row['alpha3Code'],
                        ', '.join(row['callingCodes']),
                        row['capital'],
                        ', '.join(row['altSpellings']),
                        row['region'],
                        row['subregion'],
                        row['latlng'][0],
                        row['latlng'][1],
                        row['demonym'],
                        row['area'],
                        row['gini'],
                        ', '.join(row['timezones']),
                        ', '.join(row['borders']),
                        row['nativeName'],
                        row['numericCode'],
                        row['flag'],
                        row['cioc'],
                        country_name]
        
        # Execute command
        cnxn.autocommit = False
        cursor.execute(query, country_data)
        
    except pyodbc.DatabaseError as e:
        print(' - Pyodbc error for %s: %s' % (country_name, str(e)))
    
    else:
        cnxn.commit()
        print(' - %s data updated' % country_name)
        
    finally:
        cnxn.autocommit = True
        cursor.close()
    
    return result

# DB function - Update the data of all the stored countries
def update_data(db_login, json_data):
    
    # Get country url dict
    country_list = get_country_list(db_login)
    
    for row in json_data:
        country_name = row['name']
        if country_name in country_list:
            result = update_country_data(db_login, row)
            
            if result:
                print(' - Warning: the data for the country of %s could not be updated' % country_name)
    

# Call a REST api and return the data in JSON format
def call_rest_api(api_url, timeout=3):
    json_data = {}
    
    try:
        response = requests.get(api_url, timeout=timeout)
        
    except requests.exceptions.HTTPError as e:
        print('Http error:', e)
        
    except requests.exceptions.ConnectionError as e:
        print('Error connecting:', e)
        
    except requests.exceptions.Timeout as e:
        print('Timeout error:', e)
        
    except requests.exceptions.TooManyRedirects as e:
        print('URL was bad:', e)
        
    except requests.exceptions.RequestException as e:
        print('Catastrophic error:', e)
        
    else:
        if response.status_code == 200:
            json_data = response.json()
            print(' - Data obtained correctly for %s countries' % len(json_data))
    
    # Return data
    return json_data

#####################
### Start Program ###
#####################
print(">> START PROGRAM: " + str(datetime.now()))
    
# 1. Get database credentials
db_login = get_db_credentials()

# 2. Declaration of the execution variables
api_url = 'https://restcountries.eu/rest/v2/all'

# 3. Get countries data
data = call_rest_api(api_url)

# 4. Generate derived data
if len(data):
    update_data(db_login, data)

print('>> END PROGRAM: ' + str(datetime.now()))
#####################
#### End Program ####
#####################
