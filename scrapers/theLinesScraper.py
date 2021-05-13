#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 00:24:12 2021

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

def updateDateColumn(cnx,cursor):
    updateString = "update playerLines a set date = STR_TO_DATE(dateString, '%Y-%m-%d')"
    cursor.execute(updateString)
    cnx.commit()
    return

def deleteEarlyToday(cnx,cursor,month,day,year):
    dateString = year +"-"+month+"-"+day
    
    statement = "DELETE from playerLines where dateString = '" + dateString + "'"
    cursor.execute(statement)
    cnx.commit()
    return

def deleteEntireTable(cnx,cursor):
    statement = "DELETE from playerLines"
    cursor.execute(statement)
    cnx.commit()
    return
    
def getPlayerList(teamList, cnx, cursor):
    
    statement = "SELECT playerName_noAccents,teamName from playerReference where (season = 2021 and teamName = '"
    
    for team in teamList:
        statement += str(team)
        statement += "')"
        
        statement += " or (season = 2021 and teamName = '"
    
    
    size = len(statement)
    removeSize = len("') or (season = 2021 and teamName = '")
    statement = statement[:size - removeSize]
    statement += "')"
    
    print (statement)
    cursor.execute(statement)
    
    players = cursor.fetchall()
    
    return players

def listPercentS_Generator(inserts):
    
    percentSList = '('
    for i in range(0,len(inserts)):
        if i == len(inserts) - 1:
            percentSList = percentSList + '%s)'
        else:
            percentSList = percentSList + '%s, '
    
    return percentSList

def getPlayerURL(playerName):
    
    driver.get('https://www.thelines.com/betting/prop-bets/nba/')
    select = driver.find_element_by_class_name("metabet-side-odds-browser-query")
    
    select.send_keys(playerName)
    select.send_keys(Keys.RETURN)
    currentUrl = driver.current_url
    
    return currentUrl

def selectPlayer(playerName):
    
    select = driver.find_element_by_class_name("metabet-side-odds-browser-query")
    
    select.send_keys(playerName)
    select.send_keys(Keys.RETURN)
    
    return

def getOverAndUnder(url, category, className, playerName,teamName, cnx, cursor,month,day,year):
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
    
    casinoAbbrevs = {"Fanduel": "fanduel", "MGM": "mgm", "William Hill":"william_hill", "DraftKings":"draftkings", "BetRivers":"bet_rivers","PointsBet":"pointsbet"}
    
    #driver.get(url)
    
    betOverview = driver.find_element_by_class_name(className)
    
    homeAway = betOverview.find_element(By.XPATH,'//em').text
    awayTeam = homeAway[1:4]
    homeTeam = homeAway[5:8]
    
    if teamName == awayTeam:
        opponentTeamName = homeTeam
    else:
        opponentTeamName = awayTeam
    
    overUnders = betOverview.find_elements_by_class_name("metabet-side-odds-browser-options-bet")
    
    
    i = 1
    for element in overUnders:
        
        link = element.get_attribute('href')
        
        website = "Unknown"
        for abbrev in casinoAbbrevs:
            if casinoAbbrevs[abbrev] in link:
                website = abbrev
                break
        
        if i%2==1:

            fullText = element.text
            parts = fullText.split()
    
            target = float(parts[1])
            underOdds = parts[2]
            
            if "+" in underOdds:
                underOdds = underOdds[1:]
                underOdds = int(underOdds)
            else:
                underOdds = int(underOdds)
                
            if underOdds < 0:
                underProfit = 100/(-1*underOdds)
                underPayout = 1 + underProfit
            else:
                underProfit = underOdds/100
                underPayout = 1 + underProfit
        if i%2==0:

            fullText = element.text
            parts = fullText.split()
    
            target = float(parts[1])
            overOdds = parts[2]
            
            if "+" in overOdds:
                overOdds = overOdds[1:]
                overOdds = int(overOdds)
            else:
                overOdds = int(overOdds)
            if overOdds < 0:
                overProfit = 100/(-1*float(overOdds))
                overPayout = 1 + overProfit
            else:
                overProfit = float(overOdds)/100
                overPayout = 1 + overProfit
        
        if i%2==0:

            inserts = (playerName,teamName,opponentTeamName, homeTeam,awayTeam,website, category, target, underOdds, overOdds,underProfit,overProfit,underPayout,overPayout,dateString,month,day,year)
        
            statement = "INSERT INTO playerLines (playerName,teamName,opponentTeamName,homeTeam,awayTeam, website, category, target, underOdds,overOdds,underProfit,overProfit,underPayout,overPayout,dateString,month,day,year) VALUES " + listPercentS_Generator(inserts)
            cursor.execute(statement,inserts)
            cnx.commit()
            print (inserts)
        
        i+=1
    return 

def selectState(state):
    
    selector = Select(driver.find_element_by_xpath("//select[option='" + state + "']")).select_by_value(state)
    
    return


if __name__ == "__main__":
    
    ###########################
    # start of frequently used
    ###########################
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    teamsDic = {"ATL":11, "BOS":2, "BRK":3, "CHO":13, "CHI":9, "CLE":8, "DAL":28, "DEN":17,
                      "DET":10, "GSW":24, "HOU":29, "IND":7, "LAC":22, "LAL":21, "MEM":26, "MIA":14,
                      "MIL":6, "MIN":20, "NOP":30, "NYK":4, "OKC":19, "ORL":12, "PHI":1, "PHO":23,
                      "POR":18, "SAC":25, "SAS":27, "TOR":5, "UTA":16, "WAS":15}

    #betCategories = ["POINTS", "REBOUNDS", "ASSISTS", "BLOCKS", "STEALS", "TURNOVERS", "POINTS_REBOUNDS", "POINTS_ASSISTS", "REBOUNDS_ASSISTS", "STEALS_BLOCKS", "POINTS_REBOUNDS_ASSISTS", "3_POINTERS_MADE", "DOUBLE_DOUBLE", "TRIPLE_DOUBLE", "SCORE_FIRST_FIELD_GOAL"]
    #classList = ["metabet-side-odds-browser-market-NBA_GAME_PLAYER_POINTS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_REBOUNDS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_ASSISTS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_BLOCKS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_STEALS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_TURNOVERS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_POINTS_REBOUNDS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_POINTS_ASSISTS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_REBOUNDS_ASSISTS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_STEALS_BLOCKS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_POINTS_REBOUNDS_ASSISTS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_3_POINTERS_MADE", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_DOUBLE_DOUBLE", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_TRIPLE_DOUBLE", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_SCORE_FIRST_FIELD_GOAL"]

    betCategories = ["POINTS", "REBOUNDS", "ASSISTS", "POINTS_REBOUNDS", "POINTS_ASSISTS", "REBOUNDS_ASSISTS", "POINTS_REBOUNDS_ASSISTS", "3_POINTERS_MADE"]
    classList = ["metabet-side-odds-browser-market-NBA_GAME_PLAYER_POINTS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_REBOUNDS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_ASSISTS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_POINTS_REBOUNDS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_POINTS_ASSISTS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_REBOUNDS_ASSISTS",  "metabet-side-odds-browser-market-NBA_GAME_PLAYER_POINTS_REBOUNDS_ASSISTS", "metabet-side-odds-browser-market-NBA_GAME_PLAYER_3_POINTERS_MADE"]



    categoryDict = {}
    for key in betCategories:
        for value in classList:
            categoryDict[key] = value
            classList.remove(value)
            break
    
    #########################
    # end of frequently used
    #########################
    
    ######## inputs ########
    #teamList = ["OKC","GSW","LAL","LAC"]
    
    # either use your own created team list from above or grab each teamname from the teams dictionary previously listed
    
    teamList = []
    for teamName in teamsDic:
        teamList.append(teamName)
    
    
    state = "MI"
    month = '05'
    day = '07'
    year = '2021'
    ##########################
    
    PATH = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(PATH)
    
    driver.get('https://www.thelines.com/betting/prop-bets/nba/')

    time.sleep(1)
    
    selectState(state)

    players = getPlayerList(teamList, cnx, cursor)
    
    
    deleteEntireTable(cnx,cursor)
    
    
    for result in players:
        playerName = result[0]
        teamName = result[1]
        url = getPlayerURL(playerName)
        selectState(state)
        time.sleep(1)
        for category in categoryDict:
            
            
            try:
                getOverAndUnder(url, category, categoryDict[category], playerName,teamName, cnx, cursor,month,day,year)
            except:
                print ("There are no bets available for ", playerName)
                break
        updateDateColumn(cnx,cursor)
    
    
    
    
    
    # testing out individual player for experimenting
    '''
    result = ["Kevin Durant","BRK"]
    playerName = result[0]
    teamName = result[1]
    url = getPlayerURL(playerName)
    selectState(state)
    time.sleep(1)
    for category in categoryDict:
        
        
    
        getOverAndUnder(url, category, categoryDict[category], playerName,teamName, cnx, cursor,month,day,year)
    
        print ("There are no bets available for ", playerName)
        break
    updateDateColumn(cnx,cursor)
    '''

