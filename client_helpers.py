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
    elif cmd in ["DLT","UPD","DWN"]:          # two args
        if not args == 3:
            err = "Incorrect number of arguments."
    elif cmd == "EDT":                              # three args
        if not args == 4:
            err = "Incorrect number of arguments."
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
        pass
    if cmd == "EDT":
        pass
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
        pass
    if cmd == "UPD":
        pass
    if cmd == "DWN":
        pass
    if cmd == "RMV":
        pass
    if cmd == "XIT":
        msg, address = udp_recv(socket)
        if msg == "user has exited":
            print("You have been logged off the server, goodbye!")
        return "exit"

