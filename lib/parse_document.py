# encoding: iso-8859-1
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
        with open(self._file_name, "r", encoding='latin-1') as f:
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
                    #print(line)
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
        elif read[0] == '\n':
                # print('Line null')
                return False
        else:
            read2 = read[0].split('\n')
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

if __name__ == '__main__':
    p = parse_document("modelo_entrada.txt")
    p.read_lines()
    # letter_parse()
    # v,c,n,error = letter_parse().parse("j\xc2k3\n")
    # print(str(p.dictionary))
    # doc = output_doc("teste.txt")
    # doc.write_line(v,c,n,error)
    # print(v,c,n,error)
