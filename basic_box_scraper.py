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
    table = soup.find('div', attrs={'id': 'box-WAS-game-basic'}).find("table")

    rows = table.find_all('tr')
    
    for row in rows[1:]:
        
        columns = row.find_all('td')
        
        playerName = columns[0].text
        minutesPlayed = int(columns[1].text)
        FG = int(columns[2].text)
        FGA = int(columns[3].text)
        FGPercentage = columns[4].text
        threeP = int(columns[5].text)
        threePA = int(columns[6].text)
        threePPercentage = columns[7].text
        FT = columns[8].text
        FTA = columns[9].text
        FTPercentage = columns[10].text
        offensiveReb = columns[11].text
        defensiveReb = columns[12].text
        totalReb = columns[13].text
        assist = columns[14].text
        steal = columns[15].text
        blocks = columns[16].text
        turnover = columns[17].text
        personalFouls = columns[18].text
        points = columns[19].text
        plusMinus = columns[20].text
        
        
        #inserts = [playerName, playerAge, gamesPlayed, minutesPlayed, playerEfficiency, trueShooting, 3PARate, FTRate, offensiveReb, defensiveReb, totalReb,assist, steal, blocks, turnover, usage, offensiveWinsShared, defensiveWinsShared, winsShared, winsSharedPer48min, offensiveBox, defensiveBox, box, valueOverReplacement]
        inserts = [playerName, minutesPlayed]
        statement = "INSERT INTO shaan_playerAdvancedAverages (playerName, minutesPlayed) VALUES (%s, %s)"
        
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
    
    