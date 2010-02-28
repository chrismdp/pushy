from waveapi import events
from waveapi import model
from waveapi import robot

import logging

def Main():
	logging.getLogger().setLevel(logging.DEBUG)
	logging.debug("Creating robot")
	myRobot = robot.Robot('Pushy', 
		image_url='http://chrismdp-pushy.appspot.com/assets/icon.png',
		version='0.1.2',
		profile_url='http://chrismdp-pushy.appspot.com/')
	logging.debug("Registering events")
	myRobot.RegisterHandler(events.WAVELET_PARTICIPANTS_CHANGED, OnParticipantsChanged)
	myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
	logging.debug("Running robot")
	myRobot.Run()

def OnParticipantsChanged(properties, context):
	"""Invoked when participants are added or removed"""
	added = properties['participantsAdded']
	for p in added:
		Notify(context)

def OnRobotAdded(properties, context):
	"""Invoked when the robot has been added."""
	root_wavelet = context.GetRootWavelet()
	root_wavelet.CreateBlip().GetDocument().SetText("Hello! I'm alive!")

def Notify(context):
	root_wavelet = context.GetRootWavelet()
	root_wavelet.CreateBlip().GetDocument().SetText("Hi Everybody")





