import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('data/time.csv', names=['size', 'time', 'pred'])
data = df.to_numpy()
n = data.shape[0]

plt.subplot(2,1,1)
plt.scatter(data[:,0]+np.random.randn(n)*0.5, data[:,1], alpha=0.1)
X = np.unique(data[:, 0])
Y = []
for x in X:
    print(x)
    index = data[:,0] == x
    Y.append(data[index][:,1].mean())
plt.scatter(X,Y, label='moyenne')

plt.xlabel("Evolution du temps de réponse\n selon la taille de l'horizon")
plt.ylabel("temps")
plt.legend()

plt.subplot(2,1,2)
plt.scatter(data[:,0]+np.random.randn(n)*0.5, data[:,2], alpha=0.1)
plt.xlabel("Evolution du nombre de prédiction avant succès\n selon la taille de l'horizon")
plt.ylabel("nombre de predict avant succès")

plt.tight_layout()
plt.show()