from socket import *
import sys
from ctypes import *
import struct
import string

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

#	connect	
serverPort = int( sys.argv[ 1 ] )
serverSocket = socket( AF_INET, SOCK_DGRAM )
serverSocket.bind( ( '', serverPort ) )
print 'The server is ready to receive'

message = Message( 0, 0, 0, '', 0 )
while 1:
	#	receive MSG_TYPE_GET 
	data, clientSocket = serverSocket.recvfrom( sizeof( message ) )
	#	unpack message
	packedData = data
	(i,), data = struct.unpack("I", data[:4]), data[4:]
	(i,), data = struct.unpack("I", data[:4]), data[4:]
	(i,), data = struct.unpack("I", data[-4:]), data[:-4]
	format_ = 'iii' + str( i ) + 'si'
	unpackedData = struct.unpack( format_ , packedData )
	cmd = getMessageType( unpackedData[0] )
	curSeq = unpackedData[1]
	maxSeq = unpackedData[2]
	fileName = unpackedData[ 3 ]
	payloadLen = unpackedData[4]
	print 'server: RX', str( cmd ), str( curSeq ), str( maxSeq ), str( payloadLen )
	if ( cmd == 'MSG_TYPE_GET' ):
		#	Send MSG_TYPE_GET_ERR in except if can't find file
		try:
			curSeq = 0
			maxSeq = 0
			with open( fileName, 'rb' ) as f:
				maxSeq = len( f.read() ) / buffer_size
			with open( fileName, 'rb' ) as f:
				#	read contents
				content = f.read( buffer_size )
				format_ = 'iii' + str( len( content ) ) + 'si'
				#	pack message and send
				packedMessage = struct.pack( format_, 3, curSeq, maxSeq, content, len( content ) )
				serverSocket.sendto( packedMessage, clientSocket )
				#	receive MSG_TYPE_GET_ACK message
				data = serverSocket.recv( sizeof( message ) )
				packedData = data
				(i,), data = struct.unpack("I", data[:4]), data[4:]
				(i,), data = struct.unpack("I", data[:4]), data[4:]
				(i,), data = struct.unpack("I", data[-4:]), data[:-4]
				format_ = 'iii' + str( i ) + 'si'
				unpackedData = struct.unpack( format_ , packedData )
				cmd = getMessageType( unpackedData[0] )
				fileName = unpackedData[ 3 ]
				payloadLen = unpackedData[4]
				print 'server: RX', str( cmd ), str( curSeq ), str( maxSeq ), str( payloadLen )
				curSeq += 1
				#	if there is more content to read, read and send it
				while( len( content ) == buffer_size ):
					content = f.read( buffer_size )
					format_ = 'iii' + str( len( content ) ) + 'si'
					packedMessage = struct.pack( format_, 3, curSeq, maxSeq, content, len( content ) )
					serverSocket.sendto( packedMessage, clientSocket )
					data = serverSocket.recv( buffer_size + sizeof( message ) )
					cmd = getMessageType( unpackedData[0] )
					fileName = unpackedData[ 3 ]
					payloadLen = unpackedData[4]
					print 'server: RX', str( cmd ), str( curSeq ), str( maxSeq ), str( payloadLen )
					curSeq += 1
				# 	Send MSG_TYPE_FINISH
				format_ = 'iiisi'
				packedMessage = struct.pack( format_, 5, curSeq, maxSeq, '', 1 )
				serverSocket.sendto( packedMessage, clientSocket )
				serverSocket.close()
				break
		except IOError as e:
			#	Send MSG_TYPE_GET_ERR
			format_ = 'iiisi'
			packedMessage = struct.pack( format_, 2, 0, 0, '', 1 )
			serverSocket.sendto( packedMessage, clientSocket )
			serverSocket.close()
			break
			

