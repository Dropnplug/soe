import time

from .Task_run import Task_run
from .Task_run_count import Task_run_count

DAY_IN_SEC = 86400

class Task_run_daily(Task_run):
	def __init__(self, *args, hour:int=1, min:int=0, sec:int=0, **kwargs):
		super().__init__(*args, **kwargs)
		self.hour = hour
		self.min = min
		self.sec = sec
	
	def condition(self):
		now = time.time()
		local = time.localtime(now)
		if self.hour == local.tm_hour and self.min == local.tm_min and self.sec == local.tm_sec:
			if self.last_run+1 < time.time():
				return True
		if self.last_run != 0 and self.last_run+DAY_IN_SEC < time.time():
			return True
		return False

class Task_run_count_daily(Task_run_count):
	def __init__(self, *args, hour:int=1, min:int=0, sec:int=0, **kwargs):
		super().__init__(*args, **kwargs)
		self.hour = hour
		self.min = min
		self.sec = sec
	
	def condition(self):
		now = time.time()
		local = time.localtime(now)
		if self.hour == local.tm_hour and self.min == local.tm_min and self.sec == local.tm_sec:
			if self.last_run+1 < time.time():
				return super().condition()
		if self.last_run != 0 and self.last_run+DAY_IN_SEC < time.time():
			return super().condition()
		return False