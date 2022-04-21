from state_info import *
from udp import udp_send, udp_recv

def do_login(socket):
    username, clientAddress = udp_recv(socket)
    print("[recv] " + username)

    return_val = False

    if username in ACTIVE_USERS:
        message = "user already logged in"
        print("[send] " + message)
        udp_send(socket, message, clientAddress)
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
        udp_send(socket, message, clientAddress)

        password, clientAddress = udp_recv(socket)
        print("[recv] " + password)

        if password == expected_pw:
            message = "correct password"
            ACTIVE_USERS.append(username)
            return_val = username
        else:
            message = "incorrect password"
        print("[send] " + message)
        udp_send(socket, message, clientAddress)
    else:
        message = "username does not exist"
        print("[send] " + message)
        udp_send(socket, message, clientAddress)

        password, clientAddress = udp_recv(socket)
        print("[recv] " + password)

        cred_file = open("credentials.txt", 'a')
        cred_file.write(username + " " + password + "\n")
        cred_file.close()

        ACTIVE_USERS.append(username)
        return_val = username
        message = "new user created"
        print("[send] " + message)
        udp_send(socket, message, clientAddress)

    return return_val