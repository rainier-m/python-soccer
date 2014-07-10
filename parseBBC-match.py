'''
Created on Jun 16, 2014
Modified on Jul 09, 2014
Version 0.13.f
@author: rainier.madruga@gmail.com
A simple Python Program to scrape the BBC Sports website for content.
'''
# Import Libraries needed for Scraping the various web pages
from bs4 import BeautifulSoup
import urllib2
import datetime

# Establish the process Date & Time Stamp
ts = datetime.datetime.now().strftime("%H:%M:%S")
ds = datetime.datetime.now().strftime("%Y-%m-%d")

# Create an array of URL Links.
website = ["http://www.bbc.com/sport/football/27961190","http://www.bbc.com/sport/football/28069208","http://www.bbc.com/sport/football/25285249", "http://www.bbc.com/sport/0/football/25285092", "http://www.bbc.com/sport/0/football/25285085", "http://www.bbc.com/sport/football/world-cup/results", "http://www.bbc.com/sport/football/fixtures"]

# Parse out Specific Match Results
matchResults = urllib2.urlopen(website[5])
gameURL = website[1]
gameMatch = urllib2.urlopen(gameURL)
resultSoup = BeautifulSoup(matchResults)
matchSoup = BeautifulSoup(gameMatch)
parseVersion = 'WorldCup v0.13.f'

outputBase = 'WorldCup-MatchBase.html'
with open(outputBase, "w") as f:
     f.write(matchSoup.prettify("utf-8"))
     f.close()
# Identify Team Lineup
divDetailResults = matchSoup.find_all("div", {"class":"team-match-details"})
divLineup = matchSoup.find("div", {"id":"oppm-team-list"})

listHomeRoster = divLineup.find_all("div", {"class":"home-team"})
listAwayRoster = divLineup.find_all("div", {"class":"away-team"})

# Initialize Results Output File
with open('MatchDetails-output.txt', "w") as f:
    f.write(ds + '|' + ts + '|' + parseVersion + '|' + 'Match Results File' + '\n')
    f.close()

# Identify the Starting IX and the Bench
def startingLineup(x):
    lineupCount = x
    if lineupCount < 12:
        return "Started Match"
    else:
        return "Bench"

# Function to return the Home Team Name using the divTeamDetails
def returnHome(x):
    homeTeam = x.find("div", {"id":"home-team"})
    spanHomeTeam = homeTeam.find("span", {"class":"team-name"})
    return spanHomeTeam.get_text()

# Function to return the Away Team Name using the divTeamDetails
def returnAway(x):
    awayTeam = x.find("div", {"id":"away-team"})
    spanAwayTeam = awayTeam.find("span", {"class":"team-name"})
    return spanAwayTeam.get_text()

# Function to return the Roster & Lineup of the squads
# TODO - Use the value of the Start / Substitue in the Roster coming in
def rosterOutput(x):
    rosterArray = []
    counter = 1
    for i in x:
        i.encode('utf-8')
        lineup = i.find_all("li")
        teamName = i.find("h3")

        # print i
        for i in lineup:
            playerJersey = i.text[3:5]
            playerDetails =  i.text[7:len(i.text)]
            playerDetails.encode('utf-8')
            playerStart = playerDetails.find("  ")
            playerString = len(playerDetails) 
        if len(playerDetails) - playerStart > 2:
           playerName = i.text[7:(len(i.text)-(len(playerDetails) - playerStart))]
           # print playerName
           playerUpdate = i.text[7+len(playerName):7+playerString]
           playerUpdateRow = teamName.get_text()+ '|' + playerJersey + '|' + playerName + '|' + startingLineup(counter) + '|' + playerUpdate 
           #print playerUpdateRow
           counter += 1
           rosterArray.append(playerUpdateRow.encode('utf-8'))
        else:
           playerRow = teamName.get_text() + '|' + playerJersey + '|' + playerDetails[0:len(playerDetails)-2] + '|' + startingLineup(counter) + '|'
           #print playerRow
           counter += 1
           rosterArray.append(playerRow.encode('utf-8'))
    return rosterArray

for i in rosterOutput(listHomeRoster):
    with open ('MatchDetails-output.txt', "a") as f:
        f.write(i + '\n')
        f.close()

for i in rosterOutput(listAwayRoster):
    with open ('MatchDetails-output.txt', "a") as f:
        f.write(i + '\n')
        f.close()

# Team Match Details & Team Badge
divTeamDetails = matchSoup.find("div", {"class":"post-match"})

# Initialize the Stats File
with open('MatchStats-output.txt', "w") as f:
    f.write(ds + '|' + ts + '|' + parseVersion + '|' + 'Match Stats File' + '\n')
    f.write('MatchID' + '|' + 'Team Side' + '|' + 'Team Name' + '|' + 'Goals Scored' + '|' + 'Team Badge' + '|' + 'Possession %' + '|' + 'Shots' + '|' + 'Shots On Goal' + '|' + 'Corners' + '|' + 'Fouls' + '|' + 'Match Notice' + '\n')
    f.close()

# Function to return Match Stats based on input of matchSoup
def matchStats(x,y):
    # Pull in the main Match Detail page from the Function Call
    funcMatch = x

    # Create a local copy of the Match HTML page
    with open ('MatchStats-output.html', "w") as f:
        f.write(funcMatch.prettify('utf-8'))
        f.close()

    # Parse out the two main sections of the Match (Roster & Stats)
    divTeamDetails = funcMatch.find("div", {"class":"post-match"})
    divMatchStats = funcMatch.find("div", {"id":"match-stats-wrapper"})

    # Parse out the Match Statistics
    statPossession = divMatchStats.find("div", {"id":"possession"})
    statShots = divMatchStats.find("div", {"id":"total-shots"})
    statShotsGoal = divMatchStats.find("div", {"id":"shots-on-target"})
    statCorners = divMatchStats.find("div", {"id":"corners-wrapper"})
    statFouls = divMatchStats.find("div", {"id":"fouls-wrapper"})
    statPossessionHome = statPossession.find("span", {"class":"home"})
    statPossessionAway = statPossession.find("span", {"class":"away"})
    statShotsHome = statShots.find("span", {"class":"home"})
    statShotsAway = statShots.find("span", {"class":"away"})
    statShotsGoalHome = statShotsGoal.find("span", {"class":"home"})
    statShotsGoalAway = statShotsGoal.find("span", {"class":"away"})
    statCornersHome = statCorners.find("span", {"class":"home"})
    statCornersAway = statCorners.find("span", {"class":"away"})
    statFoulsHome = statFouls.find("span", {"class":"home"})
    statFoulsAway = statFouls.find("span", {"class":"away"})

    # Parse out the Team Names, Team Badge, Scores and Scorers of Goals
    homeTeam = divTeamDetails.find("div", {"id":"home-team"})
    # print homeTeam.prettify('utf-8')

    awayTeam = divTeamDetails.find("div", {"id":"away-team"})
    homeScorer = homeTeam.find_all("p", {"class":"scorer-list blq-clearfix"})
    awayScorer = awayTeam.find_all("p", {"class":"scorer-list blq-clearfix"})
    spanHomeScore = homeTeam.find("span", {"class":"team-score"})
    spanAwayScore = awayTeam.find("span", {"class":"team-score"})
    # spanHomeScore = 0
    # spanAwayScore = 0
    homeTeamBadge = homeTeam.find("img")
    awayTeamBadge = awayTeam.find("img")

    # Create an array to store the Team-Level Statistics that will be returned
    teamStats = []

    # Parse Game URL into segments. Will be using the last portions to create a unique BBC_MatchID 
    strGameURL = y.split('/')
    BBC_MatchID = strGameURL[5]

    # Advice of Winner in event of a Penalty Shoot Out
    specNotice = funcMatch.find("div", {"id":"special-notice"})
    try:
        specNotice
    except NameError:
        specNotice = None

    if specNotice != None:
        matchNotice = "DRAW" + ' - ' + specNotice.get_text(strip=True)
    else:
        matchNotice = "No Special Notice"

    # print spanHomeScorer
    # print homeTeam.prettify('utf-8')
    # for i in homeTeam.p:
    #    print i

    # teamStats.append('MatchID' + '|' + 'Team Side' + '|' + 'Team Name' + '|' + 'Goals Scored' + '|' + 'Team Badge' + '|' + 'Possession %' + '|' + 'Shots' + '|' + 'Shots On Goal' + '|' + 'Corners' + '|' + 'Fouls' + '|' + 'Match Notice')
    teamStats.append(BBC_MatchID + '|' + 'Home' + '|' + homeTeam.a.get_text() + '|' + spanHomeScore.get_text() + '|' + homeTeamBadge["src"] + '|' + statPossessionHome.get_text() + '|' + statShotsHome.get_text() + '|' + statShotsGoalHome.get_text() + '|' + statCornersHome.get_text() + '|' + statFoulsHome.get_text() + '|' + matchNotice)
    teamStats.append(BBC_MatchID + '|' + 'Away' + '|' + awayTeam.a.get_text() + '|' + spanAwayScore.get_text() + '|' + awayTeamBadge["src"] + '|' + statPossessionAway.get_text() + '|' + statShotsAway.get_text() + '|' + statShotsGoalAway.get_text() + '|' + statCornersAway.get_text() + '|'+ statFoulsAway.get_text() + '|' + matchNotice)

    # Print Player Roster for Team
    divLineup = funcMatch.find("div", {"id":"oppm-team-list"})
    # print divLineup.prettify("utf-8")
    
    listHomeRoster = divLineup.find("div", {"class":"home-team"})
    listHomeStarter = listHomeRoster.find("ul", {"class":"player-list"})
    listHomeSubs = listHomeRoster.find("ul", {"class":"subs-list"})
    listAwayRoster = divLineup.find("div", {"class":"away-team"})
    listAwayStarter = listAwayRoster.find("ul", {"class":"player-list"})
    listAwaySubs = listAwayRoster.find("ul", {"class":"subs-list"})

    lineupHomeStarter = listHomeStarter.find_all("li")
    lineupAwayStarter = listAwayStarter.find_all("li")
    lineupHomeSubs = listHomeSubs.find_all("li")
    lineupAwaySubs = listAwaySubs.find_all("li")

    print "*** - - - - - - - - - - - - - - - - - - ***"
    print listHomeRoster.prettify("utf-8")
    # print listHomeStarter.prettify("utf-8")

    # for i in lineupHomeStarter:
    #     print i.get_text()

    return teamStats

# Print out the results of the function matchStats

print '***- - - - - - - - - - - - - - - - -***'
# for i in matchStats(matchSoup,gameURL):
#    print i
    # print '***- - - - - - - - - - - - - - - - -***'

# Output Game URLs from Results page resultSoup
def resultsURL(x):
    listURL = []
    funcSoup = x
    divMatchResults = funcSoup.find_all("div", {"class":"fixtures-table full-table-medium"})
    for i in divMatchResults:
        urlList = i.find_all('a', {'class': 'report'})
        for i in urlList:
            listURL.append("http://www.bbc.com" + i.get("href"))

    return listURL

for i in matchStats(matchSoup, gameURL):
    print i

'''
# Iterate over all Results for the World Cup
for i in resultsURL(resultSoup):
    parseURL = i
    parseMatch = urllib2.urlopen(parseURL)
    parseSoup = BeautifulSoup(parseMatch)
    print datetime.datetime.now().strftime("%H:%M:%S") + " Record Read"
    for i in matchStats(parseSoup,parseURL):
        print "Record Saved"
        with open('MatchStats-output.txt', "a") as f:
            f.write(i + '\n')
            f.close()
'''
