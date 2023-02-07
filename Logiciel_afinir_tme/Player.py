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


class Player() : 
    def __init__(self) : 
        #Le player commence par créer une instance de l'application sur laquelle il va lancer des test
        #Remarque : Creation de l'app peut se faire ne dehors du player si vous voulez ¯\_(ツ)_/¯
        app = QApplication(sys.argv) 
        window = MainWindow()
        window.show()

        #children va recevoir la liste des QAction de l'application
        children = window.findChildren(QAction)
        
        #Exemple activer l'ellipse
        for c in children : 
            print(c.text())
            if (c.text() == "&Ellipse") : 
                c.activate(QAction.Trigger)

        #Creation d'un thread pour le Player 
        #AU total : 2 thread (pour le Player et pour l'application)
        #Ca permet de ne pas faire lagé l'application si le player decide d'attendre. 
        playerThread = Thread(target=self.behaviour)
        playerThread.start()
        
        
        app.exec_()
        
        #Jointure des thread (destruction)
        playerThread.join()
        

    def behaviour(self) : 
        #Player attend 1sec avant de commencer sa behaviour histoire d'attendre que l'application se charge completement
        time.sleep(1)

        self.random_draw()


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

    player = Player()
    