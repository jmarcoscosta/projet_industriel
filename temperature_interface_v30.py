from temperature_acquisition_v30 import *

taillePolice = 15

## LES FONCTIONS LIEES A L'INTERFACE

def Traitement_Zone_Calibration():
    global photo2
    dossierActuel="Calibration"
    
    img = ImagePIL.open(path+dossierActuel+"/ImageNoirBlanc.png") #on ouvre l'image sur laquelle on va travailler
    NoirBlanc = np.array(img) #on convertit l'image en un tableau numpy
    
    NoirBlanc = Parasites_Bords(dossierActuel, NoirBlanc)
    NoirBlanc = Moyennage(dossierActuel, NoirBlanc)
    AAnalyser = Retrecissement_Zone(dossierActuel, NoirBlanc)

    AAnalyserImage = ImagePIL.fromarray(AAnalyser) #on convertit un tableau numpy en image 
    AAnalyserImage.save(path+dossierActuel+"/ImageAAnalyser.png")
    
    Canevas.delete(ALL)
    photo2 = PhotoImage(file=path+dossierActuel+"/ImageAAnalyser.png")
    Canevas.create_image(50, 50, anchor=NW, image=photo2)

init = 0 #initialisé à 0 lors du démarrage pour executer "camera = picamera.PiCamera()" une seule fois pour ne pas avoir "Failed to enable connection: Out of resources" même si non bloquant

def Selection_Zone():
    global camera, preview, init
    #ceci ne peut être fait qu'une fois après cela cause des erreurs
    if init == 0 :
        camera = picamera.PiCamera() #CECI A ETE MIS DANS SELECTION_ZONE
        camera.resolution = (1280, 720)
        camera.framerate = 24 #par défaut : 30, et tous les test ont été faits à 24
        camera.rotation = 180
        init = 1

    for dossier in os.listdir(path): #--SUPPRESSION DES DOSSIERS D'UNE CAPTURE PRECEDENTE--##
        Suppression_Dossier(dossier)
    Creation_Dossier("Calibration")
    dossierActuel = "Calibration"
 
    global longueurH, longueurV, l, a, o #, preview
    preview = 1
    l = 0 #correspond à la "ligne" d'écriture dans le Canvas acquisition.
    a = np.zeros((720, 1280, 3), dtype=np.uint8)
    try :
        longueurV = int(longueurV_SV.get())
        longueurH = int(longueurH_SV.get())
    except ValueError: #invalid literal for int() with base 10: ''
        print("En attente des valeurs") #résolu en initialisant des valeurs en global
    except AttributeError: #'int' object has no attribute 'get'
        print("Pas besoin de convertir en int")
    finally:
        a[360-longueurV:360+longueurV, 640-longueurH:640+longueurH, :] = 0xff
        a[360, :] = 0x00 #pour aider l'utilisateur à placer l'appareil droit
        a[360+round(longueurV/2), :] = 0x00
        a[:, 640] = 0x00
        
        camera.start_preview() #fullscreen=False, window=(0,0,640,480) ne peut pas être mis sinon photos pas sur l'image
        o = camera.add_overlay(a, layer=3, alpha=90) #layer=couche, alpha=transparence(0,255)






def Fleche_Droite(*event):
    global a, o, longueurH, longueurV, preview, camera
    if preview == 1: #si on est bien en phase de prévisualisation
        camera.remove_overlay(o)
        longueurH_SV.set(int(longueurH_SV.get())+5)
        longueurH = int(longueurH_SV.get())
        camera.annotate_text = 'H= '+str(longueurH)+' V= '+str(longueurV)
        a = np.zeros((720, 1280, 3), dtype=np.uint8)
        a[360-longueurV:360+longueurV, 640-longueurH:640+longueurH, :] = 0xff
        a[360, :] = 0x00 #pour aider l'utilisateur à placer l'appareil droit
        a[360+round(longueurV/2), :] = 0x00
        a[:, 640] = 0x00
        o = camera.add_overlay(a, layer=3, alpha=90) #layer=couche, alpha=transparence(0,255)

def Fleche_Gauche(*event):
    global a, o, longueurH, longueurV, preview, camera
    if preview == 1: #si on est bien en phase de prévisualisation
        camera.remove_overlay(o)
        longueurH_SV.set(int(longueurH_SV.get())-5)
        longueurH = int(longueurH_SV.get())
        camera.annotate_text = 'H= '+str(longueurH)+' V= '+str(longueurV)
        a = np.zeros((720, 1280, 3), dtype=np.uint8)
        a[360-longueurV:360+longueurV, 640-longueurH:640+longueurH, :] = 0xff
        a[360, :] = 0x00 #pour aider l'utilisateur à placer l'appareil droit
        a[360+round(longueurV/2), :] = 0x00
        a[:, 640] = 0x00
        o = camera.add_overlay(a, layer=3, alpha=90) #layer=couche, alpha=transparence(0,255)

def Fleche_Haut(*event):
    global a, o, longueurH, longueurV, preview, camera
    if preview == 1: #si on est bien en phase de prévisualisation
        camera.remove_overlay(o)
        longueurV_SV.set(int(longueurV_SV.get())+5)
        longueurV = int(longueurV_SV.get())
        camera.annotate_text = 'H= '+str(longueurH)+' V= '+str(longueurV)
        a = np.zeros((720, 1280, 3), dtype=np.uint8)
        a[360-longueurV:360+longueurV, 640-longueurH:640+longueurH, :] = 0xff
        a[360, :] = 0x00 #pour aider l'utilisateur à placer l'appareil droit
        a[360+round(longueurV/2), :] = 0x00
        a[:, 640] = 0x00
        o = camera.add_overlay(a, layer=3, alpha=90) #layer=couche, alpha=transparence(0,255)

def Fleche_Bas(*event):
    global a, o, longueurH, longueurV, preview, camera
    if preview == 1: #si on est bien en phase de prévisualisation
        camera.remove_overlay(o)
        longueurV_SV.set(int(longueurV_SV.get())-5)
        longueurV = int(longueurV_SV.get())
        camera.annotate_text = 'H= '+str(longueurH)+' V= '+str(longueurV)
        a = np.zeros((720, 1280, 3), dtype=np.uint8)
        a[360-longueurV:360+longueurV, 640-longueurH:640+longueurH, :] = 0xff
        a[360, :] = 0x00 #pour aider l'utilisateur à placer l'appareil droit
        a[360+round(longueurV/2), :] = 0x00
        a[:, 640] = 0x00
        o = camera.add_overlay(a, layer=3, alpha=90) #layer=couche, alpha=transparence(0,255)

def Echap(*event):
    global preview, o, camera
    if preview == 1: #si on est bien en phase de prévisualisation
        camera.stop_preview()
        camera.remove_overlay(o)
        dossierActuel = "Calibration"
        camera.capture(path+dossierActuel+"/ImageComplete.jpg", use_video_port=True) #la photo se prend même si la zone a été mal réglée, elle sera réécrite par dessus si mauvaise.
        Rognage(longueurH, longueurV, dossierActuel)
        
        img = ImagePIL.open(path+dossierActuel+"/ImageRognee.png")
        M = np.array(img) #on convertit l'image en un tableau numpy

        longueur = M.shape[0]
        largeur = M.shape[1]

        M1D = np.zeros((longueur, largeur), dtype=np.uint16) #ne pas mettre sur 8 bits car on dépassera très surement 255!

        M1D = M1D + M[:,:,0] + M[:,:,1] + M[:,:,2] #on somme toutes les composantes [0,3*255]
        #Ne pas oublier M1D+ sinon M1D se converti automatiquement en uint8 !

        Canevas.delete(ALL)
        txt = Canevas.create_text(150, 15, text="Choissisez une valeur entre "+str(np.min(M1D))+" et "+str(np.max(M1D)), font="Arial 8", fill="blue")
        preview = 0




def Ecriture_Etat_Acquisition(texte):
    CanevasEtat.delete(ALL)
    CanevasEtat.create_text(longueur/2, 10, text=texte, font="Arial 9", fill="black")
    CanevasEtat.update() #on force la mise  jour à cause du sleep. 

def Ecriture_Acquisition(texte):
    global l #initialisé à 0 lors de l'appuie sur "Tester la zone"
    if 15+10*l>360: #si on dépasse la fin de la zone d'écriture, on efface et on recommence au début
        Canevas.delete(ALL)
        l=0
    txt = Canevas.create_text(longueur/2, 15+10*l, text=texte, font="Arial 8", fill="blue")
    l=l+1


def Bilan(listeNombre, cheminDossierSauvegardeComplet): #affiche le bilan des erreurs et enregistre le tout dans un fichier texte
    from temperature_acquisition_v30 import listeErreursVirgule
    global l, listeErreursVirgule
    l=0
    fichier = open(cheminDossierSauvegardeComplet+"/"+nomCertificat_SV.get()+"_"+temperature_SV.get()+'_'+"erreurs.txt", "w") #ATTENTION: si le fichier existe on le supprime!
    Canevas.delete(ALL)
    
    nbreErreurs=listeNombre.count("ERREUR")                         
    Ecriture_Acquisition("BILAN CHIFFRES : Il y a eu "+str(nbreErreurs)+" erreur(s) de reconnaissance de chiffres")
    fichier.write("BILAN CHIFFRES : Il y a eu "+str(nbreErreurs)+" erreur(s) de reconnaissance de chiffres \n")
    if nbreErreurs != 0:
        Ecriture_Acquisition("Les erreurs sont sur les numéros de photos suivants:")
        fichier.write("Les erreurs sont sur les numéros de photos suivants: \n")
        for indice,valeur in enumerate(listeNombre):
            if valeur == "ERREUR":
                Ecriture_Acquisition(str(indice+1))
                fichier.write(str(indice+1)+"\n")
    Ecriture_Acquisition("BILAN VIRGULE : Il y a eu "+str(len(listeErreursVirgule))+" erreur(s) de reconnaissance de virgule")
    fichier.write("BILAN VIRGULE : Il y a eu "+str(len(listeErreursVirgule))+" erreur(s) de reconnaissance de virgule \n")
    if len(listeErreursVirgule) != 0:
        Ecriture_Acquisition("Les erreurs sont sur les numéros de photos suivants:")
        fichier.write("Les erreurs sont sur les numéros de photos suivants: \n")
        for indiceVirgule in listeErreursVirgule:
            Ecriture_Acquisition(str(indiceVirgule))
            fichier.write(str(indiceVirgule)+"\n")

    fichier.close()
    return(nbreErreurs)


def Chemin_Dossier():
    directory = askdirectory(initialdir="/home/pi",title='Choissisez un chemin', parent = Mafenetre)

    if len(directory) > 0:
        cheminDossier_SV.set(directory)


## FENETRE PREFERENCE

def Ouverture_Preferences():
    global fenetreOption
    fenetreOption = Toplevel(master=Mafenetre)
    fenetreOption.title("Préférences")
    fenetreOption.configure(background='ivory')
    fenetreOption.geometry('600x290+150+150') #'tailleX*tailleY+apparationX+apparitionY'
    
    #paramètres de previsualisation
    FrameParametresPrevisualisation = LabelFrame(fenetreOption, text="Taille du cadre de prévisualisation",fg ='red', bg ='ivory', padx=2, pady=2, font = "Arial"+str(taillePolice))
    FrameParametresPrevisualisation.pack()

    FrameHautPrevisualisation = Frame(FrameParametresPrevisualisation, bg ='ivory', padx=2, pady=2)
    FrameHautPrevisualisation.pack(side = TOP)

    FrameBasPrevisualisation = Frame(FrameParametresPrevisualisation, bg ='ivory', padx=2, pady=2)
    FrameBasPrevisualisation.pack(side = BOTTOM)

    LabelLongueurHPrevisualisation=Label(FrameHautPrevisualisation , text="Horizontale :",relief=FLAT, bg='white', font = "Arial"+str(taillePolice))
    LabelLongueurHPrevisualisation.pack(side = LEFT)
    
    longueurHPrevisualisation_texte = Entry(FrameHautPrevisualisation, textvariable=longueurHPreference_SV , width=5, justify='center', font = "Arial"+str(taillePolice))
    longueurHPrevisualisation_texte.pack(side = RIGHT)

    LabelLongueurVPrevisualisation=Label(FrameBasPrevisualisation, text="Verticale :",relief=FLAT, bg='white', font = "Arial"+str(taillePolice))
    LabelLongueurVPrevisualisation.pack(side = LEFT)
    
    longueurVPrevisualisation_texte = Entry(FrameBasPrevisualisation, textvariable=longueurVPreference_SV , width=5, justify='center', font = "Arial"+str(taillePolice))
    longueurVPrevisualisation_texte.pack(side = RIGHT)

    LabelCheminDossierPreference = LabelFrame(fenetreOption , text='Chemin du dossier', fg ='red', bg ='ivory', padx=2, pady=2, font = "Arial"+str(taillePolice))
    LabelCheminDossierPreference.pack()

    BoutonDossierSauvegardePreference = Button(LabelCheminDossierPreference, text ="Changer", width=7, command = Chemin_Dossier_Sauvegarde_Preference, font = "Arial"+str(taillePolice))
    BoutonDossierSauvegardePreference.pack(side=RIGHT, padx = 5, pady = 5)

    LabelCheminDossierSauvegardePreference=Label(LabelCheminDossierPreference, textvariable=cheminDossierSauvegardePreference_SV,relief=SUNKEN, bg='white')
    LabelCheminDossierSauvegardePreference.pack(side=LEFT)

    #choix écart absolu dans Analyse des Données
    
    LabelFrameAnalyseDonnees = LabelFrame(fenetreOption , text='Analyse des données : écart absolu entre 2 valeurs consécutives', fg ='red', bg ='ivory', padx=2, pady=2, font = "Arial"+str(taillePolice))
    LabelFrameAnalyseDonnees.pack()
    
    ecartAbsolu_texte = Entry(LabelFrameAnalyseDonnees, textvariable=ecartAbsolu_SV, width=5, justify='center', font = "Arial"+str(taillePolice))
    ecartAbsolu_texte.pack(padx = 5, pady = 5)

    #bouton "Enregistrer et Quitter"
    BoutonQuitter = Button(fenetreOption, text ="Enregistrer et Quitter", width=15, command = Sauvegarde_Parametres, font = "Arial"+str(taillePolice))
    BoutonQuitter.pack(padx = 5, pady = 5)




def Chemin_Dossier_Sauvegarde_Preference():
    directory = askdirectory(initialdir="/home/pi",title='Choissisez un chemin', parent = fenetreOption)

    if (len(directory)>0):
        cheminDossierSauvegardePreference_SV.set(directory)
        cheminDossier_SV.set(directory)


def Sauvegarde_Parametres():
    global fenetreOption

    fichier = open(FichierPrevisualisation,"w") #ATTENTION: si le fichier existe on le supprime!
    fichier.write(longueurHPreference_SV.get()+"\n")
    fichier.write(longueurVPreference_SV.get())
    fichier.close()
        
    if len(cheminDossierSauvegardePreference_SV.get())>0:
        fichier = open(FichierCheminDossierSauvegarde,"w") #ATTENTION: si le fichier existe on le supprime!
        fichier.write(cheminDossierSauvegardePreference_SV.get())
        fichier.close()

    fichier = open(FichierAnalyseDonnees,"w") #ATTENTION: si le fichier existe on le supprime!
    fichier.write(ecartAbsolu_SV.get())
    fichier.close()

    fenetreOption.destroy()



## BOUTON GENERATION

def Ouverture_Generation(*event):
    cheminDossierSauvegardeComplet = cheminDossier_SV.get()+'/'+nomCertificat_SV.get()
    if len(nomCertificat_SV.get()) > 0:
        if os.path.exists(cheminDossierSauvegardeComplet) : #si le certificat existe
            if askyesno('Génération d\'un fichier bilan', 'Êtes-vous sûr de vouloir générer un fichier bilan pour le certificat\" '+nomCertificat_SV.get()+' \"?'):
                listeFichiers = glob(cheminDossierSauvegardeComplet+'/'+nomCertificat_SV.get()+'_*[0,1,2,3,4,5,6,7,8,9].txt') #fichier texte doit finir par un fhifre avant le .txt pour ne pas prendre en compte les fichiers erreurs
                #listeFichiersTriee = sorted(listeFichiers) #fait un trie de type "date" et pas sur "nombre", par exe on a : "16, 160, 1800, 20, 25, 240, 30" avec ce tri
                listeFichiersTriee = sorted(listeFichiers, key= lambda fichier: float((fichier.split('_'))[1].split('.')[0]))
                # explications : " split("_")[1] " donne '60.txt' et " .split('.')[0] " donne '60' qu'on transforme en float
            
                Creation_PDF_Bilan(listeFichiersTriee, cheminDossierSauvegardeComplet)

                #showinfo('Information', "Un fichier bilan a été généré")
            else:
                showinfo('Information', "Vous n'avez pas généré de fichier bilan")
        else :
            showwarning('Attention', 'Ce certificat n\'existe pas, vérifiez son chemin et son nom')
    else :
        showwarning('Attention', 'Rentrez un nom de certificat!')



##FENETRE VERIFICATION

def Ouverture_Verification(*event):
    from temperature_acquisition_v30 import listeNombre
    global listeNombre,photo1,numeroPhotoAffichage, CanevasVerification, nombre_SV, numeroPhoto_SV, listeNombreCorrigee, cheminDossierSauvegardeComplet
    global listeNombre_texte, fenetreVerification
    
    listeNombreCorrigee=listeNombre[:] # [:] permet de rendre les listes indépendantes !
    numeroPhotoAffichage=1
    nombre_SV=StringVar()
    numeroPhoto_SV=StringVar()
    
    fenetreVerification = Toplevel()
    fenetreVerification.title("Vérification des données")
    fenetreVerification.configure(background='ivory')
    fenetreVerification.geometry('450x280+150+150')

    CanevasVerification = Canvas(fenetreVerification, width=400, height=150, background='#CCFFFF')
    CanevasVerification.pack()
    
    FrameGestionValeurs=Frame(fenetreVerification, bg ='ivory', padx=2, pady=2)
    FrameGestionValeurs.pack()

    numeroPhoto_texte = Entry(FrameGestionValeurs, textvariable=numeroPhoto_SV , width=5, justify='center', font = "Arial"+str(taillePolice))
    numeroPhoto_texte.pack(side=LEFT, padx = 5, pady = 5)
    numeroPhoto_SV.set(str(1))
    numeroPhoto_texte.bind('<Return>', Validation_Numero_Photo)
    numeroPhoto_texte.bind('<KP_Enter>', Validation_Numero_Photo)
    
    
    listeNombre_texte = Entry(FrameGestionValeurs, textvariable=nombre_SV , width=10, justify='center', font = "Arial"+str(taillePolice))
    listeNombre_texte.pack(side=RIGHT, padx = 5, pady = 5)
    nombre_SV.set(str(listeNombre[0]))
    listeNombre_texte.bind('<Return>', Validation_Valeur_Photo)
    listeNombre_texte.bind('<KP_Enter>', Validation_Valeur_Photo)

    LabelNomCheminFichierTexte=Label(fenetreVerification,text="Appuyez sur 'Entrée' pour valider une modication",relief=FLAT, bg='white', font=("Helvetica", 7))
    LabelNomCheminFichierTexte.pack()

    FrameGestionImage=Frame(fenetreVerification, bg ='ivory', padx=2, pady=2)
    FrameGestionImage.pack()
    
    BoutonSuivant = Button(FrameGestionImage, text ="Suivant", width=15, command = Bouton_Suivant, font = "Arial"+str(taillePolice))
    BoutonSuivant.pack(side=RIGHT, padx = 5, pady = 5)

    BoutonPrecedent = Button(FrameGestionImage, text ="Précédent", width=15, command = Bouton_Precedent, font = "Arial"+str(taillePolice))
    BoutonPrecedent.pack(side=LEFT, padx = 5, pady = 5)

    BoutonQuitter = Button(fenetreVerification, text ="Quitter", width=15, command = Bouton_Quitter, font = "Arial"+str(taillePolice))
    BoutonQuitter.pack(padx = 5, pady = 5)
    
    photo1 = PhotoImage(file=cheminDossierSauvegardeComplet+"/Photos/"+nomCertificat_SV.get()+"_"+temperature_SV.get()+"_Photo1.png")
    CanevasVerification.create_image(200,75,anchor=CENTER, image=photo1)


def Bouton_Suivant():
    global numeroPhotoAffichage, CanevasVerification, photo, cheminDossierSauvegardeComplet

    nombreImagesPng=len(glob(cheminDossierSauvegardeComplet+'/Photos/'+'*'+temperature_SV.get()+'*.png'))
    if numeroPhotoAffichage+1<=nombreImagesPng:
        listeNombre_texte.configure(bg='white')
        nombre_SV.set(str(listeNombreCorrigee[numeroPhotoAffichage]))
        numeroPhotoAffichage+=1
        numeroPhoto_SV.set(str(numeroPhotoAffichage))
        CanevasVerification.delete(ALL)
        photo = PhotoImage(file=cheminDossierSauvegardeComplet+"/Photos/"+nomCertificat_SV.get()+"_"+temperature_SV.get()+'_Photo'+str(numeroPhotoAffichage)+".png")
        CanevasVerification.create_image(200,75,anchor=CENTER, image=photo)

def Bouton_Precedent():
    global numeroPhotoAffichage, CanevasVerification, photo, cheminDossierSauvegardeComplet
    
    nombreImagesPng=len(glob(cheminDossierSauvegardeComplet+'/Photos/'+'*'+temperature_SV.get()+'*.png'))
    if numeroPhotoAffichage-1>=1:
        listeNombre_texte.configure(bg='white')
        numeroPhotoAffichage-=1
        numeroPhoto_SV.set(str(numeroPhotoAffichage))
        CanevasVerification.delete(ALL)
        photo = PhotoImage(file=cheminDossierSauvegardeComplet+"/Photos/"+nomCertificat_SV.get()+"_"+temperature_SV.get()+'_Photo'+str(numeroPhotoAffichage)+".png")
        CanevasVerification.create_image(200,75,anchor=CENTER, image=photo)
        nombre_SV.set(str(listeNombreCorrigee[numeroPhotoAffichage-1]))


def Validation_Numero_Photo(*event):
    global numeroPhotoAffichage, photo, cheminDossierSauvegardeComplet
    numeroPhotoAffichage = int(numeroPhoto_SV.get())
    nombreImagesPng = len(glob(cheminDossierSauvegardeComplet+'/Photos/'+'*'+temperature_SV.get()+'*.png'))
    if numeroPhotoAffichage > nombreImagesPng:
        numeroPhotoAffichage = nombreImagesPng
        numeroPhoto_SV.set(str(numeroPhotoAffichage))
    CanevasVerification.delete(ALL)
    photo = PhotoImage(file=cheminDossierSauvegardeComplet+"/Photos/"+nomCertificat_SV.get()+"_"+temperature_SV.get()+'_Photo'+str(numeroPhotoAffichage)+".png")
    CanevasVerification.create_image(200,75,anchor=CENTER, image=photo)
    nombre_SV.set(str(listeNombreCorrigee[numeroPhotoAffichage-1]))


def Validation_Valeur_Photo(*event):
    global listeNombreCorrigee, listeNombre_texte
    numeroPhotoAffichage = int(numeroPhoto_SV.get())
    listeNombreCorrigee[numeroPhotoAffichage-1]=nombre_SV.get()
    listeNombre_texte.configure(bg='green')

def Bouton_Quitter():
    from temperature_acquisition_v30 import nbreErreurs, listeTemps

    try :
        from temperature_acquisition_v30 import listeRatioConsort, listeTemperatureConsort
    except ImportError: #c'est qu'aucun étalon n'a été sélectionné
        pass
    
    global fenetreVerification, listeNombreCorrigee, cheminDossierSauvegardeComplet, listeTemps, nbreErreurs, etalon, sonde

    nom = nomCertificat_SV.get()+'_'+temperature_SV.get()
    pathTexte=cheminDossierSauvegardeComplet
    
    if listeNombreCorrigee == listeNombre:
        showinfo('Bilan vérification', 'Vous n\'avez corrigé aucune valeur', parent=fenetreVerification)
    else:
        nbreCorrection = 0
        fichier = open(pathTexte+'/'+nom+".txt", "w") #ATTENTION: si le fichier existe on le supprime!
        
        listeNombreInt = []
        nbreErreursApres = 0
        for chaine in listeNombreCorrigee: #on passe d'une liste de char à une liste de int
            if chaine != "ERREUR":
                listeNombreInt.append(float(chaine))
            else:
                nbreErreursApres +=1
        
        [mini, maxi, moyenne, variance, ecartType] = Calculs_Statistique(listeNombreInt)

        if etalon == "Aucun":
            fichier.write("Certificat\t"+nomCertificat_SV.get()+"\n")
            fichier.write("Température\t"+temperature_SV.get()+"\n")
            fichier.write("N° Afficheur\t"+numAfficheur_SV.get()+"\n")
            fichier.write("N° Capteur\t"+numCapteur_SV.get()+"\n")
            
            if int(cocheeMode.get()) == 1 :
                fichier.write("Nb Acquisitions\t"+nbreAcquisitions_SV.get()+' dont '+str(nbreErreursApres)+' erreurs après correction ('+str(nbreErreurs)+' avant). Compensation des erreurs\n')
            else:
                fichier.write("Nb Acquisitions\t"+nbreAcquisitions_SV.get()+' dont '+str(nbreErreursApres)+' erreurs après correction ('+str(nbreErreurs)+' avant)\n')
            fichier.write("Intervalle temps\t"+tempsAcquisition_SV.get()+'s\n')
            
            fichier.write(time.strftime("%d/%m/%Y")+"\t Heure\t Valeur\t Moyenne\t Ecart-type\t Max\t Min\t Max-Min\n")
            fichier.write("\t \t \t"+str(moyenne).replace(".",",")+"\t"+str(ecartType).replace(".",",")+"\t"+str(maxi).replace(".",",")+"\t"+str(mini).replace(".",",")+"\t"+str(round(maxi-mini,3)).replace(".",",")+"\n")
            
            Ecriture_Acquisition("Suite à la correction : ")
            
            Ecriture_Acquisition("Moyenne = "+str(moyenne))
            Ecriture_Acquisition("Ecart-type = "+str(ecartType))
            Ecriture_Acquisition("Max = "+str(maxi))
            Ecriture_Acquisition("Min = "+str(mini))
            Ecriture_Acquisition("Max-Min = "+str(round(maxi-mini,3)))
            
            for i in range(len(listeNombreCorrigee)):
                if not listeNombreCorrigee[i] == listeNombre[i]:
                    nbreCorrection += 1

            for indice in range(len(listeNombre)) : 
                heure = listeTemps[indice]
                nombre = listeNombreCorrigee[indice].replace(".",",")
                fichier.write("\t"+heure+"\t"+nombre+"\n") 
            fichier.close()
            showinfo('Bilan vérification', 'Vous avez corrigé '+str(nbreCorrection)+' valeur(s)', parent=fenetreVerification)

        else:
            [miniEtalon, maxiEtalon, moyenneEtalon, varianceEtalon, ecartTypeEtalon] = Calculs_Statistique_Sonde(listeTemperatureConsort)
            
            fichier.write("Certificat\t"+nomCertificat_SV.get()+"\n")
            fichier.write("Température\t"+temperature_SV.get()+"\n")
            fichier.write("N° Afficheur\t"+numAfficheur_SV.get()+"\n")
            fichier.write("N° Capteur\t"+numCapteur_SV.get()+"\n")
            
            if int(cocheeMode.get()) == 1 :
                fichier.write("Nb Acquisitions\t"+nbreAcquisitions_SV.get()+' dont '+str(nbreErreursApres)+' erreurs après correction ('+str(nbreErreurs)+' avant). Compensation des erreurs\n')
            else:
                fichier.write("Nb Acquisitions\t"+nbreAcquisitions_SV.get()+' dont '+str(nbreErreursApres)+' erreurs après correction ('+str(nbreErreurs)+' avant)\n')
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
            fichier.write(str(moyenneEtalon).replace(".",",")+"\t"+str(ecartTypeEtalon).replace(".",",")+"\t"+str(maxiEtalon).replace(".",",")+"\t"+str(miniEtalon).replace(".",",")+"\t"+str(round(maxiEtalon-miniEtalon,3)).replace(".",",")+"\n")

            fichier.write('\n')

            if etalon == "Consort":
                fichier.write("Heure\t Valeur\t \t Valeur étalon\t Ratio brut\n")
            elif etalon == "3458A" : 
                fichier.write("Heure\t Valeur\t \t Valeur étalon\t Valeur ohmique\n")

            for indice in range(len(listeNombre)) : 
                heure = listeTemps[indice]
                nombre = listeNombreCorrigee[indice].replace(".",",")
                nombreConsort = str(round(listeTemperatureConsort[indice], 4)).replace(".",",")
                ratioConsort = str(listeRatioConsort[indice]).replace(".",",")
                
                fichier.write(heure+"\t"+nombre+"\t\t"+nombreConsort+"\t"+ratioConsort+'\n')
    
            fichier.close()
            for i in range(len(listeNombreCorrigee)):
                if not listeNombreCorrigee[i] == listeNombre[i]:
                    nbreCorrection += 1

            
            showinfo('Bilan vérification', 'Vous avez corrigé '+str(nbreCorrection)+' valeur(s)', parent=fenetreVerification)

            

    Ecriture_Etat_Acquisition("Correction terminée")
    fenetreVerification.destroy()




def Bouton_Plus():
    seuil_SV.set(int(seuil_SV.get())+10)
    Traitement_Zone_Initialisation()
    
def Bouton_Moins():
    seuil_SV.set(int(seuil_SV.get())-10)
    Traitement_Zone_Initialisation()



def Verification_Nom():
    global cheminDossierSauvegardeComplet, Verification
    nomDossierSauvegarde_SV.set(nomCertificat_SV.get())
    
    cheminDossierSauvegardeComplet = cheminDossier_SV.get()+'/'+nomDossierSauvegarde_SV.get()
    Verification = 0

    if (len(nomCertificat_SV.get())>0) & (len(temperature_SV.get())>0) :
        if os.path.exists(cheminDossierSauvegardeComplet+'/'+nomDossierSauvegarde_SV.get()+'_'+temperature_SV.get()+'.txt'):
            Ecriture_Etat_Acquisition("Nom fichier invalide : existe déjà")
            nomTemperature_texte.configure(bg='red')
        else :
            Ecriture_Etat_Acquisition("Remplissez les instructions")
            Creation_Dossier_Numero_Certificat()
            nomTemperature_texte.configure(bg='green')
            nomCertificat_texte.configure(bg='green')
            Verification = 1
    else :
        if len(nomCertificat_SV.get()) == 0:
            nomCertificat_texte.configure(bg='red')
        else:
            nomCertificat_texte.configure(bg='green')
        if len(temperature_SV.get()) == 0:
            nomTemperature_texte.configure(bg='red')
        else:
            nomTemperature_texte.configure(bg='green')


## INTERFACE PURE

# Création de la fenêtre principale
Mafenetre = Tk()
Mafenetre.title("Module d'acquisition d'images - v3.4")
Mafenetre.configure(background='ivory')

#Mafenetre.resizable(0, 0) #interdit de mettre en plein écran

#CREATION de 2 onglets
n = Notebook(Mafenetre)
f1 = Frame(n, bg ='ivory')
f2 = Frame(n, bg ='ivory')

n.add(f1, text = 'Acquisition')
n.add(f2, text = 'Communication')
n.pack()

#CREATION d'une frameDroite et frameGauche
FrameExtremeGauche=Frame(f1, bg ='ivory', padx=2, pady=2)
FrameExtremeGauche.pack(side=LEFT,anchor=NW)

FrameGauche = Frame(f1, bg ='ivory', padx=2, pady=2)
FrameGauche.pack(side=LEFT,anchor=NW)

FrameDroite = Frame(f1, bg ='ivory', padx=2, pady=2)
FrameDroite.pack(side=LEFT,anchor=NW)

#frame gestion dossiers
LabelSaisieDossier = LabelFrame(FrameExtremeGauche , text='0.Paramétrage des dossiers et fichiers',fg ='red', bg ='ivory', padx=2, pady=2,font = "Arial"+str(taillePolice))
LabelSaisieDossier.pack()

#chemin du dossier d'enregistrement
LabelCheminDossier = LabelFrame(LabelSaisieDossier, text='Chemin du dossier', relief=FLAT, fg ='#0066CC', padx=2, pady=2, font = "Arial"+str(taillePolice))
LabelCheminDossier.pack(fill = X)

BoutonDossier = Button(LabelCheminDossier, text ="Changer", width=7, command = Chemin_Dossier, font = "Arial"+str(taillePolice))
BoutonDossier.pack(side=RIGHT, padx = 5, pady = 5)

cheminDossier_SV = StringVar() #anciennement cheminDossierSauvegarde_SV 

LabelCheminDossier=Label(LabelCheminDossier, textvariable = cheminDossier_SV, relief=SUNKEN, bg='white')
LabelCheminDossier.pack(side=LEFT)
cheminDossier_SV.set("Changer le chemin")

#nom certificat
nomCertificat_SV = StringVar()

LabelNomCertificat = LabelFrame(LabelSaisieDossier , text='Nom du certificat', relief=FLAT, fg ='#0066CC', padx=2, pady=2, font = "Arial"+str(taillePolice))
LabelNomCertificat.pack(fill = X) 

nomCertificat_texte = Entry(LabelNomCertificat, textvariable=nomCertificat_SV , width=30, font = "Arial"+str(taillePolice))
nomCertificat_texte.pack() 


#température
temperature_SV = StringVar()

LabelTemperature = LabelFrame(LabelSaisieDossier, text='Température', relief=FLAT, fg ='#0066CC', padx=2, pady=2, font = "Arial"+str(taillePolice))
LabelTemperature.pack(fill = X) 

nomTemperature_texte = Entry(LabelTemperature, textvariable = temperature_SV , width=10, bg='red', font = "Arial"+str(taillePolice))
nomTemperature_texte.pack()

nomDossierSauvegarde_SV = StringVar() # on aura dans l'idée : nomDossierSauvegarde_SV = nomCertificat_SV+'_'+temperature_SV

#numéro de l'afficheur
numAfficheur_SV = StringVar()
LabelAfficheur = LabelFrame(LabelSaisieDossier, text="Numéro de l'afficheur*", relief=FLAT, fg ='#0066CC', padx=2, pady=2, font="Arial 8")
LabelAfficheur.pack(fill = X)

nomAfficheur_texte = Entry(LabelAfficheur, textvariable = numAfficheur_SV, font = "Arial"+str(taillePolice))
nomAfficheur_texte.pack()

#numéro du capteur
numCapteur_SV = StringVar()
LabelCapteur = LabelFrame(LabelSaisieDossier, text="Numéro du capteur*", relief=FLAT, fg ='#0066CC', padx=2, pady=2, font="Arial 8")
LabelCapteur.pack(fill = X)

nomCapteur_texte = Entry(LabelCapteur, textvariable = numCapteur_SV, font = "Arial"+str(taillePolice))
nomCapteur_texte.pack()

LabelCapteur = Label(LabelSaisieDossier, text="* : Informations facultatives", relief=FLAT, fg ='#0066CC', padx=2, pady=2, font="Arial 8 italic")
LabelCapteur.pack(fill=X)

sonde_SV = StringVar()
LabelSonde = Label(LabelSaisieDossier, textvariable = sonde_SV, font = "Arial 10")
LabelSonde.pack(fill=X)

sonde_SV.set("Aucune sonde sélectionnée")

#vérification (et validation)

BoutonVerification = Button(LabelTemperature, text ="Vérification", width=7, command = Verification_Nom, font = "Arial"+str(taillePolice))
BoutonVerification.pack(padx = 5, pady = 5)
Verification = 0 #variable qui permet de savoir si l'utilisateur à vérifier le nom avant de lancer l'acquisition



# frame Initialisation
FrameInitialisation = LabelFrame(FrameGauche, text='I.Initialisation',fg ='red', bg ='ivory', padx=2, pady=2, font = "Arial"+str(taillePolice))
FrameInitialisation.pack(side=TOP)

##ZONE##
longueurV_SV = StringVar()
longueurH_SV = StringVar()
longueurV_SV.set(50)
longueurH_SV.set(110)

LabelSaisieZone = LabelFrame(FrameInitialisation , text='1. Sélection de la zone', fg='blue', padx=5, pady=5, font = "Arial"+str(taillePolice))
LabelSaisieZone.pack(fill=X)

# Création d'un widget Button pour tester la zone
BoutonTestZone = Button(LabelSaisieZone, text ='Tester la zone', command = Selection_Zone, font = "Arial"+str(taillePolice))
BoutonTestZone.pack(padx = 5, pady = 5)

preview = 0 # =1 si on est entrain de faire une prévisualisation
Mafenetre.bind( '<Up>', Fleche_Haut)
Mafenetre.bind( '<Down>', Fleche_Bas)
Mafenetre.bind( '<Right>', Fleche_Droite)
Mafenetre.bind( '<Left>', Fleche_Gauche)
Mafenetre.bind( '<Escape>', Echap)

##FIN ZONE##

##SEUIL##
# Création d'un widget Label Seuil

LabelSaisieSeuil = LabelFrame(FrameInitialisation , text='2. Seuil',fg='blue', padx=5, pady=5, font = "Arial"+str(taillePolice))
LabelSaisieSeuil.pack(fill=BOTH)

seuil_SV = StringVar()
LabelValeurSeuil = Label(LabelSaisieSeuil,textvariable=seuil_SV,relief=SUNKEN, bg='white')
seuil_SV.set(200)
LabelValeurSeuil.pack()

BoutonPlus = Button(LabelSaisieSeuil, text ='+', command = Bouton_Plus, font = "Arial"+str(taillePolice))
BoutonPlus.pack(side = RIGHT, padx = 5, pady = 5)

BoutonMoins = Button(LabelSaisieSeuil, text ='-', command = Bouton_Moins, font = "Arial"+str(taillePolice))
BoutonMoins.pack(side = LEFT, padx = 5, pady = 5)

BoutonValidationSeuil = Button(LabelSaisieSeuil, text ='Valider le seuil', command = Traitement_Zone_Calibration, font = "Arial"+str(taillePolice))
BoutonValidationSeuil.pack(side = BOTTOM, padx = 5, pady = 5)
##FIN SEUIL##


##NOMBRE ACQUISITIONS##
# Création d'un widget Label NbreAcquisitions
nbreAcquisitions_SV = StringVar()

LabelSaisieNbreAcquisitions = LabelFrame(FrameInitialisation, text="3. Nombre d'acquisitions",fg='blue', padx=5, pady=5, font = "Arial"+str(taillePolice))
LabelSaisieNbreAcquisitions.pack(fill=BOTH)
 
nbreAcquisitions_texte = Entry(LabelSaisieNbreAcquisitions, textvariable=nbreAcquisitions_SV, width=30, font = "Arial"+str(taillePolice))
nbreAcquisitions_texte.pack()

##FIN NOMBRE ACQUISITIONS##


##TEMPS ACQUISITION##
# Création d'un widget Label NbreAcquisitions
tempsAcquisition_SV = StringVar() 

LabelSaisieNbreAcquisitions = LabelFrame(FrameInitialisation, text="4. Temps (en secondes) entre 2 acquisitions",fg='blue', padx=5, pady=5, font = "Arial"+str(taillePolice))
LabelSaisieNbreAcquisitions.pack(fill=BOTH)
 
tempsAcquisition_texte = Entry(LabelSaisieNbreAcquisitions, textvariable=tempsAcquisition_SV , width=30, font = "Arial"+str(taillePolice))
tempsAcquisition_texte.pack()

##FIN TEMPS ACQUISITION##


# frame Acquisition
FrameAcquisition = LabelFrame(FrameGauche, text='II.Acquisition',fg ='red', bg ='ivory', padx=2, pady=2, font = "Arial"+str(taillePolice))
FrameAcquisition.pack(side=TOP)

# Création d'un widget Checkbutton pour activer "Analyse des données"
cochee=IntVar()

c = Checkbutton(FrameAcquisition, text="Analyse des données", variable = cochee, font = "Arial"+str(taillePolice))
c.pack(fill=X)

cocheeMode = IntVar()

c = Checkbutton(FrameAcquisition, text="Compensation des erreurs", variable = cocheeMode, font = "Arial"+str(taillePolice))
c.pack(fill=X)

# Création d'un widget Button pour lancer le traitement
BoutonTraitement = Button(FrameAcquisition, text ="Lancement de l'acquisition", width=33, command = Acquisition, font = "Arial"+str(taillePolice))
BoutonTraitement.pack(padx = 5, pady = 5)

# Création d'un widget Button pour arrêter le traitement
BoutonArretTraitement = Button(FrameAcquisition, text ="Arrêt forcé de l'acquisition", width=33, command = Acquisition_Arret, font = "Arial"+str(taillePolice))
BoutonArretTraitement.pack(padx = 5, pady = 5)

# frame EtatAcquisition
FrameEtatAcquisition = LabelFrame(FrameDroite, text="III.Etat de l'acquisition",fg ='red', bg ='ivory', padx=2, pady=2, font = "Arial"+str(taillePolice))
FrameEtatAcquisition.pack(side=TOP)

#Division en 2 de la frame EtatAcquisition
FrameHaut = Frame(FrameEtatAcquisition, bg ='ivory', padx=2, pady=2)
FrameHaut.pack(side=TOP,expand=False)

FrameBas = Frame(FrameEtatAcquisition, bg ='ivory', padx=2, pady=2)
FrameBas.pack(side=BOTTOM,expand=False)


#Création zone d'affichage
longueur=350
Canevas = Canvas(FrameHaut, width=longueur, height=366, background='#CCFFFF')
Canevas.pack()

CanevasEtat = Canvas(FrameEtatAcquisition, width=longueur, height=20, background='#CCFFFF')
CanevasEtat.pack()
txt = CanevasEtat.create_text(longueur/2, 15, text="Remplissez les instructions", font="Arial 9", fill="black")


##CREATION MENU##

menubar = Menu(Mafenetre)

Mafenetre.config(menu=menubar) #affichage du menu

menu1 = Menu(menubar, tearoff=0, relief=RAISED)
menu1.add_command(label="Préférences", command=Ouverture_Preferences, font = "Arial"+str(taillePolice))
menu1.add_command(label="Vérification des données",underline=17, accelerator="Ctrl+d", command=Ouverture_Verification, font = "Arial"+str(taillePolice))
menu1.add_command(label="Génération d'un fichier bilan",underline=24, accelerator="Ctrl+b", command=Ouverture_Generation, font = "Arial"+str(taillePolice))
menubar.add_cascade(label="Menu", menu=menu1)
Mafenetre.bind('<Control-d>', Ouverture_Verification)
menu1.bind('<Control-d>', Ouverture_Verification)

Mafenetre.bind('<Control-b>', Ouverture_Generation)
menu1.bind('<Control-b>', Ouverture_Generation)

#variables globales liées au menu :


cheminDossierSauvegardePreference_SV=StringVar()

FichierPrevisualisation=repertoireScript+"/Preferences/Previsualisation.txt"
FichierCheminDossierSauvegarde=repertoireScript+"/Preferences/CheminDossierSauvegarde.txt"
FichierAnalyseDonnees=repertoireScript+"/Preferences/AnalyseDonnees.txt"

#chargement des préférences de l'utilisateur :

if not os.path.exists(repertoireScript+"/Preferences"): #si le dossier 'Preferences' n'existe pas (cela arrivera que lors de la premiere utilisation)
    os.mkdir(repertoireScript+"/Preferences")

if not os.path.exists(repertoireScript+"/Temporaire"): #si le dossier 'Temporaire' n'existe pas (cela arrivera que lors de la premiere utilisation)
    os.mkdir(repertoireScript+"/Temporaire")
    
if not os.path.exists(repertoireScript+"/Sondes"): #si le dossier 'Sondes' n'existe pas (cela arrivera que lors de la premiere utilisation)
    os.mkdir(repertoireScript+"/Sondes")
    

longueurHPreference_SV = StringVar()
longueurVPreference_SV = StringVar()
if os.path.exists(FichierPrevisualisation):
    fichier=open(FichierPrevisualisation, "r")
    longueurH = int(fichier.readline()) #int sert à enlever le saut de ligne qui serait présent
    longueurV = fichier.readline()
    longueurH_SV.set(longueurH)
    longueurV_SV.set(longueurV)
    
    longueurHPreference_SV.set(longueurH)
    longueurVPreference_SV.set(longueurV)

    fichier.close

if os.path.exists(FichierCheminDossierSauvegarde):
    fichier=open(FichierCheminDossierSauvegarde, "r")
    cheminDossierSauvegarde=fichier.readline()
    cheminDossierSauvegardePreference_SV.set(cheminDossierSauvegarde)
    cheminDossier_SV.set(cheminDossierSauvegarde)
    fichier.close

ecartAbsolu_SV=StringVar()
ecartAbsolu_SV.set(1)

if os.path.exists(FichierAnalyseDonnees):
    fichier = open(FichierAnalyseDonnees, "r")
    ecartAbsolu = fichier.readline()
    ecartAbsolu_SV.set(ecartAbsolu)
    fichier.close



##ONGLET COMMUNICATION##
sonde = 0
etalon = 0

#choix etalon
FrameListeEtalons = LabelFrame(f2, text="Choix de l'étalon", fg ='red', bg ='ivory', padx=2, pady=2, font = "Arial"+str(taillePolice))
FrameListeEtalons.pack()

listeEtalons = Listbox(FrameListeEtalons, exportselection = 0, font = "Arial"+str(taillePolice))
listeEtalons.insert(1, "Consort")
listeEtalons.insert(2, "3458A")
listeEtalons.insert(3, "Aucun")

listeEtalons.pack()

def Selection_Etalon(*event):
    global etalon

    etalon = listeEtalons.get(listeEtalons.curselection())

    if etalon == "Aucun":
        listeSondes.delete(0, END)
    else:
        listeSondes.delete(0, END)
        listeSondesTxt = os.listdir(repertoireScript+'/Sondes')
        for indice in range(len(listeSondesTxt)):
            listeSondes.insert(END, listeSondesTxt[indice].replace(".txt",""))


def Selection_Sonde(*event):
    global sonde, numSonde
    
    sonde = listeSondes.get(listeSondes.curselection())
    numSonde = listeSondes.curselection() # renvoie un tuple (numero sonde,)
    sonde_SV.set("Sonde : "+sonde)

    
listeEtalons.bind('<<ListboxSelect>>', Selection_Etalon)

#choix sonde
FrameListeSondes = LabelFrame(f2, text="Choix de la sonde", fg ='red', bg ='ivory', padx=2, pady=2, font = "Arial"+str(taillePolice))
FrameListeSondes.pack()

listeSondes = Listbox(FrameListeSondes, exportselection = 0, font = "Arial"+str(taillePolice))


listeSondes.pack()
listeSondes.bind('<<ListboxSelect>>', Selection_Sonde)

def Ouverture_Sondes():
    global EntreeMdp, fenetreMDP
    fenetreMDP = Toplevel(master=Mafenetre)
    fenetreMDP.title("Entrer le mot de passe")
    fenetreMDP.configure(background='ivory')
    fenetreMDP.geometry('350x40+150+150') #'tailleX*tailleY+apparationX+apparitionY'
    
    EntreeMdp = Entry(fenetreMDP, width=30, show = "*", font = "Arial"+str(taillePolice))
    EntreeMdp.pack(padx = 4, pady = 4)
    EntreeMdp.bind('<KP_Enter>', Validation_Mdp)
    EntreeMdp.bind('<Return>', Validation_Mdp)

#bouton pour accéder à la modification des paramètres
BoutonParamSondes = Button(f2, text='Accès aux paramètres des sondes', command=Ouverture_Sondes, font = "Arial"+str(taillePolice))
BoutonParamSondes.pack(padx = 4, pady = 4)



def Validation_Mdp(event):
    global EntreeMdp, fenetreMDP
    global EntreeNomSonde, ListeGestionSondes, coeffa, coeffb, coeffc, coeffd, EntreeCoeffa, EntreeCoeffb, EntreeCoeffc, EntreeCoeffd
    if EntreeMdp.get() == "ensea":
        fenetreMDP.destroy()
        fenetreSondes = Toplevel(master = Mafenetre)
        fenetreSondes.title("Configuration des sondes")
        fenetreSondes.configure(background='ivory')
        fenetreSondes.geometry('475x475+150+150') #'tailleX*tailleY+apparationX+apparitionY'

        ListeGestionSondes = Listbox(fenetreSondes, width=30, height=10, exportselection = 0, font = "Arial"+str(taillePolice))
        ListeGestionSondes.grid(row=0, column=0)
         
        # use entry widget to display/edit selection
        EntreeNomSonde = Entry(fenetreSondes, width=30, bg='yellow', font = "Arial"+str(taillePolice))
        EntreeNomSonde.insert(0, 'Entrez le nom de la sonde')
        EntreeNomSonde.grid(row=1, column=0)


        # button to add a line to the listbox
        BoutonAjoutSonde = Button(fenetreSondes, text='Ajouter la sonde', command=Ajout_Sonde, font = "Arial"+str(taillePolice))
        BoutonAjoutSonde.grid(row=2, column=0)
        # button to delete a line from listbox
        BoutonSuppressionSonde = Button(fenetreSondes, text='Supprimer la sonde sélectionnée', command=Suppression_Sonde, font = "Arial"+str(taillePolice))
        BoutonSuppressionSonde.grid(row=3, column=0)

        # label pour indiquer l'ordre des coefficients

        LabelCoeff = Label(fenetreSondes, text = 'Coefficients  correctifs de la sonde dans l\'ordre a, b, c et d :', font = "Arial"+str(taillePolice))
        LabelCoeff.grid(row=4, column=0, padx = 4, pady = 4)

        coeffa = StringVar()
        coeffb = StringVar()
        coeffc = StringVar()
        coeffd = StringVar()

        EntreeCoeffa = Entry(fenetreSondes, width=30, bg='grey', textvariable = coeffa, font = "Arial"+str(taillePolice))
        EntreeCoeffa.grid(row=5, column=0)

        EntreeCoeffb = Entry(fenetreSondes, width=30, bg='grey', textvariable = coeffb, font = "Arial"+str(taillePolice))
        EntreeCoeffb.grid(row=6, column=0)

        EntreeCoeffc = Entry(fenetreSondes, width=30, bg='grey', textvariable = coeffc, font = "Arial"+str(taillePolice))
        EntreeCoeffc.grid(row=7, column=0)

        EntreeCoeffd = Entry(fenetreSondes, width=30, bg='grey', textvariable = coeffd, font = "Arial"+str(taillePolice))
        EntreeCoeffd.grid(row=8, column=0)

        # clique gauche de la souris pour actualiser les coefficients par rapport à la sonde
        ListeGestionSondes.bind('<ButtonRelease-1>', actualisation_liste)

        # button to add a line to the listbox
        BoutonActualisation = Button(fenetreSondes, text='Modifier les coefficients', command=actualisation_coefficient, font = "Arial"+str(taillePolice))
        BoutonActualisation.grid(row=9, column=0)

        #chargement des étalons dans ListeGestionSondes
        listeSonde = os.listdir(repertoireScript+'/Sondes')
        for indice in range(len(listeSonde)):
            ListeGestionSondes.insert(END, listeSonde[indice].replace(".txt",""))

    else :
        showwarning('Attention', 'Mot de passe incorect', parent = fenetreMDP)
    


def Ajout_Sonde():
    global EntreeNomSonde, ListeGestionSondes
    if os.path.exists(repertoireScript+'/Sondes/'+EntreeNomSonde.get()+'.txt'):
        showwarning('Attention', 'Nom de sonde déjà existant')
    else:
        ListeGestionSondes.insert(END, EntreeNomSonde.get())
        fichier = open(repertoireScript+'/Sondes/'+EntreeNomSonde.get()+'.txt','w')
        fichier.write('1\n1\n1\n1\n')
        fichier.close()

def Suppression_Sonde():
    global ListeGestionSondes
    try:
        index = ListeGestionSondes.curselection()[0]
        nomSonde = ListeGestionSondes.get(ListeGestionSondes.curselection())
        os.remove(repertoireScript+'/Sondes/'+nomSonde+".txt")
        ListeGestionSondes.delete(index)
    except IndexError:
        pass


def actualisation_liste(event):
    global ListeGestionSondes, coeffa, coeffb, coeffc, coeffd, EntreeCoeffa, EntreeCoeffb, EntreeCoeffc, EntreeCoeffd
    nomSonde = ListeGestionSondes.get(ListeGestionSondes.curselection())
    fichier = open(repertoireScript+'/Sondes/'+nomSonde+'.txt','r')
    lignes = fichier.readlines()
    coeffa.set(lignes[0].replace("\n",""))
    coeffb.set(lignes[1].replace("\n",""))
    coeffc.set(lignes[2].replace("\n",""))
    coeffd.set(lignes[3].replace("\n",""))
    fichier.close
    EntreeCoeffa.configure(bg = 'grey')
    EntreeCoeffb.configure(bg = 'grey')
    EntreeCoeffc.configure(bg = 'grey')
    EntreeCoeffd.configure(bg = 'grey')

def actualisation_coefficient():
    global ListeGestionSondes, coeffa, coeffb, coeffc, coeffd, EntreeCoeffa, EntreeCoeffb, EntreeCoeffc, EntreeCoeffd
    nomSonde = ListeGestionSondes.get(ListeGestionSondes.curselection())
    fichier = open(repertoireScript+'/Sondes/'+nomSonde+'.txt','w')
    fichier.write(str(coeffa.get())+'\n'+str(coeffb.get())+'\n'+str(coeffc.get())+'\n'+str(coeffd.get()))
    fichier.close()
    EntreeCoeffa.configure(bg = 'green')
    EntreeCoeffb.configure(bg = 'green')
    EntreeCoeffc.configure(bg = 'green')
    EntreeCoeffd.configure(bg = 'green')

Mafenetre.withdraw()




#Mafenetre.mainloop() #NE RIEN ECRIRE APRES CETTE LIGNE


##--##--FIN PARTIE GRAPHIQUE--##--##
