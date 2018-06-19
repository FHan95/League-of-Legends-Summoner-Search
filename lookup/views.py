from __future__ import unicode_literals
from django.shortcuts import render

import requests

# Views are created here

#Grabs profile icon
def getProfileIcon(version, profileIconID):
    URL = "http://ddragon.leagueoflegends.com/cdn/" + version + "/img/profileicon/" + profileIconID + ".png"
    return URL

#Grabs summoner data
def requestSummonerData(region, username, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + username + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

#Grabs ranked data
def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

#Grabs current version data
def requestVersion(region, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/static-data/v3/versions?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

#Renders data to player.html
def apisearch(request):

    username = request.POST['username']
    #Insert API key here
    apikey = ""
    region = "na"

    #Extracts data from summoner data request
    summonerData = requestSummonerData(region, username, apikey)
    ID = summonerData['id']
    ID = str(ID)
    profileIconID = summonerData['profileIconId']
    profileIconID = str(profileIconID)
    summonerLvl = summonerData['summonerLevel']
    summonerLvl = str(summonerLvl)
    username = summonerData['name']
    username = str(username)

    rankedData = requestRankedData(region, ID, apikey)

    #Due to limit rates on version requests, a static URL will be used for testing
    #version = requestVersion(region, apikey)
    #profileIcon = getProfileIcon(version[0], profileIconID)
    profileIcon = "http://ddragon.leagueoflegends.com/cdn/8.12.1/img/profileicon/" + profileIconID + ".png"

    #If statement that stores specific data to context depending if the player is ranked
    if not rankedData:

        #The player's solo ranked icon
        ranked_solo = "provisional.png"

        context = {
            'username': username,
            'profileIcon': profileIcon,
            'tier': "Unranked",
            'rank': "",
            'ranked_solo': ranked_solo,
            'lp': "",
            'summonerLvl': summonerLvl
        }
    else:

        #The player's solo ranked icon and League points
        ranked_solo = str(rankedData[0]['tier']).lower() + "_" + str(rankedData[0]['rank']).lower() + ".png"
        lp = str(rankedData[0]['leaguePoints']) + " LP"

        context = {
            'username': username,
            'profileIcon': profileIcon,
            'tier': rankedData[0]['tier'],
            'rank': rankedData[0]['rank'],
            'ranked_solo': ranked_solo,
            'lp': lp,
            'summonerLvl': summonerLvl
        }

    return render(request, 'lookup/player.html', context)
    
def index(request):

    return render(request, 'lookup/index.html')