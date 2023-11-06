import random
import pickle

from src.memo import memo
from src.mysql_src import mysqlite

from .Task_data import Task_data
from .Task_service import Task_service

def gen_name(len=32):
	return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890") for _ in range(len))

class Task(object):
	def __init__(self):
		super().__init__()
		self.task_service = None
		if not memo["task_data"]:
			memo["task_data"] = Task_data()
			self.start_service()
	
	def start_service(self):
		self.stop_service()
		self.task_service = Task_service()
		self.task_service.start()
	
	def stop_service(self):
		memo["task_data"].set_status(False)
		if self.task_service is not None:
			self.task_service.join()
		self.task_service = None
	
	def get_id_from_name(self, name:str):
		res = mysqlite.exec("SELECT id FROM task WHERE name = ? AND enabled = 1", (name,))
		if len(res) > 0:
			return res[0]["id"]
		return None

	def add(self, task_run, name:str=None, replace=True):
		if name == None:
			name = gen_name()
			while self.get_id_from_name(name) is not None:
				name = gen_name()
		task_id = self.get_id_from_name(name)
		if task_id is None:
			mysqlite.exec("INSERT INTO task(name, task_run, enabled) VALUES (?, ?, 1)", (name, pickle.dumps(task_run)))
			return True
		elif replace:
			mysqlite.exec("UPDATE task SET task_run = ? WHERE id = ?", (pickle.dumps(task_run), str(task_id)))
			return True
		return False

	def rm(self, name):
		mysqlite.exec("DELETE FROM task WHERE name = ?", (name,))
	
	def disable(self, name):
		mysqlite.exec("UPDATE task SET enabled = 0 WHERE name = ?", (name,))
