import numpy as np
from math import sin, cos, radians, atan, degrees
import matplotlib.pylab as plot
from mpl_toolkits import mplot3d
import random
#%matplotlib qt
#%% constant
pitchD = 20.12 #m
stumpH = 0.71 #m
g = 9.8 #m/s
COR = 0.65 #for tennis ball
COF = 0.6 #for tennis ball

#%% input
#bounceD = 18 #m dist of ball bounce from bowler end
vi = 40 #m/s
thetai = -10 #deg from bowler hand
#v0 = 10 #m/s
#theta = 30 #deg
heigth = 2 #m ball release height

#%% function def
def getTime(speed, angle, pos):
    return (pos / (speed * cos(radians(angle))))

def getYPos(time, angle, speed):
    return (speed * sin(radians(angle)) * time - 0.5 * g * time**2)

def getXPos(time, angle, speed):
    return (speed * cos(radians(angle)) * time)

def getVySpeed(speed, time, angle):
    return (speed * sin(radians(angle)) + g * time)

def getImpactPos(angle, speed, ht):
    t = ((-speed * sin(radians(angle))) + np.sqrt( (speed * sin(radians(angle)))**2 - 2 * -g * ht ) ) / -g
    b = ((-speed * sin(radians(angle))) - np.sqrt( (speed * sin(radians(angle)))**2 - 2 * -g * ht ) ) / -g

    if t < 0:
        t = b
    
    dist = getXPos(t, angle, speed)

    vyo = getVySpeed(speed, t, angle)
    vxo = speed * cos(radians(angle))

    theta = atan(vyo / vxo)
    
    vo = np.sqrt(vxo**2 + vyo**2)
    
    return dist, degrees(theta), vo

def getPosVec(pos, angle, speed):
    x = pitchD - pos
    percnt = np.linspace(0,1,100)
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
        
    p = [i for i, j in enumerate(y1) if j < 0] # Don't fall through the floor                          
    
    for i in sorted(p, reverse = True):
        del x1[i]
        del y1[i]
        
    return x1, y1

def getPosVec1(pos, angle, speed):
    
#pos = bounceD
#angle = thetai
#speed = vi

    x = pos
    percnt = np.linspace(0,1,100)
    X = x * percnt
    #print(X)
    
    t=[]
    for i in range(len(X)):    
        T = (getTime(speed, angle, X[i])) #sec
        t.append(T)
        
    x1 = []
    y1 = []
    
    for k in t:
        x = getXPos(k, angle, speed)
        y = getYPos(k, angle, speed) * -1
        x1.append(x)
        y1.append(y)
        
    x1 = [20.12 - i for i in x1]
    y1 = y1[::-1]
        
    p = [i for i, j in enumerate(y1) if j < 0] # Don't fall through the floor                          
    
    for i in sorted(p, reverse = True):
        del x1[i]
        del y1[i]
    
    return x1, y1

def mathModel(speed, angle):
    spdix = speed * cos(radians(angle))
    spdiy = speed * sin(radians(angle))
    
#    print(spdix)
#    print(spdiy)

    spdoy = COR * -spdiy
    spdox = spdix + COF * (1 + COR) * spdiy
    
#    print(spdox)
#    print(spdoy)

    angleo = degrees(atan(spdoy / spdox))
    spdo = np.sqrt(spdox**2 + spdoy**2)
    
    return spdo, angleo

def plot3d(x_pts, y_pts):
#    X = x_pts[::-1]
    X = x_pts
    Y = y_pts
    
#    print(X)
#    print(Y)
    
    fig = plot.figure(figsize=(8,5))
    
    ax = plot.axes([-0.1, 0.1, 1.2, 0.7],projection='3d',xlim=(0,21.0),zlim=(0,21),ylim=(-0.5,0.5))
    
    #ax = fig.add_subplot(111,projection='3d')
    
    ax.set_xlim3d([0.0, 20.1])
    ax.set_xlabel('length_of_pitch')
    
    ax.set_ylim3d([-0.5,0.5])
    ax.set_ylabel('Z')
    
    ax.set_zlim3d([0.0, 1.65])
    ax.set_zlabel('Height')
    
    ax.set_title('Pegion Vison')
    blues= plot.get_cmap('Reds')
    colors = list(iter(blues(np.linspace(0,1,len(y1)))))
    
    plot.ion()
    
    ax.plot([20.12,20.12],[0,0],[0,0.711],'b',lw = 5)
    ax.plot([20.12,20.12],[-0.1145,-0.1145],[0,0.711],'b',lw = 5)
    ax.plot([20.12,20.12],[0.1145,0.1145],[0,0.711],'b',lw = 5)
    ax.plot([0.0,0.0],[0,0],[0,0.711],'b',lw = 5)
    ax.plot([0.0,0.0],[-0.1145,-0.1145],[0,0.711],'b',lw = 5)
    ax.plot([0.0,0.0],[0.1145,0.1145],[0,0.711],'b',lw = 5)
    
    z1 = np.zeros(np.shape(X)) #+ random.uniform(-0.4,0.4)
    
    ax.scatter3D(X,z1,Y,lw=1.5,color='r')
    
    if y2 <= stumpH and -0.1145 <= z1[1] <= 0.1145:
        ax.text(12, 0.5, 1, 'Out..!!')
    
    else:
        ax.text(12, 0.5, 1, 'Not Out..!!')
        
#%%
        
bounceD, thetaBB, vBB = (getImpactPos(thetai, vi, heigth))

print(bounceD)

#%% Calculations
print("\nInput speed: %d mps and angle: %d deg"%(vBB, thetaBB))
    
vo, thetao = mathModel(vBB, thetaBB)

print("\nOutput speed: %d mps and angle: %d deg"%(vo, thetao))
#%%

x2 = pitchD - bounceD
time = getTime(vo, thetao, x2) #sec
y2 = getYPos(time, thetao, vo)

print("\nHeight of ball at stumps: %0.2f m"%y2)

if y2 <= stumpH:
    print("\nOut !!")
else:
    print("\nNot Out !!")
    
x0, y0 = getPosVec1(bounceD, thetai, vi)

x1, y1 = getPosVec(bounceD, thetao, vo)
x1.reverse()
#y1.reverse()

x0.extend(x1)
y0.extend(y1)

plot3d(x0, y0)
#%%
