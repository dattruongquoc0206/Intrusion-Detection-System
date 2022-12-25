import socket
import pandas as pd
import sys
from sklearn.tree import DecisionTreeClassifier

file_name="Data.txt"

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #open file
    #send 
    file1 = open(file_name, 'r')
    Lines = file1.readlines()
    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        print("Line{}: {}".format(count, line.strip()))
        #data="Line{}: {}".format(count, line.strip())
        s.send(file1[line].encode('utf-8'))
    file1.close()

s.close()
print(f"[DISCONNECTED]  disconnected.")