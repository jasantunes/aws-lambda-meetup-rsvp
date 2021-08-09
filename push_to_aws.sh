#!/usr/bin/env bash
set -e

# The Lambda free tier includes 1M free requests per month and 400,000 GB-seconds of compute time per month. ~22 / min
RULE="rate(60 minutes)"
FUNCTION_NAME=meetup_rsvp

TEMP_DIR=$(mktemp -d /tmp/lambda.XXXXXXXXX)
LIBS=libs/

finish() {
  # Remove temporary files.
  [ ! -z "${TEMP_DIR}" ] && [ -d ${TEMP_DIR} ] && rm -rf ${TEMP_DIR}
  [ ! -z "${TEMP_DIR}" ] && [ -d ${TEMP_DIR} ] && rm -rf ${LIBS}
}
trap finish EXIT

echo "Installing packages ..."
pip install -q -r requirements.txt -t ${TEMP_DIR} 2> /dev/null

echo "Building zip ..."
ZIP_FILE=${FUNCTION_NAME}.zip
zip -q ${TEMP_DIR}/${ZIP_FILE} __init__.py ${FUNCTION_NAME}.py
(cd ${TEMP_DIR} && zip -q -r ${ZIP_FILE} *)

echo "Updating lambda function ..."
FUNCTION_ARN=`aws lambda update-function-code \
  --zip-file fileb://${TEMP_DIR}/${ZIP_FILE} \
  --function-name ${FUNCTION_NAME} \
| sed -n 's/.*"FunctionArn": "\(.*\)".*/\1/p'`

RULE_NAME=${FUNCTION_NAME}_rule
echo "Updating scheduling rule ..."
RULE_ARN=`aws events put-rule \
  --name ${RULE_NAME} \
  --schedule-expression "${RULE}" \
| sed -n 's/.*"RuleArn": "\(.*\)".*/\1/p'`

echo "Add lambda permission ..."
set +e
EVENT_NAME=${FUNCTION_NAME}_scheduled_event
aws lambda remove-permission \
  --function-name ${FUNCTION_NAME} \
  --statement-id ${EVENT_NAME}
set -e

aws lambda add-permission \
  --function-name ${FUNCTION_NAME} \
  --statement-id ${EVENT_NAME} \
  --action 'lambda:InvokeFunction' \
  --principal events.amazonaws.com \
  --source-arn ${RULE_ARN} > /dev/null

echo "Updating scheduling rule to lambda function ..."
TARGET_FILE=${TEMP_DIR}/targets.json
cat << EOF > ${TARGET_FILE}
[ { "Id": "1", "Arn": "${FUNCTION_ARN}" } ]
EOF
aws events put-targets \
  --rule ${RULE_NAME} \
  --targets file://${TARGET_FILE} > /dev/null

echo "All done."
echo "Make sure you set the `MEETUP_API_KEY` and `MEETUP_MEMBER_ID` environment variables in the lambda function configuration."
