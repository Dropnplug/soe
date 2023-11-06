import os
import shutil
from src.memo import memo


MODS_PWD = "./mods"
WEB_PWD = "./web"
WEB_DIRS = ["php", "routes", "static", "templates"]

PAGES_DIRS = {
	".html":"templates/mods",
	".py":"routes/mods",
	".js":"static/mods",
	".css":"static/mods"
}

STATIC_DIRS = {
	".js":"js",
	".css":"css"
}

def get_page_dir(path_list):
	for i in range(0, len(path_list)):
		if i > 3:
			if path_list[i] == "pages" and path_list[i-1] == "web" and path_list[i-3] == "mods":
				for k, v in STATIC_DIRS.items():
					if path_list[-1].endswith(k):
						return "/".join([path_list[i-2], "pages", STATIC_DIRS[k]]+path_list[i+1:])
				return "/".join([path_list[i-2], "pages"]+path_list[i+1:])
	return None

def import_mods(mods_pwd=MODS_PWD, web_pwd=WEB_PWD):
	web_path = str(os.path.realpath(web_pwd))
	for dir in WEB_DIRS:
		try:
			mod_path = web_path+"/"+dir+"/mods"
			if os.path.exists(mod_path):
				shutil.rmtree(mod_path)
			os.makedirs(mod_path)
		except Exception as e:
			pass
	res_path = str(os.path.realpath(mods_pwd))
	res_path_comp = len(str(res_path).split(os.sep))-1
	for root, dirs, files in os.walk(res_path):
		for dir in dirs:
			dirNamePath = str(os.path.join(str(root),str(dir)))
			dirPathList = dirNamePath.split(os.sep)
			if len(dirPathList) >= 4:
				if dirPathList[-1] in WEB_DIRS and dirPathList[-2] == "web" and dirPathList[-4] in mods_pwd:
					try:
						shutil.copytree(dirNamePath, web_path+"/"+dirPathList[-1]+"/mods/"+ dirPathList[-3])
						memo["mods_data"].import_web(dirPathList[-3], dirPathList[-1])
					except Exception as e:
						print(e)
						pass

		for file in files:
			fileNamePath = str(os.path.join(str(root),str(file)))
			filePathList = fileNamePath.split(os.sep)
			if len(dirPathList) >= 3:
				if filePathList[-1] == "main.py" and filePathList[-3] in mods_pwd:
					fileNamePath = str(fileNamePath)[:-3].split(os.sep)[res_path_comp:]
					lib_import_path = ".".join(str(e) for e in fileNamePath)
					__import__(lib_import_path)
					memo["mods_data"].import_main(filePathList[-2])
			page_pwd = get_page_dir(filePathList)
			if page_pwd is not None:
				for k, v in PAGES_DIRS.items():
					if file.endswith(k):
						os.makedirs(os.path.dirname(web_pwd+"/"+v+"/"+page_pwd), exist_ok=True)
						shutil.copyfile(fileNamePath, web_pwd+"/"+v+"/"+page_pwd)