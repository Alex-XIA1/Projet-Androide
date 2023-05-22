import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from SimpleCanvas import *
import resources
from Logger import Logger
from Model1 import test
from Assistant import Assistant
from AssistantGraph import AssistantGraph
from AssistantText import AssistantText
from AssistantAlert import AssistantAlert
from functools import partial
from CanvasHelp import *

class MainWindow(QMainWindow):
    def __init__(self, parent = None, save = True):
        QMainWindow.__init__(self, parent )
        print( "init mainwindow")
        self.resize(1600, 900)

        self.cont = QWidget(self)
        self.setCentralWidget(self.cont)
        self.canvas = Canvas(self)
        self.setFocus()        
        self.logger = Logger("./data/data.csv", save)

        self.textEdit = QTextEdit(self.cont)
        self.textEdit.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        #layout.addWidget(self.textEdit)
        bar = self.menuBar()

        #Variables pour l'experience : 
        self.objectif = (-1, 0)          #(objectif, angleRotation) : Va etre setup par le CanvasHelp 
        self.helper = CanvasHelp("Help")
        self.nbr_test_t = 3             #Nombre de test a faire
        self.nbr_test = 0                #Nombre de tests fait

            #Variables a sauvegarder : 
        self.nbr_shortcut_used = 0
        


        # Edit Menu
        colorMenu = bar.addMenu("Color")
        L = ["dessinRedRect", "dessinBlueRect", "dessinRedEllipse", "dessinBlueEllipse", "setRed","setBlue", "dessinRect", "dessinEllipse"]
        for s in L:
            act= colorMenu.addAction(s)
            act.triggered.connect(getattr(self.canvas, s))
            colorMenu.addAction(act)

        moveMenu = bar.addMenu("Move")
        self.addMoveFeature(moveMenu)
        rotateMenu = bar.addMenu("Rotate")
        self.addRotateFeature(rotateMenu)
        self.cont.setLayout(layout)

    def closeEvent(self, event): 
        # self.logger.file.close()
        event.accept()
        
    ##############
    def rectangle(self):
        self.log_action("Shape mode: rectangle")
        self.canvas.setTool("rectangle")

    def ellipse(self):
        self.log_action("Shape Mode: circle")
        self.canvas.setTool("ellipse")

    def move(self):
        self.log_action("Mode: move")
        self.canvas.setMode('move')

    def save(self):
        image = self.canvas.getImage()
        image.save('image.png')

    def log_action(self, str):
        content = self.textEdit.toPlainText()
        self.textEdit.setPlainText( content + "\n" + str)
    
    def addMoveFeature(self, menu):
        # MoveElement
        scale = 2
        L = ["Up", "Left", "Right", "Down"]
        for cmd in L: 
            action =  menu.addAction(cmd)
            action.setShortcuts(QKeySequence("Ctrl+%s"%cmd))
            action.triggered.connect(partial(self.canvas.move_element, cmd, scale))
            action.triggered.connect(partial(self.log_action,"Move: Big %s (%d)" %(cmd, scale)))
            menu.addAction(action)


    def addRotateFeature(self, menu):
        scale = 2
        action =  QAction("RotateLeft", self)
        action.setShortcuts(QKeySequence("Ctrl+E"))
        action.triggered.connect(lambda: self.canvas.rotate_element("E", scale))
        action.triggered.connect(lambda: self.log_action("Rotate: Big Left (%d)" %scale))
        self.addAction(action)

        action =  QAction("RotateRight", self)
        action.setShortcuts(QKeySequence("Ctrl+R"))
        action.triggered.connect(lambda: self.canvas.rotate_element("R", scale))
        action.triggered.connect(lambda: self.log_action("Rotate: Big Right (%d)" %scale))
        self.addAction(action)

    
    def keyPressEvent(self, event):
        k = event.key()
        #print(k)
        if k == Qt.Key_Up:
            self.canvas.move_element('Up')
        elif k == Qt.Key_Down:
            self.canvas.move_element('Down')
        elif k == Qt.Key_Left:
            self.canvas.move_element("Left")
        elif k == Qt.Key_Right:
            self.canvas.move_element('Right')
        elif k == Qt.Key_R:
            self.canvas.rotate_element('R')
        elif k == Qt.Key_E:
            self.canvas.rotate_element('E')

    def nextTest(self) : 
        print("Objectif réussi. Lancement du nouveau test. ")
        self.canvas.reset()
        self.helper.angle = np.random.randint(0,36) * 10
        self.helper.selected_obj = np.random.randint(0,3)
        self.objectif = (self.helper.selected_obj, self.helper.angle)
        self.nbr_test += 1
        #self.helper.update()
        if (self.nbr_test_t > self.nbr_test) : 
            self.helper.update()
        else :
            self.parent().parent().test_end()

if __name__=="__main__":
    # Hello
    modelOn = True
    app = QApplication(sys.argv)
    window = MainWindow(save = False)
    
    if modelOn:
        model = test(print_score = False)

        dockAssist = QDockWidget("Assistant", window)
        dockAssist.setMinimumSize(300, 100)
        window.addDockWidget(Qt.RightDockWidgetArea,dockAssist)


        dock = QDockWidget('Objectif ',window)
        dock.setMinimumSize(300, 100)
        window.addDockWidget(Qt.RightDockWidgetArea,dock)
        
        # Container
        container = QWidget()
        dock.setWidget(container)
        layout = QVBoxLayout(container)
        
        assistContainer = QWidget()
        dockAssist.setWidget(assistContainer)
        assistContaienrLayout = QVBoxLayout(assistContainer)
        
###########################     ASSISTANT     #################################
        
        #assist = AssistantGraph(model, window)
        assist = AssistantText(model, window)
        #assist = AssistantAlert(model, window)

###############################################################################

        # Help
        window.objectif = (window.helper.selected_obj, window.helper.angle)

        # Bouton reset
        button = QPushButton("Reset Assistant")
        button.clicked.connect(assist.reset)

        assistContaienrLayout.addWidget(button)
        assistContaienrLayout.addWidget(assist)
        layout.addWidget(window.helper)
        

        window.show()
        app.exec_()
       

