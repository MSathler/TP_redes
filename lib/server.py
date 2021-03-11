import socket
import _thread as thread
import random
import time
# from tclient import client
from .tclient import client
from lib.protocol import m_protocol

class server(object):

    def __init__(self,HOST = '127.0.0.1', PORT = 5009):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.orig = (HOST, PORT)
        self.tcp.bind(self.orig)
        self.tcp.listen(2)
        self.host = HOST
        self.port = PORT
        self.c_list = {}
        self.i = 0
        self.p = m_protocol()
        self.data = {}
        self._END = False
        print('Server started!')

    def add_client(self,con,client):
        self.i += 1
        self.c_list['k'+str(self.i)] = [con,client]
    


    def client_chooser(self):
        self.client_selected = random.randint(1,len(self.c_list))
        # print(self.c_list)
        # print(self.client_selected)
        return self.c_list['k'+str(self.client_selected)][0], self.c_list['k'+str(self.client_selected)][1],self.client_selected

    def client_r(self,con,cliente):
        self.cliente_requisitor = [con,cliente]


    def server_send(self,con2,data,client_s,client_key):
        con2.sendto("server_request\n".encode('utf-8'),client_s)
        time.sleep(1/1.5)
        con2.sendto((str(len(data))).encode('utf-8'),client_s)
        time.sleep(1/1.5)
        print(len(data))
        for i in range(len(data)):
            con2.sendto((str(data[i])).encode('utf-8'),client_s)
            time.sleep(1/1.5)
        con2.sendto(('k'+str(client_key)).encode('utf-8'),client_s)


    @property
    def _c_list(self):
        return self.c_list

    @property
    def _tcp(self):
        return self.tcp

    def close(self):
        self.tcp.close()
        self.i = 0

    def routine(self):
        con, cliente = self.tcp.accept()
        self.add_client(con,cliente)
        thread.start_new_thread(self.client_thread, tuple([con,cliente]))
        

    @property
    def END(self):
        return self._END

    def client_thread(self,con,cliente):
        END = False
        resp = False
        data = None
        print('Conectado por', cliente)
        c = client(con,cliente)
        while True:
            
            start_msg = con.recv(1024)
            while start_msg == b"client_request\n":
                self.client_r(con,cliente)
                msg = con.recv(1024)
                data, resp = c.msg(msg.decode('utf-8'))
                if resp == True: start_msg = resp
                # print cliente, msg

                if resp == True:
                    print('Received message for a Client Request -> ' + str(cliente[1]))
                    print('--------------------------------------------------')
                    print(data)
                    print('--------------------------------------------------')
                    con2,client_s, client_key = self.client_chooser()
                    print('Sending the message to a client -> ' + str(client_s[1]) + ' <- to analyze the words.' )
                    self.p.send_msg(con2,client_s,"server_request\n",len(data),data,client_key)
                    # self.server_send(con2,data,client_s,client_key)
                    break

            while start_msg == b'client_response\n':
                print('Receiving a parsed data:')
                print('--------------------------')
                len_, cr_data, client_key, have_msg = self.p.receive_msg(con,True)
                if have_msg == False: break

                print(cr_data)

                print('--------------------------')

                con_f,client_f = self.cliente_requisitor
                print('Sending final message (above) to a Client Request -> ' + str(client_f[1]))


                self.p.send_msg(con_f,client_f,"server_fresponse\n",len_,cr_data)

                # self.p.close_p(self.c_list)
                self.tcp.shutdown(socket.SHUT_RDWR)
                self.tcp.close()
                print(self.p.log)
                thread.exit()
            #         END = True
            #         start_msg = None

            #         break
            # if END == True:
                
                
                
            #     break

        # print('Finalizando conexao do cliente', cliente)
        # con.close()
        thread.exit()
