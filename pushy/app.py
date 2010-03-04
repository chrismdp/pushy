from waveapi import events
from waveapi import robot
from waveapi import appengine_robot_runner

import logging

CONSUMER_KEY = "128449655778"
CONSUMER_SECRET = "Cy0i+17WTMdj2kxsXXBvnTvq"

def Main():
	logging.getLogger().setLevel(logging.DEBUG)
	myRobot = robot.Robot('Pushy (test)', 
		image_url='http://chrismdp-test.appspot.com/assets/icon.png',
		profile_url='http://chrismdp-test.appspot.com/')
	myRobot.register_handler(events.WaveletSelfAdded, OnRobotAdded)
	appengine_robot_runner.run(myRobot)

def OnRobotAdded(event, wavelet):
	"""Invoked when the robot has been added."""
	# post welcome message
	wavelet.reply("Hi, I'm Pushy. In order to get notifications appearing in this wave, post content to:\n\nhttp://chrismdp-test.appspot.com/push/"+wavelet.wave_id+"\n\nOnce you post data to this url, it'll show up on this wave. Pushy should understand github payloads just fine in the future.\n\nYou can safely delete this message: it's just for information.")






