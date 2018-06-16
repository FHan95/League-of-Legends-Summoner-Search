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
    apikey = request.POST['apikey']
    apikey = "RGAPI-06161b9c-7c83-4bcc-a533-70755ca2ec59";
    region = "na"

    summonerData = requestSummonerData(region, username, apikey)
    ID = summonerData['id']
    ID = str(ID)
    profileIconID = summonerData['profileIconId']
    profileIconID = str(profileIconID)

    rankedData = requestRankedData(region, ID, apikey)

    version = requestVersion(region, apikey)

    profileIcon = getProfileIcon(version[0], profileIconID)

    if not rankedData:
        context = {
            'username': username,
            'profileIcon': profileIcon,
            'rank': "N/A",
            'tier': "N/A",
            'lp': "N/A"
        }
    else:
        context = {
            'username': username,
            'profileIcon': profileIcon,
            'rank': rankedData[0]['rank'],
            'tier': rankedData[0]['tier'],
            'lp': rankedData[0]['leaguePoints'] 
        }

    return render(request, 'lookup/player.html', context)
    
def index(request):

    return render(request, 'lookup/index.html')