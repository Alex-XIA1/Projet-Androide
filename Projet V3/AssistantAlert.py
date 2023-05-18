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

class AssistantAlert(QWidget) : 

    def __init__(self, model, app): 

        super(AssistantAlert, self).__init__()

        # self.setFixedSize(600, 200)

        #Variables pour la recomendations
        self.model = model 
        self.testModel = testRaccourci(print_score=False)        
        self.app = app
        self.app.logger.Lobserver.append(self) 
        self.logs = []
        self.max_size = 5

        #Initialisation de l'interface 
        self.initUI()

        self.sc_used = dict()
        self.sc_reco = dict()



    def initUI(self) : 

        self.alert = QMessageBox()
        self.alert.setWindowTitle("Assistant")

        self.show()

    def updateAlert(self) :

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

        for key, value in self.sc_reco.items() : 
            if value > 10 : 
                self.alert.setText(key)
                self.alert.setInformativeText("You should use " + sc[key] + " more often")
                self.alert.exec_()
                self.sc_reco.pop(key)
                break


    def update(self, etatDep, etatFin, commande):
        #Commande a ajouter dans un hashmap
        if (not commande in self.sc_used.keys()) : 
            self.sc_used[commande] = 1
        else : 
            self.sc_used[commande] += 1

        #check si la commande a été recommendé : 
        if (commande in self.sc_reco.keys()) : 
            self.sc_reco.pop(commande)


        size = len(self.logs)
        # print()
        # print("size: ", size)

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
            self.updateAlert()

            
                
            break
        
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

    assistant = AssistantAlert()

    assistant.show()

    sys.exit(app.exec_())