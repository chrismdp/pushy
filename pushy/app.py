from waveapi import events
from waveapi import appengine_robot_runner

import logging
import urllib

from pushy import receive

def Main():
	logging.getLogger().setLevel(logging.DEBUG)
	myRobot = receive._create_robot()
	myRobot.register_handler(events.WaveletSelfAdded, OnRobotAdded)
	appengine_robot_runner.run(myRobot)

def OnRobotAdded(event, wavelet):
	wavelet.reply("Hi, I'm Pushy. In order to get notifications appearing in this wave, post content to:\n\nhttp://pushyrobot.appspot.com/push/"+receive._mangle_wave_id(wavelet.wave_id)+"\n\nOnce you post data to this url, it'll show up on this wave. Pushy understands github payloads fine and will format them correctly.\n\nYou can safely delete this message: it's just for information.")






