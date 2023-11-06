import time
import datetime

from .Task_run_count import Task_run_count
from src.fct.logs import logs


class Task_run_date(Task_run_count):
	def __init__(self, date, *args, **kwargs):
		super().__init__(1, *args, **kwargs)
		self.date = None
		if type(date) in [float, int]:
			self.date = date
		if type(date) == str:
			try:
				self.date = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timetuple())
			except:
				self.date = None
				logs("/!\\ Invalid date format, use a time.time object or a str('%Y-%m-%d %H:%M:%S'). Disabeling task")
	
	def enabled(self):
		if self.date is None:
			return False
		return super().enabled()

	def condition(self):
		if self.date is None:
			return False
		if self.date <= time.time():
			return super().condition()
		return False