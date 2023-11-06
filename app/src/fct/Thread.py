import sys
import trace
import threading
import time

#stopable thread

class Thread(threading.Thread):
	def __init__(self, *args, **keywords):
		self.parent = threading.current_thread()
		threading.Thread.__init__(self, *args, **keywords)
		self.killed = False
		self.daemon = False
	
	def start(self):
		self.__run_backup = self.run
		self.run = self.__run
		threading.Thread.start(self)
	
	def __run(self):
		sys.settrace(self.globaltrace)
		self.__run_backup()
		self.run = self.__run_backup
	
	def globaltrace(self, frame, event, arg):
		if event == 'call':
			return self.localtrace
		else:
			return None
	
	def localtrace(self, frame, event, arg):
		if self.killed:
			if event == 'line':
				raise SystemExit()
		return self.localtrace
	
	def terminate(self):
		self.killed = True