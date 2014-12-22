class Movement:
    """ Modélise un mouvement vers une cellule.

    Chaque planète stocke la liste des mouvements qui la ciblent.

    Attributs:
        nb_units :: int         Nombre d'unités en déplacement
        owner :: int            Joueur possédant ces unités
        source :: int           Planète source
        time_remaining :: int   Temps restant avant arrivée des unités
    """

    def __init__(self, data, links):
        self.nb_units = data['units']
        self.owner = data['owner']
        self.source = data['from']
        self.time_remaining = links[self.source] - data['timestamp']
