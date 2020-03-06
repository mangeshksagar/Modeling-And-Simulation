import numpy as np
import pandas as pd
from math import sin, cos, radians, atan
import matplotlib.pylab as plot
from mpl_toolkits import mplot3d
import random
import warnings
warnings.filterwarnings("ignore")
#%% constant
#pitchD = 20.12 #m
pitchD = 2.43 #m
stumpH = 0.711 #m
g = 9.8 #m/s

#%% input

df = pd.read_csv('co-ordinates1 (1).csv')

indx = df['y'].values.argmax()

df1 = df.iloc[indx::,:]

df1.drop_duplicates("y", keep='last' , inplace=True)

df1.reset_index(inplace=True)

boundD = 8 * 0.30 * df1.iloc[0,1] / df.iloc[-1,0] #meter
#boundD = 1.73

x = df1.iloc[1,1]
x1 = df1.iloc[2,1]

y = df1.iloc[1,2]
y1 = df1.iloc[2,2]

thetaAB = -atan( (y1 - y) / (x1 - x) )

dist = np.sqrt((y1 - y)**2 + (x1 - x)**2)

velAB = (dist * 30) * 0.01454 * 0.30 #m/s
#velAB = 3.35 #m/s

#%% function def
def getTime(speed, angle, pos):
    return (pos / (speed * cos(radians(angle))))

def getYPos(time, angle, speed):
    return (speed * sin(radians(angle)) * time - 0.5 * g * time**2)

def getXPos(time, angle, speed):
    return (speed * cos(radians(angle)) * time)

def getPosVec(pos, angle, speed):
    x = pitchD - pos
    percnt = np.linspace(0,1,50)
    X = x * percnt
    
    t=[]
    for i in range(len(X)):    
        T = (getTime(speed, angle, X[i])) #sec
        t.append(T)
        
    x1 = []
    y1 = []
    
    for k in t:
        x = getXPos(k, angle, speed)
        y = getYPos(k, angle, speed)
        x1.append(x)
        y1.append(y)
        
    y1 = [-1 * i for i in y1]
        
    p = [i for i, j in enumerate(y1) if j < 0] # Don't fall through the floor                          
    
    for i in sorted(p, reverse = True):
        del x1[i]
        del y1[i]
        
    return x1, y1

def plot3d(x_pts, y_pts):
    X = x_pts[::-1]
    Y = y_pts
    
#    print(X)
#    print(Y)
    
    fig = plot.figure(figsize=(8,5))
    
    ax = plot.axes([-0.1, 0.1, 1.2, 0.7],projection='3d',xlim=(0,2.43),zlim=(0,2.43),ylim=(-0.5,0.5))
    
    #ax = fig.add_subplot(111,projection='3d')
    
    ax.set_xlim3d([0.0, 2.43])
    ax.set_xlabel('length_of_pitch')
    
    ax.set_ylim3d([-0.5,0.5])
    ax.set_ylabel('Z')
    
    ax.set_zlim3d([0.0, 1.65])
    ax.set_zlabel('Height')
    
    ax.set_title('Pegion Vison')
    blues= plot.get_cmap('Reds')
#    colors = list(iter(blues(np.linspace(0,1,len(y1)))))
    
    plot.ion()
    
#    ax.plot([2.43,2.43],[0,0],[0,0.711],'b',lw = 2)
#    ax.plot([2.43,2.43],[-0.1145,-0.1145],[0,0.711],'b',lw = 2)
#    ax.plot([2.43,2.43],[0.1145,0.1145],[0,0.711],'b',lw = 2)
#    ax.plot([0.0,0.0],[0,0],[0,0.711],'b',lw = 2)
#    ax.plot([0.0,0.0],[-0.1145,-0.1145],[0,0.711],'b',lw = 2)
#    ax.plot([0.0,0.0],[0.1145,0.1145],[0,0.711],'b',lw = 2)
    
    ax.plot([2.43,2.43],[0,0],[0,0.711],'b',lw = 2)
    ax.plot([2.43,2.43],[-0.05,-0.05],[0,0.711],'b',lw = 2)
    ax.plot([2.43,2.43],[0.05,0.05],[0,0.711],'b',lw = 2)
    ax.plot([0.0,0.0],[0,0],[0,0.711],'b',lw = 2)
    ax.plot([0.0,0.0],[-0.05,-0.05],[0,0.711],'b',lw = 2)
    ax.plot([0.0,0.0],[0.05,0.05],[0,0.711],'b',lw = 2)
    
    z1 = np.zeros(np.shape(X)) #+ random.uniform(-0.4,0.4)
    
    ax.scatter3D(X,z1,Y,lw=1.5,color='r')
    
    if y2 <= stumpH and -0.05 <= z1[1] <= 0.05:
        ax.text(1.2, 1, 0.4, 'Out..!!')
    
    else:
        ax.text(1.2, 1, 0.4, 'Not Out..!!')
        
#%%
x2 = pitchD - boundD
time = getTime(velAB, thetaAB, x2) #sec
y2 = -getYPos(time, thetaAB, velAB)

print("\nHeight of ball at stumps: %0.2f m"%y2)

if y2 <= stumpH:
    print("\nOut !!")
else:
    print("\nNot Out !!")

x3, y3 = getPosVec(boundD, thetaAB, velAB)

plot3d(x3, y3)
#%%')