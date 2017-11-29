# Group 1
## FoodieVision
### Jason Elting
### Clayton Horstman
### Noah Taylor
### Kyle Weinle

# FoodieVision-Server/
	client-api/ : folder containing python flask API and database interface
		API.py : Application programing interface to use with the andorid application in Foodlife/FoodieVision-Client
		foodiedb.py : Database Interface to bridge the API and the mysql database
		seefood.py : Python wrapper for SeeFood AI
		samplepost : A sample post request of what should be sent to the API from the android app or any other application
	DB/ : sql scripts to set up mysql databases for use with foodiedb.py
		db_procs.sql : defines procedures used by the database
		tables.sql : defines tables used by the database
# FoodieVision-Client/
	android-studio project of the FoodieVision android application
