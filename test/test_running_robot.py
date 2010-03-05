import unittest

from webtest import TestApp
from waveapi import robot
from waveapi import appengine_robot_runner
from pushy import receive
from pushy import test

from google.appengine.ext import webapp

class TestReceivePush(unittest.TestCase):
	def setUp(self):
		self._application = webapp.WSGIApplication([('/push.*', receive.PushHandler)], debug=True)
		self._app = TestApp(self._application)
		# Mock out wave specific methods
		receive.PushHandler._initialize_robot = lambda self : 0
		receive.PushHandler._reply_to_wave = lambda self, w, wv : 0

	def assertContains(self, itemToLookFor, itemToSearch):
		def escapeHtml(string):
			return string.replace("<", "&lt;")

		escapedItemToLookFor = escapeHtml(itemToLookFor)
		escapedItemToSearch = escapeHtml(str(itemToSearch))
		self.assertTrue(itemToLookFor in itemToSearch, "%s did not contain %s" % (escapedItemToSearch, escapedItemToLookFor))

	def testPostsToWaveOnPush(self):
		response = self._app.post('/push/wavesandbox.com!F+33934934')
		self.assertContains('OK', response)
	
	def testMalformedRequestShouldFail(self):
		response = self._app.post('/push')
		self.assertContains("Malformed URL", response)

class TestReceive(unittest.TestCase):
	def testExtractWaveId(self):
		id = receive._extract_wave_id("/push/wavesandbox.com%21w%2B27uuNu-2A")
		self.assertEquals("wavesandbox.com!w+27uuNu-2A", id)

	def testExtractWaveIdReturnsEmptyOnMalformedLink(self):
		id = receive._extract_wave_id("/push")
		self.assertEquals("", id)

	def testGenerateWaveletIdFromWaveId(self):
		self.assertEquals("wavesandbox.com!conv+root", receive._generate_wavelet_id_from_wave_id("wavesandbox.com!w+27uuNu-2A"))

