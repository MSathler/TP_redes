import socket
from lib.word_parse import word_parse
from lib.parse_document import parse_document
from lib.tclient import client
from lib.output_doc import output_doc
import _thread as thread
import time

global T

def listen(c,ap,doc):
        global T
        con = c.con
        data = []
        FIM = False
        while True:
            st = con.recv(1024)
            if not st: break

            while st == b'server_request\n':
                print('Processing a server request')
                msg = con.recv(1024)
                if not msg: break
                len_i = msg
                for i in range(int(len_i)):
                    msg = con.recv(1024)
                    msg,error = ap.parse(msg)
                    if error == 0:
                        data.append(msg)
                    else:
                        data.append('error')
                msg = con.recv(1024)
                client_key = msg
                print('Received a server request to another client (server_key = '+ str(client_key)+') to parse the words.')
                print('Parsed data:')
                print('--------------------------')
                for i in range(int(len_i)):
                    print(data[i])
                print('--------------------------')
                con.send(('client_response\n').encode('utf-8'))
                con.send(len_i)
                time.sleep(1/1.5)
                for i in range(int(len_i)):
                    con.send((str(data[i])).encode('utf-8'))
                    time.sleep(1/1.5)
                con.send((str(client_key)).encode('utf-8'))
                st = None
                break

            while st == b'server_fresponse\n':
                print('Received a request answer:')
                print('--------------------------')
                msg = con.recv(1024)
                if not msg: break
                len_sr = msg
                for i in range(int(len_sr)):
                    msg = con.recv(1024)
                    msg = msg.decode('utf-8')
                    msg = msg.split('\'')[1]
                    print(msg)
                    doc.write_line(msg)
                print('--------------------------')
                # FIM = True
                break
            if st == b'CloseClient':
                
                break
            
            
        T = False
        print('Finalizando conexao do cliente')
        con.close()
        thread.exit()



if __name__ == '__main__':
    # doc_msg = parse_document("modelo_entrada.txt")
    # print('Open archive named: modelo_entrada.txt.')
    # doc_msg.read_lines()
    # msg_len = len(doc_msg.dictionary)
    # print('Document data parsed.')

    T = True

    ap = word_parse()

    HOST = '127.0.0.1'     # Endereco IP do Servidor
    PORT = 5006            # Porta que o Servidor esta
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
