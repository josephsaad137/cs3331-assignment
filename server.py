from socket import *
from threading import Thread
import sys, select
from server_helpers import do_login
from state_info import *
from udp import udp_send, udp_recv

# acquire server host and port from command line parameter
if len(sys.argv) != 2:
    print("\n===== Error usage, python3 TCPServer3.py SERVER_PORT ======\n")
    exit(0)
serverHost = "127.0.0.1"
serverPort = int(sys.argv[1])
serverAddress = (serverHost, serverPort)

# define socket for the server side and bind address
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddress)

"""
    Define multi-thread class for client
    This class would be used to define the instance for each connection from each client
    For example, client-1 makes a connection request to the server, the server will call
    class (ClientThread) to define a thread for client-1, and when client-2 make a connection
    request to the server, the server will call class (ClientThread) again and create a thread
    for client-2. Each client will be runing in a separate therad, which is the multi-threading
"""
class ClientThread(Thread):
    def __init__(self, clientAddress):
        Thread.__init__(self)
        self.clientAddress = clientAddress
        #self.clientSocket = clientSocket
        self.clientAlive = False
        self.clientName = None
        
        print("===== New connection created for: ", clientAddress)
        self.clientAlive = True
        
    # def run(self):
    #     message = ''
        
    #     while self.clientAlive:
    #         # use recv() to receive message from the client
    #         data, address = serverSocket.recvfrom(1024)
    #         message = data.decode()
            
    #         # if the message from client is empty, the client would be off-line then set the client as offline (alive=Flase)
    #         if message == '':
    #             self.clientAlive = False
    #             print("===== the user disconnected - ", clientAddress)
    #             break

    """
        You can create more customized APIs here, e.g., logic for processing user authentication
        Each api can be used to handle one specific function, for example:
        def process_login(self):
            message = 'user credentials request'
            self.clientSocket.send(message.encode())
    """
    def process_login(self):
        username = do_login(serverSocket)
        if username:
            self.clientName = username
    
    def process_msg(self, msg):
        if msg == 'login':
            print("[recv] New login request")
            self.process_login()
            return
        
        print("[recv] " + msg)
        words = msg.strip().split(" ")
        cmd = words[0]

        if cmd == "CRT":
            self.do_create(words[1])
        if cmd == "LST":
            self.do_list()
        if cmd == "MSG":
            msg = ' '.join(words[2:])
            self.do_msg(words[1], msg)
        if cmd == "DLT":
            pass
        if cmd == "RDT":
            self.do_read(words[1])
        if cmd == "EDT":
            msg = ' '.join(words[3:])
            self.do_edit(words[1], words[2], msg)
        if cmd == "UPD":
            pass
        if cmd == "DWN":
            pass
        if cmd == "RMV":
            pass
        if cmd == "XIT":
            self.do_exit()
    
    def do_exit(self):
        ACTIVE_USERS.remove(self.clientName)
        CLIENTS.pop(self.clientAddress)

        message = "user has exited"
        print("[send] " + message)
        udp_send(serverSocket, message, self.clientAddress)
    
    def do_create(self, title):
        if title in THREADS:
            print("[send] thread already exists")
            udp_send(serverSocket, 'thread already exists', self.clientAddress)
            return
        
        f = open(title, 'w')
        f.write(self.clientName + '\n')
        f.close()
        details = {
            "msg_num": 1,
            "num_msgs": 0,
            "creator": self.clientName,
            "msgs": {}
        }
        THREADS[title] = details

        udp_send(serverSocket, 'thread created', self.clientAddress)
    
    def do_list(self):
        if not THREADS:
            udp_send(serverSocket, 'no active threads', self.clientAddress)
            return
        
        threads = ' '.join(THREADS.keys())
        udp_send(serverSocket, threads, self.clientAddress)
    
    def do_msg(self, title, msg):
        if title not in THREADS.keys():
            udp_send(serverSocket, "thread does not exist", self.clientAddress)
            return
        
        f = open(title, 'a')
        msg_num = THREADS[title]["msg_num"]
        f.write(str(msg_num) + " " + self.clientName + ": " + msg + "\n")
        f.close()
        THREADS[title]["msgs"][msg_num] = {
            "msg": msg,
            "author": self.clientName
        }
        THREADS[title]["msg_num"] += 1
        THREADS[title]["num_msgs"] += 1
        udp_send(serverSocket, "message sent", self.clientAddress)

    def do_read(self, title):
        if title not in THREADS.keys():
            udp_send(serverSocket, "thread does not exist", self.clientAddress)
            return
        
        f = open(title, 'r')
        f.readline()
        contents = f.read()
        f.close()
        udp_send(serverSocket, contents, self.clientAddress)
    
    def do_edit(self, title, msg_num, msg):
        if title not in THREADS.keys():
            udp_send(serverSocket, "thread does not exist", self.clientAddress)
            return
        
        if not int(msg_num) in THREADS[title]["msgs"].keys():
            udp_send(serverSocket, "message number not valid", self.clientAddress)
            return

        if not self.clientName == THREADS[title]["msgs"][int(msg_num)]["author"]:
            udp_send(serverSocket, "user not authorised", self.clientAddress)
            return
        
        f = open(title, 'r')
        contents = f.read()
        f.close()
        og_msg = msg_num + " " + self.clientName + ": " + THREADS[title]["msgs"][int(msg_num)]["msg"] + "\n"
        new_msg = msg_num + " " + self.clientName + ": " + msg + "\n"
        contents = contents.replace(og_msg, new_msg)
        f = open(title, 'w')
        f.write(contents)
        f.close()

        THREADS[title]["msgs"][int(msg_num)]["msg"] = msg
        udp_send(serverSocket, "message edited", self.clientAddress)


CLIENTS = {}
THREADS = {}

print("\n===== Server is running =====")
print("===== Waiting for connection request from clients...=====")


while True:
    # serverSocket.listen()
    # clientSockt, clientAddress = serverSocket.accept()
    # clientThread = ClientThread(clientAddress, clientSockt)
    # clientThread.start()
    data, address = serverSocket.recvfrom(1024)
    if address in CLIENTS:
        CLIENTS[address].process_msg(data.decode())
    else:
        clientThread = ClientThread(address)
        CLIENTS[address] = clientThread
        clientThread.start()
        clientThread.process_msg(data.decode())