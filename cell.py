class Cell:
    def __init__(self, data):
        self.id = data['cellid']
        self.max_off = data['offsize']
        self.max_def = data['defsize']
        self.speed_prod = data['prod'] # TODO à parser ?
        self.nb_off = 0
        self.nb_def = 0
        self.owner = None
        self.moves = []
