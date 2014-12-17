from cell import Cell

class Match:
    def __init__(self, init):
        self.id = init['matchid']
        self.cells = {cell['cellid']: Cell(cell, init['lines']) for cell in init['cells']}
        self.nb_players = init['nb_players']
        self.me = init['id_us']
        self.speed = init['speed']

    def update(self, state):
        """ Met à jour les cellules avec le nouvel état."""
        for cell in state['cells']:
            self.cells[cell['cellid']].update(cell, state['moves'])

    def compute_strategy(self):
        pass
