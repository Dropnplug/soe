import multiprocessing
import time
import pickle

from src.memo import memo
from src.mysql_src import mysqlite
from src.fct.logs import logs

import config

class Task_service(multiprocessing.Process):
	def __init__(self):
		super().__init__()
		if config.DEBUG:
			logs("/!\\ init Task_service")
		self.daemon = True
		self.tasks = []
	
	def run_task(self):
		task_list = mysqlite.exec("SELECT id, name, task_run FROM task WHERE enabled = 1")
		for task in task_list:
			try:
				task_run = pickle.loads(task["task_run"])
				t = task_run.run()
				if t is not None:
					self.tasks.append(t)
					enabled = int(task_run.enabled())
					mysqlite.exec("UPDATE task SET task_run = ? , enabled = ? WHERE id = ?", (pickle.dumps(task_run),enabled, task["id"]))
			except Exception as e:
				logs("/!\\ error while running", task["name"])
				mysqlite.exec("UPDATE task SET enabled = 0 WHERE id = ?", (task["id"],))
				if config.DEBUG:
					print(task["name"], e)

	def timeout(self):
		rm = []
		for t in self.tasks:
			if t["start"]+t["timeout"] < time.time():
				t["task"].terminate()
				rm.append(t)
		for t in rm:
			self.tasks.remove(t)

	def run(self):
		if config.DEBUG:
			logs("/!\\ start Task_service")
		memo["task_data"].set_status(True)
		time.sleep(20)
		while memo["task_data"].status:
			try:
				self.run_task()
				self.timeout()
				time.sleep(.1)
			except Exception as e:
				logs("/!\\ error in main task loop")
				if config.DEBUG:
					print(e)
		memo["task_data"].set_status(False)
		if config.DEBUG:
			logs("/!\\ stop Task_service")