#!/usr/bin/env python3

from cell  import *
from match import *
"""Module contenant les fonctions nécéssaires au calcul des stratégies
"""

def weakest_neighbour_foe(cell, match):
    """ Retourne la cellule enemie adjacente ayant le moins d'unitée défensive
    
    Argument : 
        cell  :: Cell     Objet Cell pour lequel on veut la cellule enemie
        match :: Match    Match en cours

    Retour:
        Cell ou None        cellule enemie adjacente ayant le moins d'unitée défensive ( ou None si la cellule passée en paramêtre n'a pas de cellule enemie adjacente)
    Si il n'y a pas de cellule enemie adjacente la fonction renvoie None
    """
    weakest=None
    for id_ in cell.links:
        if match.cells[id_].owner != cell.owner:
            if weakest!=None and match.cells[id_].nb_def<weakest.nb_def:
                weakest=match.cells[id_]
            elif weakest == None:
                weakest=match.cells[id_]
    return weakest

def weakest_neighbour_friend(cell, match):
    """ Retourne la cellule alliée adjacente ayant le moins d'unitée défensive
    
    Argument : 
        cell  :: Cell     Objet Cell pour lequel on veut la cellule enemie
        match :: Match    Match en cours

    Retour:
        Cell ou None        cellule enemie adjacente ayant le moins d'unitée défensive ( ou None si la cellule passée en paramètre n'a pas de cellule alliée adjacente)
    Si il n'y a pas de cellule enemie adjacente la fonction renvoie None
    """
    weakest=None
    for id_ in cell.links:
        if match.cells[id_].owner == cell.owner:
            if weakest!=None and match.cells[id_].nb_def<weakest.nb_def:
                weakest=match.cells[id_]
            elif weakest == None:
                weakest=match.cells[id_]
    return weakest


def distance(match, begin, end, _visited=None):
    """retourne la distance mimimale entre begin et end

    Argument:
        begin :: Cell     Cellule à partir de laquelle il faut calculer la distance
        end   :: Cell     Cellule jusqu'à laquelle il faut calculer la distance
        match :: Match    Match en cours

    Retour:
        Int               Distance minimale entre les cellules begin et end
    """
    if not _visited:
        _visited = set()
    if begin == end:
        return 0
    else:
        dist_min=float("inf")
        for id, dist in begin.links.items():
            tmp = match.cells[id]
            if tmp not in _visited:
                _visited.add(tmp)
                dist_tmp = 1+distance(match,tmp, end, _visited)
                if dist_tmp < dist_min:
                    dist_min=dist_tmp
        return dist_min
    
def distance2(match,begin,end):
    queue = []
    queue.append(begin)
    visited = {}
    visited[begin]=0
    while len(queue)>0:
        t=queue.pop()
        if t==end:
            return visited[t]
        for _id in t.links.keys():
            u= match.cells[_id]
            if u not in visited.keys():
                visited[u]=visited[t]+1
                queue.append(u)
    return 42
    





def time_remaining_per_cent(match, mvt, dest):
    """Fonction retournant le temps restant à un groupe d'unité pour arriver à la cible en pourcentage du temps maximum de trajet

    Argument:
        match :: Match     Match en cours
        mvt   :: Movement  Mouvement dont il faut calculer le temps restant pour arriver à ça cible
        dest  :: Cell      Cellule cible des unités en mouvement
    
    Retour:
        Int                Temps restant (en pourcentage) aux unités pour arriver à leurs cible
    """
    total_time = match.cells[mvt.source].links[dest.id]
    return (mvt.time_remaining/total_time)*100

class Action:
    """Classe servant à faciliter l'envoi d'ordre
    """
    def __init__(self, src, dest, percent_unit):
        """Constructeur de la classe Action
        Argument:
            src          :: int ou Cell    Source du mouvement
            dest         :: int ou Cell    Destination du mouvement
            percent_unit :: int            pourcentage d'unité à envoyer
        """
        self.src = 0                  #cell id
        if isinstance(src, int):
            self.src = src
        elif isinstance(src, Cell):
            self.src = src.id
        self.dest = 0                  #cell id
        if isinstance(dest, int):
            self.dest = dest
        elif isinstance(dest, Cell):
            self.dest = dest.id
        self.units_sent = percent_unit     # nombre d'unité à envoyer

    def to_dict(self):
        """Fonction renvoyant le mouvement sous forme d'un dictionnaire

        Retour:
            [ {"from" : cell.id, "to" : cell.id, "percent" : int}, ... ] Liste des ordres
        """
        return { 'from':self.src , 'to':self.dest, 'percent':self.units_sent}

    def __format__(self, format_spec):
        return "from{} to:{} percent:{}".format(self.src, self.dest, self.units_sent)

def is_ally(match, cell):
    """Fonction renvoyant vrai si la cellule appartient au joueur

    Argument:
        match   :: Match    Match en cour
        cell    :: Cell     Cellule dont on doit verifier si elle nous appatient
    Retour:
        Bool                True si la cellule appartient au joueur, False sinon
    """
    return match.me == cell.owner

def unit_needed(match, cell):
    """Fonction renvoyant le nombre d'unité que la cellule à besoin

    Cette fonction calcul la "menace" de la cellule en ajoutant le nombre d'unité enemis en déplacements vers cette cellule ainsi que les unité offensives des cellules enemies adjacentes et soustrait le nombre d'unité offensive des unités alliés adjacentes ainsi que le nombre d'unité des déplacement alliés vers cette cellule

    Argument:
        cell :: Cell        Cellule pour laquelle il faut calculer la "menace"
        mine :: Function    Fonction renvoyant vrai si la cellule appartient au propriétaire de la cellule cell
    
    Retour
        Int                 "Menace" calculé selon le calcul ci-desssus
    """
    nb_unit = 0
    for c in cell.links.keys():
        c_val = match.cells[c]
        if not c_val.owner!=cell.owner:
            nb_unit += c_val.nb_off
    for m in cell.moves:
        if m.owner == cell.owner:
            nb_unit -= m.nb_units
        else:
            nb_unit += m.nb_units
    return nb_unit - ( cell.nb_off + cell.nb_def )

def neighbour_foe(match, cell):
    """Fonction renoyant les cellules non alliées adjacente à la cellule passée en paramêtre

    Arguments:
        match :: Match Match en cour
        cell  :: Cell dont on veut connaitre les cellules adjacentes qui ne nous appartiennent pas
    Retour
        [ Cell ] List des cellules adjacentes qui n'appartiennent pas au joueur
    """
    return [ c for c in cell.links if not is_ally(match, cell) ]

def list_cell_by_unit_needed(match):
    """Fonction renvoyant un dictionnaire contenant la liste des cellules enemies, alliées et neutres.

    Argument:
        match :: Match Match en cour
    Retour
        { str : [ Cell ] } dictionnnaire contenant la liste des cellules, de la forme : { "our" : [ cell alliées ], "neutral" : [ cell neutres ], "foe" : [ cells enemies ] }, triées par ordre de danger
    """
    our_cells = []
    foe_cells = []
    neutral_cells = []
    for c in match.cells.values():
        if is_ally(match, c):
            our_cells.append(c)
        elif c.owner == -1:
            neutral_cells.append(c)
        else:
            foe_cells.append(c)
    our_cells.sort(
            key=lambda c : unit_needed( c, is_ally(match,c) )
            )
    
    foe_cells.sort(
            key=lambda c : unit_needed(c, 
                lambda c : c.owner!=-1 and not is_ally(match,c)
                )
            )
    
    neutral_cells.sort(
            key=lambda c : unit_needed(c, lambda c : c.owner!=-1)
            )
    return { "our" : our_cells, "foe" : foe_cells, "neutral" : neutral_cells }

def possible_action(match, cell, cells_targeted):
    """Fonction renvoyant les actions possibles d'une cellule

    Argument:
        match          :: Match             Match en cours
        cell           :: Cell              Cellule pour laquelle on veut lister les actions possibles
        cells_targeted :: { str : Cell }    Liste des cellules formaté comme le retour de unit_needed
    Retour:
        [ (Int,Cell) ]                      Liste de couple (niveau de danger,cellule). Les cellules présentes dans cette listes sont les cellules atteignable par la cellule passée en paramêtre
    """
    tmp = []
    for neighbour_id in cell.links.keys():
        neighbour_cell = match.cells[neighbour_id]
        if neighbour_cell not in cells_targeted:
            if neighbour_cell in cells_targeted["foe"][:len(cell["foe"])//2]:
                tmp.append( (
                    unit_needed(
                        neighbour_cell,
                        lambda c : c.owner!=-1 and c.owner!=me
                        ) ),
                    neighbour_cell
                    )
            elif neighbour_cell in cells_targeted["neutral"][:len(cells["neutral"])//2]:
                tmp.append( (
                    unit_needed(
                        neighbour_cell,
                        lambda c : c.owner==-1
                        ) ),
                    neighbour_cell
                    )
            else:
                tmp.append( (
                    unit_needed(
                        neighbour_cell,
                        lambda c : c.owner!=me
                            ) ),
                        neighbour_cell
                        )
    return tmp

def to_percent(cell, units):
    """Fonction convertissant un nombre d'unité en pourcentage du nombre d'unité max de la cellule envoyant les unités
    Arguments:
        cell :: Cell Cellule envoyant les unitées
        unit :: Int  Nombre d'unitées à envoyer
    Retour:
        Int          Nombre a envoyer en pourcentage du nombre d'unités de la cellule
    """
    val = 0
    if cell.nb_off>0:
        val = int((units*100)/cell.nb_off)
    return val

def unit_awating(match, cell):
    """Fonction renvoyant le nombre d'unité qu'un cellule attend pou être capturée ou aidée

    Si la cellule est une cellule alliée, on lui envoie un nombre d'unité correspondant à son "danger" (cf unit_needed), sinon on envoie le nombre d'unité correspondant au nombre d'unité offensive + defensive de la cellule
    Argument:
        match :: Match Match en cour
        cell  :: Cellule pour laquelle on cherche à calculer le nombre d'unité à envoyer
    Retour:
        Int      Nombre d'unité à envoyer
    """
    if cell.owner == match.me:
        return unit_needed(match, cell )
    else:
        return cell.max_off + Cell.max_def

def distance_to_nearest_enemy(match,cell):
    """Retourne la distance de l'enemi le plus proche de la cellule

    Argument:
        match :: Match  match en cours
        cell  :: Cell   cellule pour laquelle on veut faire le calcul
    Retour:
        Int             Distance à l'enemi le plus proche
    """
    dist = 100000
    for c in match.cells.values():
        d =distance2(match,cell,c)
        if c.owner != match.me and c.owner != -1 and d < dist:
            dist = d
    return dist

def cell_value(match,cell):
    """Fonction calculant la valeur d'une cellule.

    La valeur d'une cellule est calculée ainsi : 
        - Si la cellule appartient au joueur : (vitesse de production) - (distance à l'enemi le plus proche)
        - Si la cellule n'appartient pas au joueur : (vitesse de production)-1
    Argument:
        match :: Match   Match en cour
        cell  :: Cell    Cellule pour laquelle on veut calculer la valeur
    Retour:
        Int              Valeur de la cellule selon le calcule ci-dessus
    """
    value = 0
    if cell.owner == match.me:
        value = 1-distance_to_nearest_enemy(match,cell)
    elif cell.owner == -1:
        value = 1+2.5*cell.speed_prod-distance_to_nearest_enemy(match,cell)
    else:
        value = cell.speed_prod-1
    return value

def should_i_attack(match,source,target):
    """
        Fonction qui permet, pour une cellule neutre, de savoir s'il faut la conquerir ou non:
               - Si il y a une cellule proche, on la laisse faire le premier pas
               - On conquiert la cellule sinon
        Argument:
        match  :: Match   Match en cour
        source :: Cell    Cellule qui veut attaquer
        target :: Cell    Cellule que l'on veut conquerir
    Retour:
            Bool          True si on peut attaquer, False sinon
        
    """
    attack = target.nb_off+target.nb_def+1
    neighbour_list = [ match.cells[id_] for id_ in target.links.keys() ]
    for c in neighbour_list:
        if (c.owner != match.me and c.owner != -1) or source.nb_off<2:
            attack = 0
    if source.nb_off == source.max_off:
        attack = 2
    for move in target.moves:
        if move.owner != match.me:
            attack = move.nb_units + 2
    return attack

def unit_to_send_(match, src, target):
    """Fonction calculant le nombre d'unité à envoyer d'une cellule à une autre.

    Le nombre d'unité à envoyer est calculé par différentes fonction par rapport au propriétaire
    de la cellule

    Arguments:
        match  :: Match  Match en cours
        src    :: Cell   Cellule envoyant les unitées
        target :: Cell   Cellule à laquelle on doit envoyer des unitées

    Retour:
        Int              Nombre d'unités à envoyer.
    """
    units = 0
    if target.owner == match.me:
        units = unit_to_send_ally(match, src, target) 
    elif target.owner == -1:
        units = unit_to_send_neutral(match, src, target) 
    else:
        units = unit_to_send_foe(match, src, target) 
    return max(abs(units),100)

def unit_to_send_ally(match, src, target):
    """Fonction calculant le nombre d'unité à envoyer à une cellule alliée

    Cette fonction renvoie le nombre d'unité calculé par unit_awating
    Argument:
        match  :: Match    Le match en cour
        src    :: Cell     Cellule envoyant les unités
        target :: Cell     Cellule cible
    Retour:
        Int                Nombre d'unité à envoyer en pourcentage du nombre max d'unité offensive
    """
    src_val = src #match.cells[src.id]#TODO Key error ici
    target_val = target # match.cells[target.id]
    return min( to_percent(target_val, unit_awating(match, target_val)), 75 )

def unit_to_send_neutral(match, src, target):
    """Renvoie le nombre d'unité à envoyer à une cellule neutre

    Cette fonction calcule le nombre d'unité qu'il resterais si toutes les
    cellules adjacentes (source exepté) envoyait leurs unités offensive sur
    la cellule neutre puis décide le nobre d'unité à envoyer
    Argument:
        match  :: Match    Le match en cour
        src    :: Cell     Cellule envoyant les unités
        target :: Cell     Cellule cible
    Retour:
        Int                Nombre d'unité à envoyer en pourcentage du nombre max d'unité offensive
    """
    src_val = src #match.cells[src.id]#TODO Key error ici
    target_val = target # match.cells[target.id]
    unit_sum = target_val.max_def + target_val.max_def
    for neighbour in target_val.links.keys():
        if neighbour != src:
            if match.cells[neighbour].owner == match.me:
                unit_sum -= match.cells[neighbour].nb_off
            elif match.cells[neighbour].owner != match.me and match.cells[neighbour].owner != -1:
                unit_sum += match.cells[neighbour].nb_off
    if unit_sum < 0: 
        return 50
    elif unit_sum - src_val.nb_off <= 0:
    # Sinon verifier qu'il y ait assez avec nous
        return 75
    else:
    # Sinon rien envoyer
        return 25

def unit_to_send_foe(match, src, target):
    """Fonction calculant le nombre d'unité à envoyer à une cellule enemie

    Cette fonction calcule la différence d'unité et de vitesse de production entre la cellule attaquante
    et la cible ainsi que le nombre d'unité en mouvement vers la cellule attaquante, puis renvoie le nombre
    d'unité à envoyer
    Argument:
        match  :: Match    Le match en cour
        src    :: Cell     Cellule envoyant les unités
        target :: Cell     Cellule cible
    Retour:
        Int                Nombre d'unité à envoyer en pourcentage du nombre max d'unité offensive
    """
    src_val = src #match.cells[src.id]#TODO Key error ici
    target_val = target # match.cells[target.id]
    sum_mvt = 0
    for move in src_val.moves:
        if move.owner == match.me:
            sum_mvt += move.nb_units
        else:
            sum_mvt -= move.nb_units
    superiority = ( (src_val.nb_off+1)*src_val.speed_prod)/( (target_val.nb_def+target_val.nb_def+1)*target_val.speed_prod )
    if superiority>2:
        return 75
    elif superiority>1 and sum_mvt>0:
        return 75
    elif superiority>1 and sum_mvt<0:
        return 25
    elif superiority<=0 and sum_mvt>0:
        return 25
    else:
        return 0

def list_targets(match):
    """Cette fonction renvoie la liste des cellules n'appartenant pas au joueur et ayant au moins
    une cellule adjacente appartenant au joueur.

    Argument:
        match  :: Match    Le match en cour
    Retour:
        [ Int ]            Liste des ID des cellules étant attaquable
    """
    targets = []
    for cell in match.cells.values():
        if cell.owner != match.me:
            #is_attackable = False
            #for neighbour_id in cell.links.keys():
            #    if match.cells[neighbour_id].owner == match.me:
#                    is_attackable = True
#            if is_attackable:
            if is_on_front(match, cell):
                targets.append(cell.id)
    return targets

def is_on_front(match, cell):
    is_on_front_ = False
    for neighbour_id in cell.links.keys():
        if match.cells[neighbour_id].owner == match.me:
            is_on_front_ = True
    return is_on_front_


def prod(cell):
        """
        Fonction qui donne la production d'une cellule en unité par milisecondes
        Argument:
        cell :: Cell  Cellule dont on veut connaitre la production
    Retout:
            float        
    """
        prod = 0
        if cell.speed_prod == 1:
                prod = 1/2000
        if cell.speed_prod == 2:
                prod = 1/1500
        if cell.speed_prod == 3:
                prod = 1/1000
        return prod

def unit_to_send(match,source,target):
        """
        Fonction qui calcule le nombre d'unités nécéssaires à la conquête d'une cellule enemie en prenant en compte sa production

        Argument:
        match  :: Match   Match en cour
        source :: Cell    Cellule qui attaque
        target :: Cell    Cellule que l'on veut conquerir
    Retour:
            int           Nombre d'unités
        
    """
        return target.nb_off + target.nb_def + int(source.links[target.id]*prod(target)) + 2
