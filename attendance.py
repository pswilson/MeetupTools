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

eventsApiPath = 'events'
rsvpsApiPath = 'rsvps'

# GET: apiBase + '/' <group_url_name> + '/events'
#    array of event objects
# GET: apiBase + '/' <group_url_name> + '/events/' + <event_id>
#    event object
# GET: apiBase + '/' <group_url_name> + '/events/' + <event_id> + '/rsvps'
#    array of rsvp objects

def getEvents(groupUrl):
    request_url = '{}/{}/{}'.format(apiBase, groupUrl, eventsApiPath)
    print("Getting events from: {}".format(request_url))
    r_events = requests.get(request_url, params = authParams)
    print("... got status: {}".format(r_events.status_code))
    return r_events.json()

def getAttendees(groupUrl, eventId):
    request_url = '{}/{}/{}/{}/{}'.format(apiBase, groupUrl, eventsApiPath, eventId, rsvpsApiPath)
    print("Getting event attendees from: {}".format(request_url))
    r_attendees = requests.get(request_url, params = authParams)
    print("... got status: {}".format(r_attendees.status_code))
    return r_attendees.json()

def getAttendanceForGroup(groupUrl):
    print('Events for {} ...'.format(groupUrl))
    events = getEvents(groupUrl)
    for event in events:
        print('{} ({}): {}'.format(event['name'], event['id'], event['yes_rsvp_count']))
        attendees = getAttendees(groupUrl, event['id'])
        for attendee in attendees:
            # print(attendee)
            print('    {} ({}): {}'.format(attendee['member']['name'], attendee['member']['id'], attendee['response']))

for groupUrl in groupUrlNames:
    getAttendanceForGroup(groupUrl)
