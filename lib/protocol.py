import socket
import time

class m_protocol(object):


    def __init__(self):
        
        self.msg = []
        self.con = None
        self._log = {}
        self.i = 0

    def receive_msg(self, con, have_key):       # Function with parse protocol configuration
        
        self.msg = []
        self.len = None
        self.msg.append(con.recv(1024))         # Store received data on variable self.msg
        
        if not self.msg: return None,self.msg,None, False 
        
        self.len = self.msg[0].decode('utf-8')  # First item of protocol its a len of data
        
        for _ in range(int(self.len)):          # Read the data

            self.msg.append(con.recv(1024).decode('utf-8'))

        if have_key == True:                    # Key of client requestor
            
            self.msg.append(con.recv(1024).decode('utf-8'))
            
        else:
            
            self.msg.append(None)
            
        self.i += 1
        self._log['data'+str(self.i)] = ['received',self.msg]   # Create a log file, to see any error
        
        return self.len,self.msg[1:-1],self.msg[-1], True


    def send_msg(self, con, client, start_msg, data_len, protocol_data, client_key = False): # Function send a message with protocol configuration
        
        con.sendto(start_msg.encode('utf-8'),client)        # Send label of the message
        time.sleep(0.5)
        con.sendto(str(data_len).encode('utf-8'),client)    # Send len of the rest of message
        time.sleep(0.3)
        
        for i in range(int(data_len)):
            
            con.sendto((str(protocol_data[i])).encode('utf-8'),client)  # Send data
            time.sleep(0.1)
            
        if client_key == False:
            pass
        
        else:
            con.sendto(('k'+str(client_key)).encode('utf-8'),client)    # If have key, send the key of client
            
        self.i += 1
        self._log['data'+str(self.i)] = ['sended',self.msg]    



    def close_p(self,c_list):               # function to close all clients
        
        for q in range(len(c_list)):
            
                    Con,Client = c_list['k'+str(q+1)][0],c_list['k'+str(q+1)][1]
                    Con.sendto(b'CloseClient',Client)
                    Con.close()
                    time.sleep(0.1)
                    print('Finalizando conexao do cliente', Client)
                    self._END = True

    @property
    def log(self):
        return self._log

