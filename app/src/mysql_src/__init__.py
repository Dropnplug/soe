try:
	from ._init import mysqlite
except:
	from ._init import init
	init()
	from ._init import mysqlite