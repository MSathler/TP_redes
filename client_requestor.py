import socket
import _thread as thread
import time
from lib.word_parse import word_parse
from lib.parse_document import parse_document
from lib.tclient import client
from lib.output_doc import output_doc
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
    doc_msg = parse_document("modelo_entrada.txt")
    print('Open archive named: modelo_entrada.txt.')
    doc_msg.read_lines()
    msg_len = len(doc_msg.dictionary)
    print('Document data parsed.')

    T = True

    ap = word_parse()

    HOST = '127.0.0.1'     # Endereco IP do Servidor
    PORT = 5009            # Porta que o Servidor esta
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
