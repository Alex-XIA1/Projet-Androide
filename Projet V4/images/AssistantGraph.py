from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx
from pyvis.network import Network
from PyQt5.QtWebEngineWidgets import QWebEngineView

#CHECK THIS : https://christophergandrud.github.io/networkD3/#force


class AssistantGraph(QWidget) : 
    def __init__(self): 
        super(AssistantGraph, self).__init__()
        self.initUI()

    def initUI(self) : 
        grid = QGridLayout()
        self.setLayout(grid)

        self.figure = plt.figure()
        self.browser = QWebEngineView()
        grid.addWidget(self.browser, 0, 1, 9, 9) 
        self.drawGraph()

        self.show()

    def drawGraph(self):
        graph = Network()
        graph.add_nodes([1, 2, 3, 4])
        graph.add_edges([(1, 2), (2, 3), (3, 4), (2, 4)])
        graph.save_graph("network.html")
        f = QUrl.fromLocalFile("C:\Projects\pandrodie\P-Androide\P-Androide\\network.html")
        print
        self.browser.load(f)


if __name__ == '__main__':

    import sys  
    app = QApplication(sys.argv)
    assistant = AssistantGraph()
    assistant.show()
    sys.exit(app.exec_())