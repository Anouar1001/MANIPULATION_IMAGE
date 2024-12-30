import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk#PIL pour traiter les images avec Tkinter


# Définit une fonction pour lire une image à partir d'un chemin donné.
def lectureImage(chemin):
    #pour que le variable img soit globale et pour l'utiliser pour tous les fonctions.
    global img
    #Utilise la fonction `imread` de Matplotlib pour lire le fichier image au chemin spécifié.
    img=plt.imread(chemin)
    #Retourne une matrice représentant les valeurs de pixels de l'image.
    return img
    # Renvoie la matrice contenant les données de l'image dans le var img.


#Définit une fonction pour afficher une image.
def AfficherImg(img):
    plt.axis("off")
    #Désactive les axes (pas de bordures ou étiquettes autour de l'image).
    plt.imshow(img, interpolation="nearest")
    #Affiche l'image donnée avec une interpolation simple (sans lissage des pixels).
    #Une autre option pour afficher l'image en nuances de gris en spécifiant une palette prédéfinie.
    plt.show()
    #Affiche effectivement l'image à l'écran.


#Définit une fonction pour enregistrer une image.
def saveImage(chemin,img):
    plt.imsave(chemin,img)
    messagebox.showinfo("Succès", f"L'image a été sauvegardée sous : {chemin}")
    #Utilise la fonction `imsave` de Matplotlib pour sauvegarder l'image avec un nom de fichier prédéfinie.
    #Sauvegarde l'image dans le répertoire courant.
