import socket
from threading import *
import threading

#Initializing server socket....
serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Initialize server ip and port#

print("Initializing server..... \n IP: localhost \n Port#: 1234")


#Bind serve_socket and listen for connections
serv_socket.bind(("localhost", 1234)) 
serv_socket.listen(10)
list_of_clients=[]
names_of_clients = []

def receive_send_client(client):

    #Gives list of currently connected users
    clientstrnames = ""
    for i in range(len(names_of_clients)):
        if i == 0:
            clientstrnames = names_of_clients[i]
        else:
            clientstrnames = clientstrnames +", " + names_of_clients[i]

    client.send("Connected Users: ".encode())
    client.send(clientstrnames.encode())

    
    #Receives message from client and sends to all other clients
    while True:
            try:     
                message = client.recv(2048)
                broadcast(message)
                
                
            except:
                #remove client from lists and close connection if client exited/error
                listindex = list_of_clients.index(client)
                nameofclient = names_of_clients[listindex]
                broadcast(f"{nameofclient} has left the server".encode())
                client.close()

                names_of_clients.remove(nameofclient)
                list_of_clients.remove(client)
                
                break
                
#Send message to all clients
def broadcast(message):
    for client in list_of_clients:
            try:
                client.send(message)
            except:
                client.close()




def receive():
    while True:
        client,address = serv_socket.accept()

        #add client address to list
        print(address, " connected")
        list_of_clients.append(client)

        #get a name to call the client that isnt address
        client.send("name".encode())
        name = client.recv(1024).decode()
        names_of_clients.append(name)
        if names_of_clients == []:
            pass
        else:
            print(names_of_clients)
        broadcast(f"{name} has connected to the server".encode())
        print("You are now able to chat!")

        thread = threading.Thread(target=receive_send_client, args=((client,)))
        thread.start()

#run server
print("Server is running.....")
receive()


#Start infinite loop

