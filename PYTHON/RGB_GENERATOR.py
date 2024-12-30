import numpy as np
from PIL import Image
from random import randrange

def initImageRGB(imageRGB):
    #Conversion d'"imageRGB" en un tableau utilisant numpy pour plus d'efficacité.
    imageRGB = np.array(imageRGB, dtype=np.uint8) #unsigned 8-bit(1octet) integer(src = module numpy).
    for i in range(imageRGB.shape[0]):# Boucle à travers les lignes
        for j in range(imageRGB.shape[1]):# Boucle à travers les colonnes
                for k in range(3): # Boucle à travers les canaux RGB
                    imageRGB[i][j][k] = randrange(256) # Attribuer une valeur aléatoire à chaque canal
    return imageRGB

def symetrie_h(img):
    #Ouvrir l'image avec Pillow
    img = Image.open(img)
    #convertir l'image en une matrice
    mat_img = np.array(img)
    #symétrie par rapport à l'axe horizontal
    #cad en doit inverser les lignes la premiere devenir la derniere, la deuxieme devenir l'avant derniere ect
    #on peut utiliser aussi la methode du slicing
    #il suffit de faire mat_img_sym_h = mat_img[::-1] cad commencer de la derniere ligne par un pas en arriere
    mat_img_sym_h = np.flipud(mat_img)
    return mat_img_sym_h

def symetrie_V(img):
    #Ouvrir l'image avec Pillow
    img = Image.open(img)
    #convertir l'image en une matrice
    mat_img = np.array(img)
    #symétrie par rapport à l'axe vertical
    #on peut aussi ici utilisant slicing tout simplement on fait juste mat_img_sym_v = mat_img[:,::-1] cad commencer par le dernier colonne :->
    mat_img_sym_V = np.fliplr(mat_img)
    return mat_img_sym_V

def grayscale(imageRGB):
    # Ouvrir l'image avec Pillow
    imageRGB = Image.open(imageRGB)
    # Convertir l'image en une matrice
    mat_img = np.array(imageRGB)
    # Crée une matrice vide pour l'image en niveaux de gris
    img_ng = np.zeros((len(mat_img), len(mat_img[0])))
    # Parcourt chaque pixel de l'image originale pour appliquer la transformation en niveaux de gris
    for i in range(len(mat_img)):
        for j in range(len(mat_img[0])):
            # Applique votre algorithme pour calculer le niveau de gris
            rgb_values = mat_img[i][j][:3]
            max_value, min_value = rgb_values[0], rgb_values[0]
            for value in rgb_values:
                if value > max_value:
                    max_value = value
                if value < min_value:
                    min_value = value
            result = max_value//2 + min_value//2
            img_ng[i][j] = result
    # Retourne la matrice calculée
    return img_ng
