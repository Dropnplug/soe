import time
import multiprocessing

from src.fct.Thread import Thread

class Task_run(object):
	def __init__(self, fct, args:list=[], kwargs:dict={}, timeout:int=60, thread:bool=True):
		super().__init__()
		self.repeat = 0
		self.last_run = 0
		self.fct = fct
		self.args = args
		self.kwargs = kwargs
		self.timeout = timeout
		self.thread = thread
	
	def condition(self):
		return True

	def enabled(self):
		return True

	def run(self):
		if self.condition():
			if self.thread:
				t = Thread(target=self.fct, args=self.args, kwargs=self.kwargs)
			else:
				t = multiprocessing.Process(target=self.fct, args=self.args, kwargs=self.kwargs)
			t.daemon = True
			t.start()
			self.repeat += 1
			self.last_run = time.time()
			return {"task":t, "start":time.time(), "timeout":self.timeout}
		return None