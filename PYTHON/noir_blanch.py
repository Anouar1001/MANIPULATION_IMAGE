import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.misc import ascent

# Fonction pour générer une image noire
def image_noire(h=512, l=512):
    # Créer une image noire (tous les pixels sont 0)
    I3 = np.zeros((h, l), dtype=np.uint8)

    # Afficher l'image (optionnel)
    plt.imshow(I3, cmap='gray')
    plt.axis('off')
    plt.title('Image Noire')
    plt.show()

    return I3


def image_blanche(h, l):
    """
    Fonction pour générer et afficher une image noire de dimensions spécifiées.

    Arguments :
        h (int) : Hauteur de l'image (nombre de lignes). Par défaut, 512.
        l (int) : Largeur de l'image (nombre de colonnes). Par défaut, 512.

    Retour :
        I3 (numpy.ndarray) : Une matrice de taille h x l contenant uniquement des 1,
                            représentant une image noire.

    Exemple d'utilisation :
        image_blanche(512, 512)  # Génère et affiche une image noire de 512 x 512
        image_blanche()          # Utilise les dimensions par défaut 512 x 512
    """
    # Étape 1 : Vérification des arguments par défaut
    # Si l'utilisateur ne spécifie pas les dimensions, on utilise les valeurs par défaut.
    if h <= 0 or l <= 0:
        raise ValueError("Les dimensions de l'image doivent être positives (h > 0, l > 0).")

    # Étape 2 : Créer une matrice remplie de 1
    # La matrice contient h lignes et l colonnes, avec des valeurs initialisées à 1.
    I3 = np.ones((h, l), dtype=np.uint8)  # Type de données uint8 pour les images (valeurs entre 0 et 255)

    # Étape 3 : Afficher l'image générée
    # On utilise matplotlib pour afficher l'image.
    plt.figure(figsize=(6, 6))  # Définir la taille de la fenêtre d'affichage
    plt.imshow(I3, cmap='gray', vmin=0, vmax=1)  # Afficher l'image avec une palette de gris (0 à 1)
    plt.axis('off')  # Masquer les axes pour une meilleure présentation
    plt.title('Image blanche')  # Ajouter un titre descriptif à l'image
    plt.show()  # Afficher l'image à l'écran

    # Étape 4 : Retourner la matrice de l'image
    return I3


def creer_img_blanc_noir(h, l):
    """
    Fonction pour créer une image avec un motif en noir et blanc.
    Chaque pixel est soit noir (0), soit blanc (255), basé sur une règle simple.

    Arguments :
        h (int) : Hauteur de l'image
        l (int) : Largeur de l'image

    Retourne :
        numpy.ndarray : Image (h x l) avec le motif en noir et blanc
    """
    # Initialiser une matrice numpy remplie de zéros (noir)
    img = np.zeros((h, l), dtype=np.uint8)

    # Appliquer un motif : si la somme des indices (i+j) est paire, le pixel est blanc
    for i in range(h):  # Parcourir les lignes
        for j in range(l):  # Parcourir les colonnes
            if (i + j) % 2 == 0:  # Vérifier si la somme des indices est paire
                img[i, j] = 255  # Blanc
            else:
                img[i, j] = 0  # Noir

    # Afficher l'image avec les paramètres corrects pour une image strictement noir et blanc
    plt.figure(figsize=(8, 8))  # Taille de la fenêtre fixe
    plt.imshow(img,
              cmap='binary_r',           # Utiliser binary_r pour avoir noir=0 et blanc=255
              interpolation='nearest',    # Pas d'interpolation entre les pixels
              vmin=0,
              vmax=255)
    plt.axis('off')
    plt.title('Image Noire et Blanche')
    plt.show()

    return img
def negatif(Img):
    """
    Fonction pour construire le négatif d'une image représentée par une matrice.
    Pour une image binaire, les pixels noirs (0) deviennent blancs (255) et vice versa.

    Arguments :
        Img (numpy.ndarray) : Matrice représentant l'image d'entrée (noir et blanc)

    Retourne :
        numpy.ndarray : Matrice représentant l'image négative
    """
    return 255 - Img  # Inversion des valeurs : 0 -> 255 et 255 -> 0

