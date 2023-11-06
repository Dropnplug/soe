import os
from .mods import MODS_PWD, WEB_PWD, WEB_DIRS, get_page_dir, PAGES_DIRS

def mods_web_data_update():
	web_path = str(os.path.realpath(WEB_PWD))
	res_path = str(os.path.realpath(MODS_PWD))
	for root, dirs, files in os.walk(res_path):
		for dir in dirs:
			dirNamePath = str(os.path.join(str(root),str(dir)))
			dirPathList = dirNamePath.split(os.sep)
			if dirPathList[-1] in WEB_DIRS and dirPathList[-2] == "web" and dirPathList[-4] in MODS_PWD:
				for in_root, _, in_files in os.walk(dirNamePath):
					for in_file in in_files:
						fileNamePath = str(os.path.join(str(in_root),str(in_file)))
						web_fileNamePath = str(web_path+"/"+dirPathList[-1]+"/mods/"+dirPathList[-3]+"/"+fileNamePath[len(root)+len(dirPathList[-1])+2:])
						mod_file_read = None
						web_file_read = None
						try:
							with open(fileNamePath, 'r') as mod_file:
								mod_file_read = mod_file.read()
							try:
								with open(web_fileNamePath, 'r') as web_file:
									web_file_read = web_file.read()
								if mod_file_read != web_file_read:
									with open(web_fileNamePath, 'w') as web_file:
										web_file.write(mod_file_read)
							except:
								with open(web_fileNamePath, 'a') as web_file:
										web_file.write(mod_file_read)
						except:
							pass
		for file in files:
			fileNamePath = str(os.path.join(str(root),str(file)))
			filePathList = fileNamePath.split(os.sep)
			page_pwd = get_page_dir(filePathList)
			if page_pwd is not None:
				for k, v in PAGES_DIRS.items():
					if file.endswith(k):
						web_fileNamePath = WEB_PWD+"/"+v+"/"+page_pwd
						mod_file_read = None
						web_file_read = None
						try:
							with open(fileNamePath, 'r') as mod_file:
								mod_file_read = mod_file.read()
							try:
								with open(web_fileNamePath, 'r') as web_file:
									web_file_read = web_file.read()
								if mod_file_read != web_file_read:
									with open(web_fileNamePath, 'w') as web_file:
										web_file.write(mod_file_read)
							except:
								with open(web_fileNamePath, 'a') as web_file:
										web_file.write(mod_file_read)
						except:
							pass
