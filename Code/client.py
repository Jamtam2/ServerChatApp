import socket
from threading import *
import threading
 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Please enter your name: ")
name = input()

client_socket.connect(("localhost", 1234))
 
def receive_messages():
    while True: 
        try: 
            message = client_socket.recv(1024).decode()
            if message == "name":
                client_socket.send(name.encode())
            else:
                print(message)
        except:
            print("Error, closing connection! Sorry!")
            client_socket.close()
            break

def send_messages():
    while True:
        sent_msg = f"[{name}] - {input()}" 
        client_socket.send(sent_msg.encode())

read_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)

read_thread.start()
send_thread.start()

