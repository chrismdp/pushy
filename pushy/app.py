from waveapi import events
from waveapi import robot
from waveapi import appengine_robot_runner

import logging

def Main():
	logging.getLogger().setLevel(logging.DEBUG)
	myRobot = robot.Robot('Pushy', 
		image_url='http://chrismdp-pushy.appspot.com/assets/icon.png',
		profile_url='http://chrismdp-pushy.appspot.com/')
	myRobot.register_handler(events.WaveletSelfAdded, OnRobotAdded)
	appengine_robot_runner.run(myRobot)

def OnRobotAdded(event, wavelet):
	"""Invoked when the robot has been added."""
	# post welcome message
	#wavelet.reply("Hello!")
	wavelet.reply("Hi, I'm Pushy. In order to get notifications appearing in this wave, post content to:\n\nhttp://chrismdp-pushy.appspot.com/push/"+wavelet.wave_id+"\n\nOnce you post data to this url, it'll show up on this wave. Pushy should understand github payloads just fine in the future.\n\nYou can safely delete this message: it's just for information.")






