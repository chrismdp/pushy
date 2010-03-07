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
		profile_url='http://pushyrobot.appspot.com/')
	return _robot

def _mangle_wave_id(wave_id):
	return "%s/%s" % (wave_id.split("!")[0], wave_id.split("+")[1])

def _extract_wave_id(url):
	_split = url.split('/')
	if (len(_split) < 4):
		return ""
	return "%s!w+%s" % (_split[2], _split[3])

def _discover_server(wave_id):
	return wave_id.split("!")[0]

def _generate_wavelet_id_from_wave_id(wave_id):
	return _discover_server(wave_id) + "!conv+root"

def _gravatar_url_from(email):
	gravatar_url = "http://www.gravatar.com/avatar/"+hashlib.md5(email).hexdigest() + "?s=30"
	return gravatar_url

def _convert_time(tstr):
	ts = time.strptime(tstr, "%Y-%m-%dT%H:%M:%S-08:00")
	t = time.mktime(ts)
	t += 8 * 60 * 60
	return _format_for_commit(t)

def _format_for_commit(t):
	return time.strftime("%a, %d %b %Y %H:%M", time.gmtime(t))

def _add_github_message(wavelet, myJson):
	payload = json.loads(urllib.unquote(myJson))
	for commit in payload['commits']:
		reply = wavelet.reply()
		reply.append("[github: "+payload['repository']['url']+"]\n\n")
		commit['timestamp'] = _convert_time(commit['timestamp'])
		commit['image'] = _gravatar_url_from(commit['author']['email'])
		commit['author'] = commit['author']['name']
		reply.append(element.Gadget("http://pushyrobot.appspot.com/gadgets/github.xml", 
			{'commit': urllib.quote(json.dumps(commit))}))

def _add_googlecode_message(wavelet, myJson):
	payload = json.loads(myJson)
	for commit in payload['revisions']:
		reply = wavelet.reply()
		reply.append("[googlecode: "+payload['repository_path']+"]\n\n")
		commit['timestamp'] = _format_for_commit(commit['timestamp'])
		commit['id'] = str(commit['revision'])
		reply.append(element.Gadget("http://pushyrobot.appspot.com/gadgets/github.xml", 
			{'commit': urllib.quote(json.dumps(commit))}))
		
def _generate_message(body):
	if (body.startswith('{"repository_path":"')):
		def _hook(wavelet):
			_add_googlecode_message(wavelet, body)
		return _hook
	data = body.split("=")
	if (len(data) < 2):
		return body
	if (data[0] == 'payload'):
		def _hook(wavelet):
			_add_github_message(wavelet, data[1])
		return _hook
	return body

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
		RPC = {'wavesandbox.com': 'http://sandbox.gmodules.com/api/rpc',
				   'googlewave.com': 'http://gmodules.com/api/rpc'}
		self._robot.setup_oauth(OAUTH['key'], OAUTH['secret'], 
			server_rpc_base = RPC[_discover_server(wave_id)])	
		wavelet = self._robot.fetch_wavelet(wave_id, wavelet_id)
		if (types.FunctionType == type(message)):
			message(wavelet)
		else:
		  wavelet.reply(message)
		self._robot.submit(wavelet)

	def _initialize_robot(self):
		self._robot = _create_robot()

def main():
	application = webapp.WSGIApplication([('/push.*', PushHandler)], debug=True)
	run_wsgi_app(application)                                    

if __name__ == '__main__':
	main()
