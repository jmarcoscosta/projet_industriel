#NOUVEAUTES DE LA VERSION 1.2 :
# - ajout d'un curseur pour choisir et seuil
# - ajout du bouton validation du seuil pour faire le traitement une fois le seuil choisi (gain fluidité)
# - ajout non graphique de l'endroit de sauvegarde des fichiers texte pathTexte
#NOUVEAUTES DE LA VERSION 1.3 :
# - ajout gestion des chemins et nom des dossiers
# - ajout d'une barre de menu avec l'onglet "option" pour régler le temps de prévisualisation
#NOUVEAUTES DE LA VERSION 1.4 :
# - ajout d'exlorateur d'images pour vérifier rapidement si les résultats sont corrects
# - ajout de l'exportation des données en cas d'erreur après visualisation des images 
# - suppression de l'import de matplotlib qui était inutilisée
# - 2 importations pour ne pas avoir d'erreurs lors de la création d'un exécutable
# - ajout de la gestion du nom du fichier/dossier déjà existant lorsque le chemin a déjà été choisi
##NOUVEAUTES DE LA VERSION 1.5 :
# - modification de l'onglet "option" en "préférences"
# - ajout à l'onglet "préférences" des Entry permettant à l'utilisateur d'avoir des chemins par défauts lors de l'ouverture du logiciel
# - amélioration de la gestion des chemins avec le répertoire courant
# - création du dossier "Temporaire"
##NOUVEAUTES DE LA VERSION 1.6 :
# - suppression du cas "if nbrePhoto==1". En fait ce n'est pas un cas particulier : allégement du code.
# - ajout du signe
# - traitement du cas ou la photo a été prise lorsqu'il n'y avait pas de chiffres (bug : arrêt de l'acquisition) : signalement à l'utilisateur
##NOUVEAUTES DE LA VERSION 1.7 :
# - ajout : une fois qu'on arrive à la fin de Canevas, l'effacer puis remettre les nouveaux affichages au début
# - modification : quand au moins 1 chiffre est faux dans le nombre, on remplace tout le nombre par 'ERREUR'
# - ajout : à la fin de l'acquisition, effacer totalement Canevas Etat et retourner un bilan complet des erreurs (également dans fichier texte): 
# ce bilan complet des erreurs contient : numéros de photo ou chiffre n'a pas été déctecté + les numéros de photo sans virgule
##NOUVEAUTES DE LA VERSION 1.8 :
# - modification du choix du seuil par deux boutons + et - pour faciliter ce choix sur écran tactile
# - ajout dans Parasites_Bords du côté du bas
# - modification de la manière dont on sélectionne la zone : à l'aide des flèches et échap pour quitter
# - suppression du temps de prévisualisation dans les préférences mais ajout des préférences sur lV et lH par défaut lors début prévisualisation
# - modification du fichier texte en sortie : '31/05/2018' tab '16:28:42' tab '25.32' (DATE HEURE VALEUR)
# - ajout : prise en compte du temps de traitement dans le temps d'attente
# - modification du système de vérification : photo avec valeur associée en dessous; possibilité de choisir numéro de photo à visualiser
##NOUVEAUTES DE LA VERSION 1.9 :
# - ajout de l'analyse des données pour essayer de détecter les transitions (écriture dans le fichier erreur)
# - ajout de longueurH et longueurV dans la prévisualisation pour permettre à l'utilisateur de connaitre la valeur pour mettre dans préférences
# - correction d'un bug qui ne prenait pas en compte les préférences de la zone de prévisualisation
# - correction d'un bug qui créait un décallage entre les photos et la valeur lue lorsqu'il n'y avait pas de chiffres ("ERREUR" maintenant)
# - ajout d'un bouton "Arrêt de l'acquisition" puis demande d'enregistrement des fichiers à l'utilisateur
# - version optimisée : limitation du nombre de sauvegarde pour réduire les temps anormaux de traitement, diminution du temps pour prendre une
                        #capture à l'aide de l'option 'use_video_poirt=True'
# - ajout de la fonction Calculs_Statistique qui renvoie [mini, maxi, moyenne, variance, ecartType]
##NOUVEAUTES DE LA VERSION 2.0 :
# - ajout : génération d'un PDF du fichier texte
# - modification : transformation du '.' en ',' (facilité pour ouverture sur excel etc) (.replace(".",",") avant écriture dans fichier)
# - modification importante pour l'application de température : le dossier de sauvegarde portera le nom du certificat. Dans ce dossier,
#    il y aura un dossier "Photos", type Certificat_Photo10_température ou température et certificat seront à rentrer par l'utilisateur.
#    de même pour les fichiers texte et pdf qui seront du type : Certificat_temperature.extension.
# - ajout sur les fichiers textes + pdf du nom du certificat, température, numéro d'afficheur, numéro capteur, nb acquisitions, temps acqui, erreurs
##NOUVEAUTES DE LA VERSION 2.1 :
# - ajout dans le Menu de "Générer un fichier bilan". Ce fichier reprendra les informations des fichiers textes pour chaque température d'un certif
# - ajout du mode "Compensation des erreurs" : le nbre d'acquisitions peut varier (s'il y a x erreurs, on refait x acquisitions)
##NOUVEAUTES DE LA VERSION 3.0 :
# - ajout d'une fenêtre au début pour choisir entre "labo température" ou "labo élec"
# - modification de la fenêtre principal, qui sera composée de 2 onglets (ex : 1. acquisition et 2. communication série)
# - division du code en plusieurs fichiers : - 'principal.py' (lancement)
#                                            - 'elec_acquisition.py' et 'elec_interface'
#                                            - 'temperature_acquisition.py' et 'temperature_interface.py'
# - correction d'un bug dans enregistrement du nom des photos (ajout de '_' pour différencier 14 et 145 comme température)
# - modification : 'compensation des erreurs' est même rajouté après correction
# - correction : 'compensation des erreurs' dépassait de la page PDF. 
##NOUVEAUTES DE LA VERSION 3.1 :
# - début de l'interface comm série de l'élec
##NOUVEAUTES DE LA VERSION 3.2 :
# - gestion des sondes : modification du nom des sondes existantes ("suppression") et ajout 2 sondes avec nom paramétrable.
##NOUVEAUTES DE LA VERSION 3.3 :
# - modification de la création des interfaces (création de élec uniquement lors de l'appuie sur labo élec)
##NOUVEAUTES DE LA VERSION 3.4 :
# - ajout de l'Agilent 3458A dans la liste des étalons (communication IEEE)
# - correction d'un bug qui ne permettait pas de mettre de '.' dans le nom des sondes

import six #les 6 imports servent à pouvoir générer l'éxecutable depuis import visa
import packaging
import packaging.version
import packaging.specifiers
import appdirs
import packaging.requirements


from temperature_interface_v30 import *
from elec_interface_v30 import *

def Ouverture_Labo_Temperature():
    Mafenetre.deiconify() #on affiche la fenêtre température
    MafenetrePrincipale.destroy() #on détruit la fenêtre de choix du labo

def Ouverture_Labo_Elec():
    
    Creation_Fenetre_Elec()
    MafenetrePrincipale.destroy() 


# Création de la fenêtre principale
MafenetrePrincipale = Tk()
MafenetrePrincipale.title("Choix du laboratoire - v3.4")
MafenetrePrincipale.configure(background='ivory')
MafenetrePrincipale.geometry('350x80+300+300') #'tailleX*tailleY+apparationX+apparitionY'

# Création d'un widget Button pour patie température
BoutonLaboTemperature = Button(MafenetrePrincipale, text ="Partie température", width=33, command = Ouverture_Labo_Temperature, font = "Arial"+str(taillePolice))
BoutonLaboTemperature.pack(padx = 5, pady = 5)

# Création d'un widget Button pour partie élec
BoutonLaboElec = Button(MafenetrePrincipale, text ="Partie électricité", width=33, command = Ouverture_Labo_Elec, font = "Arial"+str(taillePolice))
BoutonLaboElec.pack(padx = 5, pady = 5)

def Fermeture_Totale(): #appelée lors de l'appui sur la croix haut à droite de la fenêtre du choix du labo
    MafenetrePrincipale.destroy() #on détruit la fenêtre de choix du labo
    Mafenetre.destroy() #on détruit la fenêtre de température qui n'est pas affichée mais bien existante
    
MafenetrePrincipale.protocol("WM_DELETE_WINDOW", Fermeture_Totale) 

   

MafenetrePrincipale.mainloop() #NE RIEN ECRIRE APRES CETTE LIGNE
