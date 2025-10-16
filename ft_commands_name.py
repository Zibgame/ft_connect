import os

def launch_command(nb):
	match nb:
		case 1:
			return xdg()

def xdg():
	print("please specify a file/website to open:")
	file_path = "/sgoinfre/goinfre/Perso/zcadinot/ft_connect/asset"
	asset_list = os.listdir(file_path)
	for files in asset_list:
		print(files)
	print("----")
	file = input()
	if len(file) >= 4 and file[0:4] == "http":
		return f"xdg-open {file}"
	elif file in asset_list:
		return f"~/../..{file_path}/{file}"
	else:
		print("not a valid argument")
		return 0