from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np


class CanvasHelp(QWidget):
    def __init__(self, parent = None):
        print("class CanvasHelp")
        super(CanvasHelp,self).__init__()

        self.parent = parent
        self.setMinimumSize(500//2,500//2)
        self.setMouseTracking(True)
        self.cursorPos = None
        self.pStart = None

        # attributs d'affichage
        self.bkcolor = QColor(Qt.blue)
        self.width = 1
        self.painterTranslation = QPoint(0,0)

        # attributs memoire
        
        self.color = "blue"
        self.form = "drawRect"
        self.angle = np.random.randint(0,36) * 10
        self.objectifs = [QRect(0, 225//2, 50//2, 50//2), QRect(225//2, 0, 50//2, 50//2), QRect(225//2, 425//2, 50//2, 50//2), QRect(425//2, 225//2, 50//2, 50//2)]
        
        # Un des 4 point objectif
        alls = [(0,225//2), (225//2,0), (225//2,425//2),(425//2,225//2)]

        self.selected_obj = np.random.randint(0,3)
        self.rect = QRect(alls[self.selected_obj][0],alls[self.selected_obj][1], 100//2, 50//2)
        self.rect2 = QRect(alls[self.selected_obj][0]+4,alls[self.selected_obj][1]+4, 100//2, 50//2)
        
        
    def paintEvent(self, event):
        alls = [(0,225//2), (225//2,0), (225//2,425//2),(425//2,225//2)]

        self.rect = QRect(alls[self.selected_obj][0],alls[self.selected_obj][1], 100//2, 50//2)
        self.rect2 = QRect(alls[self.selected_obj][0]+4,alls[self.selected_obj][1]+4, 100//2, 50//2)

        painter = QPainter(self)
        painter.translate(self.rect.center())
        painter.rotate(self.angle)
        painter.translate(-self.rect.center())
        
        if self.color != None:
            painter.setBrush(Qt.blue)
        if self.form != None:
            getattr(painter, self.form)(self.rect)
            painter.setBrush(Qt.magenta)
            getattr(painter,self.form)(self.rect2)

        
        #AFFICHAGE DES OBJECTIFS :
        #Remarque : afficher les objectifs en dernier pour les afficher par dessu la forme
        #           (axe Z)
        painter.resetTransform()
        painter.setBrush(Qt.red)
        for i in range (len(self.objectifs)) : 
            if (i == self.selected_obj) : 
                painter.setBrush(Qt.green)
            else : 
                painter.setBrush(Qt.red)
            getattr(painter, "drawEllipse")(self.objectifs[i])
        

        #Affichage du centre de l'objet toujours en dernier, on le laisse un peu gros ici pour donner de la marge a l'utilisateur
        painter.setBrush(Qt.cyan)
        painter.drawEllipse(self.rect.center(), 5, 5)

        

