# wrapper functions for reliable UDP transmission using sendto() and recvfrom().

def udp_send(socket, msg, dest):
    socket.sendto(msg.encode(), dest)

def udp_recv(socket):
    msg, address = socket.recvfrom(1024)
    msg = msg.decode()
    return msg, address
