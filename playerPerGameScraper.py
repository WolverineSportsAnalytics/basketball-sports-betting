#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 20:24:11 2021

@author: ryanhertzberg
"""
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


def myScraper2(soup, cnx, cursor):

    
    #find the id of the table you're trying to scrape and insert it below
    table = soup.find('div', attrs={'id': 'all_per_game'}).find("table")

    rows = table.find_all('tr')
    
    for row in rows[1:]:
        
        columns = row.find_all('td')
        
        playerName = columns[0].text
        games = int(columns[2].text)
        gamesStarted = int(columns[3].text)
        minutesPlayed = float(columns[4].text)
        fgMade = float(columns[5].text)
        fgAttempts = float(columns[6].text)
        fgPercent = float(columns[7].text)
        threePtMade = float(columns[8].text)
        threePtAttempts = float(columns[9].text)
        
        if columns[10].text == "":
            threePtPercent = None
        else:
            threePtPercent = float(columns[10].text)
            
        twoPtMade = float(columns[11].text)
        twoPtAttempts = float(columns[12].text)
        
        if columns[13].text == "":
            twoPtPercent = None
        else:
            twoPtPercent = float(columns[13].text)
        
        effFgPercent = float(columns[14].text)
        ftMade = float(columns[15].text)
        ftAttempts = float(columns[16].text)
        
        if columns[17].text == "":
            ftPercent = None
        else:
            ftPercent = float(columns[17].text)
        
        offRebounds = float(columns[18].text)
        defRebounds = float(columns[19].text)
        totalRebounds = float(columns[20].text)
        assists = float(columns[21].text)
        steals = float(columns[22].text)
        blocks = float(columns[23].text)
        turnovers = float(columns[24].text)
        fouls = float(columns[25].text)
        points = float(columns[26].text)
        
        inserts = [playerName, games, gamesStarted, minutesPlayed, fgMade, fgAttempts, fgPercent,
                    threePtMade, threePtAttempts, threePtPercent, twoPtMade, twoPtAttempts, twoPtPercent, 
                    effFgPercent, ftMade, ftAttempts, ftPercent, offRebounds, defRebounds, totalRebounds, 
                    assists, steals, blocks, turnovers, fouls, points]
        statement = "INSERT INTO ryan_playerPerGame (playerName, games, gamesStarted, minutesPlayed, fgMade, fgAttempts, fgPercent,threePtMade, threePtAttempts, threePtPercent, twoPtMade, twoPtAttempts, twoPtPercent, effFgPercent, ftMade, ftAttempts, ftPercent, offRebounds, defRebounds, totalRebounds, assists, steals, blocks, turnovers, fouls, points) VALUES" + percentS_Creater(inserts)
        print(inserts)
        cursor.execute(statement,inserts)
        cnx.commit()

if __name__ == "__main__":
    
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    
    
    #insert URL here
    url = requests.get('https://www.basketball-reference.com/teams/CHI/2021.html')
    
    soup = BeautifulSoup(url.text, 'html.parser')
    
    myScraper2(soup, cnx, cursor)
