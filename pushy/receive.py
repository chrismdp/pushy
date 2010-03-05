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

CONSUMER_KEY = "128449655778"
CONSUMER_SECRET = "Cy0i+17WTMdj2kxsXXBvnTvq"

def _create_robot():
	logging.debug("Creating Robot")
	_robot = robot.Robot('Pushy (test)', 
		image_url='http://chrismdp-test.appspot.com/assets/icon.png',
		profile_url='http://chrismdp-test.appspot.com/')
	_robot.setup_oauth(CONSUMER_KEY, CONSUMER_SECRET, server_rpc_base='http://sandbox.gmodules.com/api/rpc')	
	return _robot

def _mangle_wave_id(wave_id):
	return "%s/%s" % (wave_id.split("!")[0], wave_id.split("+")[1])

def _extract_wave_id(url):
	_split = url.split('/')
	if (len(_split) < 4):
		return ""
	return "%s!w+%s" % (_split[2], _split[3])

def _generate_wavelet_id_from_wave_id(wave_id):
	return "%s!conv+root" % wave_id.split('!')[0]

def _gravatar_url_from(email):
	gravatar_url = "http://www.gravatar.com/avatar/"+hashlib.md5(email).hexdigest() + "?s=40"
	return gravatar_url

def _convert_time(tstr):
	ts = time.strptime(tstr, "%Y-%m-%dT%H:%M:%S-08:00")
	t = time.mktime(ts)
	t += 8 * 60 * 60
	return time.strftime("%a, %d %b %Y %H:%M", time.gmtime(t))

def _add_github_message(wavelet, myJson):
	payload = json.loads(urllib.unquote(myJson))
	for commit in payload['commits']:
		_blip = wavelet.reply()
		title = "[Github] " + commit['message']
		_blip.append(title+"\n\n")
		_blip.first(title).annotate("style/fontWeight", "bold")
		_blip.append(element.Image(_gravatar_url_from(commit['author']['email'])))
		_blip.append("\n\n" + commit['author']['name']+" on ")
		_blip.append(_convert_time(commit['timestamp'])+"\n\n")
		for modified in commit['modified']:
			_blip.append(modified + "\n")
			_blip.first(modified).annotate("style/fontStyle", "italic")
		_blip.append("\n"+commit['id'])
		_blip.append("\n"+payload['repository']['url'])
		_blip.first(commit['id']).annotate("link/manual", commit['url'])

def _generate_message(body):
	data = body.split("=")
	if (len(data) < 2):
		return body
	if (data[0] == 'payload'):
		def _hook(wavelet):
			_add_github_message(wavelet, data[1])
		return _hook
	return data[1]

class PushHandler(webapp.RequestHandler):
	def __init__(self):
		self._initialize_robot()

	def post(self):
		wave_id = _extract_wave_id(self.request.path)
		if (wave_id == ""):
			self.response.out.write("Malformed URL")
			return
		wavelet_id = _generate_wavelet_id_from_wave_id(wave_id)
		message = _generate_message(self.request.body)
		self._reply_to_wave(wave_id, wavelet_id, message)
		self.response.out.write("OK")
	
	def _reply_to_wave(self, wave_id, wavelet_id, message):
		logging.debug("Fetching wavelet: "+wave_id+", "+wavelet_id)
		wavelet = self._robot.fetch_wavelet(wave_id, wavelet_id)
		if (types.FunctionType == type(message)):
			message(wavelet)
		else:
		  wavelet.reply(message)
		self._robot.submit(wavelet)

	def _initialize_robot(self):
		logging.debug("ROBOT INIT")
		self._robot = _create_robot()

def main():
	application = webapp.WSGIApplication([('/push.*', PushHandler)], debug=True)
	run_wsgi_app(application)                                    

if __name__ == '__main__':
	main()
