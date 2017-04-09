if __name__ == "__main__":
	print("---------------------------------------------------")
	print("----------------Mabi Server Setup------------------")
	print("---------------------------------------------------")
	print("---------------------------------------------------")
	print("---------------------------------------------------")
	print("---------------------------------------------------")

	dbName = raw_input("What database do you want to use (default mabi)? ")
	user = raw_input("What user do you want to use (default root)? ")
	passwd = raw_input("What is your mysql users password (default '')?" )
	host = raw_input("What host would you like to use (default localhost)? ")

	if dbName == None:
		dbName = "mabi"
	if user == None:
		user = "root"
	if passwd == None:
		passwd = ""
	if host == None:
		host = "localhost"	
