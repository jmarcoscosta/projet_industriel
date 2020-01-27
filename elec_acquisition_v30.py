####LES IMPORTATIONS et VARIABLES/DEFINITIONS GLOBALES####


from tkinter.ttk import * #a mettre avant ligne suivante
from tkinter import *
from tkinter.filedialog import * #pour le parcours des dossiers
from tkinter.messagebox import * #pour les alertes

import serial
import time
import os

# import picamera
import numpy as np
from PIL import Image as ImagePIL #ATTENTION : "as ImagePIL" a été rajouté sinon il y a un conflit (type object 'Image' has no attribute 'open') avec tkinter
from math import log10


def Ecriture(texte):
    from elec_interface_v30 import MafenetreElec, ZoneInstruction
    ZoneInstruction.delete(ALL)
    ZoneInstruction.create_text(250, 15, text=texte, font="Arial 9", fill="black")
    MafenetreElec.update()

def Ecriture_Canevas(texte):
    from elec_interface_v30 import MafenetreElec, Canevas
    global l
    l = l + 10
    Canevas.create_text(128, l, text=texte, font="Arial 9", fill="black")
    Canevas.update()


numSequence = -1

#les 8 listes suivantes représentent chacune une fonction (après chaque liste, l'utilisateur devra effectuer un changement sur le multimètre).

VDCmV = [25.0000e-3, 250.000e-3]
VDC = [0.500000, 2.50000, 4.50000, -4.50000, 25.0000, 250.000, 500.000]

VAC = [[0.5,50], [2.5,50], [2.5,400], [2.5,1000], [4.5,50], [25,50], [250,50], [375,50]]

IDCmA = [250e-3, 2.5, 25, 250]
IDC = [5]

IACmA = [250e-3, 2.5, 25, 250]
IAC = [5]

R = [10, 100, 1e3, 10e3, 100e3, 1e6, 10e6]

listeNbreDigits=[]
listeErreursVirgule = []
listeTemps=[]

listeNombre=[]
listeNombreInt=[]
listeImagesRognees=[]

longueurSequence = len(VDCmV)+len(VDC)+len(VAC)+len(IDCmA)+len(IDC)+len(IACmA)+len(IAC)+len(R)
print(longueurSequence)

tempsAttente = 5000 #en ms

# from main import *
from Meatest_API import *
from Fluke_API import *
# from Calibrators.Meatest_API import *
# from Calibrators.CX_Metrix_API import *
from sequences_manager import *

def Sequence():
    from elec_interface_v30 import MafenetreElec, Canevas, liste
    global  numSequence, longueurSequence
    global VDCmV, VDC, VAC, IDCmA, IDC, IACmA, IAC, R
    global listeNombre, l
    
    numSequence += 1

    # ser = serial.Serial( #RS232 avec Fluke
    # port = '/dev/ttyUSB0',
    # baudrate = 9600,
    # parity = serial.PARITY_NONE,
    # stopbits = serial.STOPBITS_ONE,
    # bytesize = serial.EIGHTBITS,
    # xonxoff = True,
    # timeout = 1
    # )
    #
    # print(ser.isOpen())

    device_name = liste.get(ACTIVE)
    print(device_name)


    if device_name == "Fluke":
        print("entrou")
        device = Fluke()
    elif device_name == "Meatest":
        device = Meatest()
    elif device_name == "CX_1651":
        device = Meatest()

    Canevas.delete(ALL)
    l = 0 #on écrit en haut du Canevas
    from tkinter.filedialog import askopenfilename
    filename = askopenfilename(filetypes=(("Text files", "*.txt"),
                                           ("HTML files", "*.html;*.htm"),
                                           ("All files", "*.*") ))

    device.setup_communication()
    # from sequences_manager import execute_sequence_file
    execute_sequence_file(device,filename,Ecriture,Acquisition)

    Ecriture("Etalonnage terminé")
    numSequence = 0
        
    fichier = open("certificatMX55.txt", "w") #ATTENTION: si le fichier existe on le supprime!
    fin = open(filename, "rt")
    data = fin.readlines()
    for i,l in enumerate(data):
        if i >0:
            measured = l.replace('#', listeNombre[i - 1])
            data[i] = measured
    # data = data.replace('pyton', 'python')
    fin.close()

    fin = open(filename, "wt")
    fin.write("\n".join(data))
    fin.close()

    for indice in range(len(listeNombre)) : 
        nombre = listeNombre[indice].replace(".",",")
        fichier.write(nombre+"\n")
    fichier.close()
    device.close_communication()
    from pdf_report_generator import generate_pdf
    generate_pdf(filename)
    # ser.close()


##MafenetreElec.withdraw()


repertoireScript = os.getcwd() #renvoie le chemin absolu du script
path = repertoireScript+"/Temporaire/"



def Creation_Dossier(NomDossier):
    if not os.path.exists(path+NomDossier): #si dossier existe pas
        os.makedirs(path+NomDossier)

def Suppression_Dossier(NomDossier):
    if os.path.exists(path+NomDossier): #si le dossier existe
        for fichier in os.listdir(path+NomDossier): #on supprime les fichiers du dossiers
            os.remove(path+NomDossier+"/"+fichier)
        os.rmdir(path+NomDossier) #pour ensuite supprimer le dossier


nbrePhoto = longueurSequence


def Acquisition(texte): #texte du type 'IDCmA_'+str(courant) => IDCmA_50

    from elec_interface_v30 import camera, longueurH, longueurV

    global longueurH,longueurV, cheminDossierSauvegardeComplet,listeNombre, listeErreursVirgule, listeTemps, running, listeImagesRognees, l, nbreErreurs, Verification

    global longueurSequence, listeNbreDigits, listeErreursVirgule, listeTemps
     
    
    dossierActuel="Photo"+texte #on se place dans le bon dossier
    
    Creation_Dossier(dossierActuel)
    camera.capture(path+dossierActuel+"/ImageComplete.jpg", use_video_port=True)
        
    try:
        
        Rognage(longueurH,longueurV,dossierActuel)
        
        NoirBlanc = Traitement_Zone(dossierActuel)

        NoirBlanc = Parasites_Bords(dossierActuel, NoirBlanc)
        
        NoirBlanc = Moyennage(dossierActuel, NoirBlanc)
        
        AAnalyser = Retrecissement_Zone(dossierActuel, NoirBlanc)
        
        [listeDigits, listeDigitsNonRetrecis] = Separation_Parfaite_Digits(dossierActuel, AAnalyser)

        [listeDigits,signe] = Analyse_Signe(listeDigits, dossierActuel, AAnalyser)
        cAAnalyser=Analyse_Colonnes_Sans_Signe(signe, listeDigitsNonRetrecis, dossierActuel, AAnalyser)

        nbreDigits = len(listeDigits)
        if nbreDigits != 1:
            [nbreTraits,lTraits] = Detection_Virgule_Verticale(nbreDigits, listeDigits)
            [listeDigits,division] = Suppression_Virgule(listeDigits,nbreDigits, nbreTraits, lTraits)
           
            [nombreStr, nombreInt]=Analyse_Sequence_Chiffre(nbreDigits,listeDigits,division,signe,cAAnalyser)
            listeNombre.append(nombreStr)
            listeNombreInt.append(nombreInt)
            Ecriture_Canevas(nombreStr)
        else: #si nbreDigits = 1, ceci est en fait impossible : il s'agit d'un changement de calibre ou la virgule n'a pas été totalement effacée (sinon on serait dans l'exception) et elle sera considérée comme un 1
            listeNombre.append("ERREUR") #pour ne pas créer un décalage lors de vérification
            listeNombreInt.append("ERREUR")
            
    except IndexError: #lorsque la photo est prise sur un changement de calibre, donc aucun chiffre sur la photo
        listeNombre.append("ERREUR") #pour ne pas créer un décalage lors de vérification
        listeNombreInt.append("ERREUR")
            
    except TypeError: #lorsque des parasites ne sont pas totalement éliminés
        listeNombre.append("ERREUR") #pour ne pas créer un décalage lors de vérification
        listeNombreInt.append("ERREUR")
    
    print(listeNombre)

    




def Rognage(longueurH, longueurV, dossierActuel):
    im = ImagePIL.open(path+dossierActuel+"/ImageComplete.jpg")
    

    left = 640-longueurH #détermine la marge de gauche par raport point (0,0)
    top = 360-longueurV #détermine la marge du haut par raport point (0,0)
    width = 2*longueurH #détermine la largeur de la zone souhaitée
    height = 2*longueurV #détermine la longueur de la zone souhaitée
    box = (left, top, left+width, top+height) #(xdepart,ydepart,xarrive,yarrive) et trace rectangle
    area = im.crop(box)

    area.save(path+dossierActuel+"/ImageRognee.png")


def Traitement_Zone(dossierActuel):
    from elec_interface_v30 import seuilF
    global listeImagesRognees
    img = ImagePIL.open(path+dossierActuel+"/ImageRognee.png")
    listeImagesRognees.append(img) #contient toutes les images qui seront sauvegardées dans le dossier de sauvegarde
    M = np.array(img) #on convertit l'image en un tableau numpy

    longueur = M.shape[0]
    largeur = M.shape[1]

    M1D = np.zeros((longueur,largeur), dtype=np.uint16) #ne pas mettre sur 8 bits car on dépassera très surement 255!

    M1D = M1D + M[:,:,0] + M[:,:,1] + M[:,:,2] #on somme toutes les composantes [0,3*255]
    #Ne pas oublier M1D+ sinon M1D se converti automatiquement en uint8 !

    NoirBlanc = np.zeros((longueur,largeur), dtype=np.uint8) #noir=0, blanc =255
    for i in range(0, longueur-1):
        for j in range(0, largeur-1):
            if M1D[i,j] < seuilF:
                NoirBlanc[i,j] = 255 #blanc

    return(NoirBlanc)

#PARASITES_BORDS#
def Parasites_Bords(dossierActuel, NoirBlanc):
    [l,c] = NoirBlanc.shape

    #On traite les parasites dans le haut de l'image
    listeColonneH = []
    for j in range(0, c):
        if NoirBlanc[0,j] == 255: #blanc
            listeColonneH.append(j) #on ajoute le numéro de colonne à traiter 
    for j in listeColonneH:
        i = 0
        while (i+1 != l) & (NoirBlanc[i,j] == 255):
            NoirBlanc[i,j] = 0
            i = i + 1
    #On traite les parasites à droite de l'image(dernière et avant dernière colonne)
    listeLigneD = []
    for i in range(0, l):
        if NoirBlanc[i,c-1] == 255: #blanc
            listeLigneD.append(i)
    for i in listeLigneD:
        j = c - 1
        while (j != 0) & (NoirBlanc[i,j] == 255):
            NoirBlanc[i,j] = 0
            j = j - 1
            
    listeLigneD = []
    for i in range(0, l):
        if NoirBlanc[i,c-2] == 255: #blanc
            listeLigneD.append(i)
    for i in listeLigneD:
        j = c - 2
        while (j != 0) & (NoirBlanc[i,j] == 255):
            NoirBlanc[i,j] = 0
            j = j - 1
    #On traite les parasites à gauche de l'image
    listeLigneG = []
    for i in range(0, l):
        if NoirBlanc[i,0] == 255: #blanc
            listeLigneG.append(i)
    for i in listeLigneG:
        j = 0
        while (j != c) & (NoirBlanc[i,j] == 255):
            NoirBlanc[i,j] = 0
            j = j + 1

    #On traite les parasites dans le bas de l'image (dernière ligne et avant dernière ligne)
    listeColonneB = []
    for j in range(0, c):
        if NoirBlanc[l-1,j] == 255: #blanc
            #listeColonneB.append(j) #on ajoute le numéro de colonne à traiter 
            i = l - 1
            while (i+1 != 0) & (NoirBlanc[i,j] == 255):
                NoirBlanc[i,j] = 0
                i = i - 1

    #On traite les parasites dans le bas de l'image
    listeColonneB = []
    for j in range(0, c):
        if NoirBlanc[l-2,j] == 255: #blanc
            #listeColonneB.append(j) #on ajoute le numéro de colonne à traiter 
            i = l - 2
            while (i+1 != 0) & (NoirBlanc[i,j] == 255):
                NoirBlanc[i,j] = 0
                i = i - 1

    return (NoirBlanc)

#MOYENNAGE#
def Moyennage(dossierActuel, NoirBlanc):

    longueur = NoirBlanc.shape[0]
    largeur = NoirBlanc.shape[1]
    somme = int(0)

    for i in range(1, longueur-2): #pour ne pas avoir de problème de bords
        for j in range(1, largeur-2):
            somme = somme + NoirBlanc[i-1,j] + NoirBlanc[i+1,j] + NoirBlanc[i,j+1] + NoirBlanc[i,j-1]
            if (somme > 510) & (NoirBlanc[i,j] == 0): #si le pixel (i,j) est noir ET entouré de 3/4 blancs
                NoirBlanc[i,j] = 255 #blanc
            elif (somme >= 510) & (NoirBlanc[i,j] == 255): #si le pixel (i,j) est blanc ET entouré de 2/3/4 blancs
                NoirBlanc[i,j] = 255 #blanc
            else: #si le pixel (i,j) est noir ET entouré de 0/1/2 blancs
                  # ou si pixel blanc et 0/1 blanc coté
                NoirBlanc[i,j] = 0 #noir
            somme = 0
                    
    return(NoirBlanc)

#RETRECISSEMENT_ZONE#
def Retrecissement_Zone(dossierActuel, NoirBlancMoy): #sans argument d'entrée et sans sortie.
    [l,c] = NoirBlancMoy.shape

    #H=haut/B=bas/G=gauche/D=droite
    ligneH = 0
    sommeLigneH = sum(NoirBlancMoy[ligneH,:])
    colonneG = 0
    sommeColonneG = sum(NoirBlancMoy[:,colonneG])
    ligneB = -1
    sommeLigneB = sum(NoirBlancMoy[ligneB,:])
    colonneD = -1
    sommeColonneD = sum(NoirBlancMoy[:,colonneD])

    nbrePixelsBlanc = 4 #si moins de  PixelsBlancs, on supprime la ligne/colonne
#avant : 4, je test de mettre 8 : un probleme a été rencontré lors du 7.7 : virgule non detectée car elle a été enlevée ar rognage (Probleme NbrePixelsBlancs)
    #autre probleme avec 8 : barre horizontale du 7 a été toute enlevé : RETOUR a 4 !
    #255=blanc!!
    while (sommeColonneG < nbrePixelsBlanc*255): #on regarde colonnes de gauche
        colonneG = colonneG + 1
        sommeColonneG = sum(NoirBlancMoy[:,colonneG])
    while (sommeLigneH < nbrePixelsBlanc*255): #on regarde lignes du haut
        ligneH = ligneH + 1
        sommeLigneH = sum(NoirBlancMoy[ligneH,:])
    while (sommeLigneB < nbrePixelsBlanc*255): #on regarde lignes du bas
        ligneB = ligneB - 1
        sommeLigneB = sum(NoirBlancMoy[ligneB,:]) 
    while (sommeColonneD < nbrePixelsBlanc*255): #on regarde colonnes de droite
        colonneD = colonneD - 1
        sommeColonneD = sum(NoirBlancMoy[:,colonneD])

    left = colonneG #détermine la marge du haut par raport point (0,0)
    top = ligneH #détermine la marge de gauche par raport point (0,0)
    width = c - colonneG + colonneD #détermine la largeur de la zone souhaitéesachant colonneD<0
    height = l - ligneH + ligneB #détermine la longueur de la zone souhaitée sachant ligneB<0
    box = (left, top, left+width, top+height) #(xdepart,ydepart,xarrive,yarrive) et trace rectangle

    NoirBlancMoyRognee = np.zeros((height, width), dtype=np.uint8)
    NoirBlancMoyRognee = NoirBlancMoy[top:top+height, left:left+width]
    
    return(NoirBlancMoyRognee)



def Retrecissement_Zone_Argument(AAnalyser, nbrePixelsBlanc): #2 arguments entrée, 1 argument sortie
    img = ImagePIL.fromarray(AAnalyser) #on transforme le tableau en image pour pouvoir le rogner à l'aide de crop
    [l,c] = AAnalyser.shape

    #H=haut/B=bas/G=gauche/D=droite
    ligneH = 0
    sommeLigneH = sum(AAnalyser[ligneH,:])
    colonneG = 0
    sommeColonneG = sum(AAnalyser[:,colonneG])
    ligneB = -1
    sommeLigneB = sum(AAnalyser[ligneB,:])
    colonneD = -1
    sommeColonneD = sum(AAnalyser[:,colonneD])

    #255=blanc!!
    while (sommeColonneG < nbrePixelsBlanc*255): #on regarde colonnes de gauche
        colonneG = colonneG + 1
        sommeColonneG = sum(AAnalyser[:,colonneG]) 
    while (sommeLigneH < nbrePixelsBlanc*255): #on regarde lignes du haut
        ligneH = ligneH + 1
        sommeLigneH = sum(AAnalyser[ligneH,:])
    while (sommeLigneB < nbrePixelsBlanc*255): #on regarde lignes du bas
        ligneB = ligneB - 1
        sommeLigneB = sum(AAnalyser[ligneB,:])
    while (sommeColonneD < nbrePixelsBlanc*255): #on regarde colonnes de droite
        colonneD = colonneD - 1
        sommeColonneD = sum(AAnalyser[:,colonneD])

    left = colonneG #détermine la marge du haut par rapport point (0,0)
    top = ligneH #détermine la marge de gauche par rapport point (0,0)
    width = c - colonneG + colonneD #détermine la largeur de la zone souhaitéesachant colonneD<0
    height = l - ligneH + ligneB #détermine la longueur de la zone souhaitée sachant ligneB<0
    box = (left, top, left+width, top+height) #(xdepart,ydepart,xarrive,yarrive) et trace rectangle
    area = img.crop(box)
    return(np.array(area))

def Retrecissement_Gauche(AAnalyser, nbrePixelsBlanc): #si moins de  PixelsBlancs, on supprime la colonne
    img=ImagePIL.fromarray(AAnalyser) #on transforme le tableau en image pour pouvoir le rogner à l'aide de crop
    [l,c]=AAnalyser.shape

    colonneG=0
    sommeColonneG=sum(AAnalyser[:,colonneG])

    #255=blanc!!
    while(sommeColonneG<nbrePixelsBlanc*255): #on regarde colonnes de gauche
        colonneG=colonneG+1
        sommeColonneG=sum(AAnalyser[:,colonneG])
        
    left = colonneG #détermine la marge du haut par rapport point (0,0)
    top = 0 #détermine la marge de gauche par rapport point (0,0)
    width = c-colonneG #détermine la largeur de la zone souhaitéesachant colonneD<0
    height = l #détermine la longueur de la zone souhaitée sachant ligneB<0
    box = (left, top, left+width, top+height) #(xdepart,ydepart,xarrive,yarrive) et trace rectangle
    area = img.crop(box)
    return(np.array(area))

#SEPARATION_PARFAITE_DIGITS#
def Separation_Parfaite_Digits(dossierActuel, AAnalyser):
    [l,c]=AAnalyser.shape
    xk=[] # du type [xdepart, xfin] pour le repérage d'un trait blanc
    x=[] #contient les xk  
    matriceLigne=[]

    for j in range(0,c):
        if max((AAnalyser[:round(3/4*l),j])>=255): #si les 3/4 hauts de la colonne j de la matrice contient au moins 1 pixel blanc
            matriceLigne.append(255) #on ajoute 255
        else:
            matriceLigne.append(0) #sinon 0
            
    i=0
    while i<len(matriceLigne)-1: #len(matriceLigne)-1 ? mais ceci a posé problème quand virgule = 1 pixel dernière colonne
        if matriceLigne[i]==255:
            xk.append(i) #on ajoute l'indice de départ du trait
            while (i<len(matriceLigne)-1)&(matriceLigne[i]==255):
                i+=1
            xk.append(i) #on ajoute l'indice de fin du trait
            x.append(xk) #on ajoute 
            xk=[]
        else:
            i+=1

    nbreDigit=len(x)
    listeDigits=[]
    listeDigitsNonRetrecis=[AAnalyser[:,x[0][0]:x[0][1]]] #cette liste va permettre de résoudre le problème du signe avec distinction 1 et 7
                                                            
    digit=Retrecissement_Zone_Argument(AAnalyser[:,x[0][0]:x[0][1]],1) #permet d'avoir la virgule collée au bord gauche (Retrecissement_Gauche pourrait suffir mais on s'assure que le chiffre est bien centré)
    listeDigits.append(digit) #on ajoute le premier digit de xdépart1:xfin1


    for NumeroDigit in range(1,nbreDigit):
        digit=Retrecissement_Zone_Argument(AAnalyser[:,x[NumeroDigit-1][1]+2*0:x[NumeroDigit][1]],1)
        listeDigitsNonRetrecis.append(AAnalyser[:,x[NumeroDigit-1][1]:x[NumeroDigit][1]])
        listeDigits.append(digit) #on ajoute les digits suivants de xfin(digit):xfin(digit+1).       
    return (listeDigits,listeDigitsNonRetrecis)

#ANALYSE_SIGNE#
def Analyse_Signe(listeDigits, dossierActuel, AAnalyser): 
    [lAAnalyser,cAAnalyser] = AAnalyser.shape

    virgulePotentielle = listeDigits[0]
    [l,c] = virgulePotentielle.shape
    if l < lAAnalyser/3: #on discrimine le signe par son nombre de lignes
        signe = -1
        return(listeDigits[1:],signe) #on enlève le premier élément du tableau (le signe moins)
    else:
        signe = 1
        return(listeDigits,signe)


#ANALYSE_COLONNE_SANS_SIGNE#
def Analyse_Colonnes_Sans_Signe(signe,listeDigitsNonRetrecis,dossierActuel, AAnalyser):
    
    if signe == 1:
        [lAAnalyser,cAAnalyser] = AAnalyser.shape
    else:
        listeDigitsNonRetrecis[1] = Retrecissement_Zone_Argument(listeDigitsNonRetrecis[1],1)
        cAAnalyser=0
        for chiffre in listeDigitsNonRetrecis[1:]:
            [l,c] = chiffre.shape
            cAAnalyser = cAAnalyser + c
    return cAAnalyser


#DETECTION_VIRGULE_VERTICALE#
def Detection_Virgule_Verticale(nbreDigits,listeDigits):
    [nbreTraits,lTraits]=[[],[]] 
    for k in range(1,nbreDigits+1):
        nbreEtudie=listeDigits[k-1]
        [l,c]=nbreEtudie.shape
        nbreTraitsk=0 #compte le nbre de traits
        lTraitsk=[] #tableau contenant la longueur des traits
        matriceLigne=[] #ligne dont colonne vaut 255 
        for j in range(0,c):
            if max((nbreEtudie[:,j])>=255): #si la colonne j de la matrice contient au moins 1 pixel blanc
                matriceLigne.append(255) #on ajoute 255
            else:
                matriceLigne.append(0) #sinon 0
                
        i=0
        while i<len(matriceLigne)-1: #len(matriceLigne)-1 ? mais ceci a posé problème quand virgule = 1 pixel dernière colonne
            if matriceLigne[i]==255:
                nbreTraitsk+=1
                lTraitsk.append(1)
                while (i<len(matriceLigne)-1)&(matriceLigne[i]==255):
                    i+=1
                    lTraitsk[nbreTraitsk-1]+=1
            else:
                i+=1 
        lTraits.append(lTraitsk)
        nbreTraits.append(nbreTraitsk)
        
    return(nbreTraits,lTraits)

#SUPPRESSION_VIRGULE#
def Suppression_Virgule(listeDigits,nbreDigits,nbreTraits,lTraits): #supprime la virgule sur le digit concerné et renvoie la division nécessaire
    global listeErreursVirgule
    division_locale=1
    try: #on essaie de trouver 2 dans la liste
        indice2=nbreTraits.index(2)
        division_locale=10**(nbreDigits-indice2)
        listeDigits[indice2]=(listeDigits[indice2])[:,lTraits[indice2][0]:] #on enlève la virgule, dont la longueur est lTraits[indice2][0]
        listeDigits[indice2]=Retrecissement_Gauche(listeDigits[indice2],2) #une fois la virgule enlevée, on enlève le bord
    except ValueError: #si on ne le trouve pas ("ValueError: 2 is not in list"), on avertit l'utilisateur, sauf s'il y a 2 digits car la virgule est forcément au milieu
        if nbreDigits==2:
            division_locale=10         
        else:
            division_locale=1
    finally: #dans tous les cas on retourne listeDigits et division
        return(listeDigits,division_locale)

#COMPARAISON#
def Comparaison(listeliste,nbre): #regarde si dans chaque liste il y a l'élément 255. Renvoie une liste contenant 1 si égaux, 0 sinon
    listeSortie=[]
    for liste in listeliste:
        if (nbre in liste): #in renvoie TRUE si l'élément nbre est dans liste
            listeSortie.append(1)
        else:
            listeSortie.append(0)
    return listeSortie

#ANALYSE_CHIFFRE#
def Analyse_Chiffre(chiffreTableau): #renvoie le chiffre associé à chiffreTableau
    global erreur #erreur=1 quand 1 chiffre n'a pas été reconnu
    zero=[1,1,1,1,1,1,0]
    un=[0,1,1,0,0,0,0,0]
    deux=[1,1,0,1,1,0,1]
    trois=[1,1,1,1,0,0,1]
    quatre=[0,1,1,0,0,1,1]
    cinq=[1,0,1,1,0,1,1]
    six=[1,0,1,1,1,1,1]
    sept=[1,1,1,0,0,0,0]
    huit=[1,1,1,1,1,1,1]
    neuf=[1,1,1,1,0,1,1]
    listeChiffre=[zero,un,deux,trois,quatre,cinq,six,sept,huit,neuf]
    valeur=0
    for test in listeChiffre:
        if test==chiffreTableau:
            return(valeur)
        else:
            valeur=valeur+1
        if valeur==10:
            if chiffreTableau==[1,1,1,1,0,0,0]:
                return(7)
            else:
                erreur=1
                print(chiffreTableau)
                return(0)               

#ANALYSE_CHIFFRE#
def Analyse_Sequence_Chiffre(nbreDigits,listeDigits,division,signe, cAAnalyser):

    global erreur
    erreur = 0
    listeChiffre=[]
    
    for digit in listeDigits[:nbreDigits]: #on prend que le nombre correspondant au chiffre
        
        [lDigit,cDigit]=digit.shape
        
        if cDigit*2<cAAnalyser/nbreDigits: #on discrimine par rapport à la largeur du digit. CHANGEMENT DE FORMULE SUITE A UNE ERREUR AVEC 2 DIGITS COMMENCANT PAR 1. Formule était : cDigit*2<cAAnalyser/(1.5*nbreDigits):
            chiffreDecode=1
        else:
            #TEST2: une droite est testé, 1 seul point sur la droite suffit pour confirmer la présence d'un segment
            droiteA=list(digit[0:round(lDigit/4),round(cDigit/2)]) #on convertit un tableau numpy en liste
            droiteB=list(digit[round(lDigit/4),round(cDigit/2):cDigit])
            droiteC=list(digit[round(3/4*lDigit),round(cDigit/2):cDigit])
            droiteD=list(digit[round(-1/4*lDigit):,round(cDigit/2)])
            droiteE=list(digit[round(3/4*lDigit),0:round(cDigit/2)])
            droiteF=list(digit[round(lDigit/4),0:round(cDigit/2)])
            droiteG=list(digit[round(3/8*lDigit):round(5/8*lDigit),round(cDigit/2)])
            #TEST2
            chiffreTableau=Comparaison([droiteA,droiteB,droiteC,droiteD,droiteE,droiteF,droiteG],255)
            chiffreDecode=Analyse_Chiffre(chiffreTableau)
        listeChiffre.append(chiffreDecode)
    nombre=0
    if erreur == 1 :
        erreur = 0
        return("ERREUR", "ERREUR")
    else:
        for i in range(nbreDigits):
                nombre+=int(listeChiffre[i]*10**(nbreDigits-i-1))
        if division==1:
            return(str(signe*nombre), "ERREUR")
        else:
            chaine='%.'+str(int(log10(division)))+'f' #correspond au nombre de chiffres après la virgule ex : '%.3f' = 3 chiffres après virgules
            chiffre=signe*nombre/division
            return(chaine %chiffre, signe*round(nombre/division,int(log10(division))))





