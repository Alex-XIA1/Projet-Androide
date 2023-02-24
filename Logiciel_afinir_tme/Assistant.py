import csv
import numpy as np


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

class Assistant(): 
    def __init__(self, model, app, zone) : 
        self.model = model
        self.app = app
        self.app.logger.Lobserver.append(self)
        self.zone = zone
        self.cmd = []
        self.logs = []

    def update(self, etatDep, etatFin, commande):
        if len(self.logs)>0:
            start = self.logs.pop(0)
            self.cmd.pop(0)
            # cree la donnee a predire
            if etatDep == etatFin:
                print("T'as pas beaucoup bouge")
                
            else:
                x = flatten_list([start, etatFin])
                sortie = self.model.predict([x])
                if commande != sortie:
                    if sortie not in self.cmd:
                        # Si true on dit a l'utilisateur d'utiliser la commande en sortie
                        test = 'transition: {} -> {} \n'.format(start, etatFin)
                        confiance = 'Confiance: \n'
                        classes= self.model.model.classes_
                        predictions = np.around((self.model.predict_proba([x])[0]), 3)
                        for i in range(len(classes)):
                            if predictions[i] == 0:
                                continue
                            confiance += ' - {} {}\n'.format(classes[i], predictions[i])
                        texte = "{}\n {}\n On vous propose la commande suivante car il faut bourrer son pantatlon: {}".format(test, confiance, sortie[0])
                        self.zone.setPlainText(texte)
        self.cmd.append(commande)
        self.logs.append(etatDep)
        print("YES")
        """        
        x =  [flatten_list([etatDep,etatFin])]
        sortie = self.model.predict(x)
        if self.compare(sortie,commande):
            #print("PASSED ",self.cmd, commande)
            # Potentiellement ne pas spammer l'utilisateur apres l'avoir fait decouvert la commande ?
            if sortie not in self.cmd:
                #print("Utiliser la commande suivante:", sortie)
                texte = "On vous propose la commande suivante car il faut bourrer son pantatlon: "+sortie[0]
                self.zone.setPlainText(texte)
                self.cmd.append(sortie)"""
    





    