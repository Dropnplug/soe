try:
	from ._init import app
except:
	from ._init import init
	init()
	from ._init import app