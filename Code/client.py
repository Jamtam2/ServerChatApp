import socket
import select
import sys
 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Enter the server IP Address: ")
client_host = input()

print("Enter the server Port # ")
client_port = int(input())

client_socket.connect((client_host, client_port))
 
while True:
 
    # maintains a list of possible input streams
    sockets_list = [socket.socket(), client_socket]
 
    """ There are two possible input situations. Either the
    user wants to give manual input to send to other people,
    or the server is sending a message to be printed on the
    screen. Select returns from sockets_list, the stream that
    is reader for input. So for example, if the server wants
    to send a message, then the if condition will hold true
    below.If the user wants to send a message, the else
    condition will evaluate as true"""
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
 
    for socks in read_sockets:
        if socks == client_socket:
            message = socks.recv(2048)
            print (message)
        else:
            message = input()
            client_socket.send(message)
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()