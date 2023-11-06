from src.memo import memo
from .src.Onduleurs_data import Onduleurs_data, Onduleurs


if not memo["onduleurs_data"]:
	memo["onduleurs_data"] = Onduleurs_data()
	Onduleurs().start()