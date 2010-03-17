import logging
import os
import time
import hashlib,urllib

from waveapi import element
from waveapi import robot
from waveapi import simplejson as json

ROBOT_URL = "http://pushyrobot.appspot.com"

def _create_robot():
	logging.debug("Creating Robot")
	_robot = robot.Robot('Pushy', 
		image_url= ROBOT_URL + '/assets/icon.png',
		profile_url='http://bit.ly/9whjgr')
	return _robot

def _mangle_wave_id(wave_id):
	return "%s/%s" % (wave_id.split("!")[0], wave_id.split("+")[1])

def extract_wave_id(url):
	_split = url.split('/')
	if(len(_split) < 4):
		return ""
	return "%s!w+%s" % (_split[2], _split[3])

def _discover_server(wave_id):
	return wave_id.split("!")[0]

def generate_wavelet_id_from_wave_id(wave_id):
	return _discover_server(wave_id) + "!conv+root"

def _gravatar_url_from(email):
	gravatar_url = "http://www.gravatar.com/avatar/"+hashlib.md5(email).hexdigest() + "?s=30"
	return gravatar_url

def _convert_time(tstr):
	[date, seperator, tz] = tstr.rpartition('-')
	ts = time.strptime(date, "%Y-%m-%dT%H:%M:%S")
	t = time.mktime(ts)
	t += int(tz[0:2]) * 60 * 60
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
		reply.append(element.Gadget(ROBOT_URL + "/gadgets/github.xml", 
			{'commit': urllib.quote(json.dumps(commit))}))

def _add_googlecode_message(wavelet, myJson):
	payload = json.loads(myJson)
	for commit in payload['revisions']:
		reply = wavelet.reply()
		reply.append("[googlecode: "+payload['repository_path']+"]\n\n")
		commit['timestamp'] = _format_for_commit(commit['timestamp'])
		commit['id'] = str(commit['revision'])
		reply.append(element.Gadget(ROBOT_URL + "/gadgets/github.xml", 
			{'commit': urllib.quote(json.dumps(commit))}))
		
def generate_message(body):
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


