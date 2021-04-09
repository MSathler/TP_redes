import socket
import _thread as thread
import random
import time
# from tclient import client
from .tclient import client
from lib.protocol import m_protocol


class server(object):

    def __init__(self, HOST='127.0.0.1', PORT=5000):
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.orig = (HOST, PORT)
        self.tcp.bind(self.orig)
        self.tcp.listen()
        
        #Initiated variables
        
        self.host = HOST
        self.port = PORT
        self.c_list = {}
        self.i = 0
        self.p = m_protocol()   
        self.data = {}
        self._END = False
        print('Server started!')


    # Function to add the informations of the new client
    def add_client(self, con, client):
        
        self.i += 1
        self.c_list['k'+str(self.i)] = [con, client]

    # Function where the server chooses a random client
    def client_chooser(self):
        self.client_selected = random.randint(1, len(self.c_list))
        print(len(self.c_list))
        return self.c_list['k'+str(1)][0], self.c_list['k'+str(1)][1], 1

    def client_r(self, con, cliente):
        self.cliente_requisitor = [con, cliente]

    # Property or getter of client dictionary
    @property
    def _c_list(self):
        return self.c_list

    # Property or getter of socket information
    @property
    def _tcp(self):
        return self.tcp

    # Close socket
    def close(self):
        self.tcp.close()
        self.i = 0

    
    def routine(self):      # routine function to colect new clients... Put it inside a while;
        con, cliente = self.tcp.accept()
        self.add_client(con, cliente)
        thread.start_new_thread(self.client_thread, tuple([con, cliente]))

    @property
    def END(self):
        return self._END

    # Client routine thread 
    def client_thread(self, con, cliente):
        END = False
        resp = False
        data = None
        print('Conected by', cliente)
        c = client(con, cliente)                        # Create a client object named 'c'
        
        while True:

            start_msg = con.recv(1024)                  # Read socket msg
            while start_msg == b"client_request\n":     # Routine for client request
                self.client_r(con, cliente)             # Save client name into a server variable
                msg = con.recv(1024) 
                data, resp = c.msg(msg.decode('utf-8')) # client msg function receive all msg package and return the data and quality of message
                if resp == True:
                    start_msg = resp

                if resp == True:
                    print('Received message for a Client Request -> ' +
                          str(cliente[1]))
                    print('--------------------------------------------------')
                    print(data)
                    print('--------------------------------------------------')
                    con2, client_s, client_key = self.client_chooser() # Choose randomly one client in the client dictionary
                    print('Sending the message to a client -> ' +
                          str(client_s[1]) + ' <- to analyze the words.')
                    self.p.send_msg(con2, client_s, "server_request\n", len(
                        data), data, client_key)        # Send 'data' message to client con2
                    break

            while start_msg == b'client_response\n':    # Server routine for client response
                
                print('Receiving a parsed data:')
                print('--------------------------')
                len_, cr_data, client_key, have_msg = self.p.receive_msg(
                    con, True)                          # Parse message data
                
                if have_msg == False:
                    break

                print(cr_data)                          # print table

                print('--------------------------')

                con_f, client_f = self.cliente_requisitor   # Recover the client requisitor information its important when have multiple clients
                # print(self._c_list)
                print(
                    'Sending final message (above) to a Client Request -> ' + str(client_f[1]))

                self.p.send_msg(con_f, client_f,
                                "server_fresponse\n", len_, cr_data) # Send server response data
                # print(self.p.log)
                self.p.close_p(self.c_list)     # Send command to close all  clients

                self.tcp.close()                # Close socket
                thread.exit()                   # Close thread
                END = True                      # Set variable to end a while routine
                start_msg = None

                break
            if END == True:                     # Conditional to break a while routine
                break
