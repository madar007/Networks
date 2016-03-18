from socket import *
import sys

		
serverPort = int( sys.argv[ 1 ] ) 	
serverSocket = socket( AF_INET, SOCK_STREAM )
serverSocket.bind( ( '', serverPort ) )
#	start listening TCP connections on dsport
serverSocket.listen( 1 )

#	start of response message for list-servers
listOfServers = 'success\r'

while 1:
	connectionSocket, addr = serverSocket.accept()
	registerMessage = connectionSocket.recv( 1024 )
	registerMessageList = registerMessage.split( " " )
	#	print received messages
	print registerMessage
	#	app-server register itself
	if( registerMessageList[ 0 ] == 'register' ):
		ipAddr = registerMessage.split( " " )[ 1 ]
		portNo = registerMessage.split( " " )[ 2 ][:-2] # removed last two chars '\r\n'
		#	add to list of servers
		listOfServers += ipAddr + ' ' + portNo + '\r'
		#	response to app-server
		if( ipAddr != None and portNo.isdigit() ):
			connectionSocket.send( "success\r\n" )
		else:
			connectionSocket.send( "failure\r\n" )
		connectionSocket.close()
	#	app-client request list of servers
	elif( registerMessageList[ 0 ] == 'list-servers\r\n' ):
		#	response for app-client
		if( type( listOfServers ) == str ):
			connectionSocket.send( listOfServers + '\n' )
		else:
			connectionSocket.send( 'failure\r\n' )
		connectionSocket.close()
