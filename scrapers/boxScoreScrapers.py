#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 19:01:55 2021

@author: lissjust
"""

import requests
from bs4 import BeautifulSoup
import os
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd

def deleteDuplicateRows(cnx,cursor):

    playerAdvanced = "select playerAdvancedBoxStatsID from playerAdvancedBoxStats where playerAdvancedBoxStatsID not in (select max(playerAdvancedBoxStatsID) from playerAdvancedBoxStats group by playerName,teamName,opponentTeamName,`date`)"
    cursor.execute(playerAdvanced)
    playerAdvanced = cursor.fetchall()
    for row in playerAdvanced:
        ID = row[0]
        statement = "DELETE from playerAdvancedBoxStats where playerAdvancedBoxStatsID = " + str(ID)
        cursor.execute(statement)
        cnx.commit()
    print ("Finished deleting duplicate playerAdvanced")

    playerBasic = "select playerBasicBoxStatsID from playerBasicBoxStats where playerBasicBoxStatsID not in (select max(playerBasicBoxStatsID) from playerBasicBoxStats group by playerName,teamName,opponentTeamName,`date`)"
    cursor.execute(playerBasic)
    playerBasic = cursor.fetchall()
    for row in playerBasic:
        ID = row[0]
        statement = "DELETE from playerBasicBoxStats where playerBasicBoxStatsID = " + str(ID)
        cursor.execute(statement)
        cnx.commit()
    print ("Finished deleting duplicate playerBasic")
        

    teamAdvanced = "select teamAdvancedBoxStatsID from teamAdvancedBoxStats where teamAdvancedBoxStatsID not in (select max(teamAdvancedBoxStatsID) from teamAdvancedBoxStats group by teamName,opponentTeamName,`date`)"
    cursor.execute(teamAdvanced)
    teamAdvanced = cursor.fetchall()
    for row in teamAdvanced:
        ID = row[0]
        statement = "DELETE from teamAdvancedBoxStats where teamAdvancedBoxStatsID = " + str(ID)
        cursor.execute(statement)
        cnx.commit()
    print ("Finished deleting duplicate teamAdvanced")

    teamBasic = "select teamBasicBoxStatsID from teamBasicBoxStats where teamBasicBoxStatsID not in (select max(teamBasicBoxStatsID) from teamBasicBoxStats group by teamName,opponentTeamName,`date`)"
    cursor.execute(teamBasic)
    teamBasic = cursor.fetchall()
    for row in teamBasic:
        ID = row[0]
        statement = "DELETE from teamBasicBoxStats where teamBasicBoxStatsID = " + str(ID)
        cursor.execute(statement)
        cnx.commit()
    print ("Finished deleting duplicate teamBasic")

    
    return

def updateDateColumn(cnx,cursor):
    updateString = "update playerAdvancedBoxStats a set a.date = STR_TO_DATE(dateString, '%Y-%m-%d')"
    cursor.execute(updateString)
    cnx.commit()
    updateString = "update playerBasicBoxStats b set b.date = STR_TO_DATE(dateString, '%Y-%m-%d')"
    cursor.execute(updateString)
    cnx.commit()
    updateString = "update teamAdvancedBoxStats c set c.date = STR_TO_DATE(dateString, '%Y-%m-%d')"
    cursor.execute(updateString)
    cnx.commit()
    updateString = "update teamBasicBoxStats d set d.date = STR_TO_DATE(dateString, '%Y-%m-%d')"
    cursor.execute(updateString)
    cnx.commit()
    return

def getIndexPausedAt(datesList, date):
    ticker = 0
    for element in datesList:
        if element == date:
            return ticker
        else:
            ticker +=1
    return "Error occured trying to get index paused at"

def listOfDates(startYear,endYear,startMonth,endMonth,startDay,endDay):
    
    years = consecutiveNumberList_Generator(startYear,endYear)
    months = consecutiveNumberList_Generator(startMonth,endMonth)
    days = consecutiveNumberList_Generator(startDay,endDay)
    
    datesList = []
    
    for year in years:
        for month in months:
            for day in days:
                date = [month,day,year]
                datesList.append(date)
    
    #print (datesList)
    return datesList
    
def consecutiveNumberList_Generator(startYear, endYear):
    
    yearsList = []
    
    i = startYear
    while i <= endYear:
        if i <10:
            yearsList = yearsList + ["0" +str(i)]
        else:
            yearsList = yearsList + [str(i)]
        i +=1
    
    return yearsList

def getTeamsPlayed(soup):
    teamsDic = {"ATL":11, "BOS":2, "BRK":3, "CHO":13, "CHI":9, "CLE":8, "DAL":28, "DEN":17,
                      "DET":10, "GSW":24, "HOU":29, "IND":7, "LAC":22, "LAL":21, "MEM":26, "MIA":14,
                      "MIL":6, "MIN":20, "NOP":30, "NYK":4, "OKC":19, "ORL":12, "PHI":1, "PHO":23,
                      "POR":18, "SAC":25, "SAS":27, "TOR":5, "UTA":16, "WAS":15}
    
    fullList = soup.find_all('a')
    
    awayHref = fullList[36].get('href')
    homeHref = fullList[37].get('href')
    
    awayTeamAbbrev = awayHref[7:10]
    homeTeamAbbrev = homeHref[7:10]


    return [awayTeamAbbrev,homeTeamAbbrev]

def teamScheduleBoxScore_UrlGenerator(year,month,date,teamName):
    
    url = "https://www.basketball-reference.com/boxscores/" + str(year) + str(month) + str(date) + "0" + teamName + ".html"
    
    return url


def listPercentS_Generator(inserts):
    
    percentSList = '('
    for i in range(0,len(inserts)):
        if i == len(inserts) - 1:
            percentSList = percentSList + '%s)'
        else:
            percentSList = percentSList + '%s, '
    
    return percentSList

def teamBasicBoxScore(soup, cnx, cursor, teamName,teamID,opponentTeamName,opponentTeamID,home,month,day,year,season,url):
    dateString = year +"-"+month+"-"+day
    
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
    
    #find the id of the table you're trying to scrape and insert it below
    #tables = soup.find_all('table')
    #awayTable = tables[0]
    #homeTable = tables[8]

    stringID = "div_box-"+teamName+"-game-basic"
    table = soup.find('div', attrs={'id': stringID}).find("table")
    #start with the away team players
    rows = table.find_all('tr')
    row = rows[-1]
        
    columns = row.find_all('td')

    MP = int(columns[0].text)

    FG = int(columns[1].text)

    FGA = int(columns[2].text)
    
    if columns[3].text == "":
        FG_percent = None
    else:
        FG_percent = float(columns[3].text)
    threeP = int(columns[4].text)
    threePA = int(columns[5].text)
    
    if columns[6].text == "":
        threeP_percent = None
    else:
        threeP_percent = float(columns[6].text)
    FT = int(columns[7].text)
    FTA = int(columns[8].text)
    
    if columns[9].text == "":
        FT_percent = None
    else:
        FT_percent = float(columns[9].text)
    ORB = int(columns[10].text)
    DRB = int(columns[11].text)
    TRB = int(columns[12].text)
    AST = int(columns[13].text)
    STL = int(columns[14].text)
    BLK = int(columns[15].text)
    TOV = int(columns[16].text)
    PF = int(columns[17].text)
    PTS = int(columns[18].text)

    inserts = [MP, FG, FGA, FG_percent, threeP, threePA, threeP_percent, FT, FTA, FT_percent, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, teamName,teamID,opponentTeamName,opponentTeamID,home,month,year,day,url,dateString,season]
    statement = "INSERT INTO teamBasicBoxStats (MP, FG, FGA, FG_percent, threeP, threePA, threeP_percent, FT, FTA, FT_percent, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, teamName,teamID,opponentTeamName,opponentTeamID,home,month,year,day,url,dateString,season) VALUES " + listPercentS_Generator(inserts)

    print(inserts)
    cursor.execute(statement,inserts)
    cnx.commit()


def teamAdvancedBoxScore(soup,cnx,cursor,teamName,teamID,opponentTeamName,opponentTeamID,home,month,day,year,season,url):
    #find the id of the table you're trying to scrape and insert it below
    #tables = soup.find_all('table')
    #awayTable = tables[7]
    #homeTable = tables[15]
    dateString = year +"-"+month+"-"+day
    
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

    stringID = "div_box-"+teamName+"-game-advanced"
    table = soup.find('div', attrs={'id': stringID}).find("table")
    
    rows = table.find_all('tr')
    row = rows[-1]
    columns = row.find_all('td')

    
    #splitting the minutes into a number

    MP = columns[0].text
    
    if columns[1].text == "":
        TS_percent = None
    else:
        TS_percent = float(columns[1].text)
    
    if columns[2].text == "":
        eFG_percent = None
    else:
        eFG_percent = float(columns[2].text)
    
    if columns[3].text == "":
        threePAr = None
    else:
        threePAr = float(columns[3].text)
    
    if columns[4].text == "":
        FTr = None
    else:
        FTr = float(columns[4].text)
    
    if columns[5].text == "":
        ORB_percent = None
    else:
        ORB_percent = float(columns[5].text)
    
    if columns[6].text == "":
        DRB_percent = None
    else:
        DRB_percent = float(columns[6].text)
        
    if columns[7].text == "":
        TRB_percent = None
    else:
        TRB_percent = float(columns[7].text)
    
    if columns[8].text == "":
        AST_percent = None
    else:
        AST_percent = float(columns[8].text)
        
    if columns[9].text == "":
        STL_percent = None
    else:
        STL_percent = float(columns[9].text)
    
    if columns[10].text == "":
        BLK_percent = None
    else:
        BLK_percent = float(columns[10].text)
    
    if columns[11].text == "":
        TOV_percent = None
    else:
        TOV_percent = float(columns[11].text)

    if columns[12].text == "":
        USG_percent = None
    else:
        USG_percent = float(columns[12].text)
    
    if columns[13].text == "":
        ORtg = None
    else:
        ORtg = float(columns[13].text)
    
    if columns[14].text == "":
        DRtg = None
    else:
        DRtg = float(columns[14].text)
    
    inserts = [MP,TS_percent,eFG_percent,threePAr, FTr,ORB_percent,DRB_percent,TRB_percent,AST_percent,STL_percent,BLK_percent,TOV_percent,USG_percent,ORtg,DRtg,teamName,teamID,opponentTeamName,opponentTeamID,home,month,day,year,url,dateString,season]
    statement = "INSERT INTO teamAdvancedBoxStats (MP,TS_percent,eFG_percent,threePAr, FTr,ORB_percent,DRB_percent,TRB_percent,AST_percent,STL_percent,BLK_percent,TOV_percent,USG_percent,ORtg,DRtg,teamName,teamID,opponentTeamName,opponentTeamID,home,month,day,year,url,dateString,season) VALUES " + listPercentS_Generator(inserts)
    print (inserts)
    cursor.execute(statement,inserts)
    cnx.commit()

def playerAdvancedBoxScore(soup,cnx,cursor,teamName,teamID,opponentTeamName,opponentTeamID,home,month,day,year,season,url):
    dateString = year +"-"+month+"-"+day
    
    
    #find the id of the table you're trying to scrape and insert it below
    #tables = soup.find_all('table')
    #awayTable = tables[7]
    #homeTable = tables[15]
    
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

    stringID = "div_box-"+teamName+"-game-advanced"
    table = soup.find('div', attrs={'id': stringID}).find("table")
    
    rows = table.find_all('tr')
    counter = 2
    row_count = len(rows)
    for row in rows[2:row_count-1]:
        counter+=1
        if (counter == 8):
            continue
        
            
        columns = row.find_all('td')
        playerName = row.find('th').text
        if len(columns) == 1:
            break
        else:
            
            #splitting the minutes into a number
            min_string = columns[0].text

            min_list = min_string.split(":")
            minute = int(min_list[0])
            second = int(min_list[1])
        
            total_min = minute + second/60
        
            MP = total_min
            
            if columns[1].text == "":
                TS_percent = None
            else:
                TS_percent = float(columns[1].text)
            
            if columns[2].text == "":
                eFG_percent = None
            else:
                eFG_percent = float(columns[2].text)
            
            if columns[3].text == "":
                threePAr = None
            else:
                threePAr = float(columns[3].text)
            
            if columns[4].text == "":
                FTr = None
            else:
                FTr = float(columns[4].text)
            
            if columns[5].text == "":
                ORB_percent = None
            else:
                ORB_percent = float(columns[5].text)
            
            if columns[6].text == "":
                DRB_percent = None
            else:
                DRB_percent = float(columns[6].text)
                
            if columns[7].text == "":
                TRB_percent = None
            else:
                TRB_percent = float(columns[7].text)
            
            if columns[8].text == "":
                AST_percent = None
            else:
                AST_percent = float(columns[8].text)
                
            if columns[9].text == "":
                STL_percent = None
            else:
                STL_percent = float(columns[9].text)
            
            if columns[10].text == "":
                BLK_percent = None
            else:
                BLK_percent = float(columns[10].text)
            
            if columns[11].text == "":
                TOV_percent = None
            else:
                TOV_percent = float(columns[11].text)
        
            if columns[12].text == "":
                USG_percent = None
            else:
                USG_percent = float(columns[12].text)
            
            if columns[13].text == "":
                ORtg = None
            else:
                ORtg = float(columns[13].text)
            
            if columns[14].text == "":
                DRtg = None
            else:
                DRtg = float(columns[14].text)
            try:
                if columns[15].text == "":
                    BPM = None
                else:
                    BPM = float(columns[15].text)
            except:
                break
            inserts = [playerName,MP,TS_percent,eFG_percent,threePAr, FTr,ORB_percent,DRB_percent,TRB_percent,AST_percent,STL_percent,BLK_percent,TOV_percent,USG_percent,ORtg,DRtg,BPM,teamName,teamID,opponentTeamName,opponentTeamID,home,month,day,year,url,dateString,season]
            statement = "INSERT INTO playerAdvancedBoxStats (playerName,MP,TS_percent,eFG_percent,threePAr, FTr,ORB_percent,DRB_percent,TRB_percent,AST_percent,STL_percent,BLK_percent,TOV_percent,USG_percent,ORtg,DRtg,BPM,teamName,teamID,opponentTeamName,opponentTeamID,home,month,day,year,url,dateString,season) VALUES " + listPercentS_Generator(inserts)
            print (inserts)
            cursor.execute(statement,inserts)
            cnx.commit()

def playerBasicBoxScore(soup, cnx, cursor, teamName,teamID,opponentTeamName,opponentTeamID,home,month,day,year,season,url):
    dateString = year +"-"+month+"-"+day
    
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
    
    #find the id of the table you're trying to scrape and insert it below
    #tables = soup.find_all('table')
    #awayTable = tables[0]
    #homeTable = tables[8]
    
    stringID = "div_box-"+teamName+"-game-basic"
    table = soup.find('div', attrs={'id': stringID}).find("table")
    #start with the away team players
    rows = table.find_all('tr')
    counter = 2
    row_count = len(rows)
    for row in rows[2:row_count-1]:
        counter += 1
        if (counter == 8):
            continue
        
            
        columns = row.find_all('td')
        playerName = row.find('th').text
        if len(columns) == 1:
            break
        else:
            
            #splitting the minutes into a number
            min_string = columns[0].text
            
            min_list = min_string.split(":")
            minute = int(min_list[0])
            second = int(min_list[1])
    
            total_min = minute + second/60
    
            MP = total_min
    
            FG = int(columns[1].text)
    
            FGA = int(columns[2].text)
            
            if columns[3].text == "":
                FG_percent = None
            else:
                FG_percent = float(columns[3].text)
            threeP = int(columns[4].text)
            threePA = int(columns[5].text)
            
            if columns[6].text == "":
                threeP_percent = None
            else:
                threeP_percent = float(columns[6].text)
            FT = int(columns[7].text)
            FTA = int(columns[8].text)
            
            if columns[9].text == "":
                FT_percent = None
            else:
                FT_percent = float(columns[9].text)
            ORB = int(columns[10].text)
            DRB = int(columns[11].text)
            TRB = int(columns[12].text)
            AST = int(columns[13].text)
            STL = int(columns[14].text)
            BLK = int(columns[15].text)
            TOV = int(columns[16].text)
            PF = int(columns[17].text)
            PTS = int(columns[18].text)
            if columns[19].text == "":
                plusMinus = None
            else:
                plusMinus = columns[19].text
                if plusMinus[0] == "+":
                    plusMinus = plusMinus[1:]
                    plusMinus = int(plusMinus)
                else:
                    plusMinus = int(plusMinus)
    
            inserts = [playerName, MP, FG, FGA, FG_percent, threeP, threePA, threeP_percent, FT, FTA, FT_percent, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, plusMinus,teamName,teamID,opponentTeamName,opponentTeamID,home,month,year,day,url,dateString,season]
            statement = "INSERT INTO playerBasicBoxStats (playerName, MP, FG, FGA, FG_percent, threeP, threePA, threeP_percent, FT, FTA, FT_percent, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, plusMinus,teamName,teamID,opponentTeamName,opponentTeamID,home,month,year,day,url,dateString,season) VALUES " + listPercentS_Generator(inserts)
        
            print(inserts)
            cursor.execute(statement,inserts)
            cnx.commit()

def updateBoxStats(cnx,cursor,startMonth,startDay,startYear,endMonth,endDay,endYear,season):
    # this function takes in dates as strings so month 5 should be month '05'
    
    # Go through all possible urls and run a scraper
    # determine the maximum ID from a table so that you know what has been added
    
    teamsDic = {"ATL":11, "BOS":2, "BRK":3, "CHO":13, "CHI":9, "CLE":8, "DAL":28, "DEN":17,
                      "DET":10, "GSW":24, "HOU":29, "IND":7, "LAC":22, "LAL":21, "MEM":26, "MIA":14,
                      "MIL":6, "MIN":20, "NOP":30, "NYK":4, "OKC":19, "ORL":12, "PHI":1, "PHO":23,
                      "POR":18, "SAC":25, "SAS":27, "TOR":5, "UTA":16, "WAS":15}
    
    beginDate = [startMonth,startDay,startYear]
    endDate = [endMonth,endDay,endYear]
    
    if startMonth[0] == "0":
        startMonth = startMonth[1]
        startMonth = int(startMonth)
    else:
        startMonth = int(startMonth)
        
    if endMonth[0] == "0":
        endMonth = endMonth[1]
        endMonth = int(endMonth)
    else:
        endMonth = int(endMonth)
    
    if startDay[0] == "0":
        startDay = startDay[1]
        startDay = int(startDay) 
    else:
        startDay = int(startDay)  
        
    if endDay[0] == "0":
        endDay = endDay[1]
        endDay = int(endDay) 
    else:
        endDay = int(endDay)  
    
    startYear = int(startYear)
    endYear = int(endYear)
    
    datesList = listOfDates(startYear,endYear,startMonth,endMonth,startDay,endDay)
    
    startTicker = getIndexPausedAt(datesList, beginDate)
    endTicker = getIndexPausedAt(datesList, endDate)
    
    ticker = -1
    for date in datesList:   
        ticker +=1
        if (ticker >= startTicker) and (ticker <= endTicker):
        
           for team in teamsDic:
               month = date[0]
               day = date[1]
               year = date[2]
               url = requests.get(teamScheduleBoxScore_UrlGenerator(year,month,day,team))
               webLink = teamScheduleBoxScore_UrlGenerator(year,month,day,team)
               soup = BeautifulSoup(url.text, 'html.parser')
               
    
               if soup.find_all('p')[0].text == "We apologize, but we could not find the page requested by your device.":
                   print ("There is not a game where",team,"played as the home team on",month,"/",day,"/",year)
               else:
                   awayAndHome = getTeamsPlayed(soup)
                   awayTeam = awayAndHome[0]
                   homeTeam = awayAndHome[1]
                   teamAdvancedBoxScore(soup,cnx,cursor,awayTeam,teamsDic[awayTeam],homeTeam,teamsDic[homeTeam],0,month,day,year,season,webLink)
                   teamAdvancedBoxScore(soup,cnx,cursor,homeTeam,teamsDic[homeTeam],awayTeam,teamsDic[awayTeam],1,month,day,year,season,webLink)
                   teamBasicBoxScore(soup,cnx,cursor,awayTeam,teamsDic[awayTeam],homeTeam,teamsDic[homeTeam],0,month,day,year,season,webLink)
                   teamBasicBoxScore(soup,cnx,cursor,homeTeam,teamsDic[homeTeam],awayTeam,teamsDic[awayTeam],1,month,day,year,season,webLink)
                   print ("______________________________________")
                   print ("Finished team box stats for", awayTeam,"on",month,"/",day,"/",year)
                   print ("______________________________________")
                   playerBasicBoxScore(soup,cnx,cursor,awayTeam,teamsDic[awayTeam],homeTeam,teamsDic[homeTeam],0,month,day,year,season,webLink)
                   playerBasicBoxScore(soup,cnx,cursor,homeTeam,teamsDic[homeTeam],awayTeam,teamsDic[awayTeam],1,month,day,year,season,webLink)
                   playerAdvancedBoxScore(soup,cnx,cursor,awayTeam,teamsDic[awayTeam],homeTeam,teamsDic[homeTeam],0,month,day,year,season,webLink)
                   playerAdvancedBoxScore(soup,cnx,cursor,homeTeam,teamsDic[homeTeam],awayTeam,teamsDic[awayTeam],1,month,day,year,season,webLink)
                   print ("______________________________________")
                   print ("Finished player box stats for", awayTeam,"on",month,"/",day,"/",year)
                   print ("______________________________________")

               
    updateDateColumn(cnx,cursor)

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

    #updateBoxStats(cnx,cursor,'10','01','2014','12','31','2014',2015)
    #updateBoxStats(cnx,cursor,startMonth,startDay,startYear,endMonth,endDay,endYear,season)
    '''
    # end of first month
    startMonth = '04'
    startDay = '21'
    startYear = '2021'
    
    endMonth = '04'
    endDay = '31'
    endYear = '2021'
    
    season = 2021
    
    updateBoxStats(cnx,cursor,startMonth,startDay,startYear,endMonth,endDay,endYear,season)
    
    # start of second month
    startMonth = '05'
    startDay = '01'
    startYear = '2021'
    
    endMonth = '05'
    endDay = '10'
    endYear = '2021'
    
    season = 2021
    
    updateBoxStats(cnx,cursor,startMonth,startDay,startYear,endMonth,endDay,endYear,season)
    '''
    # you should probably always run these functions
    updateDateColumn(cnx,cursor)
    deleteDuplicateRows(cnx,cursor)
    
    
    
    
    
    
    

    