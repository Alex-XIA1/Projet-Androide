import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from SimpleCanvas import *
import resources
from Logger import Logger
from Model1 import test
from Assistant import Assistant



class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent )
        print( "init mainwindow")
        self.resize(500, 500)

        self.cont = QWidget(self)
        self.setCentralWidget(self.cont)
        self.canvas = Canvas(self)
        #self.setCentralWidget(self.canvas)
        
        
        
        self.logger = Logger("./data/data.csv")

        self.textEdit = QTextEdit(self.cont)

        layout = QVBoxLayout()

        sp = QSlider(Qt.Horizontal)
        sp.setMinimum(1)
        sp.setMaximum(10)
        sp.valueChanged.connect(self.scaleChange)
        
        layout.addWidget(sp)
        layout.addWidget(self.canvas)
        layout.addWidget(self.textEdit)

        bar = self.menuBar()
        # File Menu
        
        fileMenu = bar.addMenu("File")

        # Edit Menu
        colorMenu = bar.addMenu("Color")
        actPen = fileMenu.addAction(QIcon(":/icons/pen.png"), "&Pen color", self.pen_color, QKeySequence("Ctrl+P"))
        actBrush = fileMenu.addAction(QIcon(":/icons/brush.png"), "&Brush color", self.brush_color, QKeySequence("Ctrl+B"))
        
        L = ["dessinRedRect", "dessinBlueRect", "dessinRedEllipse", "dessinBlueEllipse", "setRed","setBlue", "dessinRect", "dessinEllipse"]
        for s in L:
            act= colorMenu.addAction(s)
            act.triggered.connect(getattr(self.canvas, s))
            colorMenu.addAction(act)
            
        self.cont.setLayout(layout)

    def closeEvent(self, event): 
        self.logger.file.close()
        event.accept()
        
    ##############
    def pen_color(self):
        self.log_action("choose pen color")

    def brush_color(self):
        self.log_action("choose brush color")

    def rectangle(self):
        self.log_action("Shape mode: rectangle")
        self.canvas.setTool("rectangle")

    def ellipse(self):
        self.log_action("Shape Mode: circle")
        self.canvas.setTool("ellipse")

    def free_drawing(self):
        self.log_action("Shape mode: free drawing")

    def move(self):
        self.log_action("Mode: move")
        self.canvas.setMode('move')

    def draw(self):
        self.log_action("Mode: draw")
        self.canvas.setMode('draw')

    def select(self):
        self.log_action("Mode: select")
        self.canvas.setMode('select')

    def save(self):
        image = self.canvas.getImage()
        image.save('image.png')

    def log_action(self, str):
        content = self.textEdit.toPlainText()
        self.textEdit.setPlainText( content + "\n" + str)

    def scaleChange(self, value):
        self.log_action("Action change")
        self.canvas.setScale(value)


def getData():
    print("GetData")
    df = pd.read_csv("data/train.csv")
    print(df.shape)
    print("Filter")
    df = df.drop_duplicates()
    X = df.to_numpy()
    X,Y = X[:,:-1], X[:,-1]
    return X,Y

if __name__=="__main__":
    # Hello
    model = test()
    app = QApplication(sys.argv)
    window = MainWindow()

    dock = QDockWidget('Assistant qui bourre le pantalon',window)
    test = QWidget(dock)
    dock.setWidget(test)
    doctext = QTextEdit(test)
    doctext.setReadOnly(True)
    window.addDockWidget(Qt.RightDockWidgetArea,dock)
    assist = Assistant(model, window,doctext)

    

    window.show()
    app.exec_()

