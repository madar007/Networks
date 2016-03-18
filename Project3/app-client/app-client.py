from socket import *
import sys
import time

serverName = 'apollo.cselabs.umn.edu'
dsPort = int( sys.argv[ 1 ] )
dbPort = int( sys.argv[ 2 ] )
#	connect to dir-server
dirSocket = socket( AF_INET, SOCK_STREAM )
dirSocket.connect(( serverName, dsPort ))
#	request list of servers
listServersMessage = 'list-servers\r\n'
dirSocket.send( listServersMessage )
listOfServersReturnMessage = dirSocket.recv( 1024 )
listOfServersAndPorts = listOfServersReturnMessage.split( '\r' )
#	print response message from dir-server
for item in listOfServersAndPorts:
	print item

dirSocket.close()

#	for each server and port , do this
for serverAndPort in listOfServersAndPorts:
	if( serverAndPort == 'success' ):
		continue
	if( serverAndPort == '\n' or serverAndPort == '\r' ):		
		continue
	if( serverAndPort == '' ):
		continue
	lineSplit = serverAndPort.split( " " )
	#	connect to app-server
	clientSocket = socket( AF_INET, SOCK_STREAM )
	clientSocket.connect(( lineSplit[ 0 ], int( lineSplit[ 1 ] ) ))
	#	send 10KB file five times and record time taken
	with open( '10KB', 'r' ) as f:
		upload = f.read()
	totalUploadTime = 0
	for i in range( 5 ):
		start = time.time()
		clientSocket.send( upload )
		recMessage = clientSocket.recv( 1024 ) 
		end = time.time()
		uploadTime = end - start
		totalUploadTime += uploadTime
	print recMessage
	averageUploadTime = totalUploadTime / 5
	#	connect to db server and set-record of the average upload time taken
	dbSocket = socket( AF_INET, SOCK_STREAM )
	dbSocket.connect(( 'atlas.cselabs.umn.edu', dbPort ) )
	dbSocket.send( 'set-record ' + gethostbyname( gethostname() ) + ' ' + lineSplit[ 0 ] + ' ' + lineSplit[ 1 ] + ' 10 ' + str( averageUploadTime ) + '\r\n' )
	dbRec = dbSocket.recv( 1024 )
	dbSocket.close()
	print dbRec
	totalUploadTime = 0
	#	send 100KB file five times and record time taken
	with open( '100KB', 'r' ) as f:
		upload = f.read()
	for i in range( 5 ):
		start = time.time()
		clientSocket.send( upload )
		recMessage = clientSocket.recv( 1024 ) 
		end = time.time()
		uploadTime = end - start
		totalUploadTime += uploadTime
	print recMessage
	averageUploadTime = totalUploadTime / 5
	#	connect to db server and set-record of the average upload time taken
	dbSocket = socket( AF_INET, SOCK_STREAM )
	dbSocket.connect(( 'atlas.cselabs.umn.edu', dbPort ) )
	dbSocket.send( 'set-record ' + gethostbyname( gethostname() ) + ' ' + lineSplit[ 0 ] + ' ' + lineSplit[ 1 ] + ' 100 ' + str( averageUploadTime ) + '\r\n' )
	dbRec = dbSocket.recv( 1024 )
	dbSocket.close()
	print dbRec
	totalUploadTime = 0
	#	send 1000KB file five times and record time taken
	with open( '1000KB', 'r' ) as f:
		upload = f.read()
	for i in range( 5 ):
		start = time.time()
		clientSocket.send( upload )
		recMessage = clientSocket.recv( 1024 ) 
		end = time.time()
		uploadTime = end - start
		totalUploadTime += uploadTime
	print recMessage
	averageUploadTime = totalUploadTime / 5
	#	connect to db server and set-record of the average upload time taken
	dbSocket = socket( AF_INET, SOCK_STREAM )
	dbSocket.connect(( 'atlas.cselabs.umn.edu', dbPort ) )
	dbSocket.send( 'set-record ' + gethostbyname( gethostname() ) + ' ' + lineSplit[ 0 ] + ' ' + lineSplit[ 1 ] + ' 1000 ' + str( averageUploadTime ) + '\r\n' )
	dbRec = dbSocket.recv( 1024 )
	dbSocket.close()
	print dbRec
	totalUploadTime = 0
	#	send 10000KB file five times and record time taken
	with open( '10000KB', 'r' ) as f:
		upload = f.read()
	for i in range( 5 ):
		start = time.time()
		clientSocket.send( upload )
		recMessage = clientSocket.recv( 1024 ) 

		end = time.time()
		uploadTime = end - start
		totalUploadTime += uploadTime
	print recMessage
	averageUploadTime = totalUploadTime / 5
	#	connect to db server and set-record of the average upload time taken
	dbSocket = socket( AF_INET, SOCK_STREAM )
	dbSocket.connect(( 'atlas.cselabs.umn.edu', dbPort ) )
	dbSocket.send( 'set-record ' + gethostbyname( gethostname() ) + ' ' + lineSplit[ 0 ] + ' ' + lineSplit[ 1 ] + ' 10000 ' + str( averageUploadTime ) + '\r\n' )
	dbRec = dbSocket.recv( 1024 )
	dbSocket.close()
	print dbRec
	dbSocket = socket( AF_INET, SOCK_STREAM )
	dbSocket.connect(( 'atlas.cselabs.umn.edu', dbPort ) )
	dbSocket.send( 'get-records\r\n' )
	dbGetRecordLength = ''
	dbGetRecord = ''
	firstTime = True 
	while( firstTime or len( dbGetRecordLength ) == 1024 ): 
		dbGetRecordLength = dbSocket.recv( 1024 )
		dbGetRecord += dbGetRecordLength
		firstTime = False
	dbSocket.close()
	dbRecordsList = dbGetRecord.split( '\r' )
	for item in dbRecordsList:
		print item
	clientSocket.close()

	
