# Démo opérationelle de pilotage d'un arduino depuis un script python.
# Attention, par défaut, la connection provoque un reset de l'arduino.
### NOTES
# Une fois le timeout défini, la non reception ne gene pas
# juste après readline on a if len(rx) == 0: si rien n'est reçu. 
import numpy as numpy
import math
import time
import pylab as plt          #regroupe matplotlib et numpy
import serial
### Initialisation du port série ###
ser = serial.Serial(port='COM3',baudrate=9600)  # Config du port série
ser.timeout = 5                           # Au bout de 5s d'attente, on considère pas de réponse.      
print (ser.portstr)                              # Affichage du port utilisé
if  (ser.isOpen()==True):
    print("Open")                                # True si vraiment open
time.sleep (2)                                   # IMPORTANT timeout de 2s SI CAVALIER REBOOT PRESENT
ser.flushOutput()
ser.flushInput()
### EXEMPLE DE LECTURE A LA DEMANDE.
### Cette fonction envoie à l'arduino le string qu'elle reçoit.
### La fonction puis retourne la réponse.
def LireUneLigneSurCommande(MyChar):
    """ Cette fonction envoie un charactère à l'arduino, et attends la réponse sous forme d'une ligne  """
    mystr = ""
    ser.flushOutput()              # On tire la chasse sur le tampon de sortie
    TX = MyChar + "\n"             # Chaine simple, \n est un retour chariot
    ser.flushInput()               # Précaution, on vide le buffer de ce qui reste a lire
    ser.write( TX.encode( ) )      # Ecriture sur le port série
    time.sleep (0.05)              # Délai pour la réponse
    rx=ser.readline()              # Lecture de la réception
    # print (rx)                    # Debug
    ### Lecture ligne il faut  ***println*** dans le code arduino ###
    ### Si rien n'est reçu audela du timeout, la chaine est vide et on quitte ou pas ###
    if len(rx) == 0:
        print ("Oups ...")
        print ("Rien n'est reçu ...")
        return ('x')
    ### Filtrage des receptions initiales incomplètes. Le mini de RX est un char + \r\n ###    
    if len(rx) > 0: 
        mystr = bytes.decode(rx)     # Passage d'un array de bytes a un string
        mystr  = mystr.rstrip()
    return  mystr


    
### SAUVEGARDE EVENTUELLE ### 
def FileSave (datata,filename):
    fichier = open ( filename , "a")
    fichier.write( datata)
    fichier.close()

### DECODAGE REPONSE
### M une mesure
### m moyenne de 100 mesures
NbMesures    = 50     ### NB DE MESURES A REALISER
Intervalle_S = 3    ### SECONDES EN PLUS DU DELAI INCOMPRESSIBLE DE MESURE ASSEZ LONG
print ("Minimum " , NbMesures * Intervalle_S )
t,T,C,Th,H=[],[],[],[],[]
print ("Start mesures pour " , NbMesures*Intervalle_S , " en secondes")


### Mode graphique interactif pour le graphique.
# plt.ion()

for i in range (NbMesures ):
    ### Envoi de "T" et lecture de la réponse
    MaPetiteLigne = LireUneLigneSurCommande("T")
    ### Transformation de la réponse en liste
    data =  MaPetiteLigne.split(";")
    ### Affichage de debug ...
    print(data)
    ### Délai entre mesures ...
    time.sleep(Intervalle_S)
    print ( "Délai d'attente " , Intervalle_S , "s ") 
    ### Transformation en listes:
    t.append(( data[0] ))
    C1.append(( data[1] ))
    C2.append(( data[2] ))
    C3.append(( data[3] ))
    T.append(( data[4] ))
    H.append(( data[5] ))
  
    ### Sauvegarde des données dans un fichier.
    ### Création de la liste à sauvegarder 
    MyTmpString =  data[0] + ";" + data[1] + ";" + data[2] + ";" + data[3] + ";" + data[4] + ";" + data[5] "\n"
    ### Sauvegarde réelle ( attention ... marche que pour une sauvegarde assez lente, genre dt=1s )
    FileSave ( MyTmpString , "test.txt")
    ### Tracage des graphs
    # ax1=plt.gca()
    # ax2=ax1.twinx()
    
    # plt.subplot(1,2,1)
    # ax1.plot(t,C,marker='o',label='concentration',color='g')
    # ax2.plot(t,H,marker='o',label='H',color='m')
    # plt.legend()
    # ax1.set_ylabel('concentration')
    # ax2.set_ylabel('Humidité')
    # ax1.set_xlabel('temps')
    # ax2.set_ylim(30,70)
    # ax1.set_ylim(400,2500)
    # ax1.plot()
    # ax2.plot()
    
    
    # plt.subplot(1,2,2)
    # plt.plot(t,T,marker='o',label='T°',color='r')
    plt.plot(t,C1,marker='o',label='Concentration',color='b')
    plt.ylabel('concentration (ppm)')
    plt.xlabel('temps (min)')
    # plt.set_ylabel('Concentration')
    # plt.set_xlabel('Temps')
    
    plt.draw() 
    plt.pause(1)
  
    
print ( "End mesures..." )    
plt.ioff() # mode interaction off


plt.show()
plt.savefig("dimanche essai.png")
plt.close()


### Sauvegarde des listes de données.
AdresseFichier = "test.txt"
### Sauvegarde des listes basiques, écrase le dernier fichier 
fichier = open ( AdresseFichier, "w")
### Ligne 1 : Titre avec un # au début pour pas poser de pb lors de l'utilisation du .txt
# MyTmpString = "# Première experience !"  + "\n" 
fichier.write(MyTmpString  )
### Ligne 2 : Notes importantes avec un # au début
# MyTmpString = "# On va voir ce que ca donne !" + "\n"
fichier.write(MyTmpString  )    
### Ligne 3 : En tête des différentes colonnes avec un # au début
# MyTmpString = ("# t , C, T, H ") + "\n"
fichier.write(MyTmpString  )   
### Ecriture de la boucle de sauvevardes des listes.     
for i in range( 0, len(t) ):
    MyTmpString = str(t[i])  + ";" + str(C[i])  + ";" + str(T[i]) + ";" + str(H[i]) + "\n"
    fichier.write(MyTmpString )  
fichier.close()


### FERMETURE DU PORT SERIE
print ("Port série en voie de fermeture")
ser.close()
print ("Port série fermé ")