import requests
from bs4 import BeautifulSoup, Comment
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
    '''
    To parse the comments
    https://stackoverflow.com/questions/33138937/how-to-find-all-comments-with-beautiful-soup
    '''
    for comments in soup.findAll(text=lambda text:isinstance(text, Comment)):
        comments.extract()
        commentsoup = BeautifulSoup(comments, 'html.parser')
        table = commentsoup.find('div', {'id': 'div_per_minute'})
        if table:
            # prints out the right table
            print(table)
    
    # #find the id of the table you're trying to scrape and insert it below
    

    # rows = table.find_all('tr')
    
    # for row in rows[1:]:
        
    #     columns = row.find_all('td')
        
    #     '''
        
    #     INSERT YOUR CODE HERE
        
    #     '''
        
    #     inserts = []
    #     statement = "" + percentS_Creater(inserts)
        
        

if __name__ == "__main__":
    
    '''
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    '''
    
    
    #insert URL here
    url = requests.get('https://www.basketball-reference.com/teams/BOS/2021.html')
    
    soup = BeautifulSoup(url.text, 'html.parser')
    
    myScraper2(soup)