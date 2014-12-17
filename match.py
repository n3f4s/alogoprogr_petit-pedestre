from cell import Cell

class Match:
    def __init__(self, init):
        self.id = init['matchid']
        self.cells = {cell['cellid']: Cell(cell) for cell in init['cells']}
        self.nb_players = init['nb_players']
        self.me = init['id_us']
        self.speed = init['speed']
        # TODO : lines

    def update(self, state):
        # TODO : moves
        for cell in state['cells']:
            self.cells[cell['cellid']].update(cell)

    def compute_strategy(self):
        pass
