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
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()

        children = window.findChildren(QAction)
        for c in children : 
            print(c.text())
            if (c.text() == "&Ellipse") : 
                c.activate(QAction.Trigger)

        playerThread = Thread(target=self.behaviour)
        playerThread.start()
        app.exec_()
        playerThread.join()
        

    def behaviour(self) : 
        time.sleep(1)
        self.random_draw()


    def random_draw(self) : 
        
        pyautogui.moveTo(750, 500, 0.2, pyautogui.easeOutQuad)
        pyautogui.drag(100, -100, 0.2, pyautogui.easeOutQuad,  button='left')

    def random_tool(self) : 
        print("qsd")
    
    def random_color(self) : 
        print("sdqsd")

    def random_shortcut(self) : 
        print("sdsqdsqd")


if __name__=="__main__":    
    player = Player()
    