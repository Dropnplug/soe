import flask as fl
import random
import time

from src.fct.logs import logs

PRINT_LOGS = False
LOGS_FILE_PWD = "./data/logs/request.txt"

def log_request(logs_print:bool=PRINT_LOGS, logs_pwd:str=LOGS_FILE_PWD):
	def decorator(func):
		def inner(*args, **kwargs):
			identifier = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890") for _ in range(16))
			log = {
				"identifier":identifier,
				"method":fl.request.method,
				"url": fl.request.base_url,
				"headers":fl.request.headers,
				"data":fl.request.data,
				"ip":fl.request.remote_addr,
				"time":time.time()
			}
			logs("REQUEST", log, logs_print=logs_print, logs_pwd=logs_pwd)
			res = func(*args, **kwargs)
			log = {
				"identifier":identifier,
				"data":res,
				"time":time.time()
			}
			logs("RESPONSE", log, logs_print=logs_print, logs_pwd=logs_pwd)
			return res
		decoret = inner
		decoret.__name__ = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890") for _ in range(16))
		return decoret
	return decorator