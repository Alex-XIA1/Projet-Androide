from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Canvas(QWidget):
    def __init__(self, parent = None):
        print("class Canvas")
        super(Canvas,self).__init__()
        self.setMinimumSize(300,300)
        self.setMouseTracking(True)
        self.cursorPos = None
        self.pStart = None

        # par défaut
        self.currentTool = "drawRect"
        self.bkcolor = Qt.blue
        self.width = 1
        self.Lforms = []
        self.mode = 'draw'
        self.selected = None
    
    
    def mousePressEvent(self, event):
        if self.mode == 'select':
            p = event.pos()
            for i in range(len(self.Lforms)-1, -1, -1):
                if self.Lforms[i][1].contains(p):
                    self.selected = self.Lforms.pop(i)
                    self.update()
                    break
        else:
            self.pStart = event.pos()
            self.cursorPos = event.pos()
            if self.mode=='draw':
                rect = QRect(self.pStart.x(), self.pStart.y(), 0, 0)
                self.Lforms.append([self.currentTool, rect, self.bkcolor])
    
    def mouseMoveEvent(self, event):
        if self.pStart != None:
            o_xt, o_yt = self.cursorPos.x() - self.pStart.x(), self.cursorPos.y() - self.pStart.y()
            self.cursorPos = event.pos()
            if self.mode=='draw':
                self.Lforms[-1][1].setBottomRight(self.cursorPos)

            elif self.mode=='move':
                xt, yt = self.cursorPos.x() - self.pStart.x(), self.cursorPos.y() - self.pStart.y()
                for _,form,_ in self.Lforms:
                    form.translate(xt-o_xt, yt-o_yt)
            self.update()

    def mouseReleaseEvent(self, event):
        self.cursorPos = event.pos()
        self.pStart = None
        
    def paintEvent(self, event):
        painter = QPainter(self)
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
        print("add object")

    def set_color(self, color):
        print("set color")
        if self.mode == 'select' and self.selected!=None and self.selected[1]!=color:
            self.selected[2] = color
            self.update()
        else:
            self.bkcolor = color

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
        if self.mode == "select" and mode!='select':
            self.Lforms.append(self.selected)
            self.selected = None
            self.update()
        self.mode = mode
        
    def deleteLastObject(self):
        self.Lforms.pop()
        self.update()