import socket
# import thread
import random
import time
# from lib.c_parse_document import client
from lib.server import server
# from lib.client import client

# from c_parse_document import client



# class server(object):

    # def __init__(self,HOST = '', PORT = 5001):
    #     self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.orig = (HOST, PORT)
    #     self.tcp.bind(self.orig)
    #     self.tcp.listen(2)
    #     self.c_list = {}
    #     self.i = 0
    #     self.data = {}

    # def add_client(self,con,client):
    #     self.i += 1
    #     self.c_list['k'+str(self.i)] = [con,client]
    


    # def client_chooser(self):
    #     self.client_selected = random.randint(1,len(self.c_list))
    #     # print(self.c_list)
    #     # print(self.client_selected)
    #     return self.c_list['k'+str(self.client_selected)][0], self.c_list['k'+str(self.client_selected)][1],self.client_selected

    # def client_r(self,con,cliente):
    #     self.cliente_requisitor = [con,cliente]


    # def server_send(self,con2,data,client_s,client_key):
    #     con2.sendto("server_request\n",client_s)
    #     time.sleep(1/1.5)
    #     con2.sendto(str(len(data)),client_s)
    #     time.sleep(1/1.5)
    #     for i in range(len(data)):
    #         con2.sendto(str(data[i]),client_s)
    #         time.sleep(1/1.5)
    #     con2.sendto('k'+str(client_key),client_s)


    # @property
    # def _c_list(self):
    #     return self.c_list

    # @property
    # def _tcp(self):
    #     return self.tcp

    # def close(self):
    #     self.tcp.close()
    #     self.i = 0

    # def routine(self):
    #     con, cliente = self.tcp.accept()
    #     self.add_client(con,cliente)
    #     thread.start_new_thread(self.client_thread, tuple([con,cliente]))


    # def client_thread(self,con,cliente):
    #     resp = False
    #     data = None
    #     print 'Conectado por', cliente
    #     c = client(con,cliente)
    #     while True:
    #         start_msg = con.recv(1024)
    #         while start_msg == "client_request\n":
    #             self.client_r(con,cliente)
    #             msg = con.recv(1024)
    #             if not msg: break
    #             data, resp = c.msg(msg)
    #             if resp == True: start_msg = resp
    #             # print cliente, msg

    #             if resp == True:
    #                 print('Received message for a Client Request -> ' + str(cliente[1]))
    #                 print('--------------------------------------------------')
    #                 print(data)
    #                 print('--------------------------------------------------')
    #                 con2,client_s, client_key = s.client_chooser()
    #                 print('Sending the message to a client -> ' + str(client_s[1]) + ' <- to analyze the words.' )
    #                 # print('--------------------------------------------------')
    #                 # print(data)
    #                 # print('--------------------------------------------------')
    #                 s.server_send(con2,data,client_s,client_key)
    #                 break
    #         while start_msg == 'client_response\n':
    #             print('Receiving a parsed data:')
    #             print('--------------------------')
    #             cr_data = []
    #             response_msg = con.recv(1024)

    #             if not response_msg: break

    #             len_t = response_msg
    #             for i in range(int(len_t)):
    #                 response_msg = con.recv(1024)
    #                 cr_data.append(response_msg)
    #                 print(response_msg)
    #             print('--------------------------')
    #             response_msg = con.recv(1024)
    #             client_key = response_msg
    #             con_f,client_f = self.cliente_requisitor
    #             print('Sending final message (above) to a Client Request -> ' + str(client_f[1]))
    #             con_f.sendto('server_fresponse\n',client_f)
    #             time.sleep(1/1.5)
    #             con_f.sendto(str(len(cr_data)),client_f)
    #             time.sleep(1/1.5)

    #             for i in range(len(cr_data)):
    #                 con_f.sendto(str(cr_data[i]),client_f)
    #                 time.sleep(1/1.5)

    #             break

    #     print 'Finalizando conexao do cliente', cliente
    #     con.close()
    #     thread.exit()

if __name__ == '__main__':
    s = server()

    while True:
        s.routine()

    s.close()
