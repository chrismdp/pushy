from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pushy import app

import urllib
import logging

def _extract_wave_id(url):
	_split = url.split('/')
	if (len(_split) < 3):
		return ""
	return urllib.unquote(_split[2])

def _generate_wavelet_id_from_wave_id(wave_id):
	return "%s!conv+root" % wave_id.split('!')[0]

class PushHandler(webapp.RequestHandler):
	def __init__(self):
		self._initialize_robot()

	def post(self):
		wave_id = _extract_wave_id(self.request.path)
		if (wave_id == ""):
			self.response.out.write("Malformed URL")
			return
		wavelet_id = _generate_wavelet_id_from_wave_id(wave_id)
		self._reply_to_wave(wave_id, wavelet_id)
		self.response.out.write("OK")
	
	def _reply_to_wave(self, wave_id, wavelet_id):
		logging.debug("Fetching wavelet: "+wave_id+", "+wavelet_id)
		wavelet = self._robot.fetch_wavelet(wave_id, wavelet_id)
		wavelet.reply(self.request.body)
		self._robot.submit(wavelet)

	def _initialize_robot(self):
		logging.debug("ROBOT INIT")
		self._robot = app.create_robot()

def main():
	application = webapp.WSGIApplication([('/push.*', PushHandler)], debug=True)
	run_wsgi_app(application)                                    

if __name__ == '__main__':
	main()
