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

