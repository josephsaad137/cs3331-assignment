from socket import *
import sys
from client_helpers import check_cmd, cmd_handler
from udp import udp_send, udp_recv

#Server would be running on the same host as Client
if len(sys.argv) != 3:
    print("\n===== Error usage, python3 TCPClient3.py SERVER_IP SERVER_PORT ======\n")
    exit(0)
serverHost = sys.argv[1]
serverPort = int(sys.argv[2])
serverAddress = (serverHost, serverPort)

# define a socket for the client side, it would be used to communicate with the server
clientSocket = socket(AF_INET, SOCK_DGRAM)

# build connection with the server and send message to it
clientSocket.connect(serverAddress)

# user authentication
while True:
    message = "login"
    udp_send(clientSocket, message, serverAddress)

    username = input("Username: ")
    udp_send(clientSocket, username, serverAddress)

    receivedMessage, address = udp_recv(clientSocket)

    if receivedMessage == "username exists":
        password = input("Password: ")
        udp_send(clientSocket, password, serverAddress)
        receivedMessage, address = udp_recv(clientSocket)

        if receivedMessage == "correct password":
            break
        else:
            print("Incorrect password, try again.")
        
    elif receivedMessage == "username does not exist":
        print("Creating a new user.")
        password = input("Password: ")
        udp_send(clientSocket, password, serverAddress)
        receivedMessage, address = udp_recv(clientSocket)
        break
    
    elif receivedMessage == "user already logged in":
        print("This user is already logged in, please enter another username.")

print("User authentication successful.")

while True:
    message = input("Please enter one of the following commands: CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT: ")
    err, cmd = check_cmd(message)
    if err is not None:
        print("ERROR: " + err)
        continue
    udp_send(clientSocket, message, serverAddress)
    res = cmd_handler(cmd, clientSocket)
    if res == "exit":
        break
    if res == "upload":
        tcpSocket = socket(AF_INET, SOCK_STREAM)
        tcpSocket.connect(serverAddress)
        
        words = message.strip().split(' ')
        filename = words[2]
        f = open(filename, 'rb')
        data = f.read()
        f.close()
        
        tcpSocket.sendall(data)
        tcpSocket.close()

        msg, address = udp_recv(clientSocket)
        if msg == 'file uploaded':
            print("File uploaded.")
    
    if res == "download":
        tcpSocket = socket(AF_INET, SOCK_STREAM)
        tcpSocket.connect(serverAddress)

        data = tcpSocket.recv(1024)
        tcpSocket.close()

        words = message.strip().split(' ')
        filename = words[2]
        f = open(filename, 'wb')
        f.write(data)
        f.close()

        msg, address = udp_recv(clientSocket)
        if msg == 'file downloaded':
            print("File downloaded.")
    
    # if receivedMessage == "":
    #     print("[recv] Message from server is empty!")
    # elif receivedMessage == "user has exited":
    #     print("You have been logged off the server, goodbye!")
    #     break
    # elif receivedMessage == "download filename":
    #     print("[recv] You need to provide the file name you want to download")
    # else:
    #     print("[recv] Message makes no sense")
        
    # ans = input('\nDo you want to continue(y/n) :')
    # if ans == 'y':
    #     continue
    # else:
    #     break

# close the socket
clientSocket.close()
