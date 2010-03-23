import unittest
import types
import utils

GITHUB_JSON = 'payload={"repository":{"watchers":2,"description":"Google Wave Robot to publish Github commits","open_issues":0,"fork":false,"forks":0,"url":"http://github.com/chrismdp/pushy","private":false,"homepage":"","owner":{"email":"chris@edendevelopment.co.uk","name":"chrismdp"},"name":"pushy"},"before":"bf48c69ca8d7608be49887d08d59dfc43eec1540","ref":"refs/heads/master","after":"8af0e96ca42840501f556a3c1ad653c10980aa92","commits":[{"message":"Working version with sandbox","removed":[],"modified":["pushy/app.py","pushy/utils.py","test/test_running_robot.py"],"url":"http://github.com/chrismdp/pushy/commit/43821d6797ac5d5f66fa37bcc5146305e008013b","author":{"email":"dev+chrismdp+ecomba@edendevelopment.co.uk","name":"Chris Parsons and Enrique Comba Riepenhausen"},"timestamp":"2010-03-04T16:41:53-08:00","added":[],"id":"43821d6797ac5d5f66fa37bcc5146305e008013b"},{"message":"Moved away from urlencode to simpler paths","removed":[],"modified":["pushy/app.py","pushy/utils.py","test/test_running_robot.py"],"url":"http://github.com/chrismdp/pushy/commit/8af0e96ca42840501f556a3c1ad653c10980aa92","author":{"email":"chris@edendevelopment.co.uk","name":"Chris Parsons"},"timestamp":"2010-03-04T17:11:48-08:00","added":[],"id":"8af0e96ca42840501f556a3c1ad653c10980aa92"}]}'

class TestUtils(unittest.TestCase):
	def testMangleWaveId(self):
		url = utils._mangle_wave_id("wavesandbox.com!w+27uuNu-2A")
		self.assertEquals("wavesandbox.com/27uuNu-2A", url)

	def testExtractWaveId(self):
		id = utils.extract_wave_id("/push/wavesandbox.com/27uuNu-2A")
		self.assertEquals("wavesandbox.com!w+27uuNu-2A", id)

	def testExtractWaveIdReturnsEmptyOnMalformedLink(self):
		id = utils.extract_wave_id("/push")
		self.assertEquals("", id)

	def testGenerateWaveletIdFromWaveId(self):
		self.assertEquals("wavesandbox.com!conv+root", utils.generate_wavelet_id_from_wave_id("wavesandbox.com!w+27uuNu-2A"))
	def testGravatarUrlGeneration(self):
		self.assertEquals("http://www.gravatar.com/avatar/3f174ec378d1c94977a5ac7f4aea9df8?s=30", utils._gravatar_url_from("chris@test.com"))

	def testConvertTime(self):
		self.assertEquals("Fri, 05 Mar 2010 01:11", utils._convert_time("2010-03-04T17:11:48-08:00"))
		self.assertEquals("Fri, 05 Mar 2010 01:11", utils._convert_time("2010-03-04T18:11:48-07:00"))
		self.assertEquals("Fri, 05 Mar 2010 01:11", utils._convert_time("2010-03-05T01:11:48-00:00"))

class TestGenerateMessage(unittest.TestCase):
	def testReturnsBlankIfBodyIsBlank(self):
		self.assertEquals("", utils.generate_message(""))

	def testReturnsIdentityIfJustMessage(self):
		self.assertEquals("foo", utils.generate_message("foo"))

	def testReturnsNormalMessages(self):
		self.assertEquals("data=foo", utils.generate_message("data=foo"))

	def testReturnsGitHubFormatted(self):
		message = utils.generate_message(GITHUB_JSON)
		self.assertEquals(types.FunctionType, type(message))

