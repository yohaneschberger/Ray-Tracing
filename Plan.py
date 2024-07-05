import numpy as np
import Objet3D as lObjet
import Couleur as lCouleur


class Plan(lObjet.Objet3D):
    '''
    Classe pour les plans
        Parametres OBJET3D
        normal : Vecteur3D
    '''
    def __init__(self, position, normal, couleur, diffuse, specular, reflection, texture = None):
        super().__init__(position, couleur, diffuse, specular, reflection)
        self.normal = normal.normalisation()
        self.texture = texture

    def intersection(self, rayO, rayD):
        '''
        Calcul de l'intersection entre un rayon et un plan
            rayO : Vecteur3D (origine du rayon)
            rayD : Vecteur3D (direction du rayon)
        Retourne la distance entre l'origine du rayon et le point d'intersection
        '''
        denominateur = rayD.prod_scal(self.normal)                            # Produit scalaire entre la direction du rayon et la normale du plan
        if np.abs(denominateur) < 1e-10:                                # Si le dénominateur est proche de 0, le rayon est parallèle au plan
            return np.inf                                               # Pas d'intersection
        d = (self.position.soustraction(rayO).prod_scal(self.normal)) / denominateur   # Distance entre l'origine du rayon et le point d'intersection
        if d < 0:
            return np.inf                                               # Pas d'intersection si la distance est négative
        return d
    
    def normale(self, M):
        '''
        Calcul de la normale à un point
            M : inutilisé car la normale est constante
        '''
        return self.normal
    
    def get_uv(self, M):
        '''
        Calcul des coordonnées uv du point d'intersection
            M : Vecteur3D (point d'intersection)
        Retourne les coordonnées uv
        '''
        u = (M.x - np.floor(M.x)) # Coordonnée u
        v = (M.z - np.floor(M.z)) # Coordonnée v
        return u, v
    
    def couleur_texture(self, M):
        '''
        Calcul de la couleur d'un point sur le plan (en utilisant la texture)
            M : Vecteur3D (point d'intersection)
        Retourne la couleur du point
        '''
        if self.texture is None:
            return self.couleur
        
        u, v = self.get_uv(M)   # Coordonnées uv du point d'intersection
        x, y = self.texture.size    # Dimensions de la texture
        u = min(max(u, 0), 1) * (x - 1) # Coordonnée u de la texture (entre 0 et x - 1)
        v = min(max(v, 0), 1) * (y - 1) # Coordonnée v de la texture (entre 0 et y - 1)
        i = min(int(u), x - 2)  # Partie entière de u
        j = min(int(v), y - 2)  # Partie entière de v
        
        u_ratio = u - i        # Partie décimale de u
        v_ratio = v - j       # Partie décimale de v
        u_opposite = 1 - u_ratio    # Partie opposée de u
        v_opposite = 1 - v_ratio    # Partie opposée de v

        p1 = self.texture.getpixel((i, j))  # Pixel en haut à gauche
        p2 = self.texture.getpixel((i + 1, j))  # Pixel en haut à droite
        p3 = self.texture.getpixel((i, j + 1))  # Pixel en bas à gauche
        p4 = self.texture.getpixel((i + 1, j + 1))  # Pixel en bas à droite

        # Interpolation bilinéaire
        if isinstance(p1, int):
            r = (p1*u_opposite + p2*u_ratio)*v_opposite + (p3*u_opposite + p4*u_ratio)*v_ratio
            g = (p1*u_opposite + p2*u_ratio)*v_opposite + (p3*u_opposite + p4*u_ratio)*v_ratio
            b = (p1*u_opposite + p2*u_ratio)*v_opposite + (p3*u_opposite + p4*u_ratio)*v_ratio
        else:
            r = (p1[0]*u_opposite + p2[0]*u_ratio)*v_opposite + (p3[0]*u_opposite + p4[0]*u_ratio)*v_ratio
            g = (p1[1]*u_opposite + p2[1]*u_ratio)*v_opposite + (p3[1]*u_opposite + p4[1]*u_ratio)*v_ratio
            b = (p1[2]*u_opposite + p2[2]*u_ratio)*v_opposite + (p3[2]*u_opposite + p4[2]*u_ratio)*v_ratio
        return lCouleur.Couleur(r / 255, g / 255, b / 255)   # Retourne la couleur normalisée
