import movement

class Cell:
    def __init__(self, data):
        self.id = data['cellid']
        self.max_off = data['offsize']
        self.max_def = data['defsize']
        self.speed_prod = data['prod'] # TODO à parser ?
        self.nb_off = 0
        self.nb_def = 0
        self.owner = 0
        self.moves = []
        self.links = {}
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
