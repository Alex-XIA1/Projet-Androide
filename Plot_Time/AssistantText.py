from time import time
from PyQt5.QtCore import *

from PyQt5.QtWidgets import *

from PyQt5.QtGui import *

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import networkx as nx

from networkx.algorithms import dag

from pyvis.network import Network

from PyQt5.QtWebEngineWidgets import QWebEngineView

import csv

import numpy as np

from utils import flatten_list

from Model1 import testRaccourci

class AssistantText(QWidget) : 

    def __init__(self, app, model, modeltest, size = 5, writer = None): 

        super(AssistantText, self).__init__()

        # self.setFixedSize(600, 200)

        #Variables pour la recomendations
        self.model = model 
        self.testModel = modeltest       
        self.app = app
        self.app.logger.Lobserver.append(self) 
        self.logs = []
        self.max_size = size
        self.writer = writer

        #Initialisation de l'interface 
        self.initUI()

        #Variables a sauvegarder : 
        # self.nbr_shortcut_used = 0
        # self.nbr_big_r = 0              #nbr de big right
        # self.nbr_big_l = 0              #nbr de big left
        # self.nbr_big_u = 0              #nbr de big up
        # self.nbr_big_d = 0              #nbr de big down
        # self.nbr_big_rl = 0             #nbr de big rotation right
        # self.nbr_big_rr = 0             #nbr de big rotation left
        self.sc_used = dict()
        self.sc_reco = dict()




    def initUI(self) : 

        vbox = QVBoxLayout()
        vbox.addStretch()
        
        #self.setStyleSheet('background-color: lightblue;')
        self.setLayout(vbox)

        self.recomendations = QLabel()
        self.recomendations.setStyleSheet('font-size: 16px;')
        
        self.importantRecomendations = QLabel()
        self.importantRecomendations.setStyleSheet('color : red; font-weight: bold;font-size: 16px;')
        
        vbox.addWidget(self.importantRecomendations)
        vbox.addWidget(self.recomendations)

        self.show()

    def updateRecomendations(self) :

        sc = {
            "Up": "Z",
            "Down": "S",
            "Left": "Q",
            "Right": "D",
            "R": "R",
            "E": "E", 
            "Big Up": "Ctrl+Z",
            "Big Down": "Ctrl+S",
            "Big Left": "Ctrl+Q",
            "Big Right": "Ctrl+D",
            "Big R": "Ctrl+R",
            "Big E": "Ctrl+E"
        }

        lb = [] 
        li = []
        for key, value in self.sc_reco.items() : 
            if value > 10 : 
                li.append({"commande" : key, "nbr": value})
            else : 
                lb.append({"commande" : key, "nbr": value})
        content = ""
        importantContent = ""
        
        for e in sorted(lb, key=lambda d : d["nbr"], reverse=True) : 
            content += e["commande"] + " (" + sc[e["commande"]]+ ") : " + str(e["nbr"]) +"\n"

        for e in sorted(li, key=lambda d : d["nbr"], reverse=True) : 
            importantContent += e["commande"] + " (" + sc[e["commande"]]+ ") : " + str(e["nbr"]) +"\n"

        self.recomendations.setText(content)
        self.importantRecomendations.setText(importantContent)


    def update(self, etatDep, etatFin, commande):
        #Commande a ajouter dans un hashmap
        if (not commande in self.sc_used.keys()) : 
            self.sc_used[commande] = 1
        else : 
            self.sc_used[commande] += 1

        #check si la commande a été recommendé : 
        if (commande in self.sc_reco.keys()) : 
            self.sc_reco.pop(commande)
            self.updateRecomendations()


        size = len(self.logs)
        # print()
        # print("size: ", size)

        # Recherche de la commande
        t1 = time()
        num = -1
        for i in range(size): 
            state = self.logs[i]
            # cree la donnee a predire
            x = [flatten_list([state, etatFin])] 
            if state == etatFin: continue  
            if self.testModel.predict(x) == "No": continue
            if self.model.predict_proba(x).max() < 0.6:
                continue # test si y a un possible raccourci ou non
            #self.testModel.afficheConfiance(x) # affiche la confiance dans ce test
            sortie = self.model.predict(x) # predit le raccourci
            # Si true on dit a l'utilisateur d'utiliser la commande en sortie


             #commande a ajouter dans un hashmap
            if (not sortie[0] in self.sc_reco.keys()) : 
                self.sc_reco[sortie[0]] = 1
            else : 
                self.sc_reco[sortie[0]] += 1


            #Update the list of recomendations
            self.updateRecomendations()
            num = i
            break

        if self.writer is not None:
            print("num: %d" %num)
            self.writer.writerow([self.max_size, time()-t1, num])


        
        # ajoute l'etat precedent
        # supprime si la liste est trop grande
        self.logs.append(etatDep)
        
        #Check if is not using sc : 
        # page.runJavaScript('scroll(100, 0)')

        if size >= self.max_size: self.logs.pop(0)

    def reset(self):
        print("reset")
        self.sc_used = dict()
        self.sc_reco = dict()

        return  
        #icone + combo + screenshot 

if __name__ == '__main__':
    import sys  

    app = QApplication(sys.argv)

    assistant = AssistantText()

    assistant.show()

    sys.exit(app.exec_())