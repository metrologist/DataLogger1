import time
import sqlite3
import VSL

dbname='sensorsData.db'
sampleFreq = 2 # time in seconds

# get data from VSL sensor
def getVSLdata():	
	temp, hum = VSL.vsl_reading()
	logData (temp, hum)
		
# log sensor data on database
def logData (temp, hum):	
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO VSL_data values(datetime('now'), (?), (?))", (temp, hum))
	conn.commit()
	conn.close()
	
# display database data
def displayData():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	print ("\nEntire database contents:\n")
	for row in curs.execute("SELECT * FROM VSL_data"):
		print (row)
	conn.close()
	
# main function
def main():
	for i in range (0,3):
		getVSLdata()
		time.sleep(sampleFreq)
	displayData()
# Execute program 
main()