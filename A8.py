# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 01:12:27 2025

@author: Emily
"""

import numpy as np
import matplotlib.pyplot as plt

def A8Q1(a,b):
    fig,ax=plt.subplots()
    ax.scatter(a,b)
    return (fig,ax)

x, y = np.random.rand(2, 200)
A8Q1(x, y)


def A8Q2(*stuff):
    fig,ax = plt.subplots(len(stuff), 1)
    for i,array in enumerate(stuff):
        ax[1].hist(array)
    return (fig,ax)

x, y, z = np.random.rand(3, 200)
A8Q2(x, y, z)


def A8Q3(c):
    fig,ax=plt.subplots()
    ax.imshow(c)
    return (fig,ax)

im = np.random.rand(100, 100)
A8Q3(im)


def A8Q4(d,e):
    d.set_facecolor(e)
    return d

fig = plt.figure()
A8Q4(fig,'grey')


def A8Q5(f,g):
    g=np.array(g)
    fig,ax=plt.subplots()
    mask= (0<= g) & (g<= 1)
    ax.scatter(f,g*mask)
    return (fig,ax)

A8Q5(x, y)
