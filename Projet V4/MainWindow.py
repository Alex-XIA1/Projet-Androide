import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from SimpleCanvas import *
import resources
from Logger import Logger
from Model1 import test
from Assistant import Assistant
from Experience import MainWindow
from AssistantGraph import AssistantGraph
from AssistantText import AssistantText
from AssistantAlert import AssistantAlert
from functools import partial
from CanvasHelp import *


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My PyQt App')
        self.setGeometry(0, 0, 1600, 900)

        
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setGeometry(0, 0, 1600, 900)
        #Creation de la page d'acceuil ##########################################################################
        self.initial_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.label = QLabel('Bonjour et bienvenu ! Veuillez cliquer sur le boutton pour lancer l\'experience', self.initial_widget)
        layout.addWidget(self.label)

        self.button = QPushButton('Lancer l\'experience', self.initial_widget)
        layout.addWidget(self.button)

        self.initial_widget.setLayout(layout)
        self.stacked_widget.addWidget(self.initial_widget)

        #Creation de la page de fin ##########################################################################
        self.final_widget = QWidget()
        finallayout = QVBoxLayout()
        finallayout.setAlignment(Qt.AlignCenter)
        self.recoLabel = QLabel("")
        self.usedLabel = QLabel("")
        finallayout.addWidget(self.recoLabel)
        finallayout.addWidget(self.usedLabel)
        self.final_widget.setLayout(finallayout)
        self.stacked_widget.addWidget(self.final_widget)

        #Creation de la page de test ##########################################################################

        modelOn = True
        self.main_widget = MainWindow(save = False)
        
        if modelOn:
            model = test(print_score = False)

            dockAssist = QDockWidget("Assistant", self.main_widget)
            dockAssist.setMinimumSize(300, 100)
            self.main_widget.addDockWidget(Qt.RightDockWidgetArea,dockAssist)

            dock = QDockWidget('Objectif ',self.main_widget)
            dock.setMinimumSize(300, 100)
            self.main_widget.addDockWidget(Qt.RightDockWidgetArea,dock)
            
            # Container
            container = QWidget()
            dock.setWidget(container)
            layout = QVBoxLayout(container)
            
            assistContainer = QWidget()
            dockAssist.setWidget(assistContainer)
            assistContaienrLayout = QVBoxLayout(assistContainer)
            
    ###########################     ASSISTANT     #################################
            
            #assist = AssistantGraph(model, self.main_widget)
            assist = AssistantText(model, self.main_widget)
            #assist = AssistantAlert(model, self.main_widget)

            self.assist = assist
    ###############################################################################
            
            # Help
            self.main_widget.objectif = (self.main_widget.helper.selected_obj, self.main_widget.helper.angle)

            # Bouton reset
            button = QPushButton("Reset Assistant")
            button.clicked.connect(assist.reset)

            assistContaienrLayout.addWidget(button)
            assistContaienrLayout.addWidget(assist)
            layout.addWidget(self.main_widget.helper)
            self.stacked_widget.addWidget(self.main_widget)
    

        self.show()
        self.button.clicked.connect(self.on_button_click)
    
    def on_button_click(self):
        self.stacked_widget.setCurrentWidget(self.main_widget)
        
        self.main_widget.setFocus()
    
    def test_end(self) : 
        self.stacked_widget.setCurrentWidget(self.final_widget)
        used = "-Shortcuts used-\n"
       
        for key, value in self.assist.sc_used.items() : 
            used += key + " : " + str(value) + "\n"

        self.usedLabel.setText(used)
        self.usedLabel.setStyleSheet("font-size:16px;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(app.exec_())

