#!/usr/bin/python

###############################################
#	parse user's options from Argv
#	Argv information to Brute Forcing object
#	Best analysis options for using?
#	automatically something, optional options
#
#############################################3

import sys, actions, httpbrute, utils, time

srcUsrList = 'userlist.txt'
srcPassList = 'passlist.txt'
varTargetURL = ''

infUserOptions = '''
Target: TARGETURL
userlist: DEFAULT
passlist: DEFAULT
'''
################################
#	Parsing user's arguments
#	Gathering options
#
################################

if len(sys.argv) == 1:
	##############################
	#	If there is no options:
	#	print help and show how to use this script
	##############################
	utils.print_help()
	sys.exit(0)

elif len(sys.argv) == 2:
	######################
	#	if there is an options:
	#	need help or run script automatically
	######################
	if sys.argv[1] == '-h' or sys.argv[1] == '--help':
		utils.print_help()
		sys.exit(0)
	else:
		varTargetURL = sys.argv[1]
		#############################################
		#	open file here -> no delay for print help
		#############################################
		userlist = actions.actionGetFileData(srcUsrList)
		passlist = actions.actionGetFileData(srcPassList)

else:
	###########################################
	#	Get user options
	#	User option will replace default option
	#	**NEED IMPROVE**
	#
	###########################################

	userlist = actions.actionGetFileData(srcUsrList)
	passlist = actions.actionGetFileData(srcPassList)
	try:
		"if len(sys.argv) %2 != 0: Error arguments?"
		idxArgOpt = 1
		while idxArgOpt < len(sys.argv):
			if sys.argv[idxArgOpt] == '-U':
				userlist = actions.actionGetListData(sys.argv[idxArgOpt + 1])
				infUserOptions = infUserOptions.replace("userlist: DEFAULT", "userlist: %s" %(userlist))
				idxArgOpt += 1
			elif sys.argv[idxArgOpt] == '-u':
				userlist = actions.actionGetFileData(sys.argv[idxArgOpt + 1])
				infUserOptions = infUserOptions.replace("userlist: DEFAULT", "userlist: %s" %(sys.argv[idxArgOpt + 1]))
				idxArgOpt += 1
			elif sys.argv[idxArgOpt] == '-p':
				infUserOptions = infUserOptions.replace("passlist: DEFAULT", "passlist: %s" %(sys.argv[idxArgOpt + 1]))
				passlist = actions.actionGetFileData(sys.argv[idxArgOpt + 1])
				idxArgOpt += 1
			else:
				varTargetURL = sys.argv[idxArgOpt]
			idxArgOpt += 1
	except:
		sys.exit(utils.craft_msg("Parsing arguments error", "bad"))

##########################
#	CHECK REQUIRED OPTIONS
#
##########################

if not varTargetURL:
	sys.exit(utils.craft_msg("An URL is required", "bad"))

###########################################
#	print option information before running
###########################################
infUserOptions = infUserOptions.replace('TARGETURL', varTargetURL)
print(infUserOptions)


try:
	#	create object
	processBruteForcing = httpbrute.BruteForcing(varTargetURL, userlist, passlist)

	utils.printf("Starting...\n")
	timeStarting = time.time()

	# Calling method
	processBruteForcing.run()

except KeyboardInterrupt:
	utils.printf("Terminated!!!", "bad")

except:
	utils.printf("Error while running", "bad")

finally:
	############################################
	#	Get result
	#
	############################################

	try:
		creds = processBruteForcing.actGetResult()

		#	check result
		if len(creds) == 0:
			utils.printf("Password not found!", "bad")
		else:
			utils.printf("")
			utils.print_table(("Username", "Password"), *creds)
	except:
		utils.printf("\nError while getting result\n", "bad")

	utils.printf("\nCompleted. Run time: %0.5s [s]\n" %(time.time() - timeStarting), "good")

	########################################
	#	Clean resources
	#
	########################################

	try:
		passlist.close()
	except:
		pass
	try:
		userlist.close()
	except:
		pass

	sys.exit(0)