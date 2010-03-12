from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from waveapi import robot
from waveapi import element

import logging
import types
import os
import time
import hashlib,urllib
from waveapi import simplejson as json

OAUTH = { 'key': "610714189216", 'secret': "Eu3Dh0CAqzlQ1Kj4O59yuHA0" }

def _create_robot():
	logging.debug("Creating Robot")
	_robot = robot.Robot('Pushy', 
		image_url='http://pushyrobot.appspot.com/assets/icon.png',
		profile_url='http://bit.ly/9whjgr')
	return _robot

def _setup_authentication(wave_id):
	RPC = {'wavesandbox.com': 'http://sandbox.gmodules.com/api/rpc',
				 'googlewave.com': 'http://gmodules.com/api/rpc'}
	self._robot.setup_oauth(OAUTH['key'], OAUTH['secret'], 
		server_rpc_base = RPC[_discover_server(wave_id)])	

class PushHandler(webapp.RequestHandler):
	def __init__(self):
		self._initialize_robot()

	def post(self):
		if self._handle_push(self.request.path, self.request.body):
			self.response.out.write("Malformed URL")
		else:
			self.response.out.write("OK")

	def _handle_push(self, url, pushed_content):
		wave_id = utils.extract_wave_id(url)
		if (wave_id == ""):
			return False
		wavelet_id = utils.generate_wavelet_id_from_wave_id(wave_id)
		message = utils.generate_message(pushed_content)
		self._reply_to_wave(wave_id, wavelet_id, message)
		return True
		
	def _reply_to_wave(self, wave_id, wavelet_id, message):
		_setup_authentication(wave_id)
		wavelet = self._robot.fetch_wavelet(wave_id, wavelet_id)
		self.dispatch_message(wavelet, message)
		self._robot.submit(wavelet)

	def dispatch_message(self, wavelet, message):
		if (types.FunctionType == type(message)):
			message(wavelet)
		else:
		  wavelet.reply(message)

	def _initialize_robot(self):
		self._robot = _create_robot()

def main():
	application = webapp.WSGIApplication([('/push.*', PushHandler)], debug=True)
	run_wsgi_app(application)                                    

if __name__ == '__main__':
	main()
