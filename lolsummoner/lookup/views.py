from __future__ import unicode_literals
from django.shortcuts import render

# Views are created here
def apisearch(request):

    username = request.POST['username']
    apikey = request.POST['apikey']

    context = {
        'username': username,
        'apikey': apikey
    }

    return render(request, 'lookup/player.html', context)
    
def index(request):

    return render(request, 'lookup/index.html')
