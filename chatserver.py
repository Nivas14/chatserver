import socket, select


def send(sock, message):

	for socket in connected_list:
		if socket != server_socket and socket != sock :
			try :
				socket.send(message)
			except :

				socket.close()
				connected_list.remove(socket)

if __name__ == "__main__":
	name=""

	record={}

	connections = []
	buffer = 4096
	port = 5001

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server_socket.bind(("127.0.0.1", port))
	server_socket.listen(10)


	connections.append(server_socket)

	print ("\33[32m \t\t\t\tSERVER WORKING \33[0m") 

	while 1:

		rList,wList,error_sockets = select.select(connections,[],[])

		for sock in rList:

			if sock == server_socket:

				sockfd, addr = server_socket.accept()
				name=sockfd.recv(buffer)
				connections_list.append(sockfd)
				record[addr]=""

				if name in record.values():
					sockfd.send("\r\33[31m\33[1m Username already taken!\n\33[0m")
					del record[addr]
					connections.remove(sockfd)
					sockfd.close()
					continue
				else:

					record[addr]=name
					print ("Client (%s, %s) connected" % addr," [",record[addr],"]")
					sockfd.send("\33[32m\r\33[1m Welcome to chat room. Enter 'bye bye' anytime to exit\n\33[0m")
					send(sockfd, "\33[32m\33[1m\r "+name+" joined the conversation \n\33[0m")

			else:

				try:
					data1 = sock.recv(buffer)

					data=data1[:data1.index("\n")]

					i,p=sock.getpeername()
					if data == "bye bye":
						msg="\r\33[1m"+"\33[31m "+record[(i,p)]+" left the conversation \33[0m\n"
						send_to_all(sock,msg)
						print ("Client (%s, %s) is offline" % (i,p)," [",record[(i,p)],"]")
						del record[(i,p)]
						connections.remove(sock)
						sock.close()
						continue

					else:
						msg="\r\33[1m"+"\33[35m "+record[(i,p)]+": "+"\33[0m"+data+"\n"
						send(sock,msg)

				except:
					(i,p)=sock.getpeername()
					send(sock, "\r\33[31m \33[1m"+record[(i,p)]+" left the conversation unexpectedly\33[0m\n")
					print ("Client (%s, %s) is offline (error)" % (i,p)," [",record[(i,p)],"]\n")
					del record[(i,p)]
					connections.remove(sock)
					sock.close()
					continue

	server_socket.close()
