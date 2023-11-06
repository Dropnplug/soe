from multiprocessing.managers import BaseManager
import multiprocessing

from .Thread import Thread
from .RDict_manager import RDict_manager

DEFAULT_AUTHKEY = b"NotVerySecure..."

class RDict_server_process(multiprocessing.Process):

	class SManager(BaseManager): pass

	def __init__(self, ip="127.0.0.1", port=5101, authkey=DEFAULT_AUTHKEY):
		super().__init__()
		self.daemon = True
		self._ip = ip
		self._port = port
		self._authkey = authkey
	
	def run(self):
		rdict_manager = RDict_manager()
		self.SManager.register("rdict_manager", callable=lambda:rdict_manager)
		manager = self.SManager(address=(self._ip,self._port), authkey=self._authkey)
		server = manager.get_server()
		server.serve_forever()

class RDict_server_thread(Thread):

	class SManager(BaseManager): pass

	def __init__(self, ip="127.0.0.1", port=5101, authkey=DEFAULT_AUTHKEY):
		super().__init__()
		self.daemon = True
		self._ip = ip
		self._port = port
		self._authkey = authkey
	
	def run(self):
		rdict_manager = RDict_manager()
		self.SManager.register("rdict_manager", callable=lambda:rdict_manager)
		manager = self.SManager(address=(self._ip,self._port), authkey=self._authkey)
		server = manager.get_server()
		server.serve_forever()
