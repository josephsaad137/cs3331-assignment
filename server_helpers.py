from state_info import *

# wrapper function for sending UDP segments from server to clientS
def server_send(socket, msg):
    pass

def do_login(clientSocket):
    data = clientSocket.recv(1024)
    username = data.decode()
    print("[recv] " + username)

    return_val = False

    if username in ACTIVE_USERS:
        message = "user already logged in"
        print("[send] " + message)
        clientSocket.sendall(message.encode())
        return return_val

    # get a list of all the user credentials
    cred_file = open("credentials.txt", 'r')
    credentials = cred_file.readlines()
    cred_file.close()
    split_creds = []
    for line in credentials:
        split_creds.append(line.strip().split(' '))
    
    expected_pw = None
    for line in split_creds:
        if line[0] == username:
            expected_pw = line[1]
    
    if expected_pw is not None:
        message = "username exists"
        clientSocket.sendall(message.encode())

        data = clientSocket.recv(1024)
        password = data.decode()
        print("[recv] " + password)

        if password == expected_pw:
            message = "correct password"
            ACTIVE_USERS.append(username)
            return_val = username
        else:
            message = "incorrect password"
        print("[send] " + message)
        clientSocket.sendall(message.encode())
    else:
        message = "username does not exist"
        print("[send] " + message)
        clientSocket.sendall(message.encode())

        data = clientSocket.recv(1024)
        password = data.decode()
        print("[recv] " + password)

        cred_file = open("credentials.txt", 'a')
        cred_file.write(username + " " + password + "\n")
        cred_file.close()

        ACTIVE_USERS.append(username)
        return_val = username
        message = "new user created"
        print("[send] " + message)
        clientSocket.sendall(message.encode())

    return return_val