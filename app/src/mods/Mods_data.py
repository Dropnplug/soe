class Mods_data(object):
	def __init__(self):
		super().__init__()
		self._data = {}
	
	def _add_mod(self:str, name:str):
		if name in self._data.keys():
			return False
		self._data[name] = {'main':False, 'web':False, 'web_dirs':[]}

	def import_web(self, name:str, dir:str):
		self._add_mod(name)
		self._data[name]['web'] = True
		self._data[name]['web_dirs'].append(dir)
	
	def import_main(self, name:str):
		self._add_mod(name)
		self._data[name]['main'] = True
	
	def get_mods_name(self):
		return list(self._data.keys())