#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 20:16:50 2021

@author: lissjust
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 20:37:43 2021

@author: lissjust
"""

import requests
from bs4 import BeautifulSoup
import os
import mysql.connector

def percentS_Creater(inserts):
    
    percentSList = '('
    for i in range(0,len(inserts)):
        if i == len(inserts) - 1:
            percentSList = percentSList + '%s)'
        else:
            percentSList = percentSList + '%s, '
    
    return percentSList


def myScraper2(soup):

    
    #find the id of the table you're trying to scrape and insert it below
    table = soup.find('div', attrs={'id': '______INSERT ID HERE________'}).find("table")

    rows = table.find_all('tr')
    
    for row in rows[1:]:
        
        columns = row.find_all('td')
        
        '''
        
        INSERT YOUR CODE HERE
        
        '''
        
        inserts = []
        statement = "" + percentS_Creater(inserts)
        
        

if __name__ == "__main__":
    
    '''
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    '''
    
    
    #insert URL here
    url = requests.get('')
    
    soup = BeautifulSoup(url.text, 'html.parser')
    
    myScraper2(soup)
    