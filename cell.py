import movement

class Cell:
    """ Modélise une planète.

    Attibuts statiques :
        id :: int           L'id de la planète
        max_off :: int      Le nombre maximum d'unités offensives sur la planète
        max_def :: int      Le nombre maximum d'unités défensives sur la planète
        speed_prod :: str   La vitesse de production (non parsée)
        links :: {int: int} Dict associant une planète voisine à la distance qui
                            la sépare

    Attibuts dynamiques :
        owner :: int        L'id du joueur possédant la planète
        nb_off :: int       Nombre d'unités offensives sur la planète
        nb_def :: int       Nombre d'unités défensives sur la planète
        moves :: [Movement] Liste des mouvements d'unités vers la planète
    """

    def __init__(self, data, links):
        """ Initialise la cellule à l'aide du dict post-parsing."""
        self.id = data['cellid']
        self.max_off = data['offsize']
        self.max_def = data['defsize']
        self.speed_prod = len(data['prod'])
        self.nb_off = 0
        self.nb_def = 0
        self.owner = 0
        self.moves = []
        self.links = {}
        self.x = data['x']
        self.y = data['y']
        self.radius = data['radius']
        self.unit_needed = 0
        for link in links:
            if link['cellid1'] == self.id:
                self.links[link['cellid2']] = link['dist']
            elif link['cellid2'] == self.id:
                self.links[link['cellid1']] = link['dist']

    def update(self, state, moves):
        """ Met à jour les données dynamiques de la cellule."""
        self.owner = state['owner']
        self.nb_def = state['defunit']
        self.nb_off = state['offunit']
        self.moves = [movement.Movement(move, self.links) for move in moves]
