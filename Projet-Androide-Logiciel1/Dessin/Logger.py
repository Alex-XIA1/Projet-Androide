import csv

class Logger(): 
    def __init__(self, nomFichier) :
        self.Lobserver = [] 
        self.nomFichier = nomFichier
        self.file = open(nomFichier, 'w', newline='')
        self.writer = csv.writer(self.file)

    def addRow(self, etatDep, etatFin, commande) : 
        print(flatten_list([etatDep, etatFin, commande]))
        self.writer.writerow(flatten_list([etatDep, etatFin, commande]))
        for o in self.Lobserver:
            o.update(etatDep, etatFin, commande)

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list or type(element) is tuple:
            # If the element is of type list, iterate through the sublist
            flat_list.extend(flatten_list(element))
        else:
            flat_list.append(element)
    return flat_list    



        
if __name__=="__main__":    
    logger = Logger("test")
    