import numpy as np
import Vecteur3D as lVecteur
import Couleur as lCouleur


class Scene:
    '''
    Classe pour les scènes
        dimensions : tuple (largeur, hauteur)
        objets : list[Objet3D]
        lumiere : list[Lumiere]
        camera : Camera
        ambient : float (entre 0 et 1)
        profondeur_max : int
    '''
    def __init__(self, dimensions, objets, lumieres, camera, ambiante, profondeur_max):
        self.dimensions = dimensions
        self.objets = objets
        self.lumieres = lumieres
        self.camera = camera
        self.ambiante = ambiante
        self.profondeur_max = profondeur_max

    def ajouter_objet(self, objet):
        '''
        Ajout d'un objet à la scène
        '''
        self.objets.append(objet)

    def ajouter_lumiere(self, lumiere):
        '''
        Ajout d'une lumière à la scène
        '''
        self.lumieres.append(lumiere)

    def intersect(self, rayO, rayD, objet):
        '''
        Calcul de l'intersection entre un rayon et un objet
            rayO : Vecteur3D (origine du rayon)
            rayD : Vecteur3D (direction du rayon)
            objet : Objet3D
        Retourne la distance entre l'origine du rayon et le point d'intersection
        '''
        return objet.intersection(rayO, rayD)

    def get_color(self, objet, M):
        '''
        Calcul de la couleur d'un objet
            objet : Objet3D
            M : Vecteur3D (point d'intersection)
        Retourne la couleur de l'objet
        '''
        couleur = objet.couleur
        if isinstance(couleur, lCouleur.Couleur):    # Si la couleur est une couleur
            return couleur
        elif callable(couleur):             # Si la couleur est une fonction
            return couleur(M)
        
    def intersection_plus_proche(self, rayO, rayD):
        '''
        Calcul de l'intersection la plus proche entre un rayon et un objet
            rayO : Vecteur3D (origine du rayon)
            rayD : Vecteur3D (direction du rayon)
        Retourne la distance entre l'origine du rayon et le point d'intersection et l'indice de l'objet intersecté
        '''
        t = np.inf
        obj_idx = 0
        for i, objet in enumerate(self.objets): # Pour chaque objet de la scène
            t_obj = self.intersect(rayO, rayD, objet)   # Calcul de l'intersection entre le rayon et l'objet
            if t_obj < t:   # Si la distance est inférieure à la distance minimale
                t, obj_idx = t_obj, i   # Mise à jour de la distance minimale et de l'indice de l'objet
        return t, obj_idx
    
    def illumination(self, M, N, couleur, objet, O, obj_idx):
        '''
        Calcul de l'illumination d'un objet
            M : Vecteur3D (point d'intersection)
            N : Vecteur3D (normale)
            couleur : Couleur
            objet : Objet3D
            O : Vecteur3D (direction du rayon)
            obj_idx : int (indice de l'objet)
        Retourne la couleur de l'objet
        '''
        col_ray = lCouleur.Couleur(self.ambiante, self.ambiante, self.ambiante)  # Couleur du rayon (couleur ambiante)
        for lumiere in self.lumieres:   # Pour chaque lumière de la scène (on ne travaille qu'avec une seule lumière pour l'instant)
            L = (lumiere.position.soustraction(M)).normalisation()  # Direction de la lumière
            l = [self.intersect(M.addition(N.multiplication(0.000001)), L, obj) for k, obj in enumerate(self.objets) if k != obj_idx]   # Intersection entre le point d'intersection et la lumière
            if l and min(l) < np.inf:   # Si l'intersection est plus proche que la lumière
                intensite_ombre = 0.3   # Intensité de l'ombre
                couleur = couleur.multiplication(intensite_ombre)  # Couleur de l'ombre
            l_diffus = max(N.prod_scal(L), 0)   # Coefficient de diffusion
            if isinstance(couleur, tuple):  # Si la couleur est un tuple
                col_ray = col_ray.addition(lCouleur.Couleur(*[l_diffus * c for c in couleur]))   # Ajout de la couleur du rayon à la couleur ambiante
            else:
                col_ray = col_ray.addition(couleur.multiplication(l_diffus * objet.diffuse_c))  # Ajout de la couleur du rayon à la couleur ambiante
            col_ray = col_ray.addition(lumiere.couleur.multiplication(l_diffus * objet.specular_c * max(N.prod_scal((L.addition(O)).normalisation()), 0) ** 100))   # Ajout de la couleur spéculaire du rayon à la couleur ambiante
        return col_ray

    def rayon_trace(self, rayO, rayD):
        '''
        Calcul du rayon de trace
            rayO : Vecteur3D (origine du rayon)
            rayD : Vecteur3D (direction du rayon)
        Retourne l'objet intersecté, le point d'intersection, la normale et la couleur du rayon
        '''
        t, obj_idx = self.intersection_plus_proche(rayO, rayD)  # Calcul de l'intersection la plus proche
        if t == np.inf: # Si pas d'intersection
            return None
        objet = self.objets[obj_idx]    # Objet intersecté
        M = rayO.addition(rayD.multiplication(t))   # Point d'intersection
        N = objet.normale(M)    # Normale
        if hasattr(objet, 'texture'):   # Si l'objet a une texture, on utilise la couleur de la texture
            couleur = objet.couleur_texture(M)
        else:
            couleur = self.get_color(objet, M)  # Sinon, on utilise la couleur de l'objet
        O = (self.camera.position.soustraction(M)).normalisation()  # Direction du rayon
        col_ray = self.illumination(M, N, couleur, objet, O, obj_idx)   # Couleur du rayon
            
        return objet, M, N, col_ray # Objet intersecté, point d'intersection, normale et couleur
    
    def couleur_pixel(self, x, y):
        '''
        Calcul de la couleur d'un pixel
            x : float
            y : float
        Retourne la couleur du pixel
        '''
        col = lCouleur.Couleur(0, 0, 0)  # Couleur du pixel
        Q = lVecteur.Vecteur3D(x, y, -self.camera.distance_focale)  # Coordonnées du pixel
        D = (Q.soustraction(self.camera.position)).normalisation()   # Direction du rayon en utilisant la position de la caméra ()
        profondeur = 0
        rayO, rayD = self.camera.position, D    # RayO : origine du rayon, RayD : direction du rayon
        reflection = 1                        # Réflexion du rayon (1 = pas de réflexion)
        continu = True
        while profondeur < self.profondeur_max and continu: # Tant que la profondeur est inférieure à la profondeur maximale
            trace = self.rayon_trace(rayO, rayD)    # Calcul du rayon de trace (objet intersecté, point d'intersection, normale et couleur)
            if not trace:   # Si pas d'intersection
                continu = False    # Arrêt de la boucle car pas d'objet intersecté donc inutile de continuer
            else:
                objet, M, N, col_ray = trace    # Objet intersecté, point d'intersection, normale et couleur
                rayO, rayD = M.addition(N.multiplication(0.0001)), rayD.soustraction(N.multiplication(2 * N.prod_scal(rayD))) # Réflexion du rayon
                profondeur += 1
                col = col.addition(col_ray.multiplication(reflection))  # Ajout de la couleur du rayon à la couleur du pixel
                reflection *= objet.reflection  # Réflexion de l'objet
        return col

    def construire_image(self):
        '''
        Construction de l'image
        Retourne l'image de la scène
        '''
        largeur, hauteur = self.dimensions  # Dimensions de l'image
        coords_ecran = (-largeur / hauteur, -1, largeur / hauteur, 1)   # Coordonnées de l'écran de la caméra (normalisé)
        img = np.zeros((hauteur, largeur, 3))                        # Image de la scène
        # i et j sont les indices des pixels de l'image, x et y sont les coordonnées des pixels de l'écran (pour envoyer un rayon à travers chaque pixel de l'écran)
        for i, x in enumerate(np.linspace(coords_ecran[0], coords_ecran[2], largeur)):  # Pour chaque pixel de l'image (en x) np.linspace est utilisé pour obtenir un nombre de pixels égal à la largeur
            for j, y in enumerate(np.linspace(coords_ecran[1], coords_ecran[3], hauteur)):  # Pour chaque pixel de l'image (en y)
                col = self.couleur_pixel(x, y)  # Calcul de la couleur du pixel
                img[hauteur - j - 1, i, :] = np.clip(col.to_numpy(), 0, 1)  # Ajout de la couleur du pixel à l'image (inversion verticale)
        return img
