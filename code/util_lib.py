# -*- coding: utf-8 -*-
"""
    Created By: Andres Segura Tinoco
    Created On: May 05, 2020
    Version: 0.1.0
    Description: Library with utility functions
"""

# Import util libraries
import yaml
import csv

############################
### Start Util Functions ###
############################

# Data quality function - Converts a string to a number (int or float) 
def dq_parse_num(n):
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

# Data quality function - Clean html text and convert it to plain text
def dq_clean_html_text(html_text):
    plain_text = html_text.strip().replace(u'\n', u'')
    return plain_text.encode('ascii', 'ignore').decode("utf-8")

# Util function - Read dict from yaml file
def get_dict_from_yaml(yaml_path):
    result = dict()
    
    with open(yaml_path) as f:
        yaml_file = f.read()
        result = yaml.load(yaml_file, Loader=yaml.FullLoader)
    
    return result

# Util function - Read CSV file from full filepath
def read_csv_file(filename, encoding='utf-8-sig', delimiter=','):
    data = []
    
    with open(filename, 'r', encoding=encoding) as f:
        csv_file = csv.reader(f, delimiter=delimiter)
        for row in csv_file:
            data.append(row)
            
    return data

# Util function - Save data list to CSV file
def save_data_to_csv(dt, filename, header):
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

##########################
### End Util Functions ###
##########################
