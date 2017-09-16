# Meetup Utilities

## Scripts

* attendance.py - Meetup attendance aggregator ... or at least the basic start of one
* membership.py - Meetup group membership ... eventually to find unique membership across groups

### Configuration

You'll need a a few environment variables set for this to run.

MEETUP_API_BASE = <the_meetup_api_url>

MEETUP_API_KEY = <your_api_key>

### Things to do (in no particular order or structure):

* error handling
* avoidance of Meetup API rate limits
* create linked meetup events (common events across meetup groups)
    * consolidate attendance info across linked events
* structure as a service
* deploy as a service
* return some consumable format other than text
    * or have an optional return type
* pull meetup info from a db
    * list of meetup groups
    * group access info?
        * probably better to have a single user with access to all groups and get the api key from an environment var
