import mysql.connector
import requests
from bs4 import BeautifulSoup
import os

def getTeam(soup,cursor,cnx):
    i = 19
    j = 20

    print "________________________________________________________________________________________________________________________"
    print "Team Info: " + str(i) + "/" + str(j) + " season"
    list = soup.find('ul', {"class": "list-unstyled"})
    # puts the list items into an array
    list_items = list.findAll('li')
    # print list_items
    teamName = list_items[0].text
    return teamName

def scheduleStats(soup, cursor, cnx, teamName):

    #table 56 18/19 schedule
    #table 57 17/18 schedule
    #table 58 16/17 schedule
    #table 59 15/16 schedule

    tables = soup.find_all("table")

    i = 19
    j = 20
    for table in tables[56:60]:

        print "________________________________________________________________________________________________________________________"
        print "Schedule Stats: ", i,"/",j," season"
        rows = table.find_all("tr")
        for row in rows[1:]:

            points = row.find_all("td")
            dateText = points[0].text
            team = teamName
            if points[1].text == "H":
                home = 1
            else:
                home = 0
            opponent = points[3].text
            if points[5].text == "W":
                win = 1
            else:
                win = 0
            pointsScored = int(points[7].text)
            # print("Points Scored:" + str(pointsScored))
            pointsAllowed = int(points[8].text)
            # print("Points Allowed:" + str(pointsAllowed))
            margin = int(points[9].text)
            # print("Margin:" + str(margin))
            simpleRPI = int(points[12].text)
            # print("Simple RPI:" + str(simpleRPI))

            inserts = (team, dateText, home, opponent, win, pointsScored, pointsAllowed, margin, simpleRPI)

            insertStats = "INSERT INTO scheduleStats(team, dateText, home, opponent, win, ptsScored, ptsAllowed, margin, simpleRPI) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # inserts the stats into whatever table is designated
            cursor.execute(insertStats, inserts)
            cnx.commit()
            print "Finished inserting data for: " + team + " vs. " + opponent

        i-=1
        j-=1

    return

def scheduleStatsThisYear(soup, cursor, cnx, teamName):

    #table 56 18/19 schedule
    #table 57 17/18 schedule
    #table 58 16/17 schedule
    #table 59 15/16 schedule

    tables = soup.find_all("table")

    i = 19
    j = 20
    for table in tables[-10]:

        print "________________________________________________________________________________________________________________________"
        print "Schedule Stats: ", i,"/",j," season"
        rows = table.find_all("tr")
        for row in rows[1:]:

            seasonID = 5
            points = row.find_all("td")
            dateText = points[0].text
            team = teamName
            if points[1].text == "H":
                home = 1
            else:
                home = 0
            opponent = points[3].text
            if points[5].text == "W":
                win = 1
            else:
                win = 0
            pointsScored = int(points[7].text)
            # print("Points Scored:" + str(pointsScored))
            pointsAllowed = int(points[8].text)
            # print("Points Allowed:" + str(pointsAllowed))
            margin = int(points[9].text)
            # print("Margin:" + str(margin))
            simpleRPI = int(points[12].text)
            # print("Simple RPI:" + str(simpleRPI))

            inserts = (seasonID,team, dateText, home, opponent, win, pointsScored, pointsAllowed, margin, simpleRPI)

            insertStats = "INSERT INTO scheduleStats(seasonID, team, dateText, home, opponent, win, ptsScored, ptsAllowed, margin, simpleRPI) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # inserts the stats into whatever table is designated
            cursor.execute(insertStats, inserts)
            cnx.commit()
            print "Finished inserting data for: " + team + " vs. " + opponent

        i-=1
        j-=1

    return

def main():

    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="NCAAWomens",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)

    # whoever uses this needs to change the directory in the string
    for subdir, dirs, files in os.walk("/Users/lissjust/Desktop/NCAAWomens/upcomingFilesNeeded/teamFiles/teamOneTeamFile"):
        for file in files:
            #print os.path.join(subdir, file)
            filepath = subdir + os.sep + file


            if filepath.endswith(".htm"):
                html = open(filepath).read()
                soup = BeautifulSoup(html, 'html.parser')
                teamName = "Wisconsin"
                scheduleStatsThisYear(soup, cursor, cnx, teamName)
                print (filepath)
                # print(path_in_str)
    '''fileName = 'lakenwairau.htm'
    print fileName
    html = open(fileName).read()
    soup = BeautifulSoup(html, 'html.parser')
    teamStats(soup, cursor, cnx)
    '''
    cursor.close()
    cnx.commit()
    cnx.close()

    return



if __name__=="__main__":
    main()
