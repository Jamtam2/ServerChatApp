import socket
from threading import *
import threading
from sys import exit

 

print("Please enter your name: ")
name = input()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_port = 1234
client_host = "localhost"

client_socket.connect((client_host, client_port))

 
def receive_messages():
    while True: 
        try: 
            message = client_socket.recv(1024).decode()
            if message == "name":
                client_socket.send(name.encode())
            else:
                print(message)
        except:
            print("Closing connection!")
            client_socket.close()
            exit(0)

def send_messages():
    while True:
        msg = input("")
        if msg == ".exit":
            print("Closing connection")
            client_socket.close()
            exit(0)
        else:
            sent_msg = f"[{name}] - {msg}\n" 
            client_socket.send(sent_msg.encode())

read_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

read_thread.start()
send_thread.start()