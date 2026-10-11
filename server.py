# citation: Referenced NeuralNines video "Secure Login System in Python" to construct this section

import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999)) # if we arent doing local, this is the private IP Address

server.listen()

def connection_control (client):
    client.send("Username: ".encode())  # take username input from user
    username = client.recv(1024).decode() # assign 1024 bytes from client to the username information
    client.send("Password: ".encode())  # take password input from user
    password = client.recv(1024).decode() # assign 1024 bytes from client to the password information

    # need to encrypt the connection between the server and the database

    # hashes the password so it can match to the database
    password = hashlib.sha256(password.encode()).hexdigest()

    conn = sqlite3.connect("login_information.db") #changed to users because create databases doesnt have login information
    cursor = conn.cursor()

    # requires protection from SQL injection
    cursor.execute("SELECT * FROM login_information WHERE username = ? AND password = ?", (username, password))

    if cursor.fetchall():
        print("Login accepted")
        client.send("login accepted".encode()) #changed from 'cursor' to 'client'

        # controls access to rest of calendar
        
    else:
        print("Login not accepted")
        client.send("invalid login".encode()) #changed from 'cursor' to 'client'


while True:
    client, address = server.accept()
    threading.Thread (target=connection_control, args=(client,)).start()