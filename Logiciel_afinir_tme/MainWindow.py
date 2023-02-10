import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Canvas import *
import resources

class MainWindow(QMainWindow):
    def __init__(self, parent = None ):
        QMainWindow.__init__(self, parent )
        print( "init mainwindow")
        self.resize(1200, 1000)

        self.cont = QWidget(self)
        self.setCentralWidget(self.cont)
        self.canvas = Canvas(self)
        #self.setCentralWidget(self.canvas)
        

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
        editMenu = bar.addMenu("Edit")
        actCopy= editMenu.addAction("Copy")
        actCopy.triggered.connect(lambda: self.canvas.copy_element())

        actPaste=  editMenu.addAction("Paste")
        actPaste.triggered.connect(lambda: self.canvas.paste_element())

        # Menu Color
        colorMenu = bar.addMenu("Color")
        actPen = fileMenu.addAction(QIcon(":/icons/pen.png"), "&Pen color", self.pen_color, QKeySequence("Ctrl+P"))
        


        actBrush = fileMenu.addAction(QIcon(":/icons/brush.png"), "&Brush color", self.brush_color, QKeySequence("Ctrl+B"))
        
        actRed = colorMenu.addAction("Rouge")
        actRed.triggered.connect(lambda: self.canvas.set_color(QColor(Qt.red)))
        colorMenu.addAction(actRed)

        actBlue = colorMenu.addAction("Bleu")
        actBlue.triggered.connect(lambda: self.canvas.set_color(QColor(Qt.blue)))
        colorMenu.addAction(actBlue)

        actGreen = colorMenu.addAction("Vert")
        actGreen.triggered.connect(lambda: self.canvas.set_color(QColor(Qt.green)))
        colorMenu.addAction(actGreen)

        actOther = colorMenu.addAction("Autre")
        actOther.triggered.connect(lambda: self.canvas.set_color(QColorDialog.getColor()))
        colorMenu.addAction(actOther)

        colorToolBar = QToolBar("Color")
        self.addToolBar( colorToolBar )
        
        colorToolBar.addAction( actPen )
        colorToolBar.addAction( actBrush )

        shapeMenu = bar.addMenu("Shape")
        actRectangle = shapeMenu.addAction(QIcon(":/icons/rectangle.png"), "&Rectangle", self.rectangle )
        actEllipse = shapeMenu.addAction(QIcon(":/icons/ellipse.png"), "&Ellipse", self.ellipse)
        actFree = shapeMenu.addAction(QIcon(":/icons/free.png"), "&Free drawing", self.free_drawing)

        actSave = fileMenu.addAction(QIcon(":/image/images/save.png"), "&Save", self.save)

        shapeToolBar = QToolBar("Shape")
        self.addToolBar( shapeToolBar )
        shapeToolBar.addAction( actRectangle )
        shapeToolBar.addAction( actEllipse )
        shapeToolBar.addAction( actFree )

        modeMenu = bar.addMenu("Mode")
        actMove = modeMenu.addAction(QIcon(":/icons/move.png"), "&Move", self.move)
        actDraw = modeMenu.addAction(QIcon(":/icons/draw.png"), "&Draw", self.draw)
        actSelect = modeMenu.addAction(QIcon(":/icons/select.png"), "&Select", self.select)

        

        modeToolBar = QToolBar("Navigation")
        self.addToolBar( modeToolBar )
        modeToolBar.addAction( actMove )
        modeToolBar.addAction( actDraw )
        modeToolBar.addAction( actSelect )
        modeToolBar.addAction
        self.cont.setLayout(layout)


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

if __name__=="__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()
