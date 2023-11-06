import sqlite3
import time
import random

MYSQL_PWD = "./data/db/live.db"

class Mysqlite(object):
	def __init__(self):
		super().__init__()

	def add_rowid(self, cmd):
		modif = False
		if cmd.lower().startswith("select "):
			cmd =  cmd[:7]+"rowid, "+cmd[7:]
			modif = True
		return str(cmd), modif

	def exec(self, cmd, *args, executemany:bool=False, _rowid:bool=False, lastrowid:bool=True, retry:int=1, **kwargs):
		modif = False
		if _rowid:
			cmd, modif = self.add_rowid(cmd)
		with sqlite3.connect(MYSQL_PWD) as db:
			try:
				cur = db.cursor()
				if executemany:
					cur.executemany(cmd, *args, **kwargs)
				else:
					cur.execute(cmd, *args, **kwargs)
				res = cur.fetchall()
			except:
				if retry > 0:
					time.sleep(random.uniform(0.01, 0.1))
					# print("retry", cmd)
					return self.exec(cmd, *args, executemany=executemany, _rowid=_rowid, lastrowid=lastrowid, retry=retry-1, **kwargs)
				return None

			if lastrowid and "insert" in cmd.lower():
				cur.execute("SELECT LAST_INSERT_ROWID()")
				_lastrowid = int(cur.fetchall()[0][0])
			ret = []
			for r in res:
				r_e = {}
				start=0
				if len(cur.description) > 1 and modif and cur.description[0][0] == 'id':
					r_e["_rowid"] = r[0]
					start+=1
				for d in range(start, len(cur.description)):
					r_e[cur.description[d][0]] = r[d]
				ret.append(r_e)
			cur.close()
			if lastrowid and "insert" in cmd.lower():
				return _lastrowid
			return ret
		return None
	
	def detail(self, cmd, *args, **kwargs):
		with sqlite3.connect(MYSQL_PWD) as db:
			cur = db.cursor()
			cur.execute(cmd, *args, **kwargs)
			ret = []
			for d in range(len(cur.description)):
				ret.append(cur.description[d][0])
			return ret
		return None