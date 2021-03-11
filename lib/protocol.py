import socket
import time

class m_protocol(object):
    def __init__(self):
        self.msg = []
        self.con = None
        self._log = {}
        self.i = 0

    def receive_msg(self, con, have_key):
        self.msg = []
        self.len = None
        self.msg.append(con.recv(1024))
        if not self.msg: return None,self.msg,None, False 
        self.len = self.msg[0].decode('utf-8')
        for _ in range(int(self.len)):
            self.msg.append(con.recv(1024).decode('utf-8'))
        if have_key == True:
            self.msg.append(con.recv(1024).decode('utf-8'))
        else:
            self.msg.append(None)
        self.i += 1
        self._log['data'+str(self.i)] = ['received',self.msg]
        return self.len,self.msg[1:-1],self.msg[-1], True

    def send_msg(self,con,client,start_msg,data_len,protocol_data,client_key = False):
        con.sendto(start_msg.encode('utf-8'),client)
        time.sleep(1/1.5)
        con.sendto(str(data_len).encode('utf-8'),client)
        time.sleep(1/1.5)
        for i in range(int(data_len)):
            con.sendto((str(protocol_data[i])).encode('utf-8'),client)
            time.sleep(1/1.5)
        if client_key == False:
            pass
        else:
            con.sendto(('k'+str(client_key)).encode('utf-8'),client)
        self.i += 1
        self._log['data'+str(self.i)] = ['sended',self.msg]

    def close_p(self,c_list):
        for q in range(len(c_list)):
                    Con,Client = c_list['k'+str(q+1)][0],c_list['k'+str(q+1)][1]
                    Con.sendto(b'CloseClient',Client)
                    Con.close()
                    time.sleep(1)
                    print('Finalizando conexao do cliente', Client)
                    self._END = True

    @property
    def log(self):
        return self._log

