class Task_data(object):
	def __init__(self):
		super().__init__()
		self.status = False
	
	def set_status(self, status:bool):
		self.status = status
	
	def start_service(self):
		from src.task import task
		return task.start_service()

	def stop_service(self):
		from src.task import task
		return task.stop_service()