from udp import udp_send, udp_recv

def check_cmd(msg):
    words = msg.strip().split(" ")

    if len(words) == 0:
        return "No command entered.", None

    cmd = words[0]
    args = len(words)
    err = None
    if cmd in ["LST","XIT"]:                        # zero args
        if not args == 1:
            err = "Incorrect number of arguments."
    elif cmd in ["CRT","RDT","RMV"]:                # one arg
        if not args == 2:
            err = "Incorrect number of arguments."
    elif cmd in ["DLT","UPD","DWN"]:                # two args
        if not args == 3:
            err = "Incorrect number of arguments."
    elif cmd == "EDT":
        if args < 4:
            err = "Insufficient number of arguments."
    elif cmd == "MSG":
        if args < 3:
            err = "Insufficient number of arguments."
    else:
        err = "Command does not exist."

    return err, cmd

def cmd_handler(cmd, socket):
    if cmd == "CRT":
        msg, address = udp_recv(socket)
        if msg == "thread already exists":
            print("ERROR: A thread with the given title already exists.")
        else:
            print("New thread created.")

    if cmd == "MSG":
        msg, address = udp_recv(socket)
        if msg == "thread does not exist":
            print("ERROR: There is no thread with the given title.")
        else:
            print("Message sent to thread.")
    if cmd == "DLT":
        msg, address = udp_recv(socket)
        if msg == "thread does not exist":
            print("ERROR: There is no thread with the given title.")
        elif msg == "message number not valid":
            print("ERROR: The given message number is not valid.")
        elif msg == "user not authorised":
            print("ERROR: You are not authorised to delete the given message.")
        else:
            print("Message deleted.")
    if cmd == "EDT":
        msg, address = udp_recv(socket)
        if msg == "thread does not exist":
            print("ERROR: There is no thread with the given title.")
        elif msg == "message number not valid":
            print("ERROR: The given message number is not valid.")
        elif msg == "user not authorised":
            print("ERROR: You are not authorised to edit the given message.")
        else:
            print("Message edited.")
    if cmd == "LST":
        msg, address = udp_recv(socket)
        if msg == "no active threads":
            print("There are currently no active threads.")
            return
        else:
            threads = msg.split(' ')
            print("Active threads:")
            for title in threads:
                print(title)

    if cmd == "RDT":
        msg, address = udp_recv(socket)
        if msg == "thread does not exist":
            print("ERROR: There is no thread with the given title.")
        else:
            print(msg)
    if cmd == "UPD":
        msg, address = udp_recv(socket)
        if msg == "thread does not exist":
            print("ERROR: There is no thread with the given title.")
        elif msg == "file already exists":
            print("ERROR: The given file has already been uploaded to the given thread.")
        else:
            return 'upload'
    if cmd == "DWN":
        msg, address = udp_recv(socket)
        if msg == "thread does not exist":
            print("ERROR: There is no thread with the given title.")
        elif msg == "file does not exist":
            print("ERROR: The given file has not been uploaded to the given thread.")
        else:
            return 'download'
    if cmd == "RMV":
        msg, address = udp_recv(socket)
        if msg == "thread does not exist":
            print("ERROR: There is no thread with the given title.")
        elif msg == "user not authorised":
            print("ERROR: You are not authorised to delete the given thread.")
        else:
            print("Thread deleted.")
    if cmd == "XIT":
        msg, address = udp_recv(socket)
        if msg == "user has exited":
            print("You have been logged off the server, goodbye!")
        return "exit"

