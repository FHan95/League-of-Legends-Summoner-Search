from __future__ import unicode_literals
from django.shortcuts import render

import requests

# Views are created here
def requestSummonerData(region, username, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/summoner/v3/summoners/by-name/" + username + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def requestRankedData(region, ID, APIKey):
    URL = "https://" + region + "1.api.riotgames.com/lol/league/v3/positions/by-summoner/" + ID + "?api_key=" + APIKey
    response = requests.get(URL)
    return response.json()

def apisearch(request):

    username = request.POST['username']
    apikey = request.POST['apikey']
    region = "na"

    summonerData = requestSummonerData(region, username, apikey)
    ID = summonerData['id']
    ID = str(ID)

    rankedData = requestRankedData(region, ID, apikey)

    context = {
        'username': username,
        'tier': rankedData[0]['tier'],
        'rank': rankedData[0]['rank'],
        'lp': rankedData[0]['leaguePoints'] 
    }

    return render(request, 'lookup/player.html', context)
    
def index(request):

    return render(request, 'lookup/index.html')
