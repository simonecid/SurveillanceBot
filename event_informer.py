#!/usr/bin/env python3.6

'''
This script is called when an event has been recorded.
It informs the users that something happened and sends the recording.
'''

import slack
import os
import glob
import hashlib

def get_slack_token(file_path):
  with open(file_path) as token_file :
    return token_file.readline()
  return None

# find latest video in director
def get_latest_video_in_directory(path):
  list_of_files = glob.glob(path + '/*.mp4') 
  latest_file = max(list_of_files, key=os.path.getctime)
  return latest_file

# sends a message
def postMessage(client, message, channel):
  response = client.chat_postMessage(
    channel=channel,
    text=message
  )

if __name__ == "__main__":

  video_path = get_latest_video_in_directory("/home/sb17498/SSHFS/claptrapSANDISK16G/motion")
  video_name = os.path.split(video_path)[1]
  video_size = round(os.path.getsize(video_path)/1E6, 3)
  video_name_checksum = hashlib.md5(video_name.encode("utf-8")).hexdigest()
  client = slack.WebClient(token=get_slack_token("slack_token.dat"))
  # client.files_upload(channels="#surveillance-bot", file=video_path, title="Last recording", filename=os.path.split(video_path)[1], filetype="mp4")
  postMessage(client, 
    f"I have just finished recording an event: \n \
  * file name: {video_name} \n \
  * size: {video_size} MB \n \
  * id: {video_name_checksum}",
  "#surveillance-bot")