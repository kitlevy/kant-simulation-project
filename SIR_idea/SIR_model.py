#implementing SIR of infectious disease

from vectorized_RK2 import *
import matplotlib.pyplot as plt

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

days=150
y0=np.array([1-1/8000,1/8000,0])
pop=1
steps=9999

b=pop/2
k=pop/3

simulate_SIR()


