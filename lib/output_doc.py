class output_doc(object):
    
    
    def __init__(self,doc_name):
        
        self._doc_name = doc_name 

        with open(self._doc_name,'w') as f: # Open a writable file
            f.writelines("//Esse arquivo apresenta o modelo de saida esperado no programa.\n//Os resultados descritos sao referentes ao que foi apresentado no\n//arquivo de modelo de entrada.\n//C significa consoante; V significa volgal; N significa numeros\n\n")
            f.close() 

    def write_line(self,msg):           # function to write a msg into a file
        
        with open(self._doc_name,'a') as f:
            for i in range(len(msg)):
                f.writelines(msg[i] + '\n')
                print(msg[i])
            f.close()
