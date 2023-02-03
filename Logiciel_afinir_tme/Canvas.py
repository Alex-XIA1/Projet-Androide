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
        self.currentTool = "rectangle"
        self.bkcolor = Qt.blue
        self.width = 1
        self.rectangle = [] # (x,y, length, height)
        self.ellipse = [] # (x,y, length, height)
        self.mode = 'draw'
    
    
    def mousePressEvent(self, event):
        self.pStart = event.pos()
        self.cursorPos = event.pos()
        if self.mode=='draw':
            if self.currentTool=='rectangle':
                self.rectangle.append([self.pStart.x(), self.pStart.y(), 0, 0, self.bkcolor])
            else:
                self.ellipse.append([self.pStart.x(), self.pStart.y(), 0, 0, self.bkcolor])

    
    def mouseMoveEvent(self, event):
        if self.pStart != None:
            o_xt, o_yt = self.cursorPos.x() - self.pStart.x(), self.cursorPos.y() - self.pStart.y()
            self.cursorPos = event.pos()
            xt, yt = self.cursorPos.x() - self.pStart.x(), self.cursorPos.y() - self.pStart.y()
            if self.mode=='draw':
                if self.currentTool=='rectangle':
                    self.rectangle[-1][2] = xt
                    self.rectangle[-1][3] = yt
                else:
                    self.ellipse[-1][2] = xt
                    self.ellipse[-1][3] = yt

            elif self.mode=='move':
                for i in range(len(self.rectangle)):
                    x,y,l,h,c = self.rectangle[i]
                    self.rectangle[i] = x+xt-o_xt, y+yt-o_yt, l,h,c

                for i in range(len(self.ellipse)):
                    x,y,l,h,c = self.ellipse[i]
                    self.ellipse[i] = x+xt-o_xt, y+yt-o_yt, l,h,c   
            self.update()
        
        

    def mouseReleaseEvent(self, event):
        self.cursorPos = event.pos()
        self.pStart = None
        




    def paintEvent(self,event):
        painter = QPainter(self)

        for x,y,l,h,c in self.rectangle:
            pen = QPen(c)
            pen.setWidth(self.width)
            painter.setPen(pen)
            painter.setBrush(c)
            painter.drawRect(x,y,l,h)
        
        for x,y,l,h,c in self.ellipse:
            pen = QPen(c)
            pen.setWidth(self.width)
            painter.setPen(pen)
            painter.setBrush(c)
            painter.drawEllipse(x,y,l,h)


        #if self.cursorPos != None:
        #    painter.drawRect(self.cursorPos.x()-5, 
        #    self.cursorPos.y()-5,100,100)

    def reset(self):
        print("reset")

    def add_object(self):
        print("add object")

    def set_color(self, color ):
        print("set color")

    @pyqtSlot()
    def setTool(self,tool):
        if self.currentTool != tool :
            self.currentTool = tool
            print("Tool:", self.currentTool)
    
    @pyqtSlot()
    def setCol(self,qtcol):
        if self.bkcolor != qtcol :
            self.bkcolor = qtcol
            print("bkcolor:", self.bkcolor)
    
    @pyqtSlot()
    def setMode(self, mode):
        if self.mode != mode:
            self.mode = mode