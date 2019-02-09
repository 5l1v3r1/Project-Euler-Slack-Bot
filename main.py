import time
import re
import pdfkit
import json
import requests
from slackclient import SlackClient

#EDIT THIS
token = "your_token"
pjeulerbot_id = 'your_id'
#END OF EDIT

slack_client = SlackClient(token)

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
#EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    #print slack_events
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == pjeulerbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def channel_id_to_name(channel_id):
	global token
	payloads={
		'token':token,
		'channel':channel_id
	}
	r = requests.get('https://slack.com/api/channels.info', params=payloads)
	r_json = json.loads(r.content)
	return "#" + r_json["channel"]["name"]

def reply_file(file_name, channel):
	global token
	print channel
	my_file = {
		'file' : (file_name, open(file_name, 'rb'), 'pdf')
	}
	payloads = {
		"filename": file_name,
		"token":token,
		"title":"Project Euler Challenge " + file_name.split('.')[0],
		"channels":[channel]
	}
	print payloads
	r = requests.post("https://slack.com/api/files.upload", params=payloads, files=my_file)
	print r.content

def handle_command(command, channel):
	"""
		Executes bot command if the command is known
	"""
    # This is where you start to implement more commands!
    # If it's DM => Ignore.
	try:
		channel = channel_id_to_name(channel)
	except:
		pass
	if command.startswith('.rand'):
		file_name = command.split()[1] + '.pdf'
		pdfkit.from_url('https://projecteuler.net/problem=' + command.split()[1], file_name)
		reply_file(file_name, channel)

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Project Euler Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        while True:
            #print slack_client.rtm_read()
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
