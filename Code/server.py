import socket
from threading import *
import threading

#Initializing server socket....
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Initialize server ip and port#

serv_port = 1234
serv_host = "localhost"

print("Initializing server..... \n IP: localhost \n Port#: 1234")


#Bind serve_socket and listen for connections
serv_socket.bind((serv_host, serv_port)) 
serv_socket.listen(10)
client_list=[]
client_names =[]

def receive_send(client):

    #Gives list of currently connected users
    clientstrnames = ""
    for i in range(len(client_names)):
        if i == 0:
            clientstrnames = client_names[i]
        else:
            clientstrnames = clientstrnames +", " + client_names[i]

    client.send("Connected Users: ".encode())
    client.send(clientstrnames.encode())

    
    #Receives message from client and sends to all other clients
    while True:
            try:     
                message = client.recv(2048)
                broadcast(message)
                
                
            except:
                #remove client from lists and close connection if client exited/error
                listindex = client_list.index(client)
                nameofclient = client_names[listindex]
                broadcast(f"{nameofclient} has left the server".encode())
                client.close()

                client_names.remove(nameofclient)
                client_list.remove(client)
                
                break
                
#Send message to all clients
def broadcast(message):
    for client in client_list:
            try:
                client.send(message)
            except:
                client.close()




def intialize_server():
    while True:
        client,address = serv_socket.accept()

        #add client address to list
        print(address, " connected")
        client_list.append(client)

        #get a name to call the client that isnt address
        client.send("name".encode())
        name = client.recv(1024).decode()
        client_names.append(name)
        if client_names == []:
            pass
        else:
            print(client_names)
        broadcast(f"{name} has connected to the server".encode())
        print("You are now able to chat!")

        thread = threading.Thread(target=receive_send, args=((client,)))
        thread.start()

#run server
print("Server is running.....")
intialize_server()


#Start infinite loop

