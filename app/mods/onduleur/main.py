from src.memo import memo
from .src.Onduleurs_data import Onduleurs_data, Onduleurs


if not memo["onduleurs_data"]:
	memo["onduleurs_data"] = Onduleurs_data()
	Onduleurs().start()

memo["onduleurs_data"].ajouterOnduleurs()
import time
time.sleep(10)
print(memo["onduleurs_data"].execOnduleur("d8-10-9f-db-84-b3", "getNom"))