import csv

class Logger(): 
    def __init__(self, nomFichier) : 
        self.nomFichier = nomFichier
        self.file = open('./' + nomFichier, 'w', newline='')
        self.writer = csv.writer(self.file)

    def addRow(self, etatDep, etatFin, commande) : 
        print([etatDep, etatFin, commande])
        self.writer.writerow([etatDep, etatFin, commande])
        

        
if __name__=="__main__":    
    logger = Logger("test")
    