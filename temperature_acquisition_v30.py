
####LES IMPORTATIONS et VARIABLES/DEFINITIONS GLOBALES####

import os #pour gérer les fichiers/dossiers
import shutil #pour copier les fichiers textes
import time
#import picamera

import numpy.core._methods #pour l'executable
import numpy.lib.format #pour l'executable

import numpy as np
from PIL import Image as ImagePIL #ATTENTION : "as ImagePIL" a été rajouté sinon il y a un conflit (type object 'Image' has no attribute 'open') avec tkinter
from math import log10
from tkinter.ttk import * #a mettre avant ligne suivante
from tkinter import *
from tkinter.filedialog import * #pour le parcours des dossiers
from tkinter.messagebox import * #pour les alertes
from glob import * #permet de lister les éléments correspondants à un motif (nous .png)

from reportlab.lib import colors #pour générer le PDF
from reportlab.lib.pagesizes import  inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

import serial #pour communication série RS232 (Consort)
import visa #pour communicaion parallèle IEEE (3458A)

repertoireScript = os.getcwd() #renvoie le chemin absolu du script
path = repertoireScript+"/Temporaire/"


####LES FONCTIONS####

#POUR GERER LES DOSSIERS#

def Creation_Dossier(NomDossier):
    if not os.path.exists(path+NomDossier): #si dossier existe pas
        os.makedirs(path+NomDossier)

def Creation_Dossiers_Temporaires(nbrePhoto):
    for iPhoto in range (1,nbrePhoto+1):
        dossierActuel="Photo"+str(iPhoto)
        Creation_Dossier(dossierActuel)

def Suppression_Dossier(NomDossier):
    if os.path.exists(path+NomDossier): #si le dossier existe
        for fichier in os.listdir(path+NomDossier): #on supprime les fichiers du dossiers
            os.remove(path+NomDossier+"/"+fichier)
        os.rmdir(path+NomDossier) #pour ensuite supprimer le dossier

def Creation_Dossier_Numero_Certificat():
    from temperature_interface_v30 import cheminDossierSauvegardeComplet
    global cheminDossierSauvegardeComplet
    if not os.path.exists(cheminDossierSauvegardeComplet): 
        os.makedirs(cheminDossierSauvegardeComplet)
    if not os.path.exists(cheminDossierSauvegardeComplet+"/Photos"):
        os.makedirs(cheminDossierSauvegardeComplet+"/Photos")


#ROGNAGE#
def Rognage(longueurH, longueurV, dossierActuel):
    im = ImagePIL.open(path+dossierActuel+"/ImageComplete.jpg")
    
    left = 640-longueurH #détermine la marge de gauche par rapport point (0,0)
    top = 360-longueurV #détermine la marge du haut par rapport point (0,0)
    width = 2*longueurH #détermine la largeur de la zone souhaitée
    height = 2*longueurV #détermine la longueur de la zone souhaitée
    box = (left, top, left+width, top+height) #(xdepart,ydepart,xarrive,yarrive) et trace rectangle
    area = im.crop(box)
    
    area.save(path+dossierActuel+"/ImageRognee.png")

#TRAITEMENT_ZONE#
def Traitement_Zone_Initialisation():
    from temperature_interface_v30 import Canevas, seuil_SV
    dossierActuel = "Calibration"
    seuil = int(seuil_SV.get())
    global photo,seuilF #A METTRE ABSOLUMENT SINON L'IMAGE NE S'AFFICHE PAS
    img = ImagePIL.open(path+dossierActuel+"/ImageRognee.png")
    M = np.array(img) #on convertit l'image en un tableau numpy

    longueur = M.shape[0]
    largeur = M.shape[1]

    M1D = np.zeros((longueur,largeur), dtype=np.uint16) #ne pas mettre sur 8 bits car on dépassera très surement 255!

    M1D = M1D + M[:,:,0] + M[:,:,1] + M[:,:,2] #on somme toutes les composantes [0,3*255]
    #Ne pas oublier M1D+ sinon M1D se converti automatiquement en uint8 !

    NoirBlanc = np.zeros((longueur, largeur), dtype=np.uint8) #noir=0, blanc =255

    NoirBlancCopie = np.copy(NoirBlanc) #on travaille sur copie pour pouvoir baisser le seuil si besoin
    for i in range(0, longueur):
        for j in range(0, largeur):
            if M1D[i,j] < seuil:
                NoirBlancCopie[i,j] = 255 #blanc

    NoirBlancImage = ImagePIL.fromarray(NoirBlancCopie) #on convertit un tableau numpy en image         
    NoirBlancImage.save(path+dossierActuel+"/ImageNoirBlanc.png")
    seuilF = seuil

    Canevas.delete(ALL)
    photo = PhotoImage(file=path+dossierActuel+"/ImageNoirBlanc.png")
    Canevas.create_image(50, 50, anchor=NW, image=photo)


def Traitement_Zone(dossierActuel):
    global cheminDossierSauvegardeComplet, listeImagesRognees
    img = ImagePIL.open(path+dossierActuel+"/ImageRognee.png")
    listeImagesRognees.append(img) #contient toutes les images qui seront sauvegardées
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
#avant : 4, je test de mettre 8 : un probleme a été rencontré lors du 7.7 : virgule non detectée car elle a été enlevée par rognage (Probleme NbrePixelsBlancs)
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
        listeDigits.append(digit)      
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
def Suppression_Virgule(listeDigits,nbreDigits,nbreTraits,lTraits,iPhoto): #supprime la virgule sur le digit concerné et renvoie la division nécessaire
    from temperature_interface_v30 import Ecriture_Acquisition
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
            Ecriture_Acquisition("Attention, la virgule n'a pas été détectée!")
            listeErreursVirgule.append(iPhoto)
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
    from temperature_interface_v30 import Ecriture_Acquisition
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
                Ecriture_Acquisition("Erreur de reconnaissance, mais très probablement 7")
                return(7)
            else:
                Ecriture_Acquisition("Erreur : aucun chiffre n'a été reconnu")
                erreur=1
                print(chiffreTableau)
                return(0)               

#ANALYSE_CHIFFRE#
def Analyse_Sequence_Chiffre(nbreDigits,listeDigits,division,signe, cAAnalyser):
    from temperature_interface_v30 import Ecriture_Acquisition
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
            Ecriture_Acquisition("Le nombre sans la virgule est: "+str(signe*nombre))
            return(str(signe*nombre), "ERREUR")
        else:
            Ecriture_Acquisition("Le nombre est: "+str(signe*round(nombre/division,int(log10(division)))))
            chaine='%.'+str(int(log10(division)))+'f' #correspond au nombre de chiffres après la virgule ex : '%.3f' = 3 chiffres après virgules
            chiffre=signe*nombre/division
            return(chaine %chiffre, signe*round(nombre/division,int(log10(division))))


def Acquisition():
    from temperature_interface_v30 import Bilan, longueurH, longueurV, camera, Canevas, Ecriture_Acquisition, Ecriture_Etat_Acquisition, nomCertificat_SV, temperature_SV, cocheeMode, cochee, numCapteur_SV, numAfficheur_SV, nbreAcquisitions_SV, nomTemperature_texte, Verification, tempsAcquisition_SV
    from temperature_interface_v30 import etalon, sonde
    from temperature_interface_v30 import Verification_Nom
    global camera
    Canevas.delete(ALL)
    global longueurH,longueurV,seuilF,cheminDossierSauvegardeComplet,listeNombre, listeErreursVirgule, listeTemps, running, listeImagesRognees, l, nbreErreurs, Verification
    global listeTemperatureConsort, listeRatioConsort
    Verification_Nom()
    from temperature_interface_v30 import Verification #pour actualiser la valeur de Verification
    if Verification == 0:
        showwarning('Attention', "Veuillez compléter correctement l'étape 0")

    elif etalon == 0 :
        showwarning('Attention', "Veuillez compléter l'onglet Communication (étalon)")

    elif (etalon != 'Aucun') & (sonde == 0):
        showwarning('Attention', "Veuillez compléter l'onglet Communication (sonde)")
        
    else:     
        l=0 #lorsqu'on relance une acquisition on écrit en haut
        listeNbreDigits=[]
        listeErreursVirgule = []
        listeTemps=[]
        nbrePhoto=int(nbreAcquisitions_SV.get())
        if nbrePhoto>1:
            intervallePhoto=int(tempsAcquisition_SV.get())
        listeNombre=[]
        listeNombreInt=[]
        listeImagesRognees=[]
        listeRatioConsort = []
        running = 1
        enregistrement = 1 #on enregistre systématiquement les données, sauf éventuellement lors d'un arrêt forcé de l'acquisition (demande à l'uti.)

        Creation_Dossiers_Temporaires(nbrePhoto) #création des dossiers avant pour ne pas créer de décalage dans la prise des photos

        if etalon == "Consort": #partie comm
            Initialisation_Consort()
        elif etalon == "3458A":
            Initialisation_3458A()
        
        for iPhoto in range (1,nbrePhoto+1):
            if running == 1 : #passe à 0 si l'utilisateur force l'arret avec le bouton
                dossierActuel="Photo"+str(iPhoto) #on se place dans le bon dossier
                
                listeTemps.append(time.strftime("%H:%M:%S")) # de la forme '16:28:42'
                tempsDebut=time.time() #temps avant le début du traitement  

                camera.capture(path+dossierActuel+"/ImageComplete.jpg", use_video_port=True)

                if etalon == "Consort":
                    ratioConsort = Lecture_Consort()
                    listeRatioConsort.append(ratioConsort)
                elif etalon == "3458A":
                    ratioConsort = Lecture_3458A()
                    listeRatioConsort.append(ratioConsort)
                   

                Ecriture_Etat_Acquisition("Photo numéro "+str(iPhoto)+" prise, traitement en cours.")
                    
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
                        [listeDigits,division] = Suppression_Virgule(listeDigits,nbreDigits, nbreTraits, lTraits, iPhoto)
                       
                        [nombreStr, nombreInt]=Analyse_Sequence_Chiffre(nbreDigits,listeDigits,division,signe,cAAnalyser)
                        listeNombre.append(nombreStr)
                        listeNombreInt.append(nombreInt)
                        
                        
                    else: #si nbreDigits = 1, ceci est en fait impossible : il s'agit d'un changement de calibre ou la virgule n'a pas été totalement effacée (sinon on serait dans l'exception) et elle sera considérée comme un 1
                        Ecriture_Acquisition("Il n'y avait pas de chiffre sur la photo")
                        listeNombre.append("ERREUR") #pour ne pas créer un décalage lors de vérification
                        listeNombreInt.append("ERREUR")
                        
                except IndexError: #lorsque la photo est prise sur un changement de calibre, donc aucun chiffre sur la photo
                    Ecriture_Acquisition("Il n'y avait pas de chiffre sur la photo")
                    listeNombre.append("ERREUR") #pour ne pas créer un décalage lors de vérification
                    listeNombreInt.append("ERREUR")
                        
                except TypeError: #lorsque des parasites ne sont pas totalement éliminés
                    Ecriture_Acquisition("Analyse de l'image impossible")
                    listeNombre.append("ERREUR") #pour ne pas créer un décalage lors de vérification
                    listeNombreInt.append("ERREUR")
                    
                finally : #dans tous les cas on attend
                    tempsTraitement=time.time()-tempsDebut #temps à la fin du traitement raitement
                    if (nbrePhoto>1) :
                        if(iPhoto < nbrePhoto) & (intervallePhoto-tempsTraitement>0) : #pour ne pas attendre une fois la dernière photo prise
                            Ecriture_Etat_Acquisition("En attente pour la photo "+str(iPhoto+1)+" sur "+str(nbrePhoto)+" (...)")
                            time.sleep(intervallePhoto-tempsTraitement)
#AJOUT POUR LE MODE VARIABLE
        if int(cocheeMode.get()) == 1:
            nbreErreurs2=listeNombre.count("ERREUR")
            if (intervallePhoto-tempsTraitement>0) :
                Ecriture_Etat_Acquisition("En attente pour la photo "+str(len(listeNombre)+1)+" sur "+str(nbrePhoto)+" (...)")
                time.sleep(intervallePhoto-tempsTraitement)
            while nbreErreurs2 != 0:
                
                dossierActuel="Photo"+str(len(listeNombre)+1) #on se place dans le bon dossier
                os.makedirs(path+dossierActuel)
                camera.capture(path+dossierActuel+"/ImageComplete.jpg", use_video_port=True)

                if etalon == "Consort":
                    ratioConsort = Lecture_Consort()
                    listeRatioConsort.append(ratioConsort)
                elif etalon == "3458A":
                    ratioConsort = Lecture_3458A()
                    listeRatioConsort.append(ratioConsort)


                listeTemps.append(time.strftime("%H:%M:%S")) # de la forme '16:28:42'
                tempsDebut=time.time() #temps avant le début du traitement        

                Ecriture_Etat_Acquisition("Photo numéro "+str(len(listeNombre)+1)+" prise, traitement en cours.")
                    
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
                        [listeDigits,division] = Suppression_Virgule(listeDigits,nbreDigits, nbreTraits, lTraits, iPhoto)
                       
                        [nombreStr, nombreInt]=Analyse_Sequence_Chiffre(nbreDigits,listeDigits,division,signe,cAAnalyser)
                        listeNombre.append(nombreStr)
                        listeNombreInt.append(nombreInt)
                        
                    else: #si nbreDigits = 1, ceci est en fait impossible : il s'agit d'un changement de calibre ou la virgule n'a pas été totalement effacée (sinon on serait dans l'exception) et elle sera considérée comme un 1
                        Ecriture_Acquisition("Il n'y avait pas de chiffre sur la photo")
                        listeNombre.append("ERREUR") #pour ne pas créer un décalage lors de vérification
                        listeNombreInt.append("ERREUR")
                        nbreErreurs2 += 1
                        
                except IndexError: #lorsque la photo est prise sur un changement de calibre, donc aucun chiffre sur la photo
                    Ecriture_Acquisition("Il n'y avait pas de chiffre sur la photo")
                    listeNombre.append("ERREUR") #pour ne pas créer un décalage lors de vérification
                    listeNombreInt.append("ERREUR")
                    nbreErreurs2 += 1
                        
                except TypeError: #lorsque des parasites ne sont pas totalement éliminés
                    Ecriture_Acquisition("Analyse de l'image impossible")
                    listeNombre.append("ERREUR") #pour ne pas créer un décalage lors de vérification
                    listeNombreInt.append("ERREUR")
                    nbreErreurs2 += 1
                    
                finally : #dans tous les cas on attend
                    tempsTraitement=time.time()-tempsDebut #temps à la fin du traitement raitement
                    nbreErreurs2 -= 1
                    if (nbreErreurs2 != 0) :
                        if intervallePhoto - tempsTraitement > 0 : #pour ne pas attendre une fois la dernière photo prise
                            Ecriture_Etat_Acquisition("En attente pour la photo "+str(iPhoto+1)+" sur "+str(nbrePhoto)+" (...)")
                            time.sleep(intervallePhoto-tempsTraitement)
                            

#FIN POUR LE MODE VARIABLE
        #sauvegarde des photos
        for img in listeImagesRognees:         
            img.save(cheminDossierSauvegardeComplet+"/Photos/"+nomCertificat_SV.get()+"_"+temperature_SV.get()+'_Photo'+str(1+len(glob(cheminDossierSauvegardeComplet+'/Photos/'+nomCertificat_SV.get()+"_"+temperature_SV.get()+'_*.png')))+".png")

        if running == 0:
            if askyesno("Arrêt de l'acquisition", 'Voulez-vous enregistrer les données ?'):
                enregistrement = 1 
            else:
                enregistrement = 0
                for fichier in glob(cheminDossierSauvegardeComplet+"/Photos/*"+temperature_SV.get()+"_*.png"): #on va supprimer les photos correspondantes
                    os.remove(fichier)
                Ecriture_Etat_Acquisition("Acquisition arrêtée, données non enregistrées") 

        if (enregistrement == 1) & (etalon == "Aucun"):
            Ecriture_Etat_Acquisition("Acquisition terminée, enregistrement des données")
            nom = nomCertificat_SV.get()+'_'+temperature_SV.get()
            pathTexte=cheminDossierSauvegardeComplet
            nbreErreurs = Bilan(listeNombre, cheminDossierSauvegardeComplet)
            
            fichier = open(pathTexte+'/'+nom+".txt", "w") #ATTENTION: si le fichier existe on le supprime!
            
            [mini, maxi, moyenne, variance, ecartType] = Calculs_Statistique(listeNombreInt)
            fichier.write("Certificat\t"+nomCertificat_SV.get()+"\n")
            fichier.write("Température\t"+temperature_SV.get()+"\n")
            fichier.write("N° Afficheur\t"+numAfficheur_SV.get()+"\n")
            fichier.write("N° Capteur\t"+numCapteur_SV.get()+"\n")
            if int(cocheeMode.get()) == 1 :
                fichier.write("Nb Acquisitions\t"+nbreAcquisitions_SV.get()+' dont '+str(nbreErreurs)+' erreurs (et '+str(len(listeErreursVirgule))+" erreurs de détection de la virgule). Compensation des erreurs\n")
            else:
                fichier.write("Nb Acquisitions\t"+nbreAcquisitions_SV.get()+' dont '+str(nbreErreurs)+' erreurs (et '+str(len(listeErreursVirgule))+" erreurs de détection de la virgule)\n")
            fichier.write("Intervalle temps\t"+tempsAcquisition_SV.get()+"s\n")

            fichier.write(time.strftime("%d/%m/%Y")+"\t Heure\t Valeur\t Moyenne\t Ecart-type\t Max\t Min\t Max-Min\n")
            
            fichier.write("\t \t \t"+str(moyenne).replace(".",",")+"\t"+str(ecartType).replace(".",",")+"\t"+str(maxi).replace(".",",")+"\t"+str(mini).replace(".",",")+"\t"+str(round(maxi-mini,3)).replace(".",",")+"\n")
            
            for indice in range(len(listeNombre)) : 
                heure = listeTemps[indice]
                nombre = listeNombre[indice].replace(".",",")
                fichier.write("\t"+heure+"\t"+nombre+"\n")
                
            fichier.close()
            Ecriture_Etat_Acquisition("Acquisition terminée, Ctrl+d pour vérifier les données")
            Creation_PDF(listeTemps, listeNombre, cheminDossierSauvegardeComplet, nom, moyenne, ecartType, maxi, mini, nbreErreurs)
            
            if int(cochee.get()) == 1: #si la case analyse des données a été cochée
                Analyse_Donnee(listeNombre, listeNombreInt)
                
            Ecriture_Acquisition("Moyenne = "+str(moyenne))
            Ecriture_Acquisition("Ecart-type = "+str(ecartType))
            Ecriture_Acquisition("Max = "+str(maxi))
            Ecriture_Acquisition("Min = "+str(mini))
            Ecriture_Acquisition("Max-Min = "+str(round(maxi-mini,3)))
            nomTemperature_texte.configure(bg = 'red')
            Verification = 0


        if (enregistrement == 1) & (etalon != "Aucun"):
            Ecriture_Etat_Acquisition("Acquisition terminée, enregistrement des données")
            #traitement des données de l'étalon
            [aSonde, bSonde, cSonde, dSonde] = Correction_Sonde(sonde)
            listeTemperatureConsort = Conversion_Temperature(aSonde, bSonde, cSonde, dSonde, listeRatioConsort)
            [miniEtalon, maxiEtalon, moyenneEtalon, varianceEtalon, ecartTypeEtalon] = Calculs_Statistique_Sonde(listeTemperatureConsort)
        
            Ecriture_Etat_Acquisition("Acquisition terminée, enregistrement des données")
            nom = nomCertificat_SV.get()+'_'+temperature_SV.get()
            pathTexte=cheminDossierSauvegardeComplet
            nbreErreurs = Bilan(listeNombre, cheminDossierSauvegardeComplet)
            fichier = open(pathTexte+'/'+nom+".txt", "w") #ATTENTION: si le fichier existe on le supprime!
            [mini, maxi, moyenne, variance, ecartType] = Calculs_Statistique(listeNombreInt)

            fichier.write("Certificat\t"+nomCertificat_SV.get()+"\n")
            fichier.write("Température\t"+temperature_SV.get()+"\n")
            fichier.write("N° Afficheur\t"+numAfficheur_SV.get()+"\n")
            fichier.write("N° Capteur\t"+numCapteur_SV.get()+"\n")
            if int(cocheeMode.get()) == 1 :
                fichier.write("Nb Acquisitions\t"+nbreAcquisitions_SV.get()+' dont '+str(nbreErreurs)+' erreurs (et '+str(len(listeErreursVirgule))+" erreurs de détection de la virgule). Compensation des erreurs\n")
            else:
                fichier.write("Nb Acquisitions\t"+nbreAcquisitions_SV.get()+' dont '+str(nbreErreurs)+' erreurs (et '+str(len(listeErreursVirgule))+" erreurs de détection de la virgule)\n")
            fichier.write("Intervalle temps\t"+tempsAcquisition_SV.get()+"s\n")
            fichier.write("Etalon\t"+etalon+"\n")
            fichier.write("Ref. Sonde\t"+sonde+"\n")
            fichier.write("Date\t"+time.strftime("%d/%m/%Y")+"\n")
            fichier.write("Appareil\n")
            fichier.write("Moyenne\t Ecart-type\t Max\t Min\t Max-Min\n")
            fichier.write(str(moyenne).replace(".",",")+"\t"+str(ecartType).replace(".",",")+"\t"+str(maxi).replace(".",",")+"\t"+str(mini).replace(".",",")+"\t"+str(round(maxi-mini,3)).replace(".",",")+"\n")

            fichier.write('\n')
            
            fichier.write("Etalon\n")
            fichier.write("Moyenne\t Ecart-type\t Max\t Min\t Max-Min\n")
            fichier.write(str(moyenneEtalon).replace(".",",")+"\t"+str(ecartTypeEtalon).replace(".",",")+"\t"+str(maxiEtalon).replace(".",",")+"\t"+str(miniEtalon).replace(".",",")+"\t"+str(round(maxiEtalon-miniEtalon,4)).replace(".",",")+"\n")

            fichier.write('\n')
            
            if etalon == "Consort":
                fichier.write("Heure\t Valeur\t \t Valeur étalon\t Ratio brut\n")
            elif etalon == "3458A" : #A VERIFIER 
                fichier.write("Heure\t Valeur\t \t Valeur étalon\t Valeur ohmique\n")

            for indice in range(len(listeNombre)) : 
                heure = listeTemps[indice]
                nombre = listeNombre[indice].replace(".",",")
                nombreConsort = str(round(listeTemperatureConsort[indice],4)).replace(".",",")
                if etalon == 'Consort':
                    ratioConsort = listeRatioConsort[indice].replace(".",",")
                elif etalon == '3458A':
                    ratioConsort = str(listeRatioConsort[indice]).replace(".",",")
                
                fichier.write(heure+"\t"+nombre+"\t\t"+nombreConsort+"\t"+ratioConsort+'\n')
    
            fichier.close()

            Ecriture_Etat_Acquisition("Acquisition terminée, Ctrl+d pour vérifier les données")

            Creation_PDF_Etalon(listeTemps, listeNombre, cheminDossierSauvegardeComplet, nom, moyenne, ecartType, maxi, mini, nbreErreurs, listeTemperatureConsort, listeRatioConsort, miniEtalon, maxiEtalon, moyenneEtalon, varianceEtalon, ecartTypeEtalon)

            if int(cochee.get()) == 1: #si la case analyse des données a été cochée
                Analyse_Donnee(listeNombre, listeNombreInt)

            Ecriture_Acquisition("APPAREIL : ")    
            Ecriture_Acquisition("Moyenne = "+str(moyenne))
            Ecriture_Acquisition("Ecart-type = "+str(ecartType))
            Ecriture_Acquisition("Max = "+str(maxi))
            Ecriture_Acquisition("Min = "+str(mini))
            Ecriture_Acquisition("Max-Min = "+str(round(maxi-mini,3)))
            Ecriture_Acquisition("\n")
            
            Ecriture_Acquisition("ETALON : ")    
            Ecriture_Acquisition("Moyenne = "+str(moyenneEtalon))
            Ecriture_Acquisition("Ecart-type = "+str(ecartTypeEtalon))
            Ecriture_Acquisition("Max = "+str(maxiEtalon))
            Ecriture_Acquisition("Min = "+str(miniEtalon))
            Ecriture_Acquisition("Max-Min = "+str(round(maxiEtalon-miniEtalon,4)))

            nomTemperature_texte.configure(bg = 'red')
            Verification = 0

        
        if etalon == "Consort":
            Fermeture_Consort()
            


def Acquisition_Arret():
    from temperature_interface_v30 import Ecriture_Etat_Acquisition
    global running
    running = 0
    Ecriture_Etat_Acquisition("Arrêt de l'acquisition en cours, patientez")


def Creation_PDF(listeTemps, listeNombre, cheminDossierSauvegardeComplet, nom, moyenne, ecartType, maxi, mini, nbreErreurs):
    from temperature_interface_v30 import nomCertificat_SV, temperature_SV, numCapteur_SV, numAfficheur_SV, nbreAcquisitions_SV, cocheeMode, tempsAcquisition_SV
    global listeErreursVirgule
    doc = SimpleDocTemplate(cheminDossierSauvegardeComplet+"/"+nom+".pdf")

    elements = []
    
    lignes = len(listeTemps) + 2 + 4 + 2 #nbre de lignes du tableau (+2 pour la ligne Heure, Valeur etc et ligne affichant les stats, nom certif, température, num afficheur, num capteur)
    data = [['' for j in range(8)] for i in range(lignes)] #génération d'un tableau vide

    data[0]=["Certificat", '', nomCertificat_SV.get(), '', '', '', '']
    data[1]=["Température", '', temperature_SV.get(), '', '', '', '']
    data[2]=["N° Afficheur", '', numAfficheur_SV.get(), '', '', '', '']
    data[3]=["N° Capteur", '', numCapteur_SV.get(), '', '', '', '']
    if int(cocheeMode.get()) == 1 :
        data[4]=["Nb Acquisitions", '', nbreAcquisitions_SV.get()+' dont '+str(nbreErreurs)+' erreurs (et '+str(len(listeErreursVirgule))+' erreurs de détection de la virgule). Compensation des erreurs', '',  '', '']
    else:
       data[4]=["Nb Acquisitions", '', nbreAcquisitions_SV.get()+' dont '+str(nbreErreurs)+' erreurs (et '+str(len(listeErreursVirgule))+' erreurs de détection de la virgule)', '',  '', '']

    data[5]=["Intervalle temps", '', tempsAcquisition_SV.get()+"s", '', '', '', '']  
    
    
    data[0+4+2] = [time.strftime("%d/%m/%Y"), 'Heure', 'Valeur', 'Moyenne', 'Ecart-type', 'Max', 'Min', 'Max-Min']
    data[1+4+2] = ['', '', '', str(moyenne).replace(".",","), str(ecartType).replace(".",","), str(maxi).replace(".",","), str(mini).replace(".",","), str(round(maxi-mini,3)).replace(".",",")]

    for indice in range(len(listeNombre)) : 
        heure = listeTemps[indice]
        nombre = listeNombre[indice].replace(".",",")
        data[indice+2+4+2][1] = heure
        data[indice+2+4+2][2] = nombre

    t=Table(data,8*[0.8*inch], lignes*[0.2*inch]) # "[0.8*inch]" défini la largeur d'une colonne et "[0.2*inch]" celle d'une ligne

    t.setStyle(TableStyle([#('TEXTCOLOR',(0,0),(7,0),colors.red),
                           ('TEXTCOLOR',(0,4+2),(7,5+2),colors.red),
                           ('ALIGN',(0,4+2),(-1,-1),'CENTER'),
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('INNERGRID', (0,4+2), (-1,-1), 0.25, colors.black), #trace les lignes et colonnes
                           ('BOX', (0,4+2), (-1,-1), 0.25, colors.black), #encadre tout le tableau
                           ]))

    elements.append(t)
    doc.build(elements)


def Creation_PDF_Etalon(listeTemps, listeNombre, cheminDossierSauvegardeComplet, nom, moyenne, ecartType, maxi, mini, nbreErreurs, listeTemperatureConsort, listeRatioConsort, miniEtalon, maxiEtalon, moyenneEtalon, varianceEtalon, ecartTypeEtalon):
    from temperature_interface_v30 import nomCertificat_SV, temperature_SV, numCapteur_SV, numAfficheur_SV, nbreAcquisitions_SV, cocheeMode, tempsAcquisition_SV
    from temperature_interface_v30 import etalon, sonde
    global listeErreursVirgule
    doc = SimpleDocTemplate(cheminDossierSauvegardeComplet+"/"+nom+".pdf")

    elements = []

    lignes = len(listeTemps) + 18 #18 pour l'entete
    data = [['' for j in range(5)] for i in range(lignes)] #génération d'un tableau vide

    data[0]=["Certificat", nomCertificat_SV.get()]
    data[1]=["Température", temperature_SV.get()]
    data[2]=["N° Afficheur", numAfficheur_SV.get()]
    data[3]=["N° Capteur", numCapteur_SV.get()]
    if int(cocheeMode.get()) == 1 :
        data[4]=["Nb Acquisitions", nbreAcquisitions_SV.get()+' dont '+str(nbreErreurs)+' erreurs (et '+str(len(listeErreursVirgule))+' erreurs de détection de la virgule). Compensation des erreurs', '',  '', '']
    else:
        data[4]=["Nb Acquisitions", nbreAcquisitions_SV.get()+' dont '+str(nbreErreurs)+' erreurs (et '+str(len(listeErreursVirgule))+' erreurs de détection de la virgule)']
    data[5]=["Intervalle temps", tempsAcquisition_SV.get()+'s']
    data[6]=["Etalon", etalon]
    data[7]=["Ref. Sonde", sonde]
    data[8]=["Date", time.strftime("%d/%m/%Y")]

    data[9] = ["Appareil"]
    data[10] = ['Moyenne', 'Ecart-type', 'Max', 'Min', 'Max-Min']
    data[11] = [str(moyenne).replace(".",","), str(ecartType).replace(".",","), str(maxi).replace(".",","), str(mini).replace(".",","), str(round(maxi-mini,3)).replace(".",",")]

    data[13] = ["Etalon"]
    data[14] = ['Moyenne', 'Ecart-type', 'Max', 'Min', 'Max-Min']
    data[15] = [str(moyenneEtalon).replace(".",","), str(ecartTypeEtalon).replace(".",","), str(maxiEtalon).replace(".",","), str(miniEtalon).replace(".",","), str(round(maxiEtalon-miniEtalon,4)).replace(".",",")]

    if etalon == 'Consort':
        data[17] = ["Heure", "Valeur", '', "Valeur étalon", "Ratio brut"]
    elif etalon == '3458A':
        data[17] = ["Heure", "Valeur", '', "Valeur étalon", "Valeur ohmique"]


    for indice in range(len(listeNombre)) : 
        heure = listeTemps[indice]
        nombre = str(listeNombre[indice]).replace(".",",")
        nombreConsort = str(round(listeTemperatureConsort[indice], 4)).replace(".",",")
        ratioConsort = str(listeRatioConsort[indice]).replace(".",",")
        
        data[indice+18][0] = heure
        data[indice+18][1] = nombre
        data[indice+18][3] = nombreConsort
        data[indice+18][4] = ratioConsort
        

    t=Table(data,5*[1.2*inch], lignes*[0.2*inch]) # "[0.8*inch]" défini la largeur d'une colonne et "[0.2*inch]" celle d'une ligne

     #(colonnedépart, lignedépart),(colonnearrivée,lignarrivée)
    t.setStyle(TableStyle([('BOX', (0,9), (0,9), 0.25, colors.black), #encadre tout le tableau

                           ('INNERGRID', (0,10), (5,11), 0.25, colors.black), #trace les lignes et colonnes
                           ('BOX', (0,10), (5,11), 0.25, colors.black),
                           
                           ('BOX', (0,13), (0,13), 0.25, colors.black),
                           ('INNERGRID', (0,14), (5,15), 0.25, colors.black), 
                           ('BOX', (0,14), (5,15), 0.25, colors.black),

                           ('ALIGN',(0,9),(-1,-1),'CENTER'),
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           
                           #('BACKGROUND',(0,17),(5,17),colors.lightgrey),
                           ('GRID', (0, 17), (-1, -1), 0.25, colors.black),
                           ]))
    elements.append(t)
    doc.build(elements)
    



def Calculs_Statistique(listeNombreInt):
    nbreErreurs = listeNombreInt.count("ERREUR")
    while nbreErreurs != 0 :
        nbreErreurs -= 1
        listeNombreInt.remove("ERREUR")
    mini = min(listeNombreInt)
    maxi = max(listeNombreInt)
    moyenne = round(np.mean(listeNombreInt), 3) #3 chiffres après la virgule
    n = len(listeNombreInt)
    variance = np.var(listeNombreInt)*n/(n-1) #pour obtenir la variance non biaisée (divisée par n-1 au lieu de n) et 4 chiffres après virgule
    ecartType = round(np.sqrt(variance), 4)
    return(mini, maxi, moyenne, variance, ecartType)
    
def Analyse_Donnee(listeNombre, listeNombreInt):
    from temperature_interface_v30 import Ecriture_Acquisition, nomCertificat_SV, temperature_SV, ecartAbsolu_SV
    listeIndicesFaux = []
    listeIndicesFauxTaille = []

    for i in range(1, len(listeNombreInt)-1):
        if (listeNombre[i] != "ERREUR") & (listeNombre[i+1] != "ERREUR"):
            if( len(listeNombre[i+1]) == len(listeNombre[i-1]) ) & ( len(listeNombre[i]) != len(listeNombre[i+1]) ): #valeur isolée entre 2
                listeIndicesFauxTaille.append(i+1)
                print("PROBLEME DE LONGUEUR!")
            
    for i in range(1, len(listeNombreInt)):
        if (listeNombre[i] != "ERREUR") & (listeNombre[i-1] != "ERREUR"):
            ecartAbs = abs(listeNombreInt[i] - listeNombreInt[i-1])
            if ecartAbs > float(ecartAbsolu_SV.get()) : #si > 1 degré par défaut
                listeIndicesFaux.append(i+1) #(i+1 pour que cela corresponde au numéro de photo)
    
    listePhotos= list(set(listeIndicesFauxTaille) | set(listeIndicesFaux)) #pour ne pas avoir de doublon et une liste unique
    if listePhotos != []:
        fichier = open(cheminDossierSauvegardeComplet+"/"+nomCertificat_SV.get()+"_"+temperature_SV.get()+'_'+"erreurs.txt", "a") # ouverture en mode ajout à la fin du fichier (APPEND)
        fichier.write("Erreur(s) possibles de transition sur les photos suivantes :\n")
        Ecriture_Acquisition("Erreur(s) possibles de transition sur les photos suivantes :")
        for i in listePhotos:
            Ecriture_Acquisition(str(i))
            fichier.write(str(i)+"\n")
        fichier.close()



#--##--PARTIE GRAPHIQUE--##--##

#-LES FONCTIONS-#


def Creation_PDF_Bilan(listeFichiersTriee, cheminDossierSauvegardeComplet):
    from temperature_interface_v30 import nomCertificat_SV, etalon

    try : 
        if not askyesno('Génération d\'un fichier bilan', 'Avez-vous utilisé un étalon pour le certificat\" '+nomCertificat_SV.get()+' \"?'):
            doc = SimpleDocTemplate(cheminDossierSauvegardeComplet+"/"+nomCertificat_SV.get()+"_BILAN.pdf")

            elements = []
            nbFichier = len(listeFichiersTriee)
            lignes = nbFichier * 5 + 4 + nbFichier -1 #*5 car chaque fichier aporte 5 lignes, 4 pour entete, nbFichier -1 pour espace entre 2 fichiers
            data = [['' for j in range(6)] for i in range(lignes)] #génération d'un tableau vide

            #on remplit l'entete
            cheminFichier1 = listeFichiersTriee[0]
            fichier = open(cheminFichier1, 'r')
            ligne1 = fichier.readline() # 'Certificat\tcertif7\n'
            nomCertif = (ligne1.split('\t')[1]).replace('\n','') #après .split : ['Certificat', 'certif7\n']
            fichier.readline() #on ne veut pas la ligne de température
            ligne3 = fichier.readline()
            numAfficheur = (ligne3.split('\t')[1]).replace('\n','')
            ligne4 = fichier.readline()
            numCapteur = (ligne4.split('\t')[1]).replace('\n','')
            
                
            data[0]=["Certificat", nomCertif, '', '', '', '']
            data[1]=["N° Afficheur", numAfficheur, '', '', '', '']
            data[2]=["N° Capteur", '', numCapteur, '', '', '']

            for i in range(nbFichier):
                data[4+6*i][0] = "Température"
                data[5+6*i][0] = "Nb Acquisitions"
                data[6+6*i][0] = "Intervalle temps"
                data[7+6*i] = ['Date','Moyenne', 'Ecart-type', 'Max', 'Min', 'Max-Min']

            #on remplit pour chaque température
            for k in range(nbFichier):
                cheminFichier = listeFichiersTriee[k]
                fichier = open(cheminFichier, 'r')
                
                fichier.readline()
                
                ligne2 = fichier.readline()
                temperature = (ligne2.split('\t')[1]).replace('\n','')

                fichier.readline()
                fichier.readline()

                ligne5 = fichier.readline()
                nbAcquisitions = (ligne5.split('\t')[1]).replace('\n','')

                ligne6 = fichier.readline()
                intervalletemps = (ligne6.split('\t')[1]).replace('\n','')

                ligne7 = fichier.readline()
                date = (ligne7.split('\t')[0]).replace('\n','')

                ligne8 = fichier.readline()
                moyenne = (ligne8.split('\t')[3]).replace('\n','')
                ecartType = (ligne8.split('\t')[4]).replace('\n','')
                maxi = (ligne8.split('\t')[5]).replace('\n','')
                mini = (ligne8.split('\t')[6]).replace('\n','')
                maxiMoinsMini = (ligne8.split('\t')[7]).replace('\n','')

                data[4+6*k][1] = temperature
                data[5+6*k][1] = nbAcquisitions
                data[6+6*k][1] = intervalletemps
                data[8+6*k] = [date, moyenne, ecartType, maxi, mini, maxiMoinsMini]

            t=Table(data,6*[1.2*inch], lignes*[0.2*inch]) # "[0.8*inch]" défini la largeur d'une colonne et "[0.2*inch]" celle d'une ligne
            #(colonnedépart, lignedépart),(colonnearrivée,lignarrivée)
            t.setStyle(TableStyle([('TEXTCOLOR',(0,4+6*i),(1,4+6*i),colors.red) for i in range(nbFichier)
                                   ]))
            
            t.setStyle(TableStyle([('BOX', (0,7+6*i), (-1,8+6*i), 0.25, colors.black) for i in range(nbFichier)
                                   ]))

            elements.append(t)
            doc.build(elements)

        else:
            
            doc = SimpleDocTemplate(cheminDossierSauvegardeComplet+"/"+nomCertificat_SV.get()+"_BILAN.pdf")

            elements = []
            nbFichier = len(listeFichiersTriee)
            lignes = nbFichier * 9 + 3
            
            data = [['' for j in range(6)] for i in range(lignes)] #génération d'un tableau vide

            #on remplit l'entete
            cheminFichier1 = listeFichiersTriee[0]
            fichier = open(cheminFichier1, 'r')
            ligne1 = fichier.readline() # 'Certificat\tcertif7\n'
            nomCertif = (ligne1.split('\t')[1]).replace('\n','') #après .split : ['Certificat', 'certif7\n']
            fichier.readline() #on ne veut pas la ligne de température
            ligne3 = fichier.readline()
            numAfficheur = (ligne3.split('\t')[1]).replace('\n','')
            ligne4 = fichier.readline()
            numCapteur = (ligne4.split('\t')[1]).replace('\n','')
            fichier.readline() #on ne veut pas la ligne Nb Acquisitions
            fichier.readline() #on ne veut pas la ligne Intervalle Temps
            ligne7 = fichier.readline()
            nomEtalon = (ligne7.split('\t')[1]).replace('\n','')
            ligne8 = fichier.readline()
            #refSonde = (ligne8.split('\t')[1]).replace('\n','')      
            

                
            data[0]=["Certificat", nomCertif, '', '', '', '']
            data[1]=["N° Afficheur", numAfficheur, '', '', '', '']
            data[2]=["N° Capteur", numCapteur, '', '', '', '']

            for i in range(nbFichier):
                data[4+9*i][0] = "Température"
                data[5+9*i][0] = "Etalon"
                data[6+9*i][0] = "Ref. Sonde"
                data[7+9*i][0] = "Nb Acquisitions"
                data[8+9*i][0] = "Intervalle temps"
                #data[9+9*i] = ['','Moyenne', 'Ecart-type', 'Max', 'Min', 'Max-Min']
                data[10+9*i] = ['Appareil','', '']
                data[11+9*i] = ['Etalon','', '']

            #on remplit pour chaque température
            for k in range(nbFichier):
                cheminFichier = listeFichiersTriee[k]
                fichier = open(cheminFichier, 'r')
                
                fichier.readline()
                
                ligne2 = fichier.readline()
                temperature = (ligne2.split('\t')[1]).replace('\n','')

                fichier.readline()
                fichier.readline()

                ligne5 = fichier.readline()
                nbAcquisitions = (ligne5.split('\t')[1]).replace('\n','')

                ligne6 = fichier.readline()
                intervalletemps = (ligne6.split('\t')[1]).replace('\n','')

                fichier.readline()
                #fichier.readline()
                ligne8 = fichier.readline()
                refSonde = (ligne8.split('\t')[1]).replace('\n','')

                ligne9 = fichier.readline()
                date = (ligne9.split('\t')[1]).replace('\n','')

                fichier.readline()
                fichier.readline()

                ligne12 = fichier.readline()
                moyenne = (ligne12.split('\t')[0])
                ecartType = (ligne12.split('\t')[1])
                maxi = (ligne12.split('\t')[2])
                mini = (ligne12.split('\t')[3])
                maxiMoinsMini = (ligne12.split('\t')[4]).replace('\n','')

                fichier.readline()
                fichier.readline()
                fichier.readline()

                ligne16 = fichier.readline()
                moyenneEtalon = (ligne16.split('\t')[0])
                ecartTypeEtalon = (ligne16.split('\t')[1])
                maxiEtalon = (ligne16.split('\t')[2])
                miniEtalon = (ligne16.split('\t')[3])
                maxiMoinsMiniEtalon = (ligne16.split('\t')[4]).replace('\n','')

                data[4+9*k][1] = temperature
                data[5+9*k][1] = nomEtalon
                data[6+9*k][1] = refSonde
                data[7+9*k][1] = nbAcquisitions
                data[8+9*k][1] = intervalletemps
                
                data[9+9*k] = [date,'Moyenne', 'Ecart-type', 'Max', 'Min', 'Max-Min']
                data[10+9*k] = ['Appareil', moyenne, ecartType, maxi, mini, maxiMoinsMini]
                data[11+9*k] = ['Etalon', moyenneEtalon, ecartTypeEtalon, maxiEtalon, miniEtalon, maxiMoinsMiniEtalon]
                
            t=Table(data,6*[1.2*inch], lignes*[0.2*inch]) # "[0.8*inch]" défini la largeur d'une colonne et "[0.2*inch]" celle d'une ligne
            #(colonnedépart, lignedépart),(colonnearrivée,lignarrivée)
            t.setStyle(TableStyle([('TEXTCOLOR',(0,4+9*i),(1,4+9*i),colors.red) for i in range(nbFichier)
                                   ]))

            t.setStyle(TableStyle([('BOX', (0,9+9*i), (-1,11+9*i), 0.25, colors.black) for i in range(nbFichier)
                                   ]))

            elements.append(t)
            doc.build(elements)
            showinfo('Information', "Un fichier bilan a été généré")
    except IndexError:
        showwarning('Attention', "Une erreur s'est produite. Aucun certificat bilan n'a été généré.")


#PARTIE COMMUNICATION:

def Initialisation_Consort():
    global ser
    ser = serial.Serial(
        port = '/dev/ttyUSB0',
        baudrate = 4800,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        xonxoff = True,
        timeout = 1
    )


def Initialisation_3458A():
    global instru_3458A
    resources = visa.ResourceManager('@py')
    instru_3458A = resources.open_resource("GPIB0::22::INSTR")
    instru_3458A.write('END ALWAYS') #permet d'obtenir qu'une seule valeur lors d'un read()
    instru_3458A.write('FUNC OHMF')
    

def Lecture_Consort():
    global ser
    ser.write(b'ANS1\r')
    lecture = ser.readline() #on récupère sous format "byte"
    string = str(lecture, 'utf-8')
    nombre = string.split(" ")[5]
    return nombre

def Lecture_3458A():
    global instru_3458A
    lecture = instru_3458A.read() #' 1.776717762E+08\r\n'
    nombre = float(lecture.replace("\r\n", ""))
    return nombre

def Fermeture_Consort():
    global ser
    ser.close()
    

def Correction_Sonde(sonde):
    fichier = open(repertoireScript+'/Sondes/'+sonde+'.txt', 'r')
    lignes = fichier.readlines()
    aSonde = float(lignes[0].replace("\n",""))
    bSonde = float(lignes[1].replace("\n",""))
    cSonde = float(lignes[2].replace("\n",""))
    dSonde = float(lignes[3].replace("\n",""))

    return (aSonde, bSonde, cSonde, dSonde)


if not os.path.exists('parametres_sondes.txt'):
    fichier = open("parametres_sondes.txt", 'w')
    fichier.write('m\t0.999960381\n')
    fichier.write('b\t3.15885e-5\n')
    fichier.write('res_etalon\t99.99956\n')
    fichier.write('A\t3.9083e-3\n')
    fichier.write('B\t-5.775e-7\n')
    fichier.write('C\t-4.183e-12\n')
    fichier.write('R0\t100\n')
    fichier.close()  

fichier = open("parametres_sondes.txt", 'r')
lignes = fichier.readlines()

m = float(lignes[0].split("\t")[1].replace("\n",""))
b = float(lignes[1].split("\t")[1].replace("\n",""))
res_etalon = float(lignes[2].split("\t")[1].replace("\n",""))
A = float(lignes[3].split("\t")[1].replace("\n",""))
B = float(lignes[4].split("\t")[1].replace("\n",""))
C = float(lignes[5].split("\t")[1].replace("\n",""))
R0 = float(lignes[6].split("\t")[1].replace("\n",""))

fichier.close()


def Conversion_Temperature(aSonde, bSonde, cSonde, dSonde, listeRatioConsort):
    from temperature_interface_v30 import etalon
    global m, b, res_etalon
    erreur = 1e-10
    listeTemperatureConsort = []
    for ratio_lu in listeRatioConsort:
        inf = -200
        sup = 850
        ratio_lu = float(ratio_lu) #conversion d'un str en float

        if etalon == 'Consort':
            ratio_corrige = ratio_lu * m + b #correction du pont Consort
            res_corrige = ratio_corrige * res_etalon #conversion en ohm
        elif etalon == '3458A':
            res_corrige = float(ratio_lu) #on effectue pas de correction (on lit directement une valeur de résistance)

        while sup-inf > erreur: #resolution par dichotomie de l'équation de la norme R(t)
            milieu = (sup+inf)/2
            if R(milieu, aSonde, bSonde, cSonde, dSonde) < res_corrige :
                inf = milieu
            else :
                sup = milieu
        listeTemperatureConsort.append(milieu)
    return(listeTemperatureConsort)
        

def R(t, aSonde, bSonde, cSonde, dSonde):
    global R0, A, B, C
    if t > 0:
        resultat = R0*(1+A*t+B*t**2)+ aSonde+bSonde*t+cSonde*t**2+dSonde*t**3
    else:
        resultat = R0*(1+A*t+B*t**2+C*(t-100)*t**3) + aSonde+bSonde*t+cSonde*t**2+dSonde*t**3
    return resultat


def Calculs_Statistique_Sonde(listeTemperatureConsort):

    mini = round(min(listeTemperatureConsort), 4)
    maxi = round(max(listeTemperatureConsort), 4)
    moyenne = round(np.mean(listeTemperatureConsort), 4) #4 chiffres après la virgule
    n = len(listeTemperatureConsort)
    variance = np.var(listeTemperatureConsort)*n/(n-1) #pour obtenir la variance non biaisée (divisée par n-1 au lieu de n) et 4 chiffres après virgule
    ecartType = round(np.sqrt(variance), 4)
    return(mini, maxi, moyenne, variance, ecartType)


#-FIN DES FONCTIONS-#


## FONCTIONS DIVERSES


#DIVERS

