import numpy as np
import matplotlib.pyplot as plt

def RK2_vectorized(m,a,b,y0,N):
    alph=0.5
    tvals=[a]
    yvals=[y0]
    h=(b-a)/N
    for i in range(N):
        (t,y)=(tvals[-1],yvals[-1])
        tvals.append(t+h)
        slope_now=m(t,y)
        #estimating later point, slope
        estt=t+alph*h
        esty=y+slope_now*alph*h
        slope_future=m(estt,esty)
        #getting concavity from two slopes
        concavity=(slope_future-slope_now)/(alph*h)
        #quadratic approx
        y1=y+slope_now*h+concavity*h**2/2
        yvals.append(y1)
    return (tvals,yvals)
