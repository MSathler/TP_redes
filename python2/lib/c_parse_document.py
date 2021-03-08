from unicodedata import normalize
import io
import time
import socket
class parse_document(object):

    def __init__(self,file_name):
        self._file_name = file_name
        self.backup = ""
        self.first = 0
        self.qtde = 0
        self.dictionary = {}
        self.vog,self.cons,self.number = 0,0,0

    def read_lines(self):
        i = 0
        with open(self._file_name, "r") as f:
            while True:
                self.reset()
                
                line = f.readline()
                
                # End document = end while
                if len(line) == 0:
                    break

                _ = self.parse(line)
                if _ is False:
                    pass
                # elif self.backup == '' and _ == True:
                    # i+=1
                    # if i > self.qtde:
                        # break
                    # else:
                            # print(i)
                        # self.dictionary['k'+str(i)] = 'Erro'
                elif _ == 'first':
                    pass
                        
                else:
                    i+=1
                    if i > self.qtde:
                        break
                    else:   
                        # print(self.a)
                        self.dictionary['k'+str(i)] = self.a
                            # self.dictionary['k'+str(i)] = self.vog,self.cons,self.number,self.backup
            
                

    def parse(self,line):
        self.a = ""
        read = line.split('//')
        if read[0] == '':
            # print('Its a comment')
            return False
        elif read[0] == '\r\n':
                # print('Line null')
                return False
        else:
            read2 = read[0].split('\r\n')
            # print(read2[0])
            
            for string in read2[0]:
                if string.isalnum():
                    self.first += 1 
                    if self.first == 1:
                        self.qtde = int(read2[0])
                        return 'first'
                    
                    # V,C,N = self.vogal_consoant_digit(string)
                    # self.vog += V
                    # self.cons += C 
                    # self.number += N
                    self.backup += string
            self.a = read2[0]
            return True
                #return vog, cons, number,backup

    def vogal_consoant_digit(self, letra):

        if letra.isdigit():
            return 0, 0, 1
        else:
            letra = letra.upper()
            if letra == "A" or letra == "E" or letra == "I" or letra == "O" or letra == "U":
                return 1, 0, 0
            else:
                return 0, 1, 0

    @property
    def _qtde(self):
        return self.qtde

    @property
    def _dictionary(self):
        return self.dictionary


    def reset(self):
        self.vog = 0
        self.cons = 0
        self.number = 0
        self.backup = ""


class client(object):
    def __init__(self,con,cliente):
        self._con = con
        self._cliente = cliente
        self.i = 0
        self.f = 0
        self._package_len = 0
        self._msg_table = []
        self._response_table = []

    @property
    def con(self):
        return self._con

    @property
    def package_len(self):
        return self._package_len

    def clear(self):
        self.i = 0
        # self.f = 0
        self._package_len = 0
        self._msg_table = []
        # self._response_table = []

    def msg(self,msg):
        # print(self.i)
        self.i += 1
        if self.i == 1:
            self._package_len = msg
            
        else:
            self._msg_table.append(msg)
            for _ in range(int(self._package_len)-1):
                self._msg_table.append(self._con.recv(1024))
            # print(self._msg_table)    
            return self._msg_table, True
        
        return None, False

    # def response_msg(self,msg,con):
    #     self.f += 1
    #     if self.f == 1:
    #         self._response_len = msg
        
    #     else:
    #         # print(self._response_len)
    #         self._response_table.append(msg)
    #         for _ in range(int(self._response_len)-1):
    #             self._response_table.append(con.recv(1024))
    #         return self._response_table, True
        
    #     return None, False

    # def client_send(self,con2,data,client_s):
    #     con2.sendto("server_request\n",client_s)
    #     time.sleep(1/1.5)
    #     for i in range(len(data)):
    #         con2.sendto(str(data[i]),client_s)
    #         time.sleep(1/1.5)


class letter_parse(object):

    def parse(self,line):
        self.reset()
        self.a = ""
        read = line.split('\n')
        if read[0] == '':
            return False
        else:
            # if read[0].isalnum():
                for string in read[0]:
                    if string.isalnum():
                        V,C,N = self.vogal_consoant_digit(string)
                        self.vog += V
                        self.cons += C 
                        self.number += N
                        self.backup += string
                if self.backup == '':
            # else:
                    # return self.vog,self.cons,self.number,1 #self.backup, 1
                    return [('V = ' +str(self.vog) + '; C =' + str(self.cons)+ '; N ='+ str(self.number)),1]

                # return self.vog,self.cons,self.number, 0 #self.backup, 0
                return [('V = ' +str(self.vog) + '; C =' + str(self.cons)+ '; N ='+ str(self.number)),0]

    def vogal_consoant_digit(self, letra):

        if letra == '':
            return 0,0,0
        elif letra.isdigit():
            return 0, 0, 1
        else:
            letra = letra.upper()
            if letra == "A" or letra == "E" or letra == "I" or letra == "O" or letra == "U":
                return 1, 0, 0
            else:
                return 0, 1, 0

    def reset(self):
        self.vog = 0
        self.cons = 0
        self.number = 0
        self.backup = ""

class output_doc(object):
    def __init__(self,doc_name):
        self._doc_name = doc_name 

        with open(self._doc_name,'w') as f:
            f.writelines("//Esse arquivo apresenta o modelo de saida esperado no programa.\n//Os resultados descritos sao referentes ao que foi apresentado no\n//arquivo de modelo de entrada.\n//C significa consoante; V significa volgal; N significa numeros\n\n")
            f.close()

    def write_line(self,msg):
        with open(self._doc_name,'a') as f:
            f.writelines(msg + '\n')
            f.close()
            # if int(error) == 1:
            #     f.writelines("error\n")    
            #     f.close
            # else:
            #     f.writelines("V={v};C={c};N={n}\n".format(v=vogal,c=consoant,n=number))
            #     f.close()



if __name__ == '__main__':
    p = parse_document("modelo_entrada.txt")
    p.read_lines()
    # letter_parse()
    v,c,n,error = letter_parse().parse("j\xc2k3\n")
    # print(str(p.dictionary))
    doc = output_doc("teste.txt")
    doc.write_line(v,c,n,error)
    print(v,c,n,error)