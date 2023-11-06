def explore(item, path):
	if len(path) > 0:
		key = path.pop(0)
		if type(item) in [dict, list, tuple]:
			return explore(item[key], path)
		return explore(getattr(item, key), path)
	return item

class RDict_manager(object):
	def __init__(self):
		super().__init__()
		self._data = {}
	
	def is_alive(self):
		return True
	
	def getattr(self, key):
		if key not in self._data.keys():
			return None
		return self._data[key]
	
	def setattr(self, key, value):
		self._data[key] = value
	
	def delattr(self, key):
		if key not in self._data.keys():
			return None
		del self._data[key]
	
	def execattr(self, path:list, attr:str, *args, **kwargs):
		key = path.pop(0)
		if key not in self._data.keys():
			return None	
		return getattr(explore(self._data[key], path), attr)(*args, **kwargs)

	def keys(self):
		return self._data.keys()

	def values(self):
		return self._data.values()
	
	def items(self):
		return self._data.items()