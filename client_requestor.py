import socket
import _thread as thread
import time
from lib.word_parse import word_parse
from lib.parse_document import parse_document
from lib.tclient import client
from lib.output_doc import output_doc

global T

# def msg_read(con):
#     data = []
#     msg = con.recv(1024)
#     if not msg: break
#     len = msg
#     for i in range(int(len)):
#         msg = con.recv(1024)
#         data.append([ap.parse(msg)])
#     msg = con.recv(1024)
#     client_key = msg


def listen(c,ap,doc):
        global T
        con = c.con
        data = []
        FIM = False
        while True:
            st = con.recv(1024)
            if not st: break
            # print(st)

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
    doc_msg = parse_document("modelo_entrada.txt")
    print('Open archive named: modelo_entrada.txt.')
    doc_msg.read_lines()
    msg_len = len(doc_msg.dictionary)
    print('Document data parsed.')

    T = True

    ap = word_parse()

    HOST = '127.0.0.1'     # Endereco IP do Servidor
    PORT = 5006            # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c = client(tcp,'')
    dest = (HOST, PORT)
    tcp.connect(dest)
    print("Send request\n")
    doc = output_doc("output.txt")
    tcp.send(b"client_request\n")
    time.sleep(1/1.5)
    tcp.send((str(msg_len) + '\n').encode('utf-8'))
    thread.start_new_thread(listen,tuple([c,ap,doc]))
    time.sleep(1/1.5)
    print('Send the following messages:')
    print('--------------------------')
    


    for i in range(1,msg_len+1): 
        # print((str(doc_msg.dictionary['k'+str(i)])+ '\n').encode('utf-8'))
        # print((str(doc_msg.dictionary['k'+str(i)])+ '\n'))
        time.sleep(1/1.5)
        tcp.send((str(doc_msg.dictionary['k'+str(i)])+ '\n').encode('utf-8'))
        print(str(doc_msg.dictionary['k'+str(i)]))
    print('--------------------------')

    while T == True:
        pass

    tcp.close()
