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

class AssistantGraph(QWidget) : 

    def __init__(self, model, app): 

        super(AssistantGraph, self).__init__()

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

        #Variables pour l'affichage de graph
        self.last_state_node = 1
        self.last_tmp_node = 0
        self.last_node_orientation = -1 #used to alternate between up and down 

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

        grid = QGridLayout()

        self.setLayout(grid)

        self.browser = QWebEngineView()
        # self.browser.setFixedSize(600, 200)

        grid.addWidget(self.browser, 0, 1, 9, 9) 
        
        self.setupGraph()

        self.show()

    def setupGraph(self):
        self.graph = Network()

        self.graph.add_node(1, label="1", x=0, y=0)

        self.graph.toggle_physics(False)


        self.graph.save_graph("network.html")
        f = QUrl.fromLocalFile("C:\\Users\\Nassim\\Desktop\\P-Androide AC\\network.html")
        # f = QUrl("http://127.0.0.1:8050/")
        
        self.browser.load(f)
        

    def updateEdges(self, state, etatFin, i , sortie, x) :
        newnode = self.last_state_node
        self.last_tmp_node += 1
        self.graph.add_node("tmp{}".format(self.last_state_node), x = (newnode - 2) * 100, y = self.last_node_orientation * 100, size = 10, color="red", label=sortie[0])
        self.last_node_orientation *= - 1
        self.graph.add_edge(newnode - i - 1, "tmp{}".format(self.last_state_node), color='red', width=2*i)
        self.graph.add_edge("tmp{}".format(self.last_state_node), newnode, color='red', width=2*i)
        
    def updateSuggestions(self) : 
        print("lol")


    def update(self, etatDep, etatFin, commande):
       
        #Movement = new State = new node on the graph and new edge (la commande de base)
        lastnode = self.last_state_node
        self.graph.add_node(lastnode + 1, label="{}".format(lastnode + 1), x = lastnode * 100, y = 0)
        self.graph.add_edge(lastnode, lastnode + 1, label=commande)

        #Commande a ajouter dans un hashmap
        if (not commande in self.sc_used.keys()) : 
            self.sc_used[commande] = 1
        else : 
            self.sc_used[commande] += 1

        self.last_state_node += 1

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
            # size - i, le nombre de etats sauté
            self.updateEdges(state, etatFin, size - i, sortie, x)
            
             #commande a ajouter dans un hashmap
            if (not sortie[0] in self.sc_reco.keys()) : 
                self.sc_reco[sortie[0]] = 1
            else : 
                self.sc_reco[sortie[0]] += 1
                
            break
        
        # ajoute l'etat precedent
        # supprime si la liste est trop grande
        self.logs.append(etatDep)
        
        #Check if is not using sc : 

        #Update the graphe
        self.graph.save_graph("network.html")
        
        self.browser.reload()
        # self.browser.scroll(100 * self.last_state_node, 0)

        page = self.browser.page()
        page.runJavaScript('scroll(0, 150)')
        # page.runJavaScript('scroll(100, 0)')

        if size >= self.max_size: self.logs.pop(0)

    def reset(self):
        print("reset")
        self.sc_used = dict()
        self.sc_reco = dict()

        self.last_node_orientation = 1
        self.last_state_node = 1
        self.last_tmp_node = 0
        self.setupGraph()

        # self.browser.repaint()
        return  
        #icone + combo + screenshot 

if __name__ == '__main__':
    import sys  

    app = QApplication(sys.argv)

    assistant = AssistantGraph()

    assistant.show()

    sys.exit(app.exec_())