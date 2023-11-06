try:
	from ._init import memo
except:
	from ._init import init
	init()
	from ._init import memo
