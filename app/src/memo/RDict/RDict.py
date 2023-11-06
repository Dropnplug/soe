from multiprocessing.managers import BaseManager
import multiprocessing
import time

from .RDict_server import RDict_server_process, RDict_server_thread, DEFAULT_AUTHKEY

VARIABLE_TYPES = [bool, int, float, complex, str, bytes, bytearray, set, frozenset]

ITERABLE_TYPES = [list, tuple, dict]

class RDict_function(object):
	def __init__(self, rdict, path, key):
		self.rdict = rdict
		self.path = path
		self.key = key
	
	def execute(self, *args, **kwargs):
		return self.rdict.execattr(self.path, self.key, *args, **kwargs)

class RDict(object):

	class SManager(BaseManager): pass
	SManager.register("rdict_manager")

	def __init__(self, ip="127.0.0.1", port=5101, authkey=DEFAULT_AUTHKEY, process=True, master=None):
		multiprocessing.freeze_support()
		super().__init__()
		self._ip = ip
		self._port = port
		self._authkey = authkey
		self._process = process
		self.master = master
		self._server = None
		self._rdict_manager = None

	def _kill_server(self):
		if self._server is not None:
			try:
				self._server.terminate()
				self._server.join()
			except:
				return False
			self._server = None
			return True
		return False
	
	def _start_server(self):
		self._kill_server()
		if self._process:
			self._server = RDict_server_process(ip=self._ip, port=self._port, authkey=self._authkey)
		else:
			self._server = RDict_server_thread(ip=self._ip, port=self._port, authkey=self._authkey)
		self._server.start()
	
	def _start(self, retry=True):
		try:
			manager = self.SManager(address=(self._ip, self._port), authkey=self._authkey)
			manager.connect()
			self._rdict_manager = manager.rdict_manager()
		except:
			if self._server is None:
				if self.master is None or self.master == True:
					self._start_server()
				time.sleep(.1)
				if retry:
					self._start(retry=False)
	
	def _on_use(self):
		if self._rdict_manager is None:
			self._start()
		else:
			try:
				self._rdict_manager.is_alive()
			except:
				self._start()
		try:
			self._rdict_manager.is_alive()
		except:
			raise RuntimeError("Unable to start RDict server")

	def _modify_iterable(self, item, path):
		if type(item) is dict:
			for i in item.keys():
				item[i] = self._modify_item(item[i], path+[i])
		else:
			tuple_type = False
			if type(item) is tuple:
				item = list(item)
			for i in range(len(item)):
				item[i] = self._modify_item(item[i], path+[i])
			if tuple_type:
				item = tuple(item)
		return item

	def _modify_object(self, item, path):
		for key in dir(item):
			if not "__" in key:
				if callable(getattr(item, key)):
					setattr(item, key, RDict_function(self, path, key).execute)
				else:
					setattr(item, key, self._modify_item(getattr(item, key), path+[key]))
		return item

	def _modify_item(self, item, path):
		if type(item) in VARIABLE_TYPES:
			return item
		elif type(item) in ITERABLE_TYPES:
			return self._modify_iterable(item, path)
		else:
			return self._modify_object(item, path)

	def __getitem__(self, item):
		self._on_use()
		return self._modify_item(self._rdict_manager.getattr(item), [item]) 
	
	def __setitem__(self, item, value):
		self._on_use()
		return self._rdict_manager.setattr(item, value)
	
	def __delitem__(self, item):
		self._on_use()
		return self._rdict_manager.delattr(item)

	def __getattr__(self, item):
		if len(item) > 0:
			if item[0] != '_':
				self._on_use()
				return getattr(self._rdict_manager, item)
		return None
