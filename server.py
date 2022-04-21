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
            pass
        if cmd == "DLT":
            pass
        if cmd == "RDT":
            pass
        if cmd == "EDT":
            pass
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
        THREADS.append(title)

        udp_send(serverSocket, 'thread created', self.clientAddress)
    
    def do_list(self):
        if not THREADS:
            udp_send(serverSocket, 'no active threads', self.clientAddress)
            return
        
        threads = ' '.join(THREADS)
        udp_send(serverSocket, threads, self.clientAddress)


CLIENTS = {}
THREADS = []

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