from MainWindow import MainWindow
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Canvas import *
import resources
import pyautogui
from threading import Thread
import time
import random
import Logger


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
        app = QApplication(sys.argv) 
        window = MainWindow()
        window.show()

        #children va recevoir la liste des QAction de l'application
        children = window.findChildren(QAction)
        self.canvas = window.findChild(Canvas)

        self.actionsPossibles = [
            self.canvas.dessinRect, 
            self.canvas.dessinRedRect, 
            self.canvas.swapColor
        ]

        playerThread = Thread(target=self.behaviour)
        playerThread.start()

        app.exec_()

        playerThread.join()
        
    def behaviour(self) : 
        time.sleep(1)

        nb_iteration = 1000
        for i in range(nb_iteration) :     
            f = random.choice(self.actionsPossibles)
            f()

    def random_action(self) : 
        print("Random action")       

    def random_draw(self) : 
        #Click sur un endroit dans le canvas puis drag la souris vers un autre endroit.
        #Aspect random non implementé encore
        print("random draw.")
        pyautogui.moveTo(750, 500, 0.2, pyautogui.easeOutQuad)
        pyautogui.drag(100, -100, 0.2, pyautogui.easeOutQuad,  button='left')

    def random_tool_sc(self) : 
        print("select random tool using a shortcut")

    def random_tool_md(self) : 
        print("select random tool using mouse drag")
    
    def random_color_sc(self) : 
        print("select color using shortcut")

    def random_color_md(self) : 
        print("select color using mouse drag")

    def random_shortcut(self) : 
        print("use a random shortcut")

    def random_button(self): 
        print("mousedrag to a random button")

if __name__=="__main__":    
    basicPlayer = PlayerBasic()
    