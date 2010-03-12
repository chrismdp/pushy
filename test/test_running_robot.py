import unittest
import types

from webtest import TestApp
from waveapi import robot
from waveapi import appengine_robot_runner
from pushy import receive
from pushy import test

from google.appengine.ext import webapp

def contains(itemToLookFor, itemToSearch):
	def escapeHtml(string):
		return string.replace("<", "&lt;")

	escapedItemToLookFor = escapeHtml(itemToLookFor)
	escapedItemToSearch = escapeHtml(str(itemToSearch))
	return itemToLookFor in itemToSearch, "%s did not contain %s" % (escapedItemToSearch, escapedItemToLookFor)

class TestReceivePush(unittest.TestCase):
	def setUp(self):
		self._application = webapp.WSGIApplication([('/push.*', receive.PushHandler)], debug=True)
		self._app = TestApp(self._application)
		# Mock out wave specific methods
		receive.PushHandler._initialize_robot = lambda self : 0
		receive.PushHandler._reply_to_wave = lambda self, w, wv, msg : 0

	def testPostsToWaveOnPush(self):
		response = self._app.post('/push/wavesandbox.com/33934934')
		self.assertTrue(contains('OK', response))
	
	def testMalformedRequestShouldFail(self):
		response = self._app.post('/push')
		self.assertTrue(contains("Malformed URL", response))

