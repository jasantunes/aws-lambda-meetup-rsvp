# pylint: disable=missing-docstring
from __future__ import print_function

import requests
import os
import json
import re

# Get your MEETUP_API_KEY here: http://www.meetup.com/meetup_api/key/
MEETUP_API_KEY = os.getenv('MEETUP_API_KEY')
# Get your MEETUP_MEMBER_ID here: http://www.meetup.com/account/
MEETUP_MEMBER_ID = os.getenv('MEETUP_MEMBER_ID')

API_BASE_URL = 'https://api.meetup.com/'
EVENTS_URL = API_BASE_URL + '2/events'
RSVPS_URL = API_BASE_URL + '2/rsvps'
POST_RSVP_URL = API_BASE_URL + 'rsvp'

## Higher level Meetup API methods
def get_events(group_urlname):
    url = EVENTS_URL
    payload = {'key': MEETUP_API_KEY, 'group_urlname': group_urlname}
    resp = requests.get(url, params=payload, verify=True, timeout=10).json()
    return resp.get('results')

def get_rsvp(event_id):
    url = RSVPS_URL
    payload = { 'key': MEETUP_API_KEY, 'event_id': event_id }
    resp = requests.get(url, params=payload, verify=True, timeout=10).json()
    rsvps = resp.get('results')
    my_rsvps = list(filter(lambda rsvp: str(rsvp['member']['member_id']) == MEETUP_MEMBER_ID, rsvps))
    return my_rsvps[0] if len(my_rsvps) >= 1 else None

def send_rsvp_yes(event_id):
    url = POST_RSVP_URL
    payload = { 'key': MEETUP_API_KEY, 'event_id': event_id, 'rsvp': 'yes' }
    resp = requests.post(url, data=payload, verify=True, timeout=10).json()
    if resp.get('description') == 'Successful RSVP':
        return True
    print("Could not RSVP: %s" % resp)
    return False

def event_is_full(event):
    if 'rsvp_limit' in event and event['yes_rsvp_count'] >= event['rsvp_limit']:
        return True
    return False

def event_matches_regex(event_name, regex):
    match = re.match(regex, event_name)
    return bool(match)

def rsvp_for_group_events(group_urlname, regexes = []):
    events = get_events(group_urlname)
    print("Parsing {} events ...".format(len(events)))

    for event in events:
        group_name = event['group']['name']
        event_name = event['name']
        event_id = event['id']
        event_url = event['event_url']
        print("Parsing event: %s ..." % event_name)

        whitelisted = True in [event_matches_regex(event_name, regex) for regex in regexes]
        if not whitelisted:
            print('[%s - %s] Does not match filter' % (group_name, event_name))
            continue

        rsvp = get_rsvp(event_id)
        if rsvp:
            print('[%s - %s] Already RSVPed (%s)' % (group_name, event_name, event_url))
            continue

        if event_is_full(event):
            print('[%s - %s] Full (%s)' % (group_name, event_name, event_url))
            continue

        if send_rsvp_yes(event_id):
            print('[%s - %s] RSVPed (%s)' % (group_name, event_name, event_url))
        else:
            print('[%s - %s] Problem RSVPing (%s)' % (group_name, event_name, event_url))


def lambda_handler(event, context):
    try:
        rsvp_for_group_events('contracostafc', [r'TUESDAY NIGHT: Small game', 'TUESDAY NIGHT: Big game'])
        # rsvp_for_group_events('Walnut-Creek-Soccer-Meetup', [r'Pick up Soccer'])
    except Exception as e:
        print(e)
        raise e

if __name__ == '__main__':
    event = { }
    lambda_handler(event, None)
