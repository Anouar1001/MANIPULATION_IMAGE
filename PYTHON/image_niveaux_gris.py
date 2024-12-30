import numpy as np
from PIL import Image


def luminance(Img):
    # Charger l'image
    img = Image.open(Img).convert('L')  # Convertir l'image en niveaux de gris

    # Convertir l'image en une matrice numpy
    img_array = np.array(img)

    # Calculer la somme des pixels et le nombre total de pixels
    sum_pixels = np.sum(img_array)
    total_pixels = img_array.size  # Taille totale de la matrice

    # Calculer la moyenne des pixels (luminance)
    lum = sum_pixels / total_pixels

    return lum

def contrast(Img):
    # Charger l'image et la convertir en niveaux de gris
    img = Image.open(Img).convert('L')  # Convertir en niveaux de gris

    # Convertir l'image en une matrice numpy
    img_array = np.array(img)

    # Dimensions de l'image
    l, c = img_array.shape  # l = nombre de lignes, c = nombre de colonnes

    # Calcul de la moyenne des pixels (Moy)
    moy = np.mean(img_array)

    # Calcul de la variance (contraste) avec la formule donnée
    variance = 0
    for i in range(l):
        for j in range(c):
            variance += (img_array[i, j] - moy) ** 2

    # Calcul du contraste comme la variance divisée par N
    N = l * c
    contrast_value = variance / N

    return contrast_value

def profondeur(Img):
    # Charger l'image et la convertir en niveaux de gris
    img = Image.open(Img).convert('L')  # 'L' convertit en niveaux de gris

    # Convertir l'image en une matrice numpy
    img_array = np.array(img)

    # Initialiser la variable max_value avec la plus petite valeur possible
    max_value = -1

    # Parcourir chaque ligne de l'image avec i représentant l'index de chaque ligne
    for i in img_array:
        for pixel in i:
            if pixel > max_value:
                max_value = pixel

    return max_value

def Ouvrir(Img):
    # Charger l'image et la convertir en niveaux de gris
    img = Image.open(Img).convert('L')  # 'L' convertit l'image en niveaux de gris

    # Convertir l'image en une matrice numpy
    img_array = np.array(img)
    return img_array
