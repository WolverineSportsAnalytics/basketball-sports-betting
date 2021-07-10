#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 00:20:38 2021

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


def playerBasicGenerator(cnx,cursor):
    
    #################################################################################################################################
    statement = "SELECT * from playerBasicBoxStats_PerMin where MP >= 10"
    cursor.execute(statement)
    playerBasic_PerMin = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'playerBasicBoxStats_PerMin'"
    cursor.execute(statement)
    results = cursor.fetchall()
    playerBasic_PerMin_columns = []
    for result in results:
        playerBasic_PerMin_columns.append(result[0])
    playerBasic_PerMin = pd.DataFrame(playerBasic_PerMin,columns = playerBasic_PerMin_columns)
    playerBasic_PerMin = playerBasic_PerMin.add_prefix('PB_')
    
    #################################################################################################################################
    statement = "SELECT * from playerAdvancedBoxStats where MP >= 10"
    cursor.execute(statement)
    playerAdvanced = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'playerAdvancedBoxStats'"
    cursor.execute(statement)
    results = cursor.fetchall()
    playerAdvanced_columns = []
    for result in results:
        playerAdvanced_columns.append(result[0])
    playerAdvanced = pd.DataFrame(playerAdvanced,columns = playerAdvanced_columns)
    playerAdvanced = playerAdvanced.add_prefix('PA_')

    #################################################################################################################################
    statement = "SELECT * from teamBasicBoxStats_PerMin"
    cursor.execute(statement)
    teamBasic_PerMin = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamBasicBoxStats_PerMin'"
    cursor.execute(statement)
    results = cursor.fetchall()
    teamBasic_PerMin_columns = []
    for result in results:
        teamBasic_PerMin_columns.append(result[0])
    teamBasic_PerMin = pd.DataFrame(teamBasic_PerMin,columns = teamBasic_PerMin_columns)
    teamBasic_PerMin = teamBasic_PerMin.add_prefix('TB_')

    #################################################################################################################################
    statement = "SELECT * from teamAdvancedBoxStats"
    cursor.execute(statement)
    teamAdvanced = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamAdvancedBoxStats'"
    cursor.execute(statement)
    results = cursor.fetchall()
    teamAdvanced_columns = []
    for result in results:
        teamAdvanced_columns.append(result[0])
    teamAdvanced = pd.DataFrame(teamAdvanced,columns = teamAdvanced_columns)
    teamAdvanced = teamAdvanced.add_prefix('TA_')
    #################################################################################################################################
    
    #################################################################################################################################
    statement = "SELECT * from teamBasicBoxStats_PerMin"
    cursor.execute(statement)
    opponentTeamBasic_PerMin = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamBasicBoxStats_PerMin'"
    cursor.execute(statement)
    results = cursor.fetchall()
    opponentTeamBasic_PerMin_columns = []
    for result in results:
        opponentTeamBasic_PerMin_columns.append(result[0])
    opponentTeamBasic_PerMin = pd.DataFrame(opponentTeamBasic_PerMin,columns = opponentTeamBasic_PerMin_columns)
    opponentTeamBasic_PerMin = opponentTeamBasic_PerMin.add_prefix('OTB_')

    #################################################################################################################################
    statement = "SELECT * from teamAdvancedBoxStats"
    cursor.execute(statement)
    opponentTeamAdvanced = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamAdvancedBoxStats'"
    cursor.execute(statement)
    results = cursor.fetchall()
    opponentTeamAdvanced_columns = []
    for result in results:
        opponentTeamAdvanced_columns.append(result[0])
    opponentTeamAdvanced = pd.DataFrame(opponentTeamAdvanced,columns = opponentTeamAdvanced_columns)
    opponentTeamAdvanced = opponentTeamAdvanced.add_prefix('OTA_')
    #################################################################################################################################
    

    
    
    newDF = pd.merge(playerBasic_PerMin,playerAdvanced,how="left",left_on=['PB_playerName','PB_date'],right_on=['PA_playerName','PA_date'])
    
    newDF = pd.merge(newDF,teamBasic_PerMin,how="left",left_on=['PB_teamName','PB_date'],right_on=['TB_teamName','TB_date'])
    
    newDF = pd.merge(newDF,teamAdvanced,how="left",left_on=['PB_teamName','PB_date'],right_on=['TA_teamName','TA_date'])
    
    newDF = pd.merge(newDF,opponentTeamBasic_PerMin,how="left",left_on=['PB_opponentTeamName','PB_date'],right_on=['OTB_teamName','OTB_date'])
    
    newDF = pd.merge(newDF,opponentTeamAdvanced,how="left",left_on=['PB_opponentTeamName','PB_date'],right_on=['OTA_teamName','OTA_date'])
    
    
    # this is a list of things that are either constant or are game information such as a player's name
    deleteList = ["OTA_USG_percent","TA_USG_percent","PB_playerBasicBoxStats_PerMinID","PB_playerName","PB_teamName","PB_teamID","PB_opponentTeamName","PB_opponentTeamID","PB_home","PB_month","PB_day","PB_year","PB_dateString","PB_date","PB_season","PB_url","PA_playerAdvancedBoxStatsID","PA_playerName","PA_teamName","PA_teamID","PA_opponentTeamName","PA_opponentTeamID","PA_home","PA_month","PA_day","PA_year","PA_dateString","PA_date","PA_season","PA_url","TB_teamBasicBoxStatsID","TB_teamName","TB_teamID","TB_opponentTeamName","TB_opponentTeamID","TB_home","TB_month","TB_day","TB_year","TB_dateString","TB_date","TB_season","TB_url","TA_teamAdvancedBoxStatsID","TA_teamName","TA_teamID","TA_opponentTeamName","TA_opponentTeamID","TA_home","TA_month","TA_day","TA_year","TA_dateString","TA_date","TA_season","TA_url","OTB_teamBasicBoxStatsID","OTB_teamName","OTB_teamID","OTB_opponentTeamName","OTB_opponentTeamID","OTB_home","OTB_month","OTB_day","OTB_year","OTB_dateString","OTB_date","OTB_season","OTB_url","OTA_teamAdvancedBoxStatsID","OTA_teamName","OTA_teamID","OTA_opponentTeamName","OTA_opponentTeamID","OTA_home","OTA_month","OTA_day","OTA_year","OTA_dateString","OTA_date","OTA_season","OTA_url","OTA_MP","OTB_MP","TA_MP","TB_MP","PA_MP","PB_MP"]
    newDF = newDF.drop(columns=deleteList)
    
    playerPointsTarget = newDF[newDF["PB_PTS"]]
    playerReboundsTarget = newDF[newDF["PB_TRB"]]
    playerAssistsTarget = newDF[newDF["PB_AST"]]
    playerThreePointersTarget = newDF[newDF["PB_threeP"]]
    
    
    # now depending on the target variable you have to delete various elements
    
    # trying to predict player points:
    deleteList_playerPoints = ["PB_FG","PB_FGA","PB_FG_percent","PB_threeP","PB_threePA","PB_threeP_percent","PB_FT","PB_FTA","PB_FT_percent","PA_TS_percent","PA_eFG_percent","PA_threePAr","PA_FTr","PB_PTS"]
    playerPointsDF = newDF.drop(columns=deleteList_playerPoints)
    
    # trying to predict player rebounds:
    deleteList_playerRebounds = ["PB_ORB","PB_DRB","PA_ORB_percent","PA_DRB_percent","PA_TRB_percent","PB_TRB"]
    playerReboundsDF = newDF.drop(columns=deleteList_playerRebounds)
    
    # trying to predict player assists:
    deleteList_playerAssists = ["PA_AST_percent","PB_AST"]
    playerAssistsDF = newDF.drop(columns=deleteList_playerAssists)
    
    # trying to predict player threePointers:
    deleteList_playerThreePointers = ["PB_FG","PB_FGA","PB_FG_percent","PB_threePA","PB_threeP_percent","PB_PTS","PA_TS_percent","PA_eFG_percent","PA_threePAr","PB_threeP"]
    playerThreePointersDF = newDF.drop(columns=deleteList_playerThreePointers)
    
    for column in newDF.columns:
        print (column)
    
    os.chdir("/Users/lissjust/Desktop")
    #### newDF.to_csv('player_occurences_PB_PA_TB_TA_OTB_OTA.csv',index=False)
    
    return

def joinPlayerBasic_PerMinAVG(DF,team,season,date,gameColumns):
    
    for index, row in DF.iterrows():
            
        player = row['playerName']
        
        statement = "SELECT b.MP as eventMP,a.* from playerBasicBoxStats_AVG_PerMin a left join playerBasicBoxStats b on a.playerName = b.playerName where a.playerName = %s and a.season = %s and b.date = %s"
        passers = (player,season,date)
        cursor.execute(statement,passers)
        playerAverages = cursor.fetchall()
        appendDF = pd.DataFrame(playerAverages,columns = gameColumns)
        gameDF_basicAverages = DF.append(appendDF,ignore_index=True)
    
    print ("Have DF created of players that played for ", team)
    return gameDF_basicAverages

def blankPlayerBasicsAveragesPlusMinutesPlayedDF():
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'playerBasicBoxStats_AVG_PerMin'"
    cursor.execute(statement)
    results = cursor.fetchall()
    gameColumns = []
    for result in results:
        gameColumns.append(result[0])
    gameColumns.append("eventMP")
    gameDF_basicAverages = pd.DataFrame(columns = gameColumns)
    
    return gameDF_basicAverages, gameColumns

def teamPlayerMinutesPlayed_PlayerAdvancedAverages_STD_DEV(teamName,date,season):
    # this grabs the minutes played by all players on the team on that day
    # then it grabs each player's advanced averages STD DEV from that season
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    statement = "SELECT a.playerName,a.MP,b.* from playerBasicBoxStats a left join ______________ b on ____________ where a.date = %s and a.teamName = %s and b.season = %s"
    passers = (date,teamName)
    cursor.execute(statement,passers)
    teamPlayers = cursor.fetchall()
    columns = ["playerName","MP","____________________"]
    teamPlayersDF = pd.DataFrame(teamPlayers,columns = columns)
    print ("Got the minutes played of each player on ", teamName, " and the players' advanced averages STD DEV")
    
    return teamPlayersDF

def teamPlayerMinutesPlayed_PlayerAdvancedAverages(teamName,date,season):
    # this grabs the minutes played by all players on the team on that day
    # then it grabs each player's advanced averages from that season
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    statement = "SELECT a.playerName,a.MP,b.* from playerBasicBoxStats a left join ______________ b on ____________ where a.date = %s and a.teamName = %s and b.season = %s"
    passers = (date,teamName)
    cursor.execute(statement,passers)
    teamPlayers = cursor.fetchall()
    columns = ["playerName","MP","____________________"]
    teamPlayersDF = pd.DataFrame(teamPlayers,columns = columns)
    print ("Got the minutes played of each player on ", teamName, " and the players' advanced averages")
    
    return teamPlayersDF

def teamPlayerMinutesPlayed_PlayerBasicAveragesPerMin_STD_DEV(teamName,date,season):
    # this grabs the minutes played by all players on the team on that day
    # then it grabs each player's basic averages per min STD DEV from that season
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    statement = "SELECT a.playerName,a.MP,b.* from playerBasicBoxStats a left join ______________ b on ____________ where a.date = %s and a.teamName = %s and b.season = %s"
    passers = (date,teamName)
    cursor.execute(statement,passers)
    teamPlayers = cursor.fetchall()
    columns = ["playerName","MP","____________________"]
    teamPlayersDF = pd.DataFrame(teamPlayers,columns = columns)
    print ("Got the minutes played of each player on ", teamName, " and the players' basic averages per min STD DEV")
    
    return teamPlayersDF

def teamPlayerMinutesPlayed_PlayerBasicAveragesPerMin(teamName,date,season):
    # this grabs the minutes played by all players on the team on that day
    # then it grabs each player's basic averages per min from that season
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    statement = "SELECT a.playerName,a.MP,b.* from playerBasicBoxStats a left join ______________ b on ____________ where a.date = %s and a.teamName = %s and b.season = %s"
    passers = (date,teamName)
    cursor.execute(statement,passers)
    teamPlayers = cursor.fetchall()
    columns = ["playerName","MP","____________________"]
    teamPlayersDF = pd.DataFrame(teamPlayers,columns = columns)
    print ("Got the minutes played of each player on ", teamName, " and the players' basic averages per min")
    
    return teamPlayersDF
    
def teamPlayerMinutesPlayed_PlayerAverages(teamName,date,season):
    # this grabs the minutes played by all players on the team on that day
    # then it grabs each player's basic averages per min from that season
    # then it grabs each player's basic averages per min std dev from that season
    # then it grabs each player's advanced averages from that season
    # then it grabs each player's advanced averages std dev from that season
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    statement = "SELECT a.playerName,a.MP,b.*,c.*,d.*,e.* from playerBasicBoxStats a left join ______________ b on ____________ left join ______________ c on ____________ left join ______________ d on ____________ left join ______________ e on ____________ where a.date = %s and a.teamName = %s and b.season = %s and c.season = %s and d.season = %s and e.season = %s"
    passers = (date,teamName)
    cursor.execute(statement,passers)
    teamPlayers = cursor.fetchall()
    columns = ["playerName","MP"]
    teamPlayersDF = pd.DataFrame(teamPlayers,columns = columns)
    print ("Got the minutes played of each player on ", teamName)
    
    return teamPlayersDF
    
def getPreviousEvents():
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    # getting the game events
    #################################################################
    statement = "SELECT * from scheduleNBA_previous"
    cursor.execute(statement)
    queryTuple = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'scheduleNBA_previous'"
    cursor.execute(statement)
    results = cursor.fetchall()
    DFcolumns = []
    for result in results:
        DFcolumns.append(result[0])
    previousGamesDF = pd.DataFrame(queryTuple,columns = DFcolumns)
    
    print ("Finished getting previous NBA games")
    
    return previousGamesDF
    
def groupedTeamOccurencesAsPlayerAverages(cnx,cursor):
    
    '''
    So what I'm trying to do is create a dataframe that includes the minutes played
    by each player and their corresponding average stats which I will then create a new 
    dataframe from that takes the wegithed average so we can see what the team did
    '''
    
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    #########
    previousGamesDF = getPreviousEvents()
    #########

    ################################################################
    
    j = len(previousGamesDF.index)
    i = 0
    
    # going through each game
    for index, row in previousGamesDF.iterrows():
        
        team = row['teamName']
        opponent = row['opponentTeamName']
        date = row['date']
        season = row['season']
        print ("Working on ", team, opponent, date,season)
        
        # finding minutes played by each player on team for a given date
        teamPlayersMinutesPlayed_plus_AveragesDF = teamPlayerMinutesPlayed_PlayerAverages(team,date,season)

        # finding minutes played by each player on opponentTeam for a given date
        opponentTeamPlayersMinutesPlayed_plus_AveragesDF = teamPlayerMinutesPlayed_PlayerAverages(opponent,date,season)
        
        # checking how many minutes were in the game overall meaning 5*minutes of the game since there are 5 players on the floor at all times
        totalMinutesPlayed = teamPlayersMinutesPlayed_plus_AveragesDF['MP'].sum()
        
        '''
        # creating a blank dataframe to append each player's stats to
        gameDF_basicAverages_team, gameColumns = blankPlayerBasicsAveragesPlusMinutesPlayedDF()
        gameDF_basicAverages_opponent = gameDF_basicAverages_team
        
        # go through each player that played in the game for the team and append their stats to the previous stats
        gameDF_basicAverages_team = joinPlayerBasic_PerMinAVG(teamPlayerMinutesPlayedDF,team,season,date,gameColumns)
        
        # go through each player that played in the game for the opponent team and append their stats to the previous stats
        gameDF_basicAverages_opponentTeam = joinPlayerBasic_PerMinAVG(opponentTeamPlayerMinutesPlayedDF,opponent,season,date,gameColumns)
        '''
        
        print ("Finished row", i, "of", j)
        i += 1
        break
        
    return 

def joiningSQLStuff(cursor,cnx):
    
    ##################### playerBasicBoxStats_PerMin #####################
    statement = "SELECT playerName,teamName,opponentTeamName,date,season,MP,PTS,TRB,AST,threeP from playerBasicBoxStats_PerMin where MP >= 10"
    cursor.execute(statement)
    playerBasic_PerMin = cursor.fetchall()

    playerBasic_PerMin_columns = ["playerName","teamName","opponentTeamName","date","season","MP","PTS","TRB","AST","threeP"]
    playerBasic_PerMin = pd.DataFrame(playerBasic_PerMin,columns = playerBasic_PerMin_columns)
    playerBasic_PerMin = playerBasic_PerMin.add_prefix('PB_')
    ######################################################################
    print ("player basic")
    
    #################### playerBasicBoxStats_AVG_PerMin #############################################################################################################
    statement = "SELECT * from playerBasicBoxStats_AVG_PerMin"
    cursor.execute(statement)
    playerBasic_AVG = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'playerBasicBoxStats_AVG_PerMin'"
    cursor.execute(statement)
    results = cursor.fetchall()
    playerBasic_AVG_columns = []
    for result in results:
        playerBasic_AVG_columns.append(result[0])
    playerBasic_AVG = pd.DataFrame(playerBasic_AVG,columns = playerBasic_AVG_columns)
    playerBasic_AVG = playerBasic_AVG.add_prefix('PB_AVG_')
    ######################################################################
    print ("player basic AVG")
    
    #################### playerBasicBoxStats_STDDEV_PerMin #############################################################################################################
    statement = "SELECT * from playerBasicBoxStats_STDDEV_PerMin"
    cursor.execute(statement)
    playerBasic_STDDEV = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'playerBasicBoxStats_STDDEV_PerMin'"
    cursor.execute(statement)
    results = cursor.fetchall()
    playerBasic_STDDEV_columns = []
    for result in results:
        playerBasic_STDDEV_columns.append(result[0])
    playerBasic_STDDEV = pd.DataFrame(playerBasic_STDDEV,columns = playerBasic_STDDEV_columns)
    playerBasic_STDDEV = playerBasic_STDDEV.add_prefix('PB_STDDEV_')
    ######################################################################
    print ("player basic stddev")
    
    #################### playerAdvancedBoxStats_AVG #############################################################################################################
    statement = "SELECT * from playerAdvancedBoxStats_AVG"
    cursor.execute(statement)
    playerAdvanced_AVG = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'playerAdvancedBoxStats_AVG'"
    cursor.execute(statement)
    results = cursor.fetchall()
    playerAdvanced_AVG_columns = []
    for result in results:
        playerAdvanced_AVG_columns.append(result[0])
    playerAdvanced_AVG = pd.DataFrame(playerAdvanced_AVG,columns = playerAdvanced_AVG_columns)
    playerAdvanced_AVG = playerAdvanced_AVG.add_prefix('PA_AVG_')
    ######################################################################
    print ("player advanced AVG")
    
    #################### playerAdvancedBoxStats_STDDEV #############################################################################################################
    statement = "SELECT * from playerAdvancedBoxStats_STDDEV"
    cursor.execute(statement)
    playerAdvanced_STDDEV = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'playerAdvancedBoxStats_STDDEV'"
    cursor.execute(statement)
    results = cursor.fetchall()
    playerAdvanced_STDDEV_columns = []
    for result in results:
        playerAdvanced_STDDEV_columns.append(result[0])
    playerAdvanced_STDDEV = pd.DataFrame(playerAdvanced_STDDEV,columns = playerAdvanced_STDDEV_columns)
    playerAdvanced_STDDEV = playerAdvanced_STDDEV.add_prefix('PA_STDDEV_')
    ######################################################################
    print ("player advanced stddev")
    
    #################### teamBasicBoxStats_fromPlayerAverages teamName #############################################################################################################
    statement = "SELECT * from teamBasicBoxStats_fromPlayerAverages"
    cursor.execute(statement)
    teamBasic_AVG = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamBasicBoxStats_fromPlayerAverages'"
    cursor.execute(statement)
    results = cursor.fetchall()
    teamBasic_AVG_columns = []
    for result in results:
        teamBasic_AVG_columns.append(result[0])
    teamBasic_AVG = pd.DataFrame(teamBasic_AVG,columns = teamBasic_AVG_columns)
    teamBasic_AVG = teamBasic_AVG.add_prefix('TB_AVG_')
    ######################################################################
    print ("team basic avg")
    
    #################### teamBasicBoxStats_fromPlayerStddevs teamName #############################################################################################################
    statement = "SELECT * from teamBasicBoxStats_fromPlayerStddevs"
    cursor.execute(statement)
    teamBasic_STDDEV = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamBasicBoxStats_fromPlayerStddevs'"
    cursor.execute(statement)
    results = cursor.fetchall()
    teamBasic_STDDEV_columns = []
    for result in results:
        teamBasic_STDDEV_columns.append(result[0])
    teamBasic_STDDEV = pd.DataFrame(teamBasic_STDDEV,columns = teamBasic_STDDEV_columns)
    teamBasic_STDDEV = teamBasic_STDDEV.add_prefix('TB_STDDEV_')
    ######################################################################
    print ("team basic stddev")
    
    #################### teamAdvancedBoxStats_fromPlayerAverages teamName #############################################################################################################
    statement = "SELECT * from teamAdvancedBoxStats_fromPlayerAverages"
    cursor.execute(statement)
    teamAdvanced_AVG = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamAdvancedBoxStats_fromPlayerAverages'"
    cursor.execute(statement)
    results = cursor.fetchall()
    teamAdvanced_AVG_columns = []
    for result in results:
        teamAdvanced_AVG_columns.append(result[0])
    teamAdvanced_AVG = pd.DataFrame(teamAdvanced_AVG,columns = teamAdvanced_AVG_columns)
    teamAdvanced_AVG = teamAdvanced_AVG.add_prefix('TA_AVG_')
    ######################################################################
    print ("team advanced avg")
    
    #################### teamAdvancedBoxStats_fromPlayerStddevs teamName #############################################################################################################
    statement = "SELECT * from teamAdvancedBoxStats_fromPlayerStddevs"
    cursor.execute(statement)
    teamAdvanced_STDDEV = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamAdvancedBoxStats_fromPlayerStddevs'"
    cursor.execute(statement)
    results = cursor.fetchall()
    teamAdvanced_STDDEV_columns = []
    for result in results:
        teamAdvanced_STDDEV_columns.append(result[0])
    teamAdvanced_STDDEV = pd.DataFrame(teamAdvanced_STDDEV,columns = teamAdvanced_STDDEV_columns)
    teamAdvanced_STDDEV = teamAdvanced_STDDEV.add_prefix('TA_STDDEV_')
    ######################################################################
    print ("team advanced stddev")
    
    #################### teamBasicBoxStats_fromPlayerAverages opponentTeamName #############################################################################################################
    statement = "SELECT * from teamBasicBoxStats_fromPlayerAverages"
    cursor.execute(statement)
    opponentTeamBasic_AVG = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamBasicBoxStats_fromPlayerAverages'"
    cursor.execute(statement)
    results = cursor.fetchall()
    opponentTeamBasic_AVG_columns = []
    for result in results:
        opponentTeamBasic_AVG_columns.append(result[0])
    opponentTeamBasic_AVG = pd.DataFrame(opponentTeamBasic_AVG,columns = opponentTeamBasic_AVG_columns)
    opponentTeamBasic_AVG = opponentTeamBasic_AVG.add_prefix('OTB_AVG_')
    ######################################################################
    print ("opponent team basic avg")
    
    #################### teamBasicBoxStats_STDDEV_PerMin opponentTeamName #############################################################################################################
    statement = "SELECT * from teamBasicBoxStats_fromPlayerStddevs"
    cursor.execute(statement)
    opponentTeamBasic_STDDEV = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamBasicBoxStats_fromPlayerStddevs'"
    cursor.execute(statement)
    results = cursor.fetchall()
    opponentTeamBasic_STDDEV_columns = []
    for result in results:
        opponentTeamBasic_STDDEV_columns.append(result[0])
    opponentTeamBasic_STDDEV = pd.DataFrame(opponentTeamBasic_STDDEV,columns = opponentTeamBasic_STDDEV_columns)
    opponentTeamBasic_STDDEV = opponentTeamBasic_STDDEV.add_prefix('OTB_STDDEV_')
    ######################################################################
    print ("opponent team basic stddev")
    
    #################### teamAdvancedBoxStats_fromPlayerAverages opponentTeamName #############################################################################################################
    statement = "SELECT * from teamAdvancedBoxStats_fromPlayerAverages"
    cursor.execute(statement)
    opponentTeamAdvanced_AVG = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamAdvancedBoxStats_fromPlayerAverages'"
    cursor.execute(statement)
    results = cursor.fetchall()
    opponentTeamAdvanced_AVG_columns = []
    for result in results:
        opponentTeamAdvanced_AVG_columns.append(result[0])
    opponentTeamAdvanced_AVG = pd.DataFrame(opponentTeamAdvanced_AVG,columns = opponentTeamAdvanced_AVG_columns)
    opponentTeamAdvanced_AVG = opponentTeamAdvanced_AVG.add_prefix('OTA_AVG_')
    ######################################################################
    print ("opponent team advanced avg")
    
    #################### teamAdvancedBoxStats_STDDEV opponentTeamName #############################################################################################################
    statement = "SELECT * from teamAdvancedBoxStats_fromPlayerStddevs"
    cursor.execute(statement)
    opponentTeamAdvanced_STDDEV = cursor.fetchall()
    statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'teamAdvancedBoxStats_fromPlayerStddevs'"
    cursor.execute(statement)
    results = cursor.fetchall()
    opponentTeamAdvanced_STDDEV_columns = []
    for result in results:
        opponentTeamAdvanced_STDDEV_columns.append(result[0])
    opponentTeamAdvanced_STDDEV = pd.DataFrame(opponentTeamAdvanced_STDDEV,columns = opponentTeamAdvanced_STDDEV_columns)
    opponentTeamAdvanced_STDDEV = opponentTeamAdvanced_STDDEV.add_prefix('OTA_STDDEV_')
    ######################################################################
    print ("opponent team advanced stddev")
    
    # tags 
    # PB_ = playerBasicBoxStats_PerMin
    # PB_AVG_ = playerBasicBoxStats_AVG_PerMin
    # PB_STDDEV_ = playerBasicBoxStats_STDDEV_PerMin
    # TB_AVG_ = teamBasicBoxStats_fromPlayerAverages teamName
    # TB_STDDEV_ = teamBasicBoxStats_fromPlayerStddevs teamName
    # TA_AVG_ = 
    # TA_STDDEV_ = 
    # OTB_AVG_ = 
    # OTB_STDDEV_ = 
    # OTA_AVG_ = 
    # OTA_STDDEV_ = 
    
    #newDF = pd.merge(newDF,,how="left",left_on=[],right_on=[])
    newDF = pd.merge(playerBasic_PerMin,playerBasic_AVG,how="left",left_on=['PB_playerName','PB_season'],right_on=['PB_AVG_playerName','PB_AVG_season'])
    newDF = pd.merge(newDF,playerBasic_STDDEV,how="left",left_on=['PB_playerName','PB_season'],right_on=['PB_STDDEV_playerName','PB_STDDEV_season'])
    newDF = pd.merge(newDF,playerAdvanced_AVG,how="left",left_on=['PB_playerName','PB_season'],right_on=['PA_AVG_playerName','PA_AVG_season'])
    newDF = pd.merge(newDF,playerAdvanced_STDDEV,how="left",left_on=['PB_playerName','PB_season'],right_on=['PA_STDDEV_playerName','PA_STDDEV_season'])
    newDF = pd.merge(newDF,teamBasic_AVG,how="left",left_on=['PB_teamName','PB_date'],right_on=['TB_AVG_teamName', 'TB_AVG_date'])
    newDF = pd.merge(newDF,teamBasic_STDDEV,how="left",left_on=['PB_teamName','PB_date'],right_on=['TB_STDDEV_teamName', 'TB_STDDEV_date'])
    newDF = pd.merge(newDF,teamAdvanced_AVG,how="left",left_on=['PB_teamName','PB_date'],right_on=['TA_AVG_teamName', 'TA_AVG_date'])
    newDF = pd.merge(newDF,teamAdvanced_STDDEV,how="left",left_on=['PB_teamName','PB_date'],right_on=['TA_STDDEV_teamName', 'TA_STDDEV_date'])    
    newDF = pd.merge(newDF,opponentTeamBasic_AVG,how="left",left_on=['PB_opponentTeamName', 'PB_date'],right_on=['OTB_AVG_teamName', 'OTB_AVG_date'])
    newDF = pd.merge(newDF,opponentTeamBasic_STDDEV,how="left",left_on=['PB_opponentTeamName', 'PB_date'],right_on=['OTB_STDDEV_teamName', 'OTB_STDDEV_date'])
    newDF = pd.merge(newDF,opponentTeamAdvanced_AVG,how="left",left_on=['PB_opponentTeamName', 'PB_date'],right_on=['OTA_AVG_teamName', 'OTA_AVG_date'])
    newDF = pd.merge(newDF,opponentTeamAdvanced_STDDEV,how="left",left_on=['PB_opponentTeamName', 'PB_date'],right_on=['OTA_STDDEV_teamName', 'OTA_STDDEV_date'])
    
    print ('newDF created')
    
    os.chdir("/Users/lissjust/Desktop")
    
    newDF.to_csv('largeBasketballDataset.csv')
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

    
    #updateBoxStats(cnx,cursor,startMonth,startDay,startYear,endMonth,endDay,endYear,season)
    
    #updateBoxStats(cnx,cursor,'10','01','2014','12','31','2014',2015)
    
    #################################################################################################################################
    
    #playerBasicGenerator(cnx,cursor)
    #teamsPlayersGrouped(cnx,cursor)
    #teamGameDF, opponentTeamDF = groupedTeamOccurencesAsPlayerAverages(cnx,cursor)
    joiningSQLStuff(cursor, cnx)
    

        
        
    
    
    
    
    
    