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
        with open(self._file_name, "r", encoding='latin-1') as f:       # Open document
            while True:
                self.reset()            # Reset variables
                
                line = f.readline()     # Read document line
                # End document = end while
                if len(line) == 0:      # Close the while when the reading is over
                    break

                _ = self.parse(line)    # Analyze the line
                if _ is False:
                    pass

                elif _ == 'first':      # first valid word/number on the document its a len, colleted below (!!)
                    pass
                        
                else:
                    i+=1
                    if i > self.qtde:   # conditionalt o break readlines
                        break
                    else:   
                        self.dictionary['k'+str(i)] = self.a

    def parse(self,line):
        
        self.a = ""
        read = line.split('//')         # Split comment lines
        if read[0] == '':               # Remove comment line
            # print('Its a comment')
            return False
        elif read[0] == '\n':           # Remove null line
                # print('Line null')
                return False
        else:
            read2 = read[0].split('\n')        
            
            for string in read2[0]:
                if string.isalnum():    # if string is alplanumeric conditional
                    self.first += 1 
                    if self.first == 1: # Save len of words to parse (!!)
                        self.qtde = int(read2[0])
                        return 'first'
                    self.backup += string
            self.a = read2[0]
            return True

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

