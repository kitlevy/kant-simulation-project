#implementing SIR of infectious disease

import matplotlib.pyplot as plt
import numpy as np

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


#b = infection rate, k = recovery rate
#dS/dt = -bIS
#dI/dt = bIS-kI
#dR/dt = kI


def m(t,y):
    (S,I,R)=y
    Sprime=-b*S*I
    Iprime=b*S*I-k*I
    Rprime=k*I
    return np.array([Sprime,Iprime,Rprime])

def simulate_SIR():
    (tvals,yvals)=RK2_vectorized(m,0,days,y0,steps)
    yvals=np.array(yvals)
    plt.plot(tvals,yvals[:,0],color='blue',label='S(t)')
    plt.plot(tvals,yvals[:,1],color='red',label='I(t)')
    plt.plot(tvals,yvals[:,2],color='green',label='R(t)')
    plt.legend()
    plt.show()

days=20
y0=np.array([1-1/8000,1/8000,0])
pop=1
steps=50

b=pop*.8 #infection rate
k=pop/3 #recovery rate

simulate_SIR()



