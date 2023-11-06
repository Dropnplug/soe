from .Mysqlite import Mysqlite

def init():
	global mysqlite
	mysqlite = Mysqlite()