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
fullclient_list=[]
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
                message = client.recv(2048).decode()
                wordmessage = message.split()

                if wordmessage[2] == "-message":

                    client_name = wordmessage[3]
                    print("messaging: ", client_name)
                    
                    if client_name in client_names:
                        clientindex = client_names.index(client_name)
                        print(clientindex)
                        privatemsglist = [fullclient_list[clientindex]]
                        print(privatemsglist)
                        message =f"Private Message from{wordmessage[0]}:  \n " + "".join(wordmessage[4:])
                        broadcast(message.encode(),privatemsglist)
                    else:
                        print("Error: Client not in list, message has not been sent")

                else:
                    broadcast(message.encode(),fullclient_list)
                
                
            except:
                #remove client from lists and close connection if client exited/error
                listindex = fullclient_list.index(client)
                nameofclient = client_names[listindex]
                broadcast(f"{nameofclient} has left the server".encode(), fullclient_list)
                client.close()

                client_names.remove(nameofclient)
                fullclient_list.remove(client)
                
                break
                
#Send message to all clients
def broadcast(message,client_list):
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
        fullclient_list.append(client)

        #get a name to call the client that isnt address
        client.send("name".encode())
        name = client.recv(1024).decode()
        client_names.append(name)
        if client_names == []:
            pass
        else:
            print(client_names)
        broadcast(f"{name} has connected to the server".encode(),fullclient_list)
        print("You are now able to chat!")

        thread = threading.Thread(target=receive_send, args=((client,)))
        thread.start()

#run server
print("Server is running.....")
intialize_server()


#Start infinite loop

