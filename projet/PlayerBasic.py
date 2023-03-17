from MainWindow import MainWindow
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from SimpleCanvas import Canvas
from threading import Thread
import time
import random


#CE PLAYER VA LANCER DES COMMANDES ALEATOIRE PARMIS  3 : 
    #Changer de couleur entre rouge et bleu
    #Dessiner un rect de la couleur choisie 
    #Dessiner un rect rouge

    #L etat de l app est : 
    #(nbrCarréRouge, nbrCarréBleu, outilSelectioné)

    #Le fichier generé (logTest) contient : 
    #[AncienEtat, NouveauEtat, Commande]

    #Vous pouvez changer la variable nbIteration pour generer les données

class PlayerBasic() : 
    def __init__(self) : 
        self.app = QApplication(sys.argv) 
        window = MainWindow()
        window.show()

        #children va recevoir la liste des QAction de l'application
        children = window.findChildren(QAction)
        self.canvas = window.findChild(Canvas)
        self.nb_iteration = 30
        self.nb_restart = 1000
        print("\nOK\n")
        """self.actionsPossibles = [
            self.canvas.dessinRedRect, 
            self.canvas.dessinBlueRect,
            self.canvas.dessinRedEllipse, 
            self.canvas.dessinBlueEllipse,
            self.canvas.setRed,
            self.canvas.setBlue,
            self.canvas.dessinEllipse,
            self.canvas.dessinRect
        ]"""
        self.actionsPossibles = [
            (self.canvas.move_element, [["Up", "Down", "Left", "Right"], [1,2]]),
            (self.canvas.rotate_element, [['E', 'R'], [1,2]])
        ]


        playerThread = Thread(target=self.behaviour)
        playerThread.start()

        self.app.exec_()
        playerThread.join()
        
    def behaviour(self) : 
        time.sleep(1)
        print("\nOK\n")
        for x in range(self.nb_restart):
            for i in range(self.nb_iteration) :     
                f, Largs = random.choice(self.actionsPossibles)
                if len(Largs)==0:
                    f()
                else:
                    args = [random.choice(L) for L in Largs]
                    print("args: ",args)
                    f(*args)
            self.canvas.reset()
        self.app.quit()

if __name__ == '__main__':
    PlayerBasic()
    