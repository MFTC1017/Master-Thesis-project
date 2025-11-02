import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

def VPOTENTIAL(sz, z, xi1, xi2, chi12):
    v=4*(z**2) -4*(z**4)-xi1/2 + (z**2)*xi1 +sz*z*np.sqrt(1-z**2)*xi2 - 2*sz*(z**3)*np.sqrt(1-z**2)*xi2 + chi12/2 -2*(z**2)*chi12 +2*(z**4)*chi12
    return v

def test_vpot(xi1, xi2, chi12):
    szarray=[-1,1]
    zetas=np.linspace(-1, 1, 10000)

    for sz in szarray:
        for z in zetas:
            vpot=VPOTENTIAL(sz, z, xi1, xi2, chi12)
            if(vpot<0): 
                return -1
            
    return +1

szarray=[-1,1]
zetas=np.linspace(-1, 1, 10000)
chi12=15
xi1array = np.linspace(0, 14, 100)
xi2array = np.linspace(0, 14, 100)

lista1=[]
lista2=[]

for xi1 in xi1array:
    for xi2 in xi2array:
        lista1.append([xi1, xi2, chi12, test_vpot(xi1, xi2, chi12)])
                            
dfVPOT=pd.DataFrame(lista1, columns=['xi1','xi2','chi12','VPOT'])  


list2=[]
for xi1 in xi1array:
    xi2old=0
    for xi2 in xi2array:
        if(test_vpot(xi1, xi2, chi12)<0): 
            list2.append([xi1, (xi2+xi2old)/2, chi12])
            break
        xi2old=xi2        
        
df=pd.DataFrame(list2, columns=['xi1', 'xi2', 'chi12'])           

df.to_csv('vpot.csv', index=False, float_format='%.2f')    

def mpend(xi10, xi20, xi1, xi2):
    pend=(xi2-xi20)/(xi1-xi10)
    return pend

list3=[]

def pend(xi1, xi2):
    xi10=np.linspace(0,3,100)
    xi20=np.linspace(0,3,100)
    for xi1 in xi10:
        for xi2 in xi20:
            pendient=mpend(xi10, xi20, xi1, xi2)
            if(pendient==0):
                list3.append([np.nan, np.nan, chi12])
                break

dfpend=pd.DataFrame(list3, columns=['xi1', 'xi2', 'chi12'])
dfpend.to_csv('pendient.csv', index=False, float_format='%.2f')

dftmp=dfVPOT[dfVPOT['VPOT']>0]
plt.scatter(dftmp['xi1'], dftmp['xi2'], s=1, label=r'bounded from below')
dftmp=dfVPOT[dfVPOT['VPOT']<0]
plt.scatter(dftmp['xi1'], dftmp['xi2'], s=1, label=r'unbounded from below')
plt.plot(dfgood['xi1'], dfgood['xi2'], label=r'$\chi_{12}=15$')
plt.xlabel(r'$\xi_{1}$', fontsize=16)
plt.ylabel(r'$\xi_{2}$', fontsize=16)
plt.xlim(0,14)
plt.title(r'$\xi_2$ vs $\xi_1$', fontsize=13)
plt.grid(True)

plt.legend(loc='best', scatterpoints=1, markerscale=7, fontsize=12) 
plt.savefig('xi2vsxi1chi1215p0.pdf', format='pdf', bbox_inches='tight')
plt.show()
