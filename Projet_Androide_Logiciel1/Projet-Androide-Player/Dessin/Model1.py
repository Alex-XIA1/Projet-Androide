#import pydotplus
import numpy as np
import pandas as pd
from sklearn.linear_model import Perceptron
from sklearn.tree import DecisionTreeClassifier as DTree
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import time
import sklearn


def getData():
    print("GetData")
    df = pd.read_csv("data/train.csv")
    df = df.drop_duplicates()
    X = df.to_numpy()
    X,Y = X[:,:-1], X[:,-1]
    return X,Y

def generateData():
    PlayerBacic.PlayerBasic()

class Tree():
    def __init__(self):
        self.model = DTree()
        self.enc = sklearn.preprocessing.OneHotEncoder()
    def fit(self, X, Y):
        self.enc.fit(X)
        self.model.fit(self.enc.transform(X).toarray(), Y)

    def predict(self, x):
        return self.model.predict(self.enc.transform(x).toarray())
    
    def score(self, X, Y):
        return self.model.score(self.enc.transform(X).toarray(),Y)
    


def test():
    X, Y = getData()  
    # Classifier
    cf = Tree()
    cf.fit(X,Y)
    prediction = cf.predict(X)
    print("\nscore: ", cf.score(X,Y))
    for y in np.unique(Y):
        indices = Y == y
        print("Y: ", y, " - ", cf.score(X[indices],Y[indices]))
        for i in np.where(prediction[indices]!=y)[0]:
            print(X[indices][i], prediction[indices][i])
        print()
    return cf





if __name__=="__main__":
    """df = getData().to_numpy()
    X,Y = df[:,:-1], df[:,-1]
    n,d = X.shape
    cf = DTree(max_depth=d)
    cf.fit(X,Y)

    window = QApplication(sys.argv)
    window = MainWindow()

    assistant = Assistant(cf,window)

    assistT = Thread(target=self.behaviour)
    assistT.start()

    window.show()
    app.exec_()
    AssistT.join()"""
    test()

