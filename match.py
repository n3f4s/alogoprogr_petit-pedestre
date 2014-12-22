from cell import Cell
import strategy

class Match:
    """ Modélise un match en cours.

    Attibuts statiques :
        id :: str               L'UUID du match
        cells :: {int: Cell}    Dict associant un id de cellule à l'objet Cell
                                correspondant
        nb_player :: int        Nombre de participants à ce match
        me :: int               Notre id
        speed :: int            Vitesse de jeu
    """

    def __init__(self, init, strat=strategy.dummy):
        self.id = init['matchid']
        self.cells = {cell['cellid']: Cell(cell, init['lines']) for cell in init['cells']}
        self.nb_players = init['nb_players']
        self.me = init['id_us']
        self.speed = init['speed']
        self.strategy = strat

    def update(self, state):
        """ Met à jour les cellules avec le nouvel état."""
        for cell in state['cells']:
            self.cells[cell['cellid']].update(cell, state['moves'])

    def compute_strategy(self):
        """ Renvoie la stratégie à adopter en fonction de l'état courant.

        Retour :
            [{str: int}]    Chaque dictionnaire contient les clés suivantes :
                            'from', 'to', 'percent'. Voir protocol.encode_order
                            pour plus de détails
        """
        return self.strategy(self)
