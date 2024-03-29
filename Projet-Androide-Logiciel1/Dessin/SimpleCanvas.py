from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np


class Canvas(QWidget):
    def __init__(self, parent = None):
        print("class Canvas")
        super(Canvas,self).__init__()

        self.parent = parent

        self.setMinimumSize(300,300)
        self.setMouseTracking(True)
        self.cursorPos = None
        self.pStart = None

        # attributs d'affichage
        self.bkcolor = QColor(Qt.blue)
        self.width = 1
        self.painterTranslation = QPoint(0,0)

        # attributs memoire
        self.rect = QRect(100,100, 100, 100)
        self.color = None
        self.form = None
        
    def paintEvent(self, event):
        painter = QPainter(self)
        if self.color != None:
            if self.color == "red":
                painter.setBrush(Qt.red)
            else: painter.setBrush(Qt.blue)
        if self.form != None:
            getattr(painter, self.form)(self.rect)

    def reset(self):
        self.color = None
        self.form = None
        self.update()


    def set_color(self, color):
        print("set color")
        if self.mode == 'select' and self.selected!=None:
            if self.color!=color:
                self.color = color
                self.update()
        else:
            self.bkcolor = color

    @pyqtSlot()
    def setTool(self,tool):
        if tool == "rectangle":
            self.form = "drawRect"
        else:
            self.form = "drawEllipse"


################################################################
#Fonctions pour le test du players
    def etat(self):
        a = self.form
        b = self.color
        if a == None:
            a = "Rien"
        if b == None:
            b = "Rien"
        return (a, b)

    def dessinRedRect(self) : 
        etat1 = self.etat()
        self.form = "drawRect"
        self.color = "red"

        etat2 = self.etat()
        self.parent.logger.addRow(etat1, etat2, "dessinRedRect")
        self.update()

    def dessinRect(self) : 
        etat1 = self.etat()
        self.form = "drawRect"
        etat2 = self.etat()
        self.parent.logger.addRow(etat1, etat2, "dessinRect")
        self.update()

    def dessinEllipse(self) : 
        etat1 = self.etat()
        self.form = "drawEllipse"
        etat2 = self.etat()
        self.parent.logger.addRow(etat1, etat2, "dessinEllipse")
        self.update()

    def dessinBlueRect(self) : 
        etat1 = self.etat()
        self.form = "drawRect"
        self.color = "blue"

        etat2 = self.etat()
        self.parent.logger.addRow(etat1, etat2, "dessinBlueRect")
        self.update()

    def dessinRedEllipse(self) : 
        etat1 = self.etat()
        self.form = "drawEllipse"
        self.color = "red"

        etat2 = self.etat()
        self.parent.logger.addRow(etat1, etat2, "dessinRedEllipse")
        self.update()

    def dessinBlueEllipse(self) : 
        etat1 = self.etat()
        self.form = "drawEllipse"
        self.color = "blue"

        etat2 = self.etat()
        self.parent.logger.addRow(etat1, etat2, "dessinBlueEllipse")
        self.update()
        
    
    def setRed(self):
        if self.color == "red":
            return
        
        etat1 = self.etat()
        self.color = "red"
        etat2 = self.etat()
        self.parent.logger.addRow(etat1, etat2, "setRed")
        self.update()

    def setBlue(self):
        if self.color == "blue":
            return 
        etat1 = self.etat()
        self.color = "blue"
        etat2 = self.etat()
        self.parent.logger.addRow(etat1, etat2, "setBlue")
        self.update()
    

