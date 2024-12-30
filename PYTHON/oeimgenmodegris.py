from PyQt5.QtWidgets import  QMessageBox
import numpy as np


def inverser_i(img):
    """
    Renvoie l'image inversée en fonction de la profondeur maximale des pixels.
    """
    depth = img.max() #ceci est ajoutée pour les les images floats ou 16 bits
    return depth - img


def flipH(img):
    """
    Renvoie l'image retournee horizontalement (symetrie par l'axe vertical)
    en manipulant directement les matrices sans fonctions predefinies.

    :param img: Liste 2D (ou tableau 2D), representant l'image.
    :return: Image retournee horizontalement.
    """
    # Obtenir les dimensions de l'image
    rows = len(img)
    cols = len(img[0])

    # Creer une nouvelle matrice vide de mêmes dimensions
    flipped_img = [[0] * cols for _ in range(rows)]

    # Remplir la nouvelle matrice avec les pixels retournes
    for i in range(rows):
        for j in range(cols):
            flipped_img[i][j] = img[i][cols - 1 - j]

    return flipped_img

'''
def poserV(img1, img2):
    """
    Superpose verticalement deux images de mêmes dimensions.
    """
    if img1.shape != img2.shape:
        raise ValueError("Les dimensions des deux images doivent correspondre pour l'opération verticale.")
    return img1 + img2
'''
def poserV(img1, img2):
    """
    Superpose verticalement deux images. Si les deux images ont des largeurs differentes,
    on ajoute des bordures noires pour les aligner.
    """
    # Recuperer les dimensions des deux images
    hauteur1, largeur1 = img1.shape[:2]
    hauteur2, largeur2 = img2.shape[:2]

    # Trouver la largeur maximale
    largeur_max = max(largeur1, largeur2)

    # Ajuster la largeur de la première image si necessaire
    if largeur1 < largeur_max:
        bordure_gauche = (largeur_max - largeur1) // 2
        bordure_droite = largeur_max - largeur1 - bordure_gauche
        img1 = np.pad(img1, ((0, 0), (bordure_gauche, bordure_droite), (0, 0)), mode='constant')

    # Ajuster la largeur de la deuxième image si necessaire
    if largeur2 < largeur_max:
        bordure_gauche = (largeur_max - largeur2) // 2
        bordure_droite = largeur_max - largeur2 - bordure_gauche
        img2 = np.pad(img2, ((0, 0), (bordure_gauche, bordure_droite), (0, 0)), mode='constant')

    # Combiner manuellement les deux images verticalement
    hauteur_totale = hauteur1 + hauteur2
    img_combined = np.zeros((hauteur_totale, largeur_max, img1.shape[2]), dtype=img1.dtype)

    # Copier les pixels de img1
    for i in range(hauteur1):
        for j in range(largeur_max):
            img_combined[i][j] = img1[i][j]

    # Copier les pixels de img2
    for i in range(hauteur2):
        for j in range(largeur_max):
            img_combined[hauteur1 + i][j] = img2[i][j]

    return img_combined
'''
def poserH(img1, img2):
    """
    Superpose horizontalement deux images de même hauteur.
    """
    if img1.shape[0] != img2.shape[0]:
        raise ValueError("Les hauteurs des deux images doivent correspondre pour l'opération horizontale.")
    return np.vstack([img1, img2])  # Combine les lignes des deux images.
'''
def poserH(img1, img2):
    """
    Superpose horizontalement deux images. Si les deux images ont des hauteurs differentes,
    on ajoute des bordures noires pour les aligner.
    """
    # Recuperer les dimensions des deux images
    hauteur1, largeur1 = img1.shape[:2]
    hauteur2, largeur2 = img2.shape[:2]

    # Trouver la hauteur maximale
    hauteur_max = max(hauteur1, hauteur2)

    # Ajuster la hauteur de la premiere image si necessaire
    if hauteur1 < hauteur_max:
        bordure_haut = (hauteur_max - hauteur1) // 2
        bordure_bas = hauteur_max - hauteur1 - bordure_haut
        img1 = np.pad(img1, ((bordure_haut, bordure_bas), (0, 0), (0, 0)), mode='constant')

    # Ajuster la hauteur de la deuxieme image si necessaire
    if hauteur2 < hauteur_max:
        bordure_haut = (hauteur_max - hauteur2) // 2
        bordure_bas = hauteur_max - hauteur2 - bordure_haut
        img2 = np.pad(img2, ((bordure_haut, bordure_bas), (0, 0), (0, 0)), mode='constant')

    # Combiner les deux images horizontalement
    largeur_total = largeur1 + largeur2
    matrice_total = np.zeros((hauteur_max, largeur_total, img1.shape[2]), dtype=img1.dtype)

    for i in range(hauteur_max):
        for j in range(largeur1):
            matrice_total[i][j] = img1[i][j]

    for i in range(hauteur_max):
        for j in range(largeur2):
            matrice_total[i][largeur1 + j] = img2[i][j]
    return matrice_total

def afficher_erreur(message):
    """
    Affiche une boîte de dialogue d'erreur.
    """
    QMessageBox.critical(None, "Erreur", message)

