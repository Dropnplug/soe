from .RDict.RDict import RDict
import config

def init():
	global memo
	memo = RDict(ip=config.MANAGER_ADDRESS, port=config.MANAGER_PORT, authkey=config.MANAGER_KEY, process=False)
	
