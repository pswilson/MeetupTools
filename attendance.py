import os
import requests

#api_base = 'https://api.meetup.com'
# NOTE: Don't commit with a key set
#api_key = 'Your_API_Key_Here'

api_base = os.environ['MEETUP_API_BASE']
api_key = os.environ['MEETUP_API_KEY']

# API calls using an api key require ... ?key=<api_key>&sign=true
auth_params = {'key': api_key, 'sign': 'true'}

# Only get the next event
page_params = {'page': 3}

date_range_params = {'no_later_than': '2018-10-21T00:00:00.000'}

combined_params = {}
combined_params.update(auth_params)
combined_params.update(page_params)
combined_params.update(date_range_params)

group_url_names = [
   'Frederick-Startup-Community',
   'FredWebTech',
   'AWS-Frederick-Meetup',
   'python-frederick',
#    'Frederick-3d-Printing-and-Maker-Tech-Group',
   'KeyLUG',
   'Frederick-NET-Meetup',
   'Frederick-Game-Development-Meetup',
   'Frederick-Crypto',
   'function-FrontendMasters',
   'Frederick-Infosec',
   'Frederick-Innovative-Technology-Center',
   'FSpace',
#    'FredCoBio-BioBeers',
   'Frederick-WordPress-Meetup'
#    'Western-Maryland-Web-Developers'
]

events_api_path = 'events'
rsvps_api_path = 'rsvps'

all_events = {}

# TODO: Add paging to api calls

# GET: apiBase + '/' <group_url_name> + '/events'
#    array of event objects
#   limit date range ... &no_later_than=2018-10-21T00:00:00.000
#   limit number returned ... &page=3
# GET: apiBase + '/' <group_url_name> + '/events/' + <event_id>
#    event object
# GET: apiBase + '/' <group_url_name> + '/events/' + <event_id> + '/rsvps'
#    array of rsvp objects

def getEvents(group_url):
    # TODO: Add filtering to limit response size
    request_url = '{}/{}/{}'.format(api_base, group_url, events_api_path)
    # print("Getting events from: {}".format(request_url))
    r_events = requests.get(request_url, params=combined_params)
    if r_events.status_code != 200:
        print("... got status: {} from {}".format(
            r_events.status_code, request_url))
    return r_events.json()

def getAttendees(group_url, event_id):
    # TODO: Add filtering to limit response size
    request_url = '{}/{}/{}/{}/{}'.format(api_base,
                                          group_url, events_api_path, event_id, rsvps_api_path)
    # print("Getting event attendees from: {}".format(request_url))
    r_attendees = requests.get(request_url, params=auth_params)
    if r_attendees.status_code != 200:
        print("... got status: {} from {}".format(r_attendees.status_code, request_url))
    return r_attendees.json()

def getAttendanceForGroup(group_url):
    print()
    print('Events for {} ...'.format(group_url))
    events = getEvents(group_url)
    for event in events:
        # Add the event to the overall event list by location and time
        event_key = (event['venue']['id'], event['time'])
        if event_key not in all_events:
            all_events[event_key] = []
        all_events[event_key].append(event)
        print('{} @{}: {} ({})'.format(
            event['local_date'], event['local_time'], event['name'], event['id']), end='', flush=True)
        if 'venue' in event:
            print(' at {} ({})'.format(
                event['venue']['name'], event['venue']['id']), end='', flush=True)
        print(': {} yes RSVPs'.format(event['yes_rsvp_count']))

for group_url in group_url_names:
    getAttendanceForGroup(group_url)

for k, v in all_events.items():
    print()
    print("Event key: {}".format(k))
    num_combined_events = len(v)
    overall_attendees = {}
    attendee_total_count = 0
    for event in v:
        print('\t{}: {}'.format(
            event['group']['name'], event['name']), end='', flush=True)
        if 'venue' in event:
            print(' at {} ({})'.format(
                event['venue']['name'], event['venue']['id']), end='', flush=True)
        print(': {} yes RSVPs'.format(event['yes_rsvp_count']))

        # Combine all atendees to get a unique list for the combined event
        attendees = getAttendees(event['group']['urlname'], event['id'])
        for attendee in attendees:
            if attendee['response'] == 'yes':
                attendee_total_count += 1
                overall_attendees[attendee['member']
                                ['id']] = attendee['member']['name']

    if num_combined_events > 1:
        print("{} attendees across {} combined events with {} unique attendees".format(
            attendee_total_count, num_combined_events, len(overall_attendees)))
