import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QScrollBar, QVBoxLayout, QWidget
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from graph import GraphWidget

class BigWidgetWithScrollBar(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a scroll area
        scroll_area = QScrollArea()
        self.setCentralWidget(scroll_area)

        # Create a large widget, in this case a QTextEdit
        self.text_edit = GraphWidget()
        self.text_edit.setFixedSize(5000, 500)

        # Set the QTextEdit widget as the scroll area's widget
        scroll_area.setWidget(self.text_edit)

        # Add a vertical scrollbar to the scroll area
        scrollbar = QScrollBar()
        scrollbar.setOrientation(0)  # Set orientation to vertical
        scroll_area.setVerticalScrollBar(scrollbar)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BigWidgetWithScrollBar()
    window.show()
    sys.exit(app.exec_())
