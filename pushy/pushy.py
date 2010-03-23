import utils
import types

#OAUTH = { 'key': "128449655778", 'secret': "Cy0i+17WTMdj2kxsXXBvnTvq" } # chrismdp-test
OAUTH = { 'key': "610714189216", 'secret': "Eu3Dh0CAqzlQ1Kj4O59yuHA0" } # pushyrobot

def _setup_authentication(robot, wave_id):
	RPC = {'wavesandbox.com': 'http://sandbox.gmodules.com/api/rpc',
				 'googlewave.com': 'http://gmodules.com/api/rpc'}
	robot.setup_oauth(OAUTH['key'], OAUTH['secret'], 
		server_rpc_base = RPC[utils._discover_server(wave_id)])	

class Pushy:
	def __init__(self):
		self._initialize_robot()

	def handle_push(self, url, pushed_content):
		wave_id = utils.extract_wave_id(url)
		if (wave_id == ""):
			return False
		wavelet_id = utils.generate_wavelet_id_from_wave_id(wave_id)
		message = utils.generate_message(pushed_content)
		self._reply_to_wave(wave_id, wavelet_id, message)
		return True
	
	def _reply_to_wave(self, wave_id, wavelet_id, message):
		_setup_authentication(self._robot, wave_id)
		wavelet = self._robot.fetch_wavelet(wave_id, wavelet_id)
		self.dispatch_message(wavelet, message)
		self._robot.submit(wavelet)

	def dispatch_message(self, wavelet, message):
		if (types.FunctionType == type(message)):
			message(wavelet)
		else:
		  wavelet.reply(message)

	def _initialize_robot(self):
		self._robot = utils._create_robot()
