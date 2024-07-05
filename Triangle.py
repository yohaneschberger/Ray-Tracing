import numpy as np
import Objet3D as lObjet
import Couleur as lCouleur

class Triangle(lObjet.Objet3D):
    def __init__(self, position, sommet2, sommet3, couleur, diffus, specular, reflection):
        super().__init__(position, couleur, diffus, specular, reflection)
        self.sommet2 = sommet2
        self.sommet3 = sommet3

    def intersection(self, rayO, rayD):
        '''
        Calcul de l'intersection entre un rayon et un triangle
            rayO : Vecteur3D (origine du rayon)
            rayD : Vecteur3D (direction du rayon)
        Retourne la distance entre l'origine du rayon et le point d'intersection
        '''
        # Calcul du plan du triangle
        AB = self.sommet2.soustraction(self.position)
        AC = self.sommet3.soustraction(self.position)
        N = AB.prod_vectoriel(AC).normalisation()
        d = N.prod_scal(self.position)
        # Intersection avec le plan du triangle
        denominateur = rayD.prod_scal(N)
        if np.abs(denominateur) < 1e-10:
            return np.inf
        t = (d - rayO.prod_scal(N)) / denominateur
        if t < 0:
            return np.inf
        # Intersection avec le triangle
        M = rayO.addition(rayD.multiplication(t))
        AM = M.soustraction(self.position)
        AB = self.sommet2.soustraction(self.position)
        AC = self.sommet3.soustraction(self.position)
        v1 = N.prod_scal(AB.prod_vectoriel(AM))
        v2 = N.prod_scal(AM.prod_vectoriel(AC))
        v3 = N.prod_scal(AC.prod_vectoriel(AB))
        if v1 >= 0 and v2 >= 0 and v3 >= 0:
            return t
        return np.inf


    def normale(self, M):
        '''
        Calcul de la normale à un point
            M : Vecteur3D (point d'intersection)
        '''
        AB = self.sommet2.soustraction(self.position)
        AC = self.sommet3.soustraction(self.position)
        return AB.prod_vectoriel(AC).normalisation()