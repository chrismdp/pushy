from waveapi import events
from waveapi import robot
from waveapi import appengine_robot_runner

import logging
import urllib

CONSUMER_KEY = "128449655778"
CONSUMER_SECRET = "Cy0i+17WTMdj2kxsXXBvnTvq"

def create_robot():
	logging.debug("Creating Robot")
	_robot = robot.Robot('Pushy (test)', 
		image_url='http://chrismdp-test.appspot.com/assets/icon.png',
		profile_url='http://chrismdp-test.appspot.com/')
	_robot.setup_oauth(CONSUMER_KEY, CONSUMER_SECRET, server_rpc_base='http://sandbox.gmodules.com/api/rpc')	
	return _robot

def Main():
	logging.getLogger().setLevel(logging.DEBUG)
	myRobot = create_robot()
	myRobot.register_handler(events.WaveletSelfAdded, OnRobotAdded)
	appengine_robot_runner.run(myRobot)

def OnRobotAdded(event, wavelet):
	wavelet.reply("Hi, I'm Pushy. In order to get notifications appearing in this wave, post content to:\n\nhttp://chrismdp-test.appspot.com/push/"+urllib.quote_plus(wavelet.wave_id)+"\n\nOnce you post data to this url, it'll show up on this wave. Pushy should understand github payloads just fine in the future.\n\nYou can safely delete this message: it's just for information.")






