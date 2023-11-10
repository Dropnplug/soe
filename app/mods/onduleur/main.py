import time
from src.memo import memo
from .src.Onduleurs_data import Onduleurs_data, Onduleurs

from src.task import task, REPEAT_TASK_ON_TIMER
from .src.tasks.update_db import update_db

import mods.onduleur.config as config

if not memo["onduleurs_data"]:
	memo["onduleurs_data"] = Onduleurs_data()
	Onduleurs().start()

memo["onduleurs_data"].ajouterOnduleurs(_timeout=10)
task.add(REPEAT_TASK_ON_TIMER(60, config.UPDATE_DB), name="onduleurs_update_db", replace=True)

# memo["onduleurs_data"].majAllDataBdd(_timeout=100)

# time.sleep(2)
# print("salut", memo["onduleurs_data"].execOnduleur("d8:10:9f:db:84:b3", 0, "getNom",  _timeout=10))
# print("salut", memo["onduleurs_data"].execOnduleur("d8:10:9f:db:84:b3", 0, "getToutesLesDonneesBDD", _timeout=10))
