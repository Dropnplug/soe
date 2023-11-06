import datetime
import config

PRINT_LOGS = config.DEBUG
SAVE_LOGS = True
LOGS_FILE_PWD = "./data/logs/logs.txt"

def logs(*args, logs_print=PRINT_LOGS, logs_pwd=LOGS_FILE_PWD, **kwargs):
	if logs_print:
		print(*args, **kwargs)
	msg_args = []
	for ar in args:
		msg_args.append(str(ar))
	if SAVE_LOGS:
		time = datetime.datetime.now()
		msg = "["+time.strftime("%Y/%m/%d-%H:%M:%S")+"] "+" ".join(msg_args)+"\n"
		with open(logs_pwd, 'a') as f:
			f.write(msg)