class Camera:
    '''
    Classe pour la caméra
        position : Vecteur3D
        direction : Vecteur3D
    '''
    def __init__(self, position, direction, distance_focale):
        self.position = position
        self.direction = direction
        self.distance_focale = distance_focale
