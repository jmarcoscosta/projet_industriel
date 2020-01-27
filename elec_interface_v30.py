####LES IMPORTATIONS et VARIABLES/DEFINITIONS GLOBALES####

from elec_acquisition_v30 import *
from tkinter import Listbox
from tkinter import Button

##--FONCTIONS--##

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
        preview = 0

def Bouton_Plus():
    global seuil_SV
    seuil_SV = seuil_SV + 10
    LabelValeurSeuil.delete(ALL)
    LabelValeurSeuil.create_text(30, 8, text=str(seuil_SV), font="Arial 9", fill="black")
    
    Traitement_Zone_Initialisation()
    
def Bouton_Moins():
    global seuil_SV
    #seuil_SV.set(int(seuil_SV.get())-10)
    seuil_SV = seuil_SV - 10
    LabelValeurSeuil.delete(ALL)
    LabelValeurSeuil.create_text(30, 8, text=str(seuil_SV), font="Arial 9", fill="black")
    
    Traitement_Zone_Initialisation()


def Traitement_Zone_Initialisation():
    dossierActuel = "Calibration"
    seuil = seuil_SV
    global photo,seuilF #A METTRE ABSOLUMENT SINON L'IMAGE NE S'AFFICHE PAS

    global Canevas

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


##--FIN FONCTIONS--##
def open_add_sequence_interface_():
    from os import system
    system('python add_sequence_interface.py')

def Creation_Fenetre_Elec():
    global MafenetreElec, longueurV_SV, longueurH_SV, LabelValeurSeuil, ZoneInstruction, Canevas
    # Création de la fenêtre principale
    MafenetreElec = Toplevel()
    MafenetreElec.title("Module d'acquisition d'images - v3.4")
    MafenetreElec.configure(background='ivory')

    n = Notebook(MafenetreElec)
    f1 = Frame(n)
    f2 = Frame(n)

    n.add(f2, text = 'Communication')
    n.add(f1, text = 'Acquisition')
    n.pack()


    # Label2 = Label(f2, text ="Onglet Communication : non implémenté", fg = 'red', width=33)
    # Label2.pack(padx = 5, pady = 5)

    # liste pour choisir l'appareil

    # FrameListeAppareils = LabelFrame(f2, text="Marque de l'appareil",fg ='red', bg ='ivory', ipadx=2, ipady=2)
    FrameListeAppareils = LabelFrame(f2, text="I.Marque de l'appareil",fg ='red', bg ='ivory')
    FrameAddSequenceInterface= LabelFrame(f2, text="II.(facultatif) Crééer trame de vérificartion",fg ='red', bg ='ivory', width=130)
    add_sequence_button = Button(FrameAddSequenceInterface,text='Lancer', command=open_add_sequence_interface_)
    add_sequence_button.place(x = 90, y = 30)
    # FrameListeAppareils.pack()
    FrameListeAppareils.grid(row=0, column=0,ipadx=50,ipady= 50,padx = 20, pady = 20)
    FrameAddSequenceInterface.grid(row=0, column=1,ipadx=50,ipady= 50,padx = 20, pady = 20)

    global liste 
    liste = Listbox(FrameListeAppareils)
    liste.insert(1, "Fluke")
    liste.insert(2, "Meatest")
    liste.insert(3, "CX_1651")
    liste.pack()


    FrameInitialisationElec = LabelFrame(f1, text='I.Initialisation',fg ='red', bg ='ivory', padx=2, pady=2)
    FrameInitialisationElec.pack()


    FrameGaucheElec = Frame(FrameInitialisationElec, bg ='ivory', padx=2, pady=2)
    FrameGaucheElec.pack(side=LEFT,anchor=NW)

    FrameDroiteElec = Frame(FrameInitialisationElec, bg ='ivory', padx=2, pady=2)
    FrameDroiteElec.pack(side=LEFT,anchor=NW)

    longueur=258
    Canevas = Canvas(FrameDroiteElec, width=longueur, height=147, background='#CCFFFF')
    Canevas.pack()

    ##ZONE##
    longueurV_SV = StringVar()
    longueurH_SV = StringVar()
    longueurV_SV.set(50)
    longueurH_SV.set(110)

    LabelSaisieZoneElec = LabelFrame(FrameGaucheElec , text='1. Sélection de la zone', fg='blue', padx=5, pady=5)
    LabelSaisieZoneElec.pack(fill=X)

    # Création d'un widget Button pour tester la zone
    BoutonTestZoneElec = Button(LabelSaisieZoneElec, text ='Tester la zone', command = Selection_Zone)
    BoutonTestZoneElec.pack(padx = 5, pady = 5)

    preview = 0 # =1 si on est entrain de faire une prévisualisation
    MafenetreElec.bind( '<Up>', Fleche_Haut)
    MafenetreElec.bind( '<Down>', Fleche_Bas)
    MafenetreElec.bind( '<Right>', Fleche_Droite)
    MafenetreElec.bind( '<Left>', Fleche_Gauche)
    MafenetreElec.bind( '<Escape>', Echap)

    ##FIN ZONE##

    ##SEUIL##
    # Création d'un widget Label Seuil

    LabelSaisieSeuilElec = LabelFrame(FrameGaucheElec , text='2. Seuil',fg='blue', padx=5, pady=5)
    LabelSaisieSeuilElec.pack(fill=BOTH)

    LabelValeurSeuil = Canvas(LabelSaisieSeuilElec, width=60, height=16, bg='white')
    LabelValeurSeuil.pack()
    
    LabelValeurSeuil.create_text(30, 8, text=str(seuil_SV), font="Arial 9", fill="black")


    BoutonPlusElec = Button(LabelSaisieSeuilElec, text ='+', command = Bouton_Plus)
    BoutonPlusElec.pack(side = RIGHT, padx = 5, pady = 5)

    BoutonMoinsElec = Button(LabelSaisieSeuilElec, text ='-', command = Bouton_Moins)
    BoutonMoinsElec.pack(side = LEFT, padx = 5, pady = 5)

    BoutonValidationSeuilElec = Button(LabelSaisieSeuilElec, text ='Valider le seuil', command = Traitement_Zone_Calibration)
    BoutonValidationSeuilElec.pack(side = BOTTOM, padx = 5, pady = 5)
    ##FIN SEUIL##


    FrameLancement = LabelFrame(f1, text='II.Etalonnage',fg ='red', bg ='ivory', padx=2, pady=2)
    FrameLancement.pack()


    BoutonSequence = Button(FrameLancement, text ="Lancement de la séquence", width=33, command = Sequence)
    BoutonSequence.pack(padx = 5, pady = 5)

    ZoneInstruction = Canvas(FrameLancement, width=500, height=30, background='#CCFFFF')
    ZoneInstruction.pack()


    ZoneInstruction.create_text(250, 15, text="En attente du lancement", font="Arial 9", fill="black")

    MafenetreElec.protocol("WM_DELETE_WINDOW", Fermeture) #pour fermer le parent du toplevel (ie fermer la fenetre température)


init = 0 #initialisé à 0 lors du démarrage pour executer "camera = picamera.PiCamera()" une seule fois pour ne pas avoir "Failed to enable connection: Out of resources" même si non bloquant
seuil_SV = 200



def Fermeture():
    from temperature_interface_v30 import Mafenetre
    Mafenetre.destroy() #cela va aussi fermer ses descendants, donc MafenetreElec


if not os.path.exists("Certificats_Elec"):
    os.makedirs("Certificats_Elec")

#MafenetreElec.withdraw()
