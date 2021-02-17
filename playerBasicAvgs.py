import mysql.connector
import requests
from bs4 import BeautifulSoup
import os

def getTeam(soup,cursor,cnx):
    i = 18
    j = 19

    print ("________________________________________________________________________________________________________________________")
    print ("Team Info: " + str(i) + "/" + str(j) + " season")
    list = soup.find('ul', {"class": "list-unstyled"})
    # puts the list items into an array
    list_items = list.findAll('li')
    # print list_items
    teamName = list_items[0].text
    return teamName


def playerAverages(soup,cursor,cnx, teamName):

    tables = soup.find_all("table")

    i = 19
    j = 20
    q = 5

    for table in tables[48:52]:
        print ("________________________________________________________________________________________________________________________")
        print ("Player Average Stats: ", i,"/",j," season")

        rows = table.find_all("tr")
        for row in rows[1:]:
            points = row.find_all("td")
            team = teamName
            player = points[0].text

            # games
            if points[2].text != "":
                gamesPlayed = int(points[2].text)
            else:
                gamesPlayed = 0
            print("Games Played: " + str(gamesPlayed))

            # minutes
            if points[3].text != "":
                minutes = float(points[3].text)
            else:
                minutes = float(0)
            print ("Minutes: " + str(minutes))

            if gamesPlayed == 0 or (minutes == 0.0):
                # does not insert them into table
                print ("Player did not play in a game")
            else:
                # fgm
                if points[4].text != "":
                    fieldGoalMade = float(points[4].text.strip('%'))
                else:
                    fieldGoalMade = float(0)
                print ("fieldGoalMade: " + str(fieldGoalMade))

                # fga
                if points[5].text != "":
                    fieldGoalAttempt = float(points[5].text.strip('%'))
                else:
                    fieldGoalAttempt = float(0)
                print ("fga: " + str(fieldGoalAttempt))

                # field goal %
                if points[6].text != "":
                    fieldGoalPercent = float(points[6].text.strip('%'))
                else:
                    fieldGoalPercent = float(0)
                print ("FG %: " + str(fieldGoalPercent))

                # 2 pm
                if points[7].text != "":
                    twopointmade = float(points[7].text.strip('%'))
                else:
                    twopointmade = float(0)
                # print ("2ptmade: " + str(twopointmade))

                # 2 pa
                if points[8].text != "":
                    twopointattempted = float(points[8].text.strip('%'))
                else:
                    twopointattempted = float(0)
                # print ("2Ptattemped: " + str(twopointattempted))

                # 2p %
                if points[9].text != "":
                    twoPointPercent = float(points[9].text.strip('%'))
                else:
                    twoPointPercent = float(0)
                # print ("2Pt %: " + str(twoPointPercent))

                # 3pm
                if points[10].text != "":
                    threePointMade = float(points[10].text.strip('%'))
                else:
                    threePointMade = float(0)
                # print ("3pt made: " + str(threePointMade))

                # 3pa
                if points[11].text != "":
                    threePointAttempt = float(points[11].text.strip('%'))
                else:
                    threePointAttempt = float(0)
                # print ("threePointAttempt %: " + str(threePointAttempt))

                # 3pt %
                if points[12].text != "":
                    threePointPercent = float(points[12].text.strip('%'))
                else:
                    threePointPercent = float(0)
                # print ("3pt %: " + str(threePointPercent))

                # ftm
                if points[13].text != "":
                    freeThrowMade = float(points[13].text.strip('%'))
                else:
                    freeThrowMade = float(0)
                # print ("ft made: " + str(freeThrowMade))

                # fta
                if points[14].text != "":
                    freeThrowAttempt = float(points[14].text.strip('%'))
                else:
                    freeThrowAttempt = float(0)
                # print ("ft attempted: " + str(freeThrowAttempt))

                # ft %
                if points[15].text != "":
                    freeThrowPercent = float(points[15].text.strip('%'))
                else:
                    freeThrowPercent = float(0)
                # print ("ft %: " + str(freeThrowPercent))

                # orb
                if points[16].text != "":
                    offensiveRebound = float(points[16].text.strip('%'))
                else:
                    offensiveRebound = float(0)
                # print ("orb: " + str(offensiveRebound))

                # drb
                if points[17].text != "":
                    defensiveRebound = float(points[17].text.strip('%'))
                else:
                    defensiveRebound = float(0)
                # print ("drb: " + str(defensiveRebound))

                # trb
                if points[18].text != "":
                    totalRebound = float(points[18].text.strip('%'))
                else:
                    totalRebound = float(0)
                # print ("trb: " + str(totalRebound))

                # ast
                if points[19].text != "":
                    assist = float(points[19].text.strip('%'))
                else:
                    assist = float(0)
                # print ("assist: " + str(assist))

                # tov
                if points[20].text != "":
                    turnover = float(points[20].text.strip('%'))
                else:
                    turnover = float(0)
                # print ("tov: " + str(turnover))

                # stl
                if points[21].text != "":
                    steal = float(points[21].text.strip('%'))
                else:
                    steal = float(0)
                # print ("stl: " + str(steal))

                # blk
                if points[22].text != "":
                    block = float(points[22].text.strip('%'))
                else:
                    block = float(0)
                print ("block: " + str(block))

                # pf
                if points[23].text != "":
                    personalFoul = float(points[23].text.strip('%'))
                else:
                    personalFoul = float(0)
                print ("PF: " + str(personalFoul))

                # pts
                if points[24].text != "":
                    ptsScored = float(points[24].text.strip('%'))
                else:
                    ptsScored = float(0)
                print ("pts: " + str(ptsScored))

                season = (str(i) + "/" + str(j))
                seasonID = q

                inserts = (team, player, season, seasonID, gamesPlayed, minutes, fieldGoalMade, fieldGoalAttempt, fieldGoalPercent, twopointmade, twopointattempted, twoPointPercent,threePointMade, threePointAttempt, threePointPercent, freeThrowMade, freeThrowAttempt, freeThrowPercent, offensiveRebound, defensiveRebound, totalRebound, assist, turnover, steal, block, personalFoul, ptsScored)
                # print (len(inserts))

                insertStats = "INSERT INTO playerBasicAverages(team, player, season, seasonID, gamesPlayed, minutes, fgMade, fgAttempted, fgPercent, 2PtMade, 2PtAttempted, 2PtPercent, 3PtMade, 3PtAttempted, 3PtPercent, ftMade, ftAttempted, ftPercent, offReb, defReb, totReb, assist, turnover, steal, block, pf, pts) VALUES(%s, %s, %s, %s,%s,%s, %s, %s, %s,%s,%s, %s, %s, %s,%s,%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"

                # inserts the stats into whatever table is designated
                cursor.execute(insertStats, inserts)
                cnx.commit()
            print ("Finished inserting data for: " + player)

        i-=1
        j-=1
        q-=1

    return

def playerAveragesThisYear(soup,cursor,cnx, teamName,seasonID):

    tables = soup.find_all("table")

    i = 19
    j = 20
    q = 5

    for table in tables[-20]:
        print ("________________________________________________________________________________________________________________________")
        print ("Player Average Stats: ", i,"/",j," season")

        rows = table.find_all("tr")
        for row in rows[1:]:
            points = row.find_all("td")
            team = teamName
            player = points[0].text

            # games
            if points[2].text != "":
                gamesPlayed = int(points[2].text)
            else:
                gamesPlayed = 0
            print("Games Played: " + str(gamesPlayed))

            # minutes
            if points[3].text != "":
                minutes = float(points[3].text)
            else:
                minutes = float(0)
            print ("Minutes: " + str(minutes))

            if gamesPlayed == 0 or (minutes == 0.0):
                # does not insert them into table
                print ("Player did not play in a game")
            else:
                # fgm
                if points[4].text != "":
                    fieldGoalMade = float(points[4].text.strip('%'))
                else:
                    fieldGoalMade = float(0)
                print ("fieldGoalMade: " + str(fieldGoalMade))

                # fga
                if points[5].text != "":
                    fieldGoalAttempt = float(points[5].text.strip('%'))
                else:
                    fieldGoalAttempt = float(0)
                print ("fga: " + str(fieldGoalAttempt))

                # field goal %
                if points[6].text != "":
                    fieldGoalPercent = float(points[6].text.strip('%'))
                else:
                    fieldGoalPercent = float(0)
                print ("FG %: " + str(fieldGoalPercent))

                # 2 pm
                if points[7].text != "":
                    twopointmade = float(points[7].text.strip('%'))
                else:
                    twopointmade = float(0)
                # print ("2ptmade: " + str(twopointmade))

                # 2 pa
                if points[8].text != "":
                    twopointattempted = float(points[8].text.strip('%'))
                else:
                    twopointattempted = float(0)
                # print ("2Ptattemped: " + str(twopointattempted))

                # 2p %
                if points[9].text != "":
                    twoPointPercent = float(points[9].text.strip('%'))
                else:
                    twoPointPercent = float(0)
                # print ("2Pt %: " + str(twoPointPercent))

                # 3pm
                if points[10].text != "":
                    threePointMade = float(points[10].text.strip('%'))
                else:
                    threePointMade = float(0)
                # print ("3pt made: " + str(threePointMade))

                # 3pa
                if points[11].text != "":
                    threePointAttempt = float(points[11].text.strip('%'))
                else:
                    threePointAttempt = float(0)
                # print ("threePointAttempt %: " + str(threePointAttempt))

                # 3pt %
                if points[12].text != "":
                    threePointPercent = float(points[12].text.strip('%'))
                else:
                    threePointPercent = float(0)
                # print ("3pt %: " + str(threePointPercent))

                # ftm
                if points[13].text != "":
                    freeThrowMade = float(points[13].text.strip('%'))
                else:
                    freeThrowMade = float(0)
                # print ("ft made: " + str(freeThrowMade))

                # fta
                if points[14].text != "":
                    freeThrowAttempt = float(points[14].text.strip('%'))
                else:
                    freeThrowAttempt = float(0)
                # print ("ft attempted: " + str(freeThrowAttempt))

                # ft %
                if points[15].text != "":
                    freeThrowPercent = float(points[15].text.strip('%'))
                else:
                    freeThrowPercent = float(0)
                # print ("ft %: " + str(freeThrowPercent))

                # orb
                if points[16].text != "":
                    offensiveRebound = float(points[16].text.strip('%'))
                else:
                    offensiveRebound = float(0)
                # print ("orb: " + str(offensiveRebound))

                # drb
                if points[17].text != "":
                    defensiveRebound = float(points[17].text.strip('%'))
                else:
                    defensiveRebound = float(0)
                # print ("drb: " + str(defensiveRebound))

                # trb
                if points[18].text != "":
                    totalRebound = float(points[18].text.strip('%'))
                else:
                    totalRebound = float(0)
                # print ("trb: " + str(totalRebound))

                # ast
                if points[19].text != "":
                    assist = float(points[19].text.strip('%'))
                else:
                    assist = float(0)
                # print ("assist: " + str(assist))

                # tov
                if points[20].text != "":
                    turnover = float(points[20].text.strip('%'))
                else:
                    turnover = float(0)
                # print ("tov: " + str(turnover))

                # stl
                if points[21].text != "":
                    steal = float(points[21].text.strip('%'))
                else:
                    steal = float(0)
                # print ("stl: " + str(steal))

                # blk
                if points[22].text != "":
                    block = float(points[22].text.strip('%'))
                else:
                    block = float(0)
                print ("block: " + str(block))

                # pf
                if points[23].text != "":
                    personalFoul = float(points[23].text.strip('%'))
                else:
                    personalFoul = float(0)
                print ("PF: " + str(personalFoul))

                # pts
                if points[24].text != "":
                    ptsScored = float(points[24].text.strip('%'))
                else:
                    ptsScored = float(0)
                print ("pts: " + str(ptsScored))

                season = (str(i) + "/" + str(j))
                seasonID = 5

                inserts = (team, player, season, seasonID, gamesPlayed, minutes, fieldGoalMade, fieldGoalAttempt, fieldGoalPercent, twopointmade, twopointattempted, twoPointPercent,threePointMade, threePointAttempt, threePointPercent, freeThrowMade, freeThrowAttempt, freeThrowPercent, offensiveRebound, defensiveRebound, totalRebound, assist, turnover, steal, block, personalFoul, ptsScored)
                # print (len(inserts))

                #deleteStats = "DELETE from playerBasicAverages where team = '" + str(teamName) + "' and seasonID = 5" 
                insertStats = "INSERT INTO playerBasicAverages(team, player, season, seasonID, gamesPlayed, minutes, fgMade, fgAttempted, fgPercent, 2PtMade, 2PtAttempted, 2PtPercent, 3PtMade, 3PtAttempted, 3PtPercent, ftMade, ftAttempted, ftPercent, offReb, defReb, totReb, assist, turnover, steal, block, pf, pts) VALUES(%s, %s, %s, %s,%s,%s, %s, %s, %s,%s,%s, %s, %s, %s,%s,%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"

                # inserts the stats into whatever table is designated
                cursor.execute(insertStats, inserts)
                cnx.commit()
            print ("Finished inserting data for: " + player)

        i-=1
        j-=1
        q-=1

    return

def sqlUpdates(cursor,cnx):

    statement = "UPDATE playerBasicAverages a, playerReference b set a.playerID = b.playerID where a.player = b.fullName and a.seasonID = b.seasonID"
    cursor.execute(statement)
    cnx.commit()

    statement1 = "UPDATE playerBasicAverages a, teamReference b set a.teamID = b.teamID where a.team = b.teamName"
    cursor.execute(statement1)
    cnx.commit()

    statement2 = "UPDATE playerBasicAverages a, playerReference b set a.positionID = b.positionID where a.playerID = b.playerID and a.seasonID = b.seasonID"
    cursor.execute(statement2)
    cnx.commit()

    print "Finished sql updates on table"
    return 


def main():

    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="NCAAWomens",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    '''
    # whoever uses this needs to change the directory in the string
    for subdir, dirs, files in os.walk("/Users/lissjust/Documents/NCAAWomens/upcomingFilesNeeded/teamFiles/teamOneTeamFile"):
        for file in files:
            #print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            if filepath.endswith(".htm"):
                html = open(filepath).read()
                soup = BeautifulSoup(html, 'html.parser')
                teamName = "Maryland"
                playerAveragesThisYear(soup, cursor, cnx, teamName,5)
                print (filepath)
                # print(path_in_str)
    '''
    '''fileName = 'lakenwairau.htm'
    print fileName
    html = open(fileName).read()
    soup = BeautifulSoup(html, 'html.parser')
    teamStats(soup, cursor, cnx)
    '''
    sqlUpdates(cursor,cnx)

    cursor.close()
    cnx.commit()
    cnx.close()

    return



if __name__=="__main__":
    main()
