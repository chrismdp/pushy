from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import logging
import types
import os
import time
import hashlib,urllib
from waveapi import simplejson as json

from pushy import utils
from pushy import pushy

class PushHandler(webapp.RequestHandler):
	def __init__(self):
		self._pushy = pushy.Pushy()

	def post(self):
		if self._pushy.handle_push(self.request.path, self.request.body):
			self.response.out.write("OK")
		else:
			self.response.out.write("Malformed URL")

def main():
	application = webapp.WSGIApplication([('/push.*', PushHandler)], debug=True)
	run_wsgi_app(application)                                    

if __name__ == '__main__':
	main()
