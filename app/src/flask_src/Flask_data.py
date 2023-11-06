import random
import config

from .app import app

FL_SET_KEY = config.DEBUG
FL_KEY_LEN = 64

class Flask_data(object):
	def __init__(self):
		super().__init__()
		self.key = None
		self.gen_key()
	
	def get_key(self):
		return self.key

	def gen_key(self):
		if FL_SET_KEY:
			random.seed(0000)
		self.key = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890") for _ in range(FL_KEY_LEN))
		return self.key
	
	def update_key(self):
		app.secret_key = self.get_key()
		return self.key
	
	def get_app_key(self):
		return app.secret_key