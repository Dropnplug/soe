import time

from .Task_run import Task_run
from .Task_run_count import Task_run_count

class Task_run_time(Task_run):
	def __init__(self, timer:float, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.timer = timer
	
	def condition(self):
		if self.last_run+self.timer < time.time():
			return True
		return False

class Task_run_count_time(Task_run_count):
	def __init__(self, timer:float, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.timer = timer
	
	def condition(self):
		if self.last_run+self.timer < time.time():
			return super().condition()
		return False