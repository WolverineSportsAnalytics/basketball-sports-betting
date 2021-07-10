#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 20:12:03 2021

@author: lissjust
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import os
import mysql.connector
import time


def deleteEarlyToday(cnx,cursor,month,day,year):
    dateString = year +"-"+month+"-"+day
    
    statement = "DELETE from playerMinutesProjections where dateString = '" + dateString + "'"
    cursor.execute(statement)
    cnx.commit()
    return

def updateDateColumn(cnx,cursor):
    updateString = "update playerMinutesProjections set date = STR_TO_DATE(dateString, '%Y-%m-%d')"
    cursor.execute(updateString)
    cnx.commit()
    return

def listPercentS_Generator(inserts):
    
    percentSList = '('
    for i in range(0,len(inserts)):
        if i == len(inserts) - 1:
            percentSList = percentSList + '%s)'
        else:
            percentSList = percentSList + '%s, '
    
    return percentSList

def SportsLines_MinutesScraper(cnx,cursor,month,day,year):
    
    # soup stuff
    ##################################################################################################################
    url = url = requests.get('https://www.sportsline.com/nba/expert-projections/simulation/')
    soup = BeautifulSoup(url.text, 'html.parser')
    table = soup.find('table')
    ###################################################################################################################
    
    # date stuff
    ######################################################################################################

    dateString = year +"-"+month+"-"+day
    deleteEarlyToday(cnx,cursor,month,day,year)
    if month[0] == "0":
        month = month[1]
        month = int(month)
    else:
        month = int(month)
    
    if day[0] == "0":
        day = day[1]
        day = int(day) 
    else:
        day = int(day)   
    
    year = int(year)
    ######################################################################################################

    rows = table.find_all('tr')
    
    for row in rows[1:]:
        
        columns = row.find_all('td')
        
        playerName = columns[0].text
        position = columns[1].text
        teamName = columns[2].text
        game = columns[3].text
        awayTeam = game[0:3]
        homeTeam = game[4:7]
        if awayTeam == teamName:
            opponentTeamName = homeTeam
        else:
            opponentTeamName = awayTeam
        projectedMinutes = float(columns[9].text)
        website = "SportsLines.com"
        
        inserts = (playerName,website,projectedMinutes,position,teamName,opponentTeamName,game,awayTeam,homeTeam,dateString,month,day,year)
        statement = "INSERT into playerMinutesProjections (playerName,website,projectedMinutes,position,teamName,opponentTeamName,game,awayTeam,homeTeam,dateString,month,day,year) VALUES " + listPercentS_Generator(inserts)
        print (inserts)
        cursor.execute(statement,inserts)
        cnx.commit()
       
    updateDateColumn(cnx,cursor)
    print("Finished inserting minutes projections from SportsLines.com")
    return

def Lineups_MinutesScraper(cnx,cursor,month,day,year):
    
    # soup stuff
    ##################################################################################################################
    url = requests.get(r"https://www.lineups.com/nba/nba-fantasy-basketball-projections")
    soup = BeautifulSoup(url.text, 'html.parser')
    div = soup.find("div", { "class" : "horizontal-table-wrapper" })
    table = div.find('table')
    ###################################################################################################################
    
    # date stuff
    ######################################################################################################

    dateString = year +"-"+month+"-"+day
    deleteEarlyToday(cnx,cursor,month,day,year)
    if month[0] == "0":
        month = month[1]
        month = int(month)
    else:
        month = int(month)
    
    if day[0] == "0":
        day = day[1]
        day = int(day) 
    else:
        day = int(day)   
    
    year = int(year)
    
    
    
    ######################################################################################################
    rows = table.find_all('tr')
    print ("Length of rows",len(rows))
    for row in rows[2:]:
        columns = row.find_all('td')
    
        playerName = columns[0].find('span',{"class":"player-name-col-lg"}).text       
        teamName = (columns[1].text)[2:5]
        position = columns[2].text
        opponentTeamName = (columns[8].text)[2:5]
        teamSpread = float(columns[10].text)
        teamPointsOverUnder = float(columns[11].text)
        gamePointsOverUnder = float(columns[12].text)
        minutesProjection = float(columns[13].text)
        
        '''
        print ("playerName", playerName)
        print ("teamName", teamName)
        print ("position", position)
        print ("opponentTeamName", opponentTeamName)
        print ("teamSpread", teamSpread)
        print ("teamPointsOverUnder", teamPointsOverUnder)
        print ("gamePointsOverUnder", gamePointsOverUnder)
        print ("minutesProjection", minutesProjection)
        '''
        
        inserts = (playerName, teamName, position, opponentTeamName,teamSpread,teamPointsOverUnder,gamePointsOverUnder,minutesProjection,dateString,month,day,year)
        print (inserts)
        statement = "INSERT INTO playerMatchups (playerName, teamName, position, opponentTeamName,teamSpread,teamPointsOverUnder,gamePointsOverUnder,minutesProjection,dateString,month,day,year) VALUES "  + listPercentS_Generator(inserts)
        
        cursor.execute(statement,inserts)
        cnx.commit()
        
        
        
        # 0: playerName
        # 1: teamName
        # 2: position
        # 8: opponentTeamName
        # 10: gameSpread
        # 11: teamPointsOverUnder
        # 12: gamePointsOverUnder
        # 13: minutesProjection
        
    updateDateColumn(cnx,cursor)
    return

def minutesScraperTwo(cnx,cursor,month,day,year):

    # soup stuff
    ##################################################################################################################
    url = requests.get(r"https://www.lineups.com/nba/nba-player-minutes-per-game")
    soup = BeautifulSoup(url.text, 'html.parser')
    table = soup.find('table')

    
    rows = table.find_all('tr')
    for row in rows[1:]: 
        columns = row.find_all('td')
        
        playerName = columns[0].find('span',{"class":"player-name-col-lg"}).text  
        
        position = columns[1].text
        
        teamStuff = row.find_all('a', {"class":"link-black-underline"})
        print (teamStuff)
        
    
    
    
    
    return
    
    
if __name__ == "__main__":
    
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)

    teamsDic = {"ATL":11, "BOS":2, "BRK":3, "CHO":13, "CHI":9, "CLE":8, "DAL":28, "DEN":17,
                      "DET":10, "GSW":24, "HOU":29, "IND":7, "LAC":22, "LAL":21, "MEM":26, "MIA":14,
                      "MIL":6, "MIN":20, "NOP":30, "NYK":4, "OKC":19, "ORL":12, "PHI":1, "PHO":23,
                      "POR":18, "SAC":25, "SAS":27, "TOR":5, "UTA":16, "WAS":15}
    
    
    ############### ^ Frequently used ################

    
    #url = requests.get(r"https://www.sportsline.com/nba/expert-projections/simulation/")
    #soup = BeautifulSoup(url.text, 'html.parser')
    
    #table = soup.find_all("div", { "class" : "starting-lineup-loader" })
  
    #div = soup.find("div", { "class" : "horizontal-table-wrapper" })
    
    #table = div.find('table')
    
    month = "06"
    day = "19"
    year = "2021"
    
    deleteEarlyToday(cnx,cursor,month,day,year)
    SportsLines_MinutesScraper(cnx,cursor,month,day,year)

 