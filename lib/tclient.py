import socket
import _thread
import random
import time

class client(object):
    def __init__(self,con,cliente):
        self._con = con
        self._cliente = cliente
        self.i = 0
        self.f = 0
        self._package_len = 0
        self._msg_table = []
        self._response_table = []

    @property
    def con(self):
        return self._con

    @property
    def package_len(self):
        return self._package_len

    def clear(self):
        self.i = 0
        # self.f = 0
        self._package_len = 0
        self._msg_table = []
        # self._response_table = []

    def msg(self,msg):
        # print(self.i)
        self.i += 1
        if self.i == 1:
            self._package_len = msg
            
        else:
            self._msg_table.append(msg)
            for _ in range(int(self._package_len)-1):
                self._msg_table.append(self._con.recv(1024).decode('utf-8'))
            # print(self._msg_table)    
            return self._msg_table, True
        
        return None, False


    # def client_send(self,con2,data,client_s):
    #     con2.sendto("server_request\n",client_s)
    #     time.sleep(1/1.5)
    #     for i in range(len(data)):
    #         con2.sendto(str(data[i]),client_s)
    #         time.sleep(1/1.5)

