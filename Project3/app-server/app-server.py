from socket import *
import sys


#	connect			
dsPort = int( sys.argv[ 1 ] )
serverSocket = socket( AF_INET, SOCK_STREAM )
#	this sets server to a random port assigned by the OS
serverSocket.bind( ( '', 0 ) )
serverSocket.listen( 1 )
serverName = gethostbyname( gethostname() )
#	print ip address and port number to console
print serverName, serverSocket.getsockname()[1]
#	establish TCP connection with dir-server
dirServerSocket = socket( AF_INET, SOCK_STREAM )
dirServerSocket.connect(( 'apollo.cselabs.umn.edu', dsPort ))
#	send register message
registerMessage = "register " + serverName + ' ' + str( serverSocket.getsockname()[1] ) + '\r\n'
dirServerSocket.send( registerMessage )
response = dirServerSocket.recv( 1024 )
#	print response from dir-server
print response
dirServerSocket.close()

while 1:
	#	connect with app-client
	connectionSocket, addr = serverSocket.accept()
	#	get upload messages for 10KB file, 5 loops because receive 5 times
	for i in range( 5 ):
		upload = connectionSocket.recv( 10000 )
		while( len( upload ) < 10000 ):
			upload += connectionSocket.recv( 10000 )
		connectionSocket.send( 'application server received ' + str( len( upload ) ) + ' bytes' )
	#	print received messages
	print "received " + str( len( upload ) )
	#	write received messages to file
	with open( '10KB-new', 'w' ) as f:
		f.write( upload )
	#	get upload messages for 100KB file
	for i in range( 5 ):
		upload = connectionSocket.recv( 100000 )
		while( len( upload ) < 100000 ):
			upload += connectionSocket.recv( 100000 )
		connectionSocket.send( 'application server received ' + str( len( upload ) ) + ' bytes' )
	#	print received messages
	print "received " + str( len( upload ) )
	#	write received messages to file
	with open( '100KB-new', 'w' ) as f:
		f.write( upload )
	#	get upload messages for 1000KB file
	for i in range( 5 ):
		upload = connectionSocket.recv( 1000000 )
		while( len( upload ) < 1000000 ):
			upload += connectionSocket.recv( 1000000 )
		connectionSocket.send( 'application server received ' + str( len( upload ) ) + ' bytes' )
	#	print received messages
	print "received " + str( len( upload ) )
	#	write received messages to file
	with open( '1000KB-new', 'w' ) as f:
		f.write( upload )
	#	get upload messages for 10000KB file
	for i in range( 5 ):
		upload = connectionSocket.recv( 10000000 )
		while( len( upload ) < 10000000 ):
			upload += connectionSocket.recv( 10000000 )
		connectionSocket.send( 'application server received ' + str( len( upload ) ) + ' bytes' )
	#	print received messages
	print "received " + str( len( upload ) )
	#	write received messages to file
	with open( '10000KB-new', 'w' ) as f:
		f.write( upload )
	connectionSocket.close()
