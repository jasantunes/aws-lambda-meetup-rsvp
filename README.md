AWS Lambda Meetup RSVP
======================

This repository contains the lambda function code to query Meetup.com for events from a given group and automatically RSVP on specific events. There's also a script to update the lambda function as well as setting up the scheduling rule (e.g., every 5 minutes) to run the function periodically.

## Setup
1. Create AWS lambda function.
2. Set the following environment variables in the lambda function configuration:
  - `MEETUP_API_KEY`: See http://www.meetup.com/meetup_api/key/
  - `MEETUP_MEMBER_ID`: See http://www.meetup.com/account/
3. Run `push_to_lambda.sh` to update the lambda function and respective scheduling rule.

