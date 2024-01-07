


### Curve fit et exponentielle


def expfit(t,A,tau,B):
    return A*np.exp(-t/tau) + B


xt=np.array(t)
yc=np.array(C1)
p,pcov = sp.optimize.curve_fit(expfit,xt,yc)

plt.plot(xt,expfit(xt,*p),color='red',label='ajustement à une exponentielle')
plt.plot(xt,yc,label='Concentration',color='g')
plt.legend()
plt.title("taux de CO2 en fonction du temps d'aération d'une pièce")
plt.xlabel('Temps (min)')
plt.ylabel('Concentration (ppm)')
plt.show()











