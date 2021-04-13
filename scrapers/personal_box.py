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




def myScraper(soup, cnx, cursor):

    
    #find the id of the table you're trying to scrape and insert it below
    table = soup.find('div', attrs={'id': 'div_box-PHI-game-basic'}).find("table")
    
    
    
    rows = table.find_all('tr')
    counter = 2
    row_count = len(rows)
    for row in rows[2:row_count-1]:
        counter += 1
        if (counter == 8):
            continue
        
            
        columns = row.find_all('td')
        #print(row.text)
        playerName = row.find('th').text



        #print(playerName)
        #minutesPlayed = columns[1].text
        
        #splitting the minutes into a number
        min_string = columns[0].text
        if (min_string == "Did Not Play"):
            break
        
        min_list = min_string.split(":")
        minute = int(min_list[0])
        second = int(min_list[1])

        total_min = minute + second/60
        
        
        minutesPlayed = total_min
        
    
        
        
        FG = int(columns[1].text)
        
        #print(minutesPlayed)
        
        #print(FG)
        
        FGA = int(columns[2].text)
        if columns[3].text == "":
            FGPercentage = None
        else:
            FGPercentage = float(columns[3].text)
        threeP = int(columns[4].text)
        threePA = int(columns[5].text)
        
        if columns[6].text == "":
            threePPercentage = None
        else:
            threePPercentage = float(columns[6].text)
        FT = int(columns[7].text)
        FTA = int(columns[8].text)
        
        if columns[9].text == "":
            FTPercentage = None
        else:
            FTPercentage = float(columns[9].text)
        offensiveReb = int(columns[10].text)
        defensiveReb = int(columns[11].text)
        totalReb = int(columns[12].text)
        assist = int(columns[13].text)
        steal = int(columns[14].text)
        blocks = int(columns[15].text)
        turnover = int(columns[16].text)
        personalFouls = int(columns[17].text)
        points = int(columns[18].text)
        plusMinus = int(columns[19].text)
        
        
        inserts = [playerName, minutesPlayed, FG, FGA, FGPercentage, threeP, threePA, threePPercentage, FT, FTA, FTPercentage, offensiveReb, defensiveReb, totalReb, assist, steal, blocks, turnover, personalFouls, points, plusMinus]
        statement = "INSERT INTO playerBasicBoxStats (playerName, minutesPlayer, FG, FGA, FGPercentage, threeP, threePA, threePPercentage, FT, FTA, FTPercentage, offensiveReb, defensiveReb, totalReb, assists, steals, blocks, turnovers, personalFouls, points, plusminus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
        #print(inserts)
        cursor.execute(statement,inserts)
        cnx.commit()


if __name__ == "__main__":
    
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    
    
    #insert URL here
    url = requests.get('https://www.basketball-reference.com/boxscores/202012230PHI.html')
    
    soup = BeautifulSoup(url.text, 'html.parser')
    
    myScraper(soup, cnx, cursor)
    
    