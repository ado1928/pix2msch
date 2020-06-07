from socket import socket, create_connection, AF_INET, SOCK_DGRAM
from struct import unpack
from time import time
class Server():
    def __init__(self, host, server_port = 6567, socketinput_port = 6859):
        self.host = host
        self.server = (host, server_port)
        self.socketinput_port = socketinput_port
        
    def get_status(self):
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(self.server)
        s.send(b"\xfe\x01")
    
        statusdict = {}
    
        data = s.recv(1024)
        statusdict["name"] = data[1:data[0]+1].decode("utf-8")
        data = data[data[0]+1:]
        statusdict["map"] = data[1:data[0]+1].decode("utf-8")
        data = data[data[0]+1:]
        statusdict["players"] = unpack(">i", data[:4])[0]
        data = data[4:]
        statusdict["wave"] = unpack(">i", data[:4])[0]
        data = data[4:]
        statusdict["version"] = unpack(">i", data[:4])[0]
        data = data[4:]
        statusdict["vertype"] = data[1:data[0]+1].decode("utf-8")
        
        return statusdict
        
    def send_command(self, command):
        s = create_connection((self.host, self.socketinput_port))
        s.sendall(bytes(command.encode()))
        s.close()
        
    def ping(self, timeout = 10.0):
        s = socket(AF_INET, SOCK_DGRAM)
        s.settimeout(timeout)
        s.connect(self.server)
        start_t = time()
        s.sendall(b"\xfe\x01")
        s.recv(1024)
        s.close()
        return(round((time()-start_t)*1000))
    