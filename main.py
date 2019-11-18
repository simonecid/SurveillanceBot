#!/usr/bin/env python3.6

import slack
import os

def postMessage(client, message, channel):
  response = client.chat_postMessage(
    channel=channel,
    text=message
  )
  
  return response["ok"]
  
@slack.RTMClient.run_on(event="message")
def echoMessage(**payload):
  data = payload['data']
  if data.get("subtype", "user_message") != "bot_message":
    web_client = payload['web_client']
    rtm_client = payload['rtm_client']
    channel_id = data['channel']
    thread_ts = data['ts']
    user = data['user']
    web_client.chat_postMessage(
      channel=channel_id,
      text=data["text"],
    )

if __name__ == "__main__":
  client = slack.RTMClient(token=os.environ["SLACK_TOKEN"])
  client.start()