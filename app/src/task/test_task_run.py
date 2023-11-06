from src.task import task, REPEAT_TASK_ON_TICK, COUNT_TASK_ON_TICK, REPEAT_TASK_ON_TIMER, COUNT_TASK_ON_TIMER, RUN_TASK_ON_DATE, REPEAT_TASK_DAILY, COUNT_TASK_DAILY, REPEAT_TASK_WEEKLY, COUNT_TASK_WEEKLY, REPEAT_TASK_MONTHLY, COUNT_TASK_MONTHLY
import time

def test(stri):
	print(stri)

now = time.time()
local = time.localtime(now)
asc = str(time.asctime(local)).lower()
day = asc[:3]

if __name__ == '__main__':
	# task.add(REPEAT_TASK_ON_TICK(test, args=["REPEAT_TASK_ON_TICK"]), name="REPEAT_TASK_ON_TICK", replace=True)
	task.add(COUNT_TASK_ON_TICK(1, test, args=["COUNT_TASK_ON_TICK"]), name="COUNT_TASK_ON_TICK", replace=True)
	# task.add(REPEAT_TASK_ON_TIMER(10, test, args=["REPEAT_TASK_ON_TIMER"]), name="REPEAT_TASK_ON_TIMER", replace=True)
	task.add(COUNT_TASK_ON_TIMER(10, 1, test, args=["COUNT_TASK_ON_TIMER"]), name="COUNT_TASK_ON_TIMER", replace=True)
	task.add(RUN_TASK_ON_DATE(str(local.tm_year)+"-"+str(local.tm_mon)+"-"+str(local.tm_mday)+" "+str(local.tm_hour)+":"+str(format(local.tm_min+1, '02d'))+":11", test, args=["RUN_TASK_ON_DATE"]), name="RUN_TASK_ON_DATE", replace=True)
	task.add(REPEAT_TASK_DAILY(test, hour=local.tm_hour, min=local.tm_min+1, sec=11, args=["REPEAT_TASK_DAILY"]), name="REPEAT_TASK_DAILY", replace=True)
	task.add(COUNT_TASK_DAILY(1, test, hour=local.tm_hour, min=local.tm_min+1, sec=11, args=["COUNT_TASK_DAILY"]), name="COUNT_TASK_DAILY", replace=True)
	task.add(REPEAT_TASK_WEEKLY(test, day=day, hour=local.tm_hour, min=local.tm_min+1, sec=11, args=["REPEAT_TASK_WEEKLY"]), name="REPEAT_TASK_WEEKLY", replace=True)
	task.add(COUNT_TASK_WEEKLY(1, test, day=day, hour=local.tm_hour, min=local.tm_min+1, sec=11, args=["COUNT_TASK_WEEKLY"]), name="COUNT_TASK_WEEKLY", replace=True)
	task.add(REPEAT_TASK_MONTHLY(test, day=local.tm_mday, hour=local.tm_hour, min=local.tm_min+1, sec=11, args=["REPEAT_TASK_MONTHLY"]), name="REPEAT_TASK_MONTHLY", replace=True)
	task.add(COUNT_TASK_MONTHLY(1, test, day=local.tm_mday, hour=local.tm_hour, min=local.tm_min+1, sec=11, args=["COUNT_TASK_MONTHLY"]), name="COUNT_TASK_MONTHLY", replace=True)