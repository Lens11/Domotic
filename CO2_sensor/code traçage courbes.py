###Importation des modules

import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import scipy as sp
import scipy.optimize

### A remplire !
EXP=9
Num=2
"c'est le numero de l'experience dans laquelle j'ai besoin d'asymptotes verticales à cause des ouvertures (commence à 1)"

alterne=False     #True si besoin d'asymptotes, False sinon

###ouverture du fichier puis itération dans 5 listes de données

f=open('Exp 9.txt')
t,C1,C2,C3,T,H,V=[],[],[],[],[],[],[]

for ligne in f:              # On boucle sur chaque ligne du fichier
    arr=ligne.split(';')     # on split les valeurs du fichiers à chaque ';' sur la ligne
    t.append(float(arr[0]))
    C1.append(float(arr[1]))
    C2.append(float(arr[2]))
    C3.append(float(arr[3]))
    T.append(float(arr[4]))
    H.append(float(arr[5]))
    V.append(float(arr[6]))

###Correction éventuelle des bugs arduino/python sur data
"Si jamais erreur de relais entre Arduino et Python: on a une ligne 0 pour toutes les valeurs, on remplace donc les erreurs de temps par l'ecart de temps moyen de 11s"
for i in range(len(t)):
    if t[i]==0:
        t[i]=t[i-1] + 11600 # environ écart entre les mesures (environ 11s)

# def uniformisation(L,epsilon):
#
#     for i in range(len(L)):
#         if i==0 or i==len(L):
#             m=1
#         else:
#             if L[i]==0:
#                 L[i]=L[i-1]
#             if abs(L[i]-L[i-1])<epsilon:
#                 L[i]=L[i-1]
#     return L
# U1=uniformisation(C1,200)
# U2=uniformisation(C2,200)
# U3=uniformisation(C3,200)

# u=1
# for i in range(len(t),-1):
#     if t[i]>t[i+1]:
#         u=0
#
# print(u)
### Conversion des temps du fichier de µs en min

for i in range(len(t)):
    t[i]=(t[i]*60*10**(-3))*10/36

### Recuperation des paramètres préalablement définis dans un .txt

parametres=open('parametres_filtrage.txt')
ligne=parametres.readlines()
arr=ligne[EXP].split(';')
a1=float(arr[0])        #coef pour C1
a2=float(arr[1])
b1=float(arr[2])        #coef pour C2
b2=float(arr[3])
r1=float(arr[4])        #coefs de redressement
r2=float(arr[5])
lC1=float(arr[6])       #coef de temps
lC2=float(arr[7])
para=int(arr[8])        #parametre de filtrage (ordre)
parametres.close()

time=open('Temps_aeration.txt')
data=time.readlines()
content=data[Num].split(';')
ouv1=float(content[0])
ferm1=float(content[1])
ouv2=float(content[2])
ferm2=float(content[3])
ouv3=float(content[4])
ferm3=float(content[5])
ouv4=float(content[6])
ferm4=float(content[7])

temps_aeration=content
time.close()

"J'ai inversé les ouv et ferm mais c'est pas grave on va pas y preter attention (car je commence toujours par fermer en pratique"

### Détermination de la constante de temps

from math import exp

def recherche_tau(T,C):
    """ Recherche du temps caractéristique par méthode des "37%" """
    fin = C[-1] # La valeur finale: concideree comme l'asymptote
    deb = C[0] # La valeur de depart


    for i in range(len(C)):
        if abs(C[i] - fin) < abs(deb - fin)*exp(-1):
            return T[i] - T[0]


def recherche_3tau(t,u):
    """ Recherche du temps caractéristique par méthode des "5%" """
    fin = u[-1] # La valeur finale: concideree comme l'asymptote
    deb = u[0] # La valeur de depart
    for i in range(len(u)):
        if abs(u[i] - fin) < abs(deb - fin)*exp(-3):
            return (t[i] - t[0])/3

 # t3au1 = recherche_3tau(t,C1)
 # t3au2 = recherche_3tau(t,C2)
 # t3au3 = recherche_3tau(t,C3)
 # tau1 = recherche_tau(t,C1)
 # tau2 = recherche_tau(t,C2)
 # tau3 = recherche_tau(t,C3)
 #
 # print(tau,tau3)

###Optimisation des courbes
n=len(t)
def optimisation(t,C1,k):
    "On supprime au maximum le bruit des courbes, en supprimant les valeurs en dessous de k"

    C1 = np.array(C1)
    t = np.array(t)
    C1_p = C1[C1 > k]
    t1_p = t[C1 > k]

    return t1_p, C1_p


def Premier_filtrage(t,C,k,adjust1,l):
    "On garde les points uniquement dont l'écart entre les deux points successifs est inferieur à un certain paramètre definit k. adjust est l'écart qu'on doit soustraire à k à partir du temps de mesure l (pour ajuster)"

    Cp,tp=[],[]
    Cp.append(C[0])
    tp.append(t[0])
    ref=C[0]
    for i in range(n-1):
        if C[i+1]>=C[i] and abs(C[i+1]-ref)<k or abs(C[i+1]-ref)<k-adjust1 and t[i]>l :
            Cp.append(C[i+1])
            tp.append(t[i+1])
            ref=C[i+1]

    return tp,Cp




def filtrage_moyenne_glissante(t,C,p):
    "moyenne glissante sur 2p+1 pts, évidemment, plus p est grand, plus le filtrage est important"
    l=len(t)
    Cn=[]
    tn=t[p:-p]

    for i in range(p,l-p):
        moy=sum(C[i-p:i+p+1])/(2*p+1)
        Cn.append(moy)

    return tn,Cn


def tri_insertion(L):
    "Algorithme de tri le plus rapide pour de petites listes: j est l'elt à caser, et on le compare à celui en j-1"

    for i in range(1,len(L)):
        j=i
        elt=L[i]
        while j>0 and L[j-1]>elt:
            L[j]=L[j-1]
            j=j-1
        L[j]=elt

    return L


def filtrage_mediane_glissante(t,C,p):
    "prend la mediane sur 2p+1 points"
    Cn=[]
    tn=t[p:-p]

    for i in range(p,len(t)-p):
        L=tri_insertion(C[i-p:i+p+1])
        n=len(L)
        if n%2==1:
            mediane=L[n//2]
        else:
            mediane=(L[n//2-1]+L[n//2])/2

        Cn.append(mediane)

    return tn,Cn

def redressement(C1,k):
    "On deplace en masse tout les points : si pb de hauteur à cause de pin ?"
    for i in range(len(C1)):
        C1[i] = C1[i] + k
    return C1

plt.figure('graphe brut')
# C1=redressement(C1,r1+100)
# C2=redressement(C2,r2)
plt.plot(t,C1,label='Taux au niveau de la porte')
plt.plot(t,C2,label='Taux au niveau de la fenêtre')
plt.plot(t,C3,label='Taux au niveau du bureau')
plt.title('Courbes brutes ouverture fenêtre')
plt.legend(loc='upper left')
plt.ylabel('Concentration (ppm)')
plt.xlabel('Temps (min)')
# plt.savefig('exp1 brut')


plt.figure('graphe 1')
tp,cp=Premier_filtrage(t,C1,a1,a2,lC1)
plt.plot(tp,cp,label='Courbe filtrée')
plt.plot(t,C1,label='Valeurs brutes')
plt.title('1er filtrage ouverture fenêtre')
plt.legend(loc='upper left')
plt.ylabel('Concentration (ppm)')
plt.xlabel('Temps (min)')
plt.show()
# plt.savefig('exp1 1er filtrage')


plt.figure('graphe 2')
#tp,cp=Premier_filtrage(t,C1,a1,a2,lC1)
tp,cp=Premier_filtrage(t,C1,a1,a2,lC1)
X,Y=filtrage_moyenne_glissante(tp,cp,para)
X1,Y1=filtrage_mediane_glissante(tp,cp,para)
X2,Y2=filtrage_mediane_glissante(X,Y,para)
X3,Y3=filtrage_moyenne_glissante(X1,Y1,para)
plt.plot(tp,cp,color='g',label='1er filtrage')
plt.plot(X,Y,color='b',label='moyenne')
plt.plot(X1,Y1, color='r',label='mediane')
plt.plot(X2,Y2,color='c',label='moy + med')
# plt.plot(X3,Y3,color='m',label='med + moy')
plt.legend(loc='upper left')
plt.title('2nd filtrage ouverture fenêtre')
plt.ylabel('Concentration (ppm)')
plt.xlabel('Temps (min)')

plt.show()
# plt.savefig('exp3 filtrage.png')



plt.figure('graphe 3')

tp2,cp2=Premier_filtrage(t,C2,b1,b2,lC2)
tp1,cp1=Premier_filtrage(t,C1,a1,a2,lC1)

# # for i in range (215,245):
# #     cp2[i]-=18*(i-214)
# #
# # for l in range(245,274):
# #     cp2[l]-=540
# #
# # for i in range (155,180):
# #     cp1[i]-=25*(i-154)
# #
# # for l in range(180,199):
# #     cp1[l]-=620
# cp1=redressement(cp1,r1)
# cp2=redressement(cp2,r2)


X3a,Y3a=filtrage_moyenne_glissante(tp1,cp1,para)
X3b,Y3b=filtrage_moyenne_glissante(tp2,cp2,para)
# X1a,Y1a=filtrage_mediane_glissante(tp1,cp1,para)
# X3a,Y3a=filtrage_moyenne_glissante(X1a,Y1a,para)
# X1b,Y1b=filtrage_mediane_glissante(tp2,cp2,para)
# X3b,Y3b=filtrage_moyenne_glissante(X1b,Y1b,para)
Y3a=redressement(Y3a,r1)
Y3b=redressement(Y3b,r2)
# Y1a=redressement(Y1a,r1)
# Y1b=redressement(Y1b,r2)

# plt.ylim(900,1500)

# fichier = open('exp8_droite_m1.txt', 'a')
#
# for i in range(len(X3a)):
#     fichier.write(str(X3a[i]) + ';' + str(Y3a[i]) + '\n')
# fichier.close()
#
# fichier = open('exp8_droite_m2.txt', 'a')
#
# for i in range(len(X3b)):
#     fichier.write(str(X3b[i]) + ';' + str(Y3b[i]) + '\n')
# fichier.close()

# t3au1 = recherche_3tau(X1a,Y1a)
# t3au2 = recherche_3tau(X1b,Y1b)
#
# tau1 = recherche_tau(X1a,Y1a)
# tau2 = recherche_tau(X1b,Y1b)
#
#
# print(tau1,t3au1,t3au2,tau2)


plt.plot(X3a,Y3a,label='Taux au niveau de la porte')
plt.plot(X3b,Y3b,label='Taux au niveau de la fenêtre')

# plt.ylim(500,3000)
# plt.plot(tp2,cp2,marker='o',linestyle='-',color='cyan')
# plt.plot(tp1,cp1,marker='o',linestyle='-',color='magenta')
# plt.plot(X3a,Y3a,label='Taux au niveau de la porte')
# plt.plot(X3b,Y3b,label='Taux au niveau de la fenêtre')
# plt.axvline(x=65,color='gray',linestyle='--',label='Ouverture')

S,J=0,0
plt.ylim(950,1770)

for i in Y3a:
    S+=i

for l in Y3b:
    J+=i
print(S/len(Y3a))
print(J/len(Y3b))

# marker='o',linestyle='-'

if alterne==True:
    plt.axvline(x=ouv1,color='gray',linestyle='--',label='Ouverture ou fermeture')
    plt.axvline(x=ferm1,color='gray',linestyle='--')
    plt.axvline(x=ouv2,color='gray',linestyle='--')
    plt.axvline(x=ferm2,color='gray',linestyle='--')
    plt.axvline(x=ouv3,color='gray',linestyle='--')
    plt.axvline(x=ferm3,color='gray',linestyle='--')
    plt.axvline(x=ouv4,color='gray',linestyle='--')
    plt.axvline(x=ferm4,color='gray',linestyle='--')

plt.xlim(0,110)
plt.legend(loc='upper left')
plt.title('Ouverture de la fenêtre pendant 7min toutes les 23min')
# plt.title('(Lissage avec filtrage et moyenne sur 11 points)',fontsize=10)
plt.ylabel('Concentration (ppm)')
plt.xlabel('Temps (min)')

plt.show()
# plt.savefig('exp8 corr.png')



def convert_array(t1,t2,t3,C1,C2,C3):
    "Convert en array tt les tableaux pour manipuler + facilement"
    t1=np.array(t1)
    t2=np.array(t2)
    t3=np.array(t3)
    C1=np.array(C1)
    C2=np.array(C2)
    C3=np.array(C3)

    return t1,t2,t3,C1,C2,C3

### opti exp

def optimisation_expo(t,C1,k):
    "suppr du bruit si courbe decroissante (ou croissante) as expo, Programme à revoir !"
    C1 = np.array(C1)
    t = np.array(t)
    for i in range(len(t)):
        C1_p = C1[C1 > k]
        t1_p = t[C1 > k]
        k=k-10

    return t1_p, C1_p


### Tracé du graphe


# ax1=plt.gca()
# ax2=ax1.twinx()     # pour avoir des axes jumeaux en ordonnées
#
# ax1.plot(t,C,label='C',color='g')
# ax2.plot(t,H,label='H',color='m')
#
# plt.legend()
# ax1.set_ylabel('concentration (ppm)')
# ax2.set_ylabel('Humidité')
# ax1.set_xlabel('temps (min)')
# ax2.set_ylim(30,90)
# ax1.set_ylim(400,3000)
# ax1.plot()
# ax2.plot()



    # pour avoir des axes jumeaux en ordonnées

def trace_opti(t,C1,k1,C2,k2,C3,k3):
    "On trace les courbes avec optimisation (suppr bruit) et redressement (translation) pour + de visibilité"
    t1p,C1P=optimisation(t,C1,k1)
    t2p,C2P=optimisation(t,C2,k2)
    t3p,C3P=optimisation(t,C3,k3)
    C1P = redressement(C1P,-500)
    C2P = redressement(C2P,+200)

    plt.plot(t1p,C1P,label='Concentration 1',color='g')
    plt.plot(t2p,C2P,label='Concentration 2',color='b')
    plt.plot(t3p,C3P,label='Concentration 3',color='r')
    plt.ylim(950,3000)
    plt.ylabel('concentration (ppm)')
    plt.xlabel('temps (min)')
    plt.title('''taux de CO2 dans la pièce, opti''')
    plt.legend(loc='upper right')

    plt.show()

def trace_lissage(t,C1,k1,C2,k2,C3,k3):
    "On trace les courbes avec optimisation (suppr bruit) et redressement (translation) pour + de visibilité et on lisse les courbes avec filtre pour venir modeliser au mieux"

    t1p,C1P=optimisation(t,C1,k1)
    t2p,C2P=optimisation(t,C2,k2)
    t3p,C3P=optimisation(t,C3,k3)
    C1P = redressement(C1P,-500)
    C2P = redressement(C2P,+200)

    Y1 = savgol_filter(C1P,101, 2) #window_length doit etre impair
    Y2 = savgol_filter(C2P,101, 2) #plus l'ordre polynomial est grand, plus interpole de points ==> details
    Y3 = savgol_filter(C3P,101, 2)

    plt.plot(t1p,Y1,label='Concentration 1',color='g')
    plt.plot(t2p,Y2,label='Concentration 2',color='b')
   # plt.plot(t3p,Y3,label='Concentration 3',color='r')
    plt.ylim(650,3700)
    plt.ylabel('concentration (ppm)')
    plt.xlabel('temps (min)')
    plt.title('''taux de CO2 dans la pièce, lissage''')
    plt.legend(loc='upper right')

    plt.show()

def trace_brut(t,C1,C2,C3):
    "On trace les courbes avec les valeurs brutes ==> bcp de bruit et d'erreurs"

    #t1,C1=optimisation_expo(t,C1,2400)

    plt.plot(t,C1,label='Concentration 1',color='g')
    plt.plot(t,C2,label='Concentration 2',color='b')
    plt.plot(t,C3,label='Concentration 3',color='r')
    plt.ylim(650,3700)
    plt.ylabel('concentration (ppm)')
    plt.xlabel('temps (min)')
    plt.title('''taux de CO2 dans la pièce brut''')
    plt.legend(loc='upper right')

    plt.show()

def trace_filtrage(t,C1,C2,C3):
    "On trace juste l'allure de la courbe grâce au filtrage Premier_filtrage et on va chercher les paramètres d'ajustements qui ont été préalablement défini dans un .txt pour chaque EXP"

    p=open('parametres_filtrage.txt')
    content=p.readlines()
    arr=content[EXP].split(';')
    a1=float(arr[0])
    a2=float(arr[1])
    b1=float(arr[2])
    b2=float(arr[3])
    r1=float(arr[4])
    r2=float(arr[5])
    lC1=float(arr[6])
    lC2=float(arr[6])

    para=int(arr[7])
    p.close()

    t1p,C1P=Premier_filtrage(t,C1,a1,a2,lC1)
    t2p,C2P=Premier_filtrage(t,C2,b1,b2,lC2)
    C1m=redressement(C1P,r1)
    C2m=redressement(C2P,r2)
   # t3p,C3P=Premier_filtrage(t,C2,120,-30)

    t1f,C1f=filtrage_moyenne_glissante(t1p,C1m,para)
    t2f,C2f=filtrage_moyenne_glissante(t2p,C2m,para)
    plt.subplot(1,2,2)
    plt.plot(t1f,C1f,label='Concentration 1',color='g')
    plt.plot(t2f,C2f,label='Concentration 2',color='b')
    plt.title('''filtrage double''')
    plt.ylim(650,3700)
    plt.ylabel('concentration (ppm)')
    plt.xlabel('temps (min)')
    plt.subplot(1,2,1)
    plt.plot(t1p,C1m,label='Concentration 1',color='g')
    plt.plot(t2p,C2m,label='Concentration 2',color='b')
    # plt.plot(t3p,C3P,label='Concentration 3',color='r')
    plt.ylim(650,3700)
    plt.ylabel('concentration (ppm)')
    plt.xlabel('temps (min)')
    plt.title('''filtrage''')
    plt.legend(loc='upper right')
    plt.show()




###Determination vitesse de l'aération

def restriction_valeurs_intervalle(t,C,debut,fin):
    "restreint les valeurs de la liste à l'intervalle d'étude et renvoie en tableau numpy"
    t=np.array(t)
    C=np.array(C)
    C=C[t>debut]
    t=t[t>debut]
    C=C[t<fin]
    t=t[t<fin]
    return t,C

def temps_C02max(t1,C1,debut,fin):
    "calule le temps correspondant au maximum local du taux C02 sur  l'intervalle d'étude restreint par debut/fin"

    t1,C1=restriction_valeurs_intervalle(t1,C1,debut,fin)
    Max=C1[0]
    pos=0
    assert len(t1)==len(C1)
    for i in range(len(C1)):
        if C1[i]>Max:
            Max=C1[i]
            pos=i
    temps_max=t1[pos]
    return temps_max,Max

def diff_temps_sur_max(t1,C1,t2,C2,debut,fin):
    "Calcule la différence de temps entre deux pics de CO2 atteints (entre les 2 courbes) sur chaque ouverture/fermeture et renvoie aussi un tupple qui contient les valeurs des maxima"
    Tmax1,m1=temps_C02max(t1,C1,debut,fin)
    Tmax2,m2=temps_C02max(t2,C2,debut,fin)
    return abs(Tmax1-Tmax2),[m1,m2]

def diff_temps_entier_sur_max(t1,C1,t2,C2):
    "Renvoie la liste des maxima atteints durant toute l'experience pour les deux courbes ainsi que la difference de temps entre les deux maxima des deux courbes"
    L=[]
    M=[]                #Liste qui contiendra les tupples maximum
    for i in range(0,4):
        a=2*i               #On veut simplement étudier les intervalles correponsant entre les ouvertures et les fermetures et non entre 2 fermetures par ex.
        ouverture=float(temps_aeration[a])   #On restreint les intervalles au moment des ouvertures/fermetures
        fermeture=float(temps_aeration[a+1])
        Diff,m=diff_temps_sur_max(t1,C1,t2,C2,ouverture-5,fermeture+5)
        M.append(m)
        L.append(Diff)
    return L,M


def minimum_local(t,C,debut,fin):
    "Calcule le minimum local atteint par le taux de CO2 sur l'intervalle d'étude delimité par debut/fin"
    t,C=restriction_valeurs_intervalle(t,C,debut,fin)
    Min=C[0]
    pos=0
    assert len(t)==len(C)
    for i in range(len(C)):
        if C[i]<Min:
            Min=C[i]
            pos=i
    temps_min=t[pos]
    return temps_min,Min

def diff_temps_sur_min(t1,C1,t2,C2,debut,fin):
    "Calcule la différence de temps entre minima  de CO2 atteints (entre les 2 courbes) sur chaque ouverture/fermeture et renvoie aussi un tupple qui contient les valeurs des minima"

    Tmin1,m1=minimum_local(t1,C1,debut,fin)
    Tmin2,m2=minimum_local(t2,C2,debut,fin)
    return abs(Tmin1-Tmin2),[m1,m2]

def diff_temps_entier_sur_min(t1,C1,t2,C2):
    "Renvoie une liste de tous les minima locaux atteints par la deux courbes, ainsi que leur temps associé"
    M=[]                #Liste qui contiendra les tupples minimum
    L=[]
    for i in range(0,4):
        a=2*i
        ouverture=float(temps_aeration[a])   #On restreint les intervalles au moment des ouvertures/fermetures et temps\aeration est justement une liste avec ces données
        fermeture=float(temps_aeration[a+1])
        # temps_min1,Min1=minimum_local(t1,C1,t2,C2,ouverture-5,fermeture+5)
        # temps_min2,Min2=minimum_local(t1,C1,t2,C2,ouverture-5,fermeture+5)
        Diff,m=diff_temps_sur_min(t1,C1,t2,C2,fermeture-5,fermeture+5)
        M.append(m)
        L.append(Diff)

    return L,M

# Diffm,Min=diff_temps_entier_sur_min
# DiffM,Max=diff_temps_entier_sur_max
#
#
#
#
# print(diff_temps_entier_sur_min(X3a,Y3a,X3b,Y3b))
# print(diff_temps_entier_sur_max(X3a,Y3a,X3b,Y3b))

# fichier = open('difference_temps.txt', 'a')
# L,M = diff_temps_entier(X3a,Y3a,X3b,Y3b)
# fichier.write("Diff temps et max atteints Exp" + str(EXP) + '\n')
#
# for i in range(len(L)):
#     fichier.write(str(L[i]) + ';' + str(M[i][0]) + ';' + str(M[i][1])+ '\n')
# fichier.close()



# plt.figure('graphe 4')
#
# tp2,cp2=Premier_filtrage(t,C2,b1,b2,lC2)
# tp1,cp1=Premier_filtrage(t,C1,a1,a2,lC1)
# X1a,Y1a=filtrage_mediane_glissante(tp1,cp1,para)
# X3a,Y3a=filtrage_moyenne_glissante(X1a,Y1a,para)
# X1b,Y1b=filtrage_mediane_glissante(tp2,cp2,para)
# X3b,Y3b=filtrage_moyenne_glissante(X1b,Y1b,para)
# Y3a=redressement(Y3a,r1)
# Y3b=redressement(Y3b,r2)
#
# X3a,Y3a=restriction_valeurs_intervalle(X3a,Y3a,41,80)
# X3b,Y3b=restriction_valeurs_intervalle(X3b,Y3b,41,80)
#
# plt.plot(X3a,Y3a,label='C1')
# plt.plot(X3b,Y3b,label='C2')
#
# plt.show()










