#!/usr/bin/env python3.6

'''
Handles messages from the users.
1) Starts motion.
2) Stops motion.
3) Lists recent files with size.
4) Can send files.
'''

import slack
import os
import re

isOn = False

def postMessage(client, message, channel):
  response = client.chat_postMessage(
    channel=channel,
    text=message
  )
  
  return response["ok"]
  
# @slack.RTMClient.run_on(event="message")
# def echoMessage(**payload):
#   data = payload['data']
#   if data.get("subtype", "user_message") != "bot_message":
#     web_client = payload['web_client']
#     rtm_client = payload['rtm_client']
#     channel_id = data['channel']
#     thread_ts = data['ts']
#     user = data['user']
#     web_client.chat_postMessage(
#       channel=channel_id,
#       text=data["text"],
#     )

# if motion is mentioned let's act on it
def parseMotionCommands(data):
  message = data["text"]
  if re.search("motion", message, re.IGNORECASE) is not None:
    if re.search("start", message, re.IGNORECASE) is not None:
      # we need to start motion
      print("Start motion!")
    if re.search("stop", message, re.IGNORECASE) is not None:
      # we need to stop motion
      print("Stop motion!")

#if we get a list keyword, we look for a number and show the last N videos based on that number
def parseListCommands(data):
  message = data["text"]
  if re.search("list", message, re.IGNORECASE) is not None:
    number_list = [int(s) for s in message.split() if s.isdigit()]
    number_of_videos = number_list[-1] if len(number_list) > 0 else 10 # last number is used as number of videos
    print(f"Showing list of last {number_of_videos} videos.")
    # Display file name, size, and checksum id (obtained from video name, not from full path)

#sending video if send keyword if found
def parseSendCommands(data):
  message = data["text"]
  if re.search("send", message, re.IGNORECASE) is not None:
    if re.search("last", message, re.IGNORECASE) is not None:
      print("Sending last video.")
    else:
      # the word right after send is the checksum id
      word_list = message.split()
      try:
        send_index = word_list.index("send")
      except ValueError:
        send_index = None
        # this is not supposed to happen!
        print("Oops something bad happened.")
      # checksum is right after send
      if send_index is not None:
        video_name_checksum = word_list[send_index + 1]
        print(f"Sending {video_name_checksum}.")

# web_client = payload['web_client']
# rtm_client = payload['rtm_client']
# message = data["text"]

@slack.RTMClient.run_on(event="message")
def handleCommands(**payload):
  data = payload["data"]
  if data.get("user") == "UQMNRUT88":
    parseMotionCommands(data)
    parseListCommands(data)    
    parseSendCommands(data)

def get_slack_token(file_path):
  with open(file_path) as token_file :
    return token_file.readline()
  return None

if __name__ == "__main__":
  client = slack.RTMClient(token=get_slack_token("slack_token.dat"))
  client.start()