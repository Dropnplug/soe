import flask as fl
import os
import sys

ROUTES_PWD = "./web/routes"

def import_routes(pwd=ROUTES_PWD):
	res_path = str(os.path.realpath(pwd))
	res_path_comp = len(str(res_path).split(os.sep))-2
	for root, _, files in os.walk(res_path):
		for item in files:
			fileNamePath = str(os.path.join(str(root),str(item)))
			if fileNamePath.find("__") == -1 and fileNamePath.endswith(".py"):
				fileNamePath = str(fileNamePath)[:-3].split(os.sep)[res_path_comp:]
				try:
					lib_import_path = ".".join(str(e) for e in fileNamePath)
					__import__(lib_import_path)
				except:
					lib_import_path = "./"+"/".join(str(e) for e in fileNamePath[:-1])
					sys.path.insert(0, lib_import_path)
					__import__(fileNamePath[-1])
					del sys.path[0]