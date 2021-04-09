import socket
import _thread as thread
import time
from lib.word_parse import word_parse
from lib.parse_document import parse_document
from lib.tclient import client
from lib.output_doc import output_doc
from lib.protocol import m_protocol

T = True
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

def listen(c,ap,doc):
    
        global T        # Global conditional to end thread
        con = c.con
        data = []
        p = m_protocol()    # Initiate protocol object
        
        while True:

            st = con.recv(1024)         # Wait a message

            if not st: break

            st = st.decode('utf-8')         # Decote message to utf-8 formate

            while st == 'server_request\n': # Server Request routine

                print('Processing a server request')

                len_i,msg,client_key, have_msg = p.receive_msg(con,True)    # Receive and parse msg

                if have_msg == False: break

                print('Received a server request to another client (server_key = '+ str(client_key)+') to parse the words.')
                print('Parsed data:')
                print('--------------------------')

                for i in range(int(len_i)):

                    msg_i,error = ap.parse(msg[i])  # Analyze 'msg' variable

                    if error == 0:                  

                        data.append(msg_i)          
                        print(msg_i)

                    else:                       

                        data.append('error')        # Erro equal to 1, means it has no consoanant vowel or number
                        print('error')

                print('--------------------------')


                p.send_msg(con,(HOST,PORT),'client_response\n',len_i,data,client_key)   # Send response to server

                st = None
                break

            while st == 'server_fresponse\n':           # Server response routine

                print('Received a request answer:')
                print('--------------------------')
                _,msg,__, have_msg = p.receive_msg(con,False)       # Receive and parse data 

                if have_msg == False: break

                doc.write_line(msg)                                 # Write on the document
                print('--------------------------')

                break

            if st == 'CloseClient':             # Receive server command to close the client
                break
            
            
        T = False
        print('Finalizando conexao do cliente')
        con.close()
        thread.exit()




if __name__ == '__main__':
    
    doc_msg = parse_document("modelo_entrada.txt")      # Function to create a parse data
    print('Open archive named: modelo_entrada.txt. If you want to change file, please replace the name on line 89')
    doc_msg.read_lines()                                # read_lines remove unnecessary lines such as comments 
    msg_len = len(doc_msg.dictionary)                   
    print('Document data parsed.')

    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a TCP socket 
    c = client(tcp,'')                                      # Create a client Object name 'c'
    ap = word_parse()                                       # Create a word_pase object named 'ap'
    doc = output_doc("output.txt")                          # Set the name of output document
    dest = (HOST, PORT)
    tcp.connect(dest)

    print("Send request\n")
    
    tcp.send(b"client_request\n")
    time.sleep(0.5)
    tcp.send((str(msg_len) + '\n').encode('utf-8'))
    time.sleep(0.5)
    print('Send the following messages:')

    print('--------------------------')
    for i in range(1,msg_len+1):                            # For to send all data os the document
        tcp.send((str(doc_msg.dictionary['k'+str(i)])+ '\n').encode('utf-8'))
        time.sleep(0.2)
        print(str(doc_msg.dictionary['k'+str(i)]))
    print('--------------------------')

    thread.start_new_thread(listen,tuple([c,ap,doc]))       # Start a client thread

    while T == True:                                        # Condition to keep thread running
        pass

    tcp.close()                                             # Close socket
