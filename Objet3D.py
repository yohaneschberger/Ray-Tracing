
class Objet3D:
    '''
    Classe abstraite pour les objets 3D
        position : Vecteur3D
        couleur : Couleur
        diffuse_c : float (coefficient de diffusion)
        specular_c : float (coefficient de spéculaire)
        specular_k : float (exposant du spéculaire)
        reflection : float (coefficient de réflexion)
    '''
    def __init__(self, position, couleur, diffuse, specular, reflection):
        self.position = position
        self.couleur = couleur
        self.diffuse_c = diffuse
        self.specular_c = specular
        self.reflection = reflection


    def intersection(self, rayO, rayD):
        '''
        Calcul de l'intersection entre un rayon et un objet
            rayO : Vecteur3D (origine du rayon)
            rayD : Vecteur3D (direction du rayon)
        '''
        print('Méthode intersection à implémenter')

    def normale(self, M):
        '''
        Calcul de la normale à un point
            M : Vecteur3D (point)
        '''
        print('Méthode normale à implémenter')
