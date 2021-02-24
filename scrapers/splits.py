import click
import mysql.connector
import requests
from bs4 import BeautifulSoup

team_abbreviations = ["ATL", "BOS", "BRK", "CHA", "CHI", "CLE", "DAL", "DEN",
                      "DET", "GSW", "HOU", "IND", "LAC", "LAL", "MEM", "MIA",
                      "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO",
                      "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]

def get_url(teamAbbrev, year):
    team = teamAbbrev
    if teamAbbrev == "BRK" and year <= 2012:
        team = "NJN"
    elif teamAbbrev == "NOP" and year <= 2013:
        team = "NOH"
    url = "https://www.basketball-reference.com/teams/" + team + "/" + year + "/splits/"
    
    return url

@click.command()
@click.option('-c', '--conference', is_flag=True, 
              help='Gets the conference splits.')
@click.option('-d', '--division', is_flag=True, 
              help='Gets the conference splits.')
@click.option('--day', is_flag=True, 
              help='Gets the splits for each day Mon-Sun.')
@click.option('-l', '--location', is_flag=True, 
              help='Gets the home/away splits.')
@click.option('-r', '--rest', is_flag=True, 
              help='Gets the splits for each rest day.')
@click.option('-r', '--team', is_flag=True, 
              help='Gets the team splits.')
def splits(conference, division, day, location, rest, team):
    """Program that gets the splits from basketball reference."""
    cnx = mysql.connector.connect(user="wsa",
                                  host="34.68.250.121",
                                  database="Sports Betting",
                                  password="LeBron>MJ!")
    cursor = cnx.cursor(buffered=True)
    
    # for teamAbbrev in team_abbreviations:
    for year in range(2010, 2021):
        url = get_url("BOS", year)
        
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        table = soup.find('table', attrs={'id': 'team_splits'})
        
        if conference:
            get_conf_splits()
        elif division:
            get_div_splits()
        elif day:
            get_day_splits()
        elif location:
            get_location_splits()
        elif rest:
            get_rest_splits()
        elif team:
            get_team_splits()
        
    cursor.close()
    cnx.commit()
    cnx.close()
        
    return
        

def get_conf_splits():
    print('--------- Conference splits ---------')
    

def get_div_splits():
    print('--------- Division splits ---------')


def get_day_splits():
    print('--------- Day splits ---------')
 
   
def get_location_splits():
    print('--------- Location splits ---------')
    

def get_rest_splits():
    print('--------- Rest splits ---------')
    

def get_team_splits():
    print('--------- Team splits ---------')


if __name__ == '__main__':
    splits()