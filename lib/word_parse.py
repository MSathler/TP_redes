class word_parse(object):

    def parse(self,line):
        self.reset()
        self.a = ""
        read = line.decode('utf-8').split('\n')
        if read[0] == '':
            return False
        else:
                for string in read[0]:
                    if string.isalnum():
                        V,C,N = self.vogal_consoant_digit(string)
                        self.vog += V
                        self.cons += C 
                        self.number += N
                        self.backup += string
                if self.backup == 'bn':
                    return [('V = ' +str(self.vog) + '; C =' + str(self.cons)+ '; N ='+ str(self.number)),1]

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
