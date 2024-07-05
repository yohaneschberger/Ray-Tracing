import numpy as np
import Objet3D as lObjet
import Couleur as lCouleur


class Sphere(lObjet.Objet3D):
    '''
    Classe pour les sphères
        Parametres OBJET3D
        rayon : float
        n : float (indice de réfraction)
    '''
    def __init__(self, position, rayon, couleur, diffuse, specular, reflection, texture = None):
        super().__init__(position, couleur, diffuse, specular, reflection)
        self.rayon = rayon
        self.texture = texture
        
    def intersection(self, rayO, rayD):
        '''
        Calcul de l'intersection entre un rayon et une sphère
            rayO : Vecteur3D (origine du rayon)
            rayD : Vecteur3D (direction du rayon)
            a = 1 car rayD est normalisé (norme = 1) pas besoin de multiplier par a
        Retourne la distance entre l'origine du rayon et le point d'intersection
        '''
        OS = rayO.soustraction(self.position)                                        # Vecteur entre l'origine du rayon et le centre de la sphère
        b = 2 * rayD.prod_scal(OS)                                                # Coefficient du terme en t dans l'équation du second degré
        c = OS.prod_scal(OS) - self.rayon * self.rayon                            # Coefficient du terme constant dans l'équation du second degré
        delta = b * b - 4 * c                                               # Discriminant de l'équation du second degré (a = 1 car rayD est normalisé)
        if delta > 0:
            racine_delta = np.sqrt(delta)
            t1 = (-b - racine_delta) / 2
            t2 = (-b + racine_delta) / 2
            if t1 > 0:
                return t1
            elif t2 > 0:
                return t2
        elif delta == 0:
            return -b / 2
        return np.inf
    
    def normale(self, M):
        '''
        Calcul de la normal d'un point sur la sphère
            M : Vecteur3D (point d'intersection)
        Retourne la normale
        '''
        return (M.soustraction(self.position)).normalisation()

    def couleur_texture(self, M):
        '''
        Calcul de la couleur d'un point sur la sphère (en utilisant la bilinéarisation pour rendre la texture plus réaliste)
            M : Vecteur3D (point d'intersection)
        Retourne la couleur du point
        '''
        if self.texture is None:    # Si pas de texture définie, on retourne la couleur de la sphère
            return self.couleur

        M = M.soustraction(self.position).normalisation()   # Normalisation du point d'intersection par rapport au centre de la sphère

        angle_rotation = np.pi / 4  # Angle de rotation pour la texture (45° pour que la texture soit bien orientée) source Internet

        u = (0.5 + np.arctan2(M.z, M.x) + angle_rotation) / (2 * np.pi) # Coordonnée u de la texture
        v = 0.5 - np.arcsin(M.y) / np.pi                            # Coordonnée v de la texture

        x, y = self.texture.size    # Dimensions de la texture
        u = min(max(u, 0), 1) * (x - 1) # Coordonnée u de la texture (entre 0 et x - 1)
        v = min(max(v, 0), 1) * (y - 1) # Coordonnée v de la texture (entre 0 et y - 1)
        i = min(int(u), x - 2)  # Partie entière de u
        j = min(int(v), y - 2)  # Partie entière de v
        u_ratio = u - i        # Partie décimale de u
        v_ratio = v - j       # Partie décimale de v
        u_oppose = 1 - u_ratio    # Partie opposée de u
        v_oppose = 1 - v_ratio    # Partie opposée de v

        p1 = self.texture.getpixel((i, j))  # Pixel en haut à gauche
        p2 = self.texture.getpixel((i + 1, j))  # Pixel en haut à droite
        p3 = self.texture.getpixel((i, j + 1))  # Pixel en bas à gauche
        p4 = self.texture.getpixel((i + 1, j + 1))  # Pixel en bas à droite

        # Interpolation bilinéaire
        r = (p1[0]*u_oppose + p2[0]*u_ratio)*v_oppose + (p3[0]*u_oppose + p4[0]*u_ratio)*v_ratio  # Couleur rouge
        g = (p1[1]*u_oppose + p2[1]*u_ratio)*v_oppose + (p3[1]*u_oppose + p4[1]*u_ratio)*v_ratio  # Couleur verte
        b = (p1[2]*u_oppose + p2[2]*u_ratio)*v_oppose + (p3[2]*u_oppose + p4[2]*u_ratio)*v_ratio  # Couleur bleue

        return lCouleur.Couleur(r / 255, g / 255, b / 255)   # Retourne la couleur normalisée
