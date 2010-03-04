import unittest

from webtest import TestApp
from waveapi import robot
from waveapi import appengine_robot_runner
from pushy import receive

from google.appengine.ext import webapp

def assertContains(self, itemToLookFor, itemToSearch):
	def escapeHtml(string):
		return string.replace("<", "&lt;")

	escapedItemToLookFor = escapeHtml(itemToLookFor)
	escapedItemToSearch = escapeHtml(str(itemToSearch))
	self.assertTrue(itemToLookFor in itemToSearch, "%s did not contain %s" % (escapedItemToSearch, escapedItemToLookFor))

class TestReceivePush(unittest.TestCase):
	def setUp(self):
		self._application = webapp.WSGIApplication([('/push.*', receive.PushHandler)], debug=True)

	def testRespondsToPush(self):
		app = TestApp(self._application)
		response = app.get('/push')
		self.assertEquals('200 OK', response.status)

#class TestRunningRobot(unittest.TestCase):
#  def setUp(self):
#		self._robot = robot.Robot("Test Pushy")
#		self._application = appengine_robot_runner.create_robot_webapp(self._robot)

#	def test_running_tests(self):
#		app = TestApp(self._application)
#		response = app.get("/_wave/capabilities.xml")
#		self.assertEquals("200 OK", response.status)


