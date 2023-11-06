from .Task_run import Task_run

class Task_run_count(Task_run):
	def __init__(self, count:int, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.count = count
	
	def enabled(self):
		if self.repeat < self.count:
			return True
		return False
	
	def condition(self):
		if self.repeat < self.count:
			return True
		return False