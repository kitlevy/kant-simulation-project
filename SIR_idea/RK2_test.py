#testing RK2 method using Newton's Law of Cooling
#T'(t)=v(T_E-T(t))
#T(0)=T_0

import matplotlib.pyplot as plt
#importing vectorized RK2 method from other file
from vectorized_RK2 import *

#example: estimate temperature of 100 degree object in 50 degree environment
#trying 
def m0(x,y):
    return np.log(2)*(50-y)

n=8 #number of steps
(xvals,yvals)=RK2_vectorized(m0,0,5,100,n)
plt.scatter(xvals,yvals,color='red')
plt.plot(xvals,yvals,color='red')
plt.show()
