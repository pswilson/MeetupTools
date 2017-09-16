import os
import requests

#apiBase = 'https://api.meetup.com'
# NOTE: Don't commit with a key set
#apiKey = 'Your_API_Key_Here'

apiBase = os.environ['MEETUP_API_BASE']
apiKey = os.environ['MEETUP_API_KEY']

# API calls using an api key rewuire ... ?key=<api_key>&sign=true
authParams = {'key': apiKey, 'sign': 'true'}

groupUrlNames = [
   'Frederick-Startup-Community',
   'FredWebTech'
]

membersApiPath = 'members'

# GET: apiBase + '/' <group_url_name> + '/members'
#    array of member objects

def getMembers(groupUrl):
    request_url = '{}/{}/{}'.format(apiBase, groupUrl, membersApiPath)
    print("Getting members from: {}".format(request_url))
    r_members = requests.get(request_url, params = authParams)
    print("... got status: {}".format(r_members.status_code))
    if r_members.status_code == 429:
        print('Rate limited: {}'.format(r_members.text()))

    return r_members.json()

def getMembershipForGroup(groupUrl):
    print('Members for {} ...'.format(groupUrl))
    members = getMembers(groupUrl)
    for member in members:
        print('{} ({})'.format(member['name'], member['id']))

for groupUrl in groupUrlNames:
    getMembershipForGroup(groupUrl)
