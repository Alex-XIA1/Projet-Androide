from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np


class Canvas(QWidget):
    def __init__(self, parent = None):
        print("class SimpleCanvas")
        super(Canvas,self).__init__()

        self.parent = parent
        self.setMinimumSize(500,500)
        self.setMouseTracking(True)
        self.cursorPos = None
        self.pStart = None

        # attributs d'affichage
        self.bkcolor = QColor(Qt.blue)
        self.width = 4
        self.painterTranslation = QPoint(0,0)

        # attributs memoire

        # TODO positions x,y à randomiser
        self.rect = QRect(200,200, 100, 50)

        # On brise la symetrie en superposant un rectangle par dessus
        self.rect2 = QRect(210,210,100,50)
        self.color = "blue"
        self.form = "drawRect"
        self.angle = 0
        self.objectifs = [QRect(0, 225, 50, 50), QRect(225, 0, 50, 50), QRect(225, 425, 50, 50), QRect(425, 225, 50, 50)]
        self.selected_obj = -1
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.translate(self.rect.center())
        painter.rotate(self.angle)
        painter.translate(-self.rect.center())


        if self.color != None:
            if self.color == "red":
                painter.setBrush(Qt.red)
            else: painter.setBrush(Qt.blue)
        if self.form != None:
            getattr(painter, self.form)(self.rect)
            painter.setBrush(Qt.magenta)
            getattr(painter, self.form)(self.rect2)

        
        #AFFICHAGE DES OBJECTIFS :
        #Remarque : afficher les objectifs en dernier pour les afficher par dessu la forme
        #           (axe Z)
        painter.resetTransform()
        painter.setBrush(Qt.red)
        self.selected_obj = -1
        for i in range (len(self.objectifs)) : 
            if (self.objectifs[i].contains(self.rect.center())) : 
                painter.setBrush(Qt.green)
                self.selected_obj = i
            else : 
                painter.setBrush(Qt.red)
            getattr(painter, "drawEllipse")(self.objectifs[i])

        #Affichage du centre de l'objet toujours en dernier
        painter.setBrush(Qt.cyan)
        painter.drawEllipse(self.rect.center(), 5, 5)

        

    def reset(self):
        # self.color = None
        # self.form = None
        self.rect = QRect(200,200, 100, 50)
        self.rect2 = QRect(210,210,100,50)
        self.angle = 0
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
        #self.parent.logger.addRow(etat1, etat2, "dessinRedRect")
        self.update()

    def dessinRect(self) : 
        etat1 = self.etat()
        self.form = "drawRect"
        etat2 = self.etat()
        #self.parent.logger.addRow(etat1, etat2, "dessinRect")
        self.update()

    def dessinEllipse(self) : 
        etat1 = self.etat()
        self.form = "drawEllipse"
        etat2 = self.etat()
        #self.parent.logger.addRow(etat1, etat2, "dessinEllipse")
        self.update()

    def dessinBlueRect(self) : 
        etat1 = self.etat()
        self.form = "drawRect"
        self.color = "blue"

        etat2 = self.etat()
        #self.parent.logger.addRow(etat1, etat2, "dessinBlueRect")
        self.update()

    def dessinRedEllipse(self) : 
        etat1 = self.etat()
        self.form = "drawEllipse"
        self.color = "red"

        etat2 = self.etat()
        #self.parent.logger.addRow(etat1, etat2, "dessinRedEllipse")
        self.update()

    def dessinBlueEllipse(self) : 
        etat1 = self.etat()
        self.form = "drawEllipse"
        self.color = "blue"

        etat2 = self.etat()
        #self.parent.logger.addRow(etat1, etat2, "dessinBlueEllipse")
        self.update()
        
    
    def setRed(self):
        if self.color == "red":
            return
        
        etat1 = self.etat()
        self.color = "red"
        etat2 = self.etat()
        #self.parent.logger.addRow(etat1, etat2, "setRed")
        self.update()

    def setBlue(self):
        if self.color == "blue":
            return 
        etat1 = self.etat()
        self.color = "blue"
        etat2 = self.etat()
        #self.parent.logger.addRow(etat1, etat2, "setBlue")
        self.update()
    
    def move_element(self, direction, scale = 1, jump = False):
        v = None
        if direction == 'Up':
            v = QPoint(0,-10)
        elif direction == 'Down':
            v = QPoint(0,10)
        elif direction == 'Left':
            v = QPoint(-10,0)
        elif direction == 'Right':
            v = QPoint(10,0)
        if v != None :
            m = direction
            if scale > 1:           
                m = 'Big ' + direction
            etat1 = self.stateMove()
            self.rect.translate(v*scale)
            self.rect2.translate(v*scale)
            etat2 = self.stateMove()

            self.parent.logger.addRow(etat1,etat2,m)
            self.update()

    def rotate_element(self, direction, scale = 1):
        v = None
        if direction == 'R':
            v = 10
        elif direction == 'E':
            v = -10
        if v != None:
            m = direction
            if scale > 1:
                m = 'Big '+direction
            etat1 = self.stateMove()
            self.angle += v*scale
            etat2 = self.stateMove()
            
            self.parent.logger.addRow(etat1,etat2,m)
            self.update()

    def stateMove(self):
        x, y , angle = self.rect.x(),self.rect.y(),self.angle
        return x, y ,angle