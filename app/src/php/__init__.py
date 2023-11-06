import subprocess as sp
import multiprocessing
import requests
import config

PHP_PWD = "./web/php/"

def _php_start_server():
	sp.run("php -S localhost:"+str(config.PHP_PORT)+" -t "+str(PHP_PWD), shell=True)

def _php_test_server():
	try:
		requests.get("http://localhost:"+str(config.PHP_PORT), verify=False, timeout=1)
		return True
	except:
		return False

def php_init(process=True):
	if config.PHP_ENABLE:
		if not _php_test_server():
			if not process:
				_php_start_server()
			else:
				p = multiprocessing.Process(target=_php_start_server)
				p.daemon = True
				p.start()

# if __name__ == '__main__':
# 	php_init()