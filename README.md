AWS Lambda Meetup RSVP
======================

This repository contains the lambda function code to query Meetup.com for events from a given group and automatically RSVP on specific events. There's also a script to update the lambda function as well as setting up the scheduling rule (e.g., every 5 minutes) to run the function periodically.


## Meetup Setup

1. Get Meetup group short name from meetup group's URL, i.e., `https://www.meetup.com/XXXXX/events/` and take a note of the events you'd like to sign up. You'll need to modify the python scripts with the group name and event's name regular expression (see `meetup_rsvp.py`).
2. Get your Meetup API key and member ID:
  - `MEETUP_API_KEY`: See http://www.meetup.com/meetup_api/key/
  - `MEETUP_MEMBER_ID`: See http://www.meetup.com/account/


## Run locally

```
MEETUP_API_KEY=XXXXXXXX MEETUP_MEMBER_ID=XXXXXX python meetup_rsvp.py
```
or
```
MEETUP_API_KEY=XXXXXXXX MEETUP_MEMBER_ID=XXXXXX python scheduler.py
```

## Run on AWS

1. Create AWS lambda function and call it `meetup_rsvp`.
2. Set the `MEETUP_API_KEY` and `MEETUP_MEMBER_ID` environment variables in the lambda function configuration.
3. Run `push_to_aws.sh` to remotely update the lambda function and respective scheduling rule.


