import csv
import numpy as np
from utils import flatten_list

from time import time



class Assistant(): 
    def __init__(self, model, test, app, zone, filename='data/time.txt') : 
        self.model = model
        self.testModel = test
        self.app = app
        self.app.logger.Lobserver.append(self) 
        self.zone = zone # zone de texte ou l'assistant ecrit
        self.logs = [] # liste des etats
        self.max_size = 20 # taille max de la liste
        self.writer = csv.writer(open(filename, 'w', newline=''))

    # A chaque action dans app, update() est appelée
    # et cherche si y a une commande meilleure
    def update(self, etatDep, etatFin, commande):
        size = len(self.logs)
        print()
        print("size: ", size)
        t1 = time()
        for i in range(size): 
            state = self.logs[i]
            # cree la donnee a predire
            x = [flatten_list([state, etatFin])] 
            if state == etatFin: continue  
            if self.testModel.predict(x) == "No": continue
            if self.model.predict_proba(x).max() < 0.6:
                continue # test si y a un possible raccourci ou non
            self.writer.writerow(time()-t1)
            #self.testModel.afficheConfiance(x) # affiche la confiance dans ce test
            sortie = self.model.predict(x) # predit le raccourci
            # Si true on dit a l'utilisateur d'utiliser la commande en sortie
            # size - i, le nombre de etats sauté
            self.affiche(state, etatFin, size - i, sortie, x)
            break
        # ajoute l'etat precedent
        # supprime si la liste est trop grande
        self.logs.append(etatDep)
        if size >= self.max_size: self.logs.pop(0)

    def affiche(self, state, etatFin, i, sortie, x):
        test = 'transition: {} --{}--> {} \n'.format(state,i, etatFin)
        confiance = 'Confiance: \n'
        classes= self.model.model.classes_
        
        Lconfiance = np.around((self.model.predict_proba(x)[0]), 3)
        for i in range(len(classes)):
            if Lconfiance[i] == 0: continue
            confiance += ' - {} {}\n'.format(classes[i], Lconfiance[i])
        texte = "{}\n {}\n On vous propose la commande suivante car il faut bourrer son pantatlon: {}".format(test, confiance, sortie[0])
        self.zone.setPlainText(texte)

    def reset(self):
        self.logs = []
        self.zone.setPlainText('')


    





    