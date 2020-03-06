import operator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy 
from mpl_toolkits.mplot3d import Axes3D

#co_ord = pd.read_csv("file:///D:/Ball-tracking project/Ball tracking code/3demo.csv")
co_ord = pd.read_csv('co-ordinates1 (1).csv')

y_max_id= np.argmax(co_ord["y"].values) + 1
X_cord = co_ord["x"].iloc[y_max_id::]
Y_cord = co_ord["y"].iloc[y_max_id::]
z = np.polyfit(X_cord,Y_cord,2)
f = np.poly1d(z)

x_st = co_ord.x[(co_ord.y).idxmax(axis =1)]

#==========693 depend on camera placement=================#

X_TP = np.linspace(x_st,693,10)
Y_predict = f(X_TP)


max_index = (co_ord.y).idxmax(axis =1)
X_Fin = pd.concat([co_ord["x"][0:max_index+1],pd.Series(X_TP)],axis=0).reset_index()
Y_Fin = pd.concat([co_ord["y"][0:max_index+1],pd.Series(Y_predict)],axis=0).reset_index()
X_Fin = X_Fin.drop("index",axis=1)
Y_Fin = Y_Fin.drop("index",axis=1)

plt.plot(X_Fin,-Y_Fin)

Y_out = Y_Fin.iloc[len(Y_Fin)-1]


if int(Y_out) > (int(Y_Fin.iloc[y_max_id]) - 100):
    print("you ara out !!!")
    
else:
    print("Not Out Keep it up !!!")
    print("Ball missed the stumps by %f units "%((int(Y_Fin.iloc[y_max_id]) - 100) - int(Y_out)))

    
#plt.plot(co_ord['x'],-co_ord['y'])
