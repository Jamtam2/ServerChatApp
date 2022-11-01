import socket
import select
from threading import *
import sys


serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
the first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain
with any two hosts
The second argument is the type of socket. SOCK_STREAM means that data or characters are read in a continuous flow
"""
serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print("Enter your IP Address: ")
serv_host = input()

print("Enter your Port # ")
client_port = int(input())


print("This is your IP: ",serv_host)
print("This is your port: ",client_port)
serv_socket.bind((serv_host, client_port)) 
#binds the server to an entered IP address and at the specified port number. The client must be aware of these parameters
serv_socket.listen(100)
#listens for 100 active connections. This number can be increased as per convenience
list_of_clients=[]

def clientthread(conn, addr):
    message = "WELCOME TO THE CHAT!"
    bytemessage=bytes(message,"utf-8")
    conn.send(bytemessage)
    #sends a message to the client whose user object is conn
    while True:
            try:     
                message = conn.recv(2048)    
                if message:
                    print("<" + addr[0] + "> " + message)
                    message_to_send = "<" + addr[0] + "> " + message
                    broadcast(message_to_send,conn)
                    #prints the message and address of the user who just sent the message on the server terminal
                else:
                    remove(conn)
            except:
                continue

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = serv_socket.accept()
    """
    Accepts a connection request and stores two parameters, conn which is a socket object for that user, and addr which contains
    the IP address of the client that just connected
    """
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    #maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    #Prints the address of the person who just connected
    clientthread(conn,addr)
    print("Type EXIT to close server")
    x = input()
    if (x=="EXIT"):
        serv_socket.close()
        conn.close()

    #creates and individual thread for every user that connects
    

