# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
#import pandas as pd
#import random
import math as m
import matplotlib.pylab as plot
from mpl_toolkits import mplot3d
#import mpl_toolkits.mplot3d.axes3d as p3
#import mpl_toolkits.mplot3d.art3d as p1
import matplotlib.animation as animation
#from itertools import cycle
#import time

#initialize variables
#velocity, gravity
v_init = 30
g = 9.81
angle=np.random.uniform(-2,2,1)
h=1.65 ## Height of Bowler
length_of_pitch=20.1
theta = np.array([angle*m.pi/180])
Vel_decrease_factor=2
bounce_angle=15
del_t=0.02
#increment theta 25 to 60 then find  t, x, y
#define x and y as arrays

#def ball_velocity():

def vertical_projectile_motion(xx,v_init,the,t):
    tt=del_t
    #del_t=0.05
    #del_tt=0.05
    y=0
    x1=[]
    y1=[]
    z1=[]
    v =[]
    dely=0.05
    r=np.random.uniform(0,1,1)
    if r<0.3 :
        spin='leg side spin'
    elif r>0.3 and r<0.6:
        spin='off side spin'
    else:
        spin="No spin"

    delx=xx-((v_init*t)*m.cos(the))
    while(True):
        x = delx+((v_init*t)*m.cos(the))
        z = ((v_init*tt)*m.sin(the))-((0.5*g)*(tt**2))
        v_initx=v_init*m.cos(the)
        v_initz=v_init*m.sin(the)-g*tt
        v_tot=np.sqrt(v_initx**2 + v_initz**2)
        #print(x)
        if spin=='leg side spin':
            y = y-dely**2
        elif spin=='off side spin':
            y = y+dely**2
        else:
            y=0
        t=t+del_t
        tt=tt+del_t
        if x>length_of_pitch:
            break
        x1.append(x)
        y1.append(y)
        z1.append(z)
        v.append(v_tot)
    return (x1,y1,z1,v,spin)

def Horizontal_projectile_motion(v_init,theta,h):
    x1 = []
    y1 = []
    z1 = []
    v=[]
    z=h
    t=0
    #del_t=0.05
    y=0
    while(True):
        x = ((v_init*t)*m.cos(theta)) # get positions at every point in time
        z = h+ ((v_init*t)*m.sin(theta))-((0.5*g)*(t**2))
        v_initx=v_init*m.cos(theta)
        v_initz=v_init*m.sin(theta)-g*t
        v_tot=np.sqrt(v_initx**2 + v_initz**2)
        #print(x)
        if z<0:
            the=bounce_angle*m.pi/180
            v_initx=v_init*m.cos(theta)
            v_initz=v_init*m.sin(theta)-g*t
            v_init2=(np.sqrt(v_initx**2 + v_initz**2))/Vel_decrease_factor
            vals=vertical_projectile_motion(x,v_init2,the,t)
            x1.extend(vals[0])
            y1.extend(vals[1])
            z1.extend(vals[2])
            v.extend(vals[3])
            spin=vals[4]
            break
        #ax.scatter3D(x, z, y);
        plot.pause(0.0001)
        x1.append(x)
        y1.append(y)
        z1.append(z)
        v.append(v_tot)
        t=t+del_t
    return(x1,y1,z1,v,spin)

"""
def update_lines(num, data, lines) :
    # NOTE: there is no .set_data() for 3 dim data...
    #scat.set_offsets
    lines.set_data(data[0][:num],data[1][:num])
    lines.set_3d_properties(data[2][:num])
    #return lines
"""

data=Horizontal_projectile_motion(v_init,theta,h)

data1=np.array(data[0:3])
velocity=np.array(data[3])
spin=data[4]
fig = plot.figure(figsize=(8,5))
#ax = p3.Axes3D(fig)
ax = plot.axes([-0.1, 0.1, 1.2, 0.7],projection='3d',xlim=(0,21.0),zlim=(0,h),ylim=(-0.5,0.5))
#fig = plot.figure(1)
#ax = fig.add_subplot(111,projection='3d')

ax.set_xlim3d([0.0, length_of_pitch])
ax.set_xlabel('length_of_pitch')

ax.set_ylim3d([-0.5, 0.5])
ax.set_ylabel('Z')

ax.set_zlim3d([0.0, h])
ax.set_zlabel('Height')

ax.set_title('Pigeon Vison')
blues= plot.get_cmap('Reds')
colors = list(iter(blues(np.linspace(0,1,len(data[0])))))

plot.ion()

ax.plot([20.12,20.12],[0,0],[0,0.711],'b')
ax.plot([20.12,20.12],[-0.1145,-0.1145],[0,0.711],'b')
ax.plot([20.12,20.12],[0.1145,0.1145],[0,0.711],'b')
ax.plot([0.0,0.0],[0,0],[0,0.711],'b')
ax.plot([0.0,0.0],[-0.1145,-0.1145],[0,0.711],'b')
ax.plot([0.0,0.0],[0.1145,0.1145],[0,0.711],'b')

#textvar = ax.text(12, 0.5, 1.6, "Velocity"+ '='+ str(velocity[i]), color='red')
#for i in range(len(data[0])):

ax.scatter3D(data[0], data[1], data[2],lw=5)

ax.text(12, 0.5, 1.6, spin)
ax.text(12, 0.5, 1, 'Throw angle'+'='+str(angle)+'in degrees')

plot.pause(0.001)
#plot.close(fig)
