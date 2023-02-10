from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


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

        # attributs mode
        self.mode = 'draw'
        self.currentTool = "drawRect"

        # attributs memoire
        self.Lforms = []
        self.selected = None

        self.toTranslateX = 0
        self.toTranslateY = 0
        self.toScale = 1

        self.copy = None


    
    
    def mousePressEvent(self, event):
        if self.mode == 'select':
            p = event.pos()
            for i in range(len(self.Lforms)-1, -1, -1):
                if self.Lforms[i][1].contains(p):
                    if self.selected != None:
                        self.Lforms.append(self.selected)
                    self.selected = self.Lforms.pop(i)
                    self.update()
                    break
        else:
            self.pStart = event.pos() - self.painterTranslation
            self.cursorPos = event.pos()
            if self.mode=='draw':
                rect = QRect(self.pStart.x(), self.pStart.y(), 0, 0)
                self.Lforms.append([self.currentTool, rect, self.bkcolor])
    
    def mouseMoveEvent(self, event):
        if self.pStart != None:
            oldV = self.cursorPos - self.pStart
            self.cursorPos = event.pos()

            if self.mode=='draw':
                self.cursorPos-= self.painterTranslation
                self.Lforms[-1][1].setBottomRight(self.cursorPos)

            elif self.mode=='move':
                V = self.cursorPos - self.pStart - oldV
                self.painterTranslation += V
            self.update()

    def mouseReleaseEvent(self, event):
        if self.mode == 'draw':
            self.add_object()
        self.pStart = None
        
    def paintEvent(self, event):
        painter = QPainter(self)
     
        # painter.scale(float(self.toScale), float(self.toScale))

        painter.translate(self.painterTranslation)
        
        for affiche, form, c in self.Lforms:
            painter.setPen(QPen(c, self.width))
            painter.setBrush(c)
            getattr(painter, affiche)(form)

        if self.selected!=None:
            affiche, form, c = self.selected
            pen = QPen(Qt.cyan, 2,  Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(c)
            painter.setOpacity(0.6)
            getattr(painter, affiche)(form)


    def reset(self):
        print("reset")

    def add_object(self):
        affiche, form, c = self.Lforms[-1]
        s = ''
        if affiche == 'drawRect':
            s = 'rectangle '
        else:
            s = 'ellipse '
        print(form.getRect())
        x, y, w, h = form.getRect()
        color = c.getRgb()
        s = '{} {} {} {} {} {}'.format(s,x,y,w,h,color)
        self.parent.log_action(s)

    def set_color(self, color):
        print("set color")
        if self.mode == 'select' and self.selected!=None:
            if self.selected[1]!=color:
                self.selected[2] = color
                self.update()
        else:
            self.bkcolor = color
    
    def getImage(self):
        size = self.size()
        x, y = size.width(), size.height()
        image = QImage(x, y, QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(image)
        for affiche, form, c in self.Lforms:
            painter.setPen(QPen(c, self.width))
            painter.setBrush(c)
            getattr(painter, affiche)(form)

        if self.selected!=None:
            affiche, form, c = self.selected
            pen = QPen(Qt.cyan, 2,  Qt.DashLine)
            painter.setPen(pen)
            painter.setBrush(c)
            painter.setOpacity(0.6)
            getattr(painter, affiche)(form)
        return image


    @pyqtSlot()
    def setTool(self,tool):
        if self.mode == 'select':
            if self.selected!=None:
                if self.selected[0] == 'drawRect' and tool!='rectangle':
                    self.selected[0] = 'drawEllipse'
                    self.update()
                elif self.selected[0] == 'drawEllipse' and tool!='ellipse':
                    self.selected[0] = 'drawRect'
                    self.update()
        else:
            if tool == "rectangle":
                self.currentTool = "drawRect"
            else:
                self.currentTool = "drawEllipse"
    
    @pyqtSlot()
    def setMode(self, mode):
        if self.mode == "select" and mode!='select' and self.selected!=None:
            self.Lforms.append(self.selected)
            self.selected = None
            self.update()
        self.mode = mode

    @pyqtSlot()

    def setScale(self, value):
        if self.toScale != value : 
            self.toScale = value
            self.update()

    def copy_element(self):
        if self.mode == "select":
            self.copy = self.selected

    @pyqtSlot()
    def paste_element(self):
        if self.copy!=None:
            affiche, form, c = self.copy
            self.copy = affiche, form.translated(20, 20), c
            self.Lforms.append(self.copy)
            self.update()

        
    def deleteLastObject(self):
        self.Lforms.pop()
        self.update()