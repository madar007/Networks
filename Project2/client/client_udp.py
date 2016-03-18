from socket import *
import sys
from ctypes import * 
import struct
import time

#	Message structure to be send and received in sockets
class Message( Structure ):
	_fields_ = [("enum", c_int),
				("cur-seq", c_int),
				("max-seq", c_int),
				("payload", c_char_p),
				("payload_len", c_int)]

def getMessageType( index ):
	if ( index == 1 ):
		return 'MSG_TYPE_GET'
	if ( index == 2 ):
		return 'MSG_TYPE_GET_ERR'
	if ( index == 3 ):
		return 'MSG_TYPE_GET_RESP'
	if ( index == 4 ):
		return 'MSG_TYPE_GET_ACK'
	if ( index == 5 ):
		return 'MSG_TYPE_FINISH'

#	Buffer size: Change this to change buffer size 
buffer_size = 256

serverName = sys.argv[ 1 ]
serverPort = int( sys.argv[ 2 ] )
fileName = sys.argv[ 3 ]
with open( fileName, 'wb' ) as fileWrite:
	fileWrite.write( '' )

clientSocket = socket( AF_INET, SOCK_DGRAM )

#	Send MSG_TYPE_GET to server
message = Message( 1, 0, 0, fileName, len( fileName ) )
format_ = "iii%dsi" % ( len( fileName ) )
packedMessage = struct.pack( format_, 1, 0, 0, fileName, len( fileName ) )
clientSocket.sendto( packedMessage, ( serverName, serverPort ) )

while 1:
	message = Message( 0, 0, 0, '', 0 )
	#	Receive message from ( MSG_TYPE_GET_RESP, MSG_TYPE_GET_ERR, MSG_TYPE_FINISH )
	data = clientSocket.recv( buffer_size + sizeof(message) )
	packedData = data
	#	Unpack message
	(i,), data = struct.unpack("I", data[:4]), data[4:]
	(i,), data = struct.unpack("I", data[:4]), data[4:]
	(i,), data = struct.unpack("I", data[-4:]), data[:-4]
	format_ = 'iii' + str( i ) + 'si'
	unpackedData = struct.unpack( format_ , packedData )
	cmd = getMessageType( unpackedData[ 0 ] )
	curSeq = unpackedData[ 1 ] 
	print 'client: RX', str( cmd ), str( curSeq ), str( unpackedData[2] ), str( unpackedData[4] )
	
	#	Received MSG_TYPE_FINISH from server, close socket. 
	if( unpackedData[ 0 ] == 5 ):
		clientSocket.close()
		break
	
	#	Received MSG_TYPE_GET_ERR from server, close socket.
	if( unpackedData[ 0 ] == 2 ):
		clientSocket.close()
		break
	
	#	Received MSG_TYPE_GET_RESP, write the payload to file 
	with open( fileName, 'ab' ) as fileWrite:
		fileWrite.write( unpackedData[ 3 ] )
	
	#	Send MSG_TYPE_GET_ACK to server
	format_ = 'iiisi'
	packedMessage = struct.pack( format_, 4, curSeq, 0, '', 1 )
	clientSocket.sendto( packedMessage, ( serverName, serverPort ) )

clientSocket.close()

