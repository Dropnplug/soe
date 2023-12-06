from src.memo import memo
from .Mods_data import Mods_data
from .mods import import_mods
# from src.task import task, REPEAT_TASK_ON_TIMER
from .mods_web_data_update import mods_web_data_update

import config

if not memo["mods_data"]:
	memo["mods_data"] = Mods_data()
	import_mods()
	from src.task import task, REPEAT_TASK_ON_TIMER
	if config.DEBUG:
		task.add(REPEAT_TASK_ON_TIMER(1, mods_web_data_update), name="MODS_WEB_DATA_UPDATE", replace=True)
	else:
		task.rm("MODS_WEB_DATA_UPDATE")