from .run import *


try:
	from ._init import task
except:
	from ._init import init
	init()
	from ._init import task