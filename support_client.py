import socket
from lib.word_parse import word_parse
from lib.parse_document import parse_document
from lib.tclient import client
from lib.output_doc import output_doc
import _thread as thread
import time
from lib.protocol import m_protocol

global T

def listen(c,ap,doc):
        global T
        con = c.con
        data = []
        p = m_protocol()
        while True:
            st = con.recv(1024)
            if not st: break
            st = st.decode('utf-8')
            while st == 'server_request\n':
                print('Processing a server request')

                len_i,msg,client_key, have_msg = p.receive_msg(con,True)

                if have_msg == False: break

                print('Received a server request to another client (server_key = '+ str(client_key)+') to parse the words.')
                print('Parsed data:')
                print('--------------------------')

                for i in range(int(len_i)):
                    msg_i,error = ap.parse(msg[i])
                    if error == 0:
                        data.append(msg_i)
                        print(msg_i)
                    else:
                        data.append('error')
                        print('error')

                print('--------------------------')


                con.send(('client_response\n').encode('utf-8'))
                con.send(len_i.encode('utf-8'))
                time.sleep(1/1.5)
                for i in range(int(len_i)):
                    con.send((str(data[i])).encode('utf-8'))
                    time.sleep(1/1.5)
                con.send((str(client_key)).encode('utf-8'))
                st = None
                break

            while st == 'server_fresponse\n':
                print('Received a request answer:')
                print('--------------------------')

                _,msg,__, have_msg = p.receive_msg(con,False)
                if have_msg == False: break

                doc.write_line(msg)
                print('--------------------------')

                break

            if st == 'CloseClient':

                break
            
            
        T = False
        print('Finalizando conexao do cliente')
        con.close()
        thread.exit()




if __name__ == '__main__':
    T = True
    ap = word_parse()

    HOST = '127.0.0.1'     # Endereco IP do Servidor
    PORT = 5009            # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c = client(tcp,'')
    dest = (HOST, PORT)
    tcp.connect(dest)
    doc = None
    thread.start_new_thread(listen,tuple([c,ap,doc]))
    print('Waiting Server Request')

    while T == True:
        pass
  

    tcp.close()
