import socket
from c_parse_document import parse_document, word_parse,output_doc,client
import thread
import time


def listen(c,ap,doc):
        con = c.con
        data = []
        FIM = False
        while True:
            st = con.recv(1024)
            if not st: break
            # print(st)
            if st == 'server_request\n':
                doc = output_doc("testando.txt")
            while st == 'server_request\n':
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
                con.send('client_response\n')
                con.send(len_i)
                time.sleep(1/1.5)
                for i in range(int(len_i)):
                    con.send(str(data[i]))
                    time.sleep(1/1.5)
                con.send(str(client_key))
                st = None
                # print("FIM")
                break

            while st == 'server_fresponse\n':
                print('Received a request answer:')
                print('--------------------------')
                msg = con.recv(1024)
                if not msg: break
                len_sr = msg
                for i in range(int(len_sr)):
                    msg = con.recv(1024)
                    print(msg)
                    doc.write_line(msg)
                print('--------------------------')
                FIM = True
                break
            if FIM == True:
                break
            
            
            

        print 'Finalizando conexao do cliente'
        con.close()
        thread.exit()



if __name__ == '__main__':
    # doc_msg = parse_document("modelo_entrada.txt")
    # print('Open archive named: modelo_entrada.txt.')
    # doc_msg.read_lines()
    # msg_len = len(doc_msg.dictionary)
    # print('Document data parsed.')

    ap = word_parse()

    HOST = '127.0.0.1'     # Endereco IP do Servidor
    PORT = 5001            # Porta que o Servidor esta
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c = client(tcp,'')
    dest = (HOST, PORT)
    tcp.connect(dest)
    doc = None
    thread.start_new_thread(listen,tuple([c,ap,doc]))


    while True:
        pass
  

    tcp.close()
