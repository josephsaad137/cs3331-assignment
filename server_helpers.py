
def do_login(clientSocket):
    data = clientSocket.recv(1024)
    username = data.decode()
    print("[recv] " + username)

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

        message = "new user created"
        print("[send] " + message)
        clientSocket.sendall(message.encode())