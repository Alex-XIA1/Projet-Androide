import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class GraphWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.start = False
        self.x = 100
        self.y = 100

        self.node_size = 40
        self.interval = 100
        self.y_line = self.y + self.node_size/2

        self.pixmap = QPixmap(10000, 500)
        self.pixmap.fill()
        self.node_id = 1
        self.add_node()

    def on_horizontal_scrollbar_moved(self, value):
        self.scroll_area.horizontalScrollBar().setValue(value)

    def add_node(self, label = None):
        self.x += self.interval
        # Draw edges
        painter = QPainter(self.pixmap)
        pen = QPen(Qt.black)
        painter.setPen(pen)
        
        # Edges
        if self.start:
            path = QPainterPath()
            a, b = self.x - self.interval +self.node_size/2, self.y
            c, d = self.x + self.node_size/2, self.y
            path.moveTo(a,b)
            c1 = QPointF(a+self.interval/2 - 15, self.y + 15)
            c2 = QPointF(a+self.interval/2 - 15, self.y - 50)
            path.cubicTo(c1, c2, QPointF(c,d))
            painter.drawPath(path)

            painter.drawLine(self.x - self.interval + self.node_size, self.y_line , self.x, self.y_line)
        else:
            self.start = True
        painter.drawEllipse(self.x, self.y, self.node_size, self.node_size)
        painter.drawText(self.x+self.node_size/2 - 3, self.y + self.node_size + 20, str(self.node_id))
        self.node_id+=1
        painter.end()

    def mousePressEvent(self, event):
        self.add_node()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pixmap)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create the MapDisplay widget
        map_display = GraphWidget()

        # Create a QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(map_display)

        # Create a QBoxLayout and set it as the layout for the QScrollArea
        box_layout = QVBoxLayout()
        self.setLayout(box_layout)

        layout.addWidget(scroll_area)



if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()



    

"""if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = QMainWindow()
    graph_widget = GraphWidget()
    window.setCentralWidget(graph_widget)
    window.setGeometry(100, 100, 800, 600)
    window.show()

    sys.exit(app.exec_())"""