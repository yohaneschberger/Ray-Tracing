import numpy as np


class Couleur:
    '''
    Classe pour les couleurs
        r, g, b : float
    '''
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __len__(self):
        '''
        Longueur de la couleur
        '''
        return 3
    
    def to_numpy(self):
        '''
        Conversion de la couleur en tableau numpy
        '''
        return np.array([self.r, self.g, self.b])
    
    def addition(self, autre):
        '''
        Addition de deux couleurs
        '''
        if isinstance(autre, Couleur):                                                  #isinstance vérifie que autre est de classe couleur
            return Couleur(self.r + autre.r, self.g + autre.g, self.b + autre.b)
        elif isinstance(autre, (int, float)):                                           #isinstance vérifie que autre est un int ou un float
            return Couleur(self.r + autre, self.g + autre, self.b + autre)
    
    def multiplication(self, autre):
        '''
        Multiplication de deux couleurs
        '''
        if isinstance(autre, Couleur):
            return Couleur(self.r * autre.r, self.g * autre.g, self.b * autre.b)
        elif isinstance(autre, (int, float)):
            return Couleur(self.r * autre, self.g * autre, self.b * autre)
        