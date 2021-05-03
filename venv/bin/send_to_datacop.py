#!/Users/cokoro/Downloads/recfun/venv/bin/python3


import argparse
import json
import time
import base64
from stallion.auth import Authorizer

def comma_separated(item):
    return list(map(lambda s: s.strip(), filter(None, item.split(','))))

def parse_args():
    parser = argparse.ArgumentParser(description='A script for sending a properly formatted message to datacop.')
    parser.add_argument('--project' , required=True)
    parser.add_argument('--name')
    parser.add_argument('--slack_username')
    parser.add_argument('--slack_channel' )
    parser.add_argument('--slack_emoji')
    parser.add_argument('--email', type=comma_separated, help='Comma-separated list of email addresses to send alert to')
    parser.add_argument('--artifact', default=None, required=False)
    parser.add_argument('--dict', default=None, required=False, type=json.loads)
    parser.add_argument('--success', default=False, action="store_true", required=False,
                        help="By default the email subject will contained 'failed', setting this will omit that word")
    return parser.parse_args()

def current_time():
    time.ctime()
    return time.strftime('%Y-%m-%d %H:%M')

def publish(topic, blob):
    try:
        message_bytes = base64.b64encode(bytes(json.dumps(blob), encoding='utf8'))
    except TypeError as e:
        # Once we deprecate py2, we can completely remove this exception handling.
        print("WARNING: Caught TypeError while trying to encode str to bytes.")
        message_bytes = base64.b64encode(bytes(json.dumps(blob)))

    messages = {'messages': [{"data": message_bytes.decode('utf-8')}]}

    url = "https://pubsub.googleapis.com/v1/%s:publish" % topic
    session = Authorizer.read_write().get_access_session()
    resp = session.post(url, json=messages)

    if resp.status_code != 200:
        raise Exception('Error posting {} to pubsub: {}'.format(json.dumps(blob, indent=4), resp.content))


if __name__ == '__main__':
    data = {}
    data['messages'] = list()
    args = parse_args()
    timestamp = current_time()
    if args.name is None:
        args.name = "Unmarked DataCop"
    required_slack = [args.slack_username,  args.slack_channel, args.slack_emoji]
    blob = {
        "type": "generic_failure",
        "data": {"timestamp": timestamp, "project_id": args.project},
    }

    if filter(None, required_slack) == len(required_slack):
        parser.error("When enabling slack messages all of --slack_username --slack_channel and --slack_emoji are required")
    else:
        blob['slack'] = {'username': args.slack_username, "icon_emoji": args.slack_emoji, "channel": args.slack_channel }

    if args.email:
        email_subject = "[%s] %s: %s " % (timestamp, args.name, args.artifact or '') + ("" if args.success else "failed")
        blob['email'] = {"recipients": args.email, "subject": email_subject}
        blob['email_enabled'] = True

    if args.dict:
        blob['data'].update(args.dict)

    if args.artifact:
        blob['data']['artifact'] = args.artifact

    publish("projects/%s/topics/gcpnotify" % args.project, blob)
