def check_cmd(msg):
    words = msg.strip().split(" ")

    if len(words) == 0:
        return "No command entered."

    cmd = words[0]
    args = len(words)
    err = None
    if cmd in ["LST","XIT"]:                        # zero args
        if not args == 1:
            err = "Incorrect number of arguments."
    elif cmd in ["CRT","RDT","RMV"]:                # one arg
        if not args == 2:
            err = "Incorrect number of arguments."
    elif cmd in ["MSG","DLT","UPD","DWN"]:          # two args
        if not args == 3:
            err = "Incorrect number of arguments."
    elif cmd == "EDT":                              # three args
        if not args == 4:
            err = "Incorrect number of arguments."
    else:
        err = "Command does not exist."

    return err

def check_response(msg):
    if msg == "user has exited":
        return "exit", " "
    if msg == "thread already exists":
        return "print", "ERROR: The thread with the given title already exists."


    return " ", " "