import os
import re
import requests

# api_base = 'https://api.meetup.com'
# NOTE: Don't commit with a key set
# api_key = 'Your_API_Key_Here'

api_base = os.environ['MEETUP_API_BASE']
api_key = os.environ['MEETUP_API_KEY']

# API calls using an api key require ... ?key=<api_key>&sign=true
auth_params = {'sign': 'true', 'key': api_key}

group_url_names = [
   'Frederick-Startup-Community',
   'FredWebTech',
   'AWS-Frederick-Meetup',
   'python-frederick',
   'Frederick-3d-Printing-and-Maker-Tech-Group',
   'KeyLUG',
   'Frederick-NET-Meetup',
   'Frederick-Game-Development-Meetup',
   'Frederick-Crypto',
   'function-FrontendMasters',
   'Frederick-Infosec',
   'Frederick-Innovative-Technology-Center',
   'FSpace',
#    'FredCoBio-BioBeers',
   'Frederick-WordPress-Meetup',
   'Western-Maryland-Web-Developers'
]

members_api_path = 'members'

# GET: api_base + '/' <group_url_name> + '/members'
#    Response is a json array of member objects

def parseLinkHeader(hdr):

    # NOTE: Multiple link header values may be returned
    #       which will be combined into a single comma separated list by the requests library

    # link header will look something like this ...
    #   <https://api.meetup.com/Frederick-Startup-Community/members?sign=true&page=100&offset=1>; rel="next"
    # or possibly ..
    #   <https://api.meetup.com/Frederick-Startup-Community/members?sign=true&page=100&offset=1>; rel="prev", <https://api.meetup.com/Frederick-Startup-Community/members?sign=true&page=100&offset=3>; rel="next"

    # Basic regex pattern to handle a correctly formatted link header value
    pattern = '<(?P<url>(.+))> *; *rel="(?P<ref>(prev|next))"'

    links = {}

    if len(hdr) > 0:
        hdr_parts = hdr.split(',')
        for hdr_part in hdr_parts:
            m = re.search(pattern, hdr_part)
            if m:
                links[m.group('ref')] = m.group('url')

    return links

def getPagedResults(start_url):
    # Note: Need to use page and offset to get more than 200 users
    # page is max number of items returned per request (max of 200)
    # offset is 0 based page number
    # (NOTE: an offset greater than the actual number of pages based on the
    #        number of possible results seems to always return the last page of data)
    # Total number of possible responses is in the header "x-total-count"
    # link header contains a link to the "next" and/or "prev" page

    members = {}

    print("Getting members from {} ".format(start_url), end='', flush=True)

    next_url = start_url
    while next_url:
        r = requests.get(next_url)
        if r.status_code != 200:
            if r.status_code == 429:
                print('Rate limited: {}'.format(r.text()))
            else:
                print('Error fetching data: {}'.format(r.status_code))
            break

        batch_members = r.json()
        # For now we're just keeping the id and name
        for member in batch_members:
            members[str(member['id'])] = member['name']

        next_url = ''
        if 'link' in r.headers:
            links = parseLinkHeader(r.headers['link'])
            if 'next' in links:
                next_url = links['next']
                print('.', end='', flush=True)

    print() # finish out the line

    return members

overall_members = {}    # set of all members found across all groups
group_stats = {}        # count of members per group

for group_url in group_url_names:
    request_url = '{}/{}/{}'.format(api_base, group_url, members_api_path)
    members = getPagedResults(request_url)
    group_stats[group_url] = len(members)
    # Add all members to the overall member set
    for k, v in members.items():
        overall_members[k] = v

# Print a table of the membership counts
total_cnt = 0
for grp, cnt in group_stats.items():
    total_cnt += cnt
    print(f'{grp:45} {cnt:10d}')

print('{} members in {} Meetup groups with {} unique members.'.format(
    total_cnt, len(group_url_names), len(overall_members)))
