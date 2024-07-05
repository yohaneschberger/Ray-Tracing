import numpy as np


class Vecteur3D:
    '''
    Classe pour les vecteurs 3D
        x, y, z : float
    '''
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def addition(self, autre):
        '''
        addition de deux vecteurs
        '''
        return Vecteur3D(self.x + autre.x, self.y + autre.y, self.z + autre.z)

    def soustraction(self, autre):
        '''
        Soustraction de deux vecteurs
        '''
        return Vecteur3D(self.x - autre.x, self.y - autre.y, self.z - autre.z)

    def multiplication(self, scalair):
        '''
        Multiplication d'un vecteur par un scalaire
        '''
        return Vecteur3D(self.x * scalair, self.y * scalair, self.z * scalair)

    def division(self, scalair):
        '''
        Division d'un vecteur par un scalaire
        '''
        return Vecteur3D(self.x / scalair, self.y / scalair, self.z / scalair)

    def __len__(self):
        '''
        Longueur du vecteur
        '''
        return 3

    def prod_scal(self, autre):
        '''
        Produit scalaire de deux vecteurs
        '''
        return self.x * autre.x + self.y * autre.y + self.z * autre.z

    def norme(self):
        '''
        Norme du vecteur
        '''
        return np.sqrt(self.prod_scal(self))

    def normalisation(self):
        '''
        Normalisation du vecteur
        '''
        return self.division(self.norme())
    
    def coord(self):
        '''
        Coordonnées du vecteur
        '''
        return self.x, self.y, self.z
    
    def as_list(self):
        '''
        Conversion du vecteur en liste
        '''
        return [self.x, self.y, self.z]
