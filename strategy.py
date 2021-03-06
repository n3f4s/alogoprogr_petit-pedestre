#!/usr/bin/env python3

import cell
import match
from util import *
from routage import *
from random import *
import logging

"""Module contenant les stratégies
"""


# Initialisation du logging
logger = logging.getLogger("strat_logger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('\n\
=========================================================================\n\
%(name)s - %(levelname)s - %(message)s\n\
=========================================================================\n\
\n')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
_has_FileHandler = False

def strategy(match, strat):
    """Fonction calculant les ordres a donner a un instant t du match

        Argument:
            match :: Match     Match en cour
            strat :: str       Nom de la stratégie a appliquer

        Retour:
            [ {"from" : cell.id, "to" : cell.id, "percent" : int}, ... ] Liste des ordres
    """
    list_strat = {
            "idle"   : idle,
            "base"   : _strat_base,
            "base2"  : _strat_base2,
            "strat3" : _less_worse_strat,
            "strat4" : strat4,
            "strat5" : strat5,
            "strat6" : strat6,
            "random" : random
            }
    return list_strat[strat](match)

def random(match):
        orders=[]
        our_cells = [ c for c in match.cells.values() if is_ally(match, c) ]
        cell = our_cells[randint(0,len(our_cells)-1)]
        neighbour_list = [ match.cells[id_] for id_ in cell.links.keys()]
        neighbour = neighbour_list [randint(0,len(neighbour_list)-1)]
        orders.append({"from": cell.id, "to": neighbour.id, "percent": 100})
        return orders




       
def _strat_base(match):
    """Strat de base : atttaque l'enemi adjacent le plus faible ou aide l'allie adjacent le plus faible
    """
    orders = []
    for cell in match.cells.values():
        if cell.owner == match.me:
            weakest = weakest_neighbour_foe(cell, match) or weakest_neighbour_friend(cell, match)
            orders.append({"from": cell.id, "to": weakest.id, "percent": 50})
    return orders

def _strat_base2(match):
    """Strat de base ameliore

    N'attaque que si il n'y a pas de mouvement vers la cible ou si les unites attaquants la cible sont a plus de la moitie du trajet.
    Si la cible est allie et qu'elle envoie des unites, alors on ne lui envoie rien
    """
    orders = []
    for cell in match.cells.values():
        if cell.owner == match.me:
            weakest = weakest_neighbour_foe(cell, match)
            if weakest == None:
                weakest = weakest_neighbour_friend(cell, match)
            for mvt in weakest.moves:
                if mvt.owner != cell.owner:
                    if cell.id != mvt.source:
                        orders.append({"from": cell.id, "to": weakest.id, "percent": 50})
                    elif time_remaining_per_cent(match, mvt, weakest)<50:
                        orders.append({"from": cell.id, "to": weakest.id, "percent": 50})
                else:
                    as_incomming = False
                    for mvt in cell.moves:
                        if mvt.source.id == weakest.id:
                            as_incomming = True
                    if not as_incomming and cell.id != mvt.source:
                        orders.append({"from": cell.id, "to": weakest.id, "percent": 50})
                    elif not as_incomming and time_remaining_per_cent(match, mvt, weakest)<50:
                        orders.append({"from": cell.id, "to": weakest.id, "percent": 50})
    return orders

def _less_worse_strat(match):
    """
    """
    our_cells = [ c for c in match.cells.values() if c.owner==match.me ]
    cells_without_order = [ cell for cell in match.cells.values() if cell.owner == match.me ]
    cells_with_order = { cell.id : Action(cell, weakest_neighbour_foe(cell, match) , 50 )\
            for cell in our_cells\
            if weakest_neighbour_foe(cell, match)!=None and not cells_without_order.remove(cell)\
    } 

    while len(cells_without_order) > 0:
        tmp_cell = []
        for cell in cells_without_order:
            target = None
            for id in cells.links.keys():
                if id in cells_with_order.keys():
                    # On cible la cell qui est dans les cell ayant deja un ordre
                    target = id
            if target:
                # Si la cell a une cible, on l'ajoute aux celle avc un ordre
                cells_with_order.update( { cell.id : Action(cell, target, 100) } )
                tmp_cell.append(cell)
        # Suppression des cell auquels on a donner un ordre pendant la boucle
        cells_without_order.pop(tmp_cell)
    return [ act.to_dict() for act in cells_with_order.values() ]


def idle(match):
    """ Ne rien faire (une stratégie d'avenir). """
    return []

def strat4(match):
    cells = list_cell_by_unit_needed(match)
    orders = []
    for cell in cells["our"][:len(cells["our"])//2]:
        tmp = possible_action(match, cell, cells)
        tmp.sort(key=lambda t : t[0])
        unit_to_send = max( 75, to_percent(unit_awating(match, cell), tmp[-1][-1]) )
        orders.append( Action(cell,tmp[-1][-1],unit_to_send) )
        cells_targeted.append(tmp[-1][-1])
    return [ o.to_dict() for o in orders ]


def strat5(match):
        
    for cell in match.cells.values():
        cell.unit_needed = unit_needed(match,cell)
    cell_value_list = [c for c in match.cells.values()]
    cell_value_list.sort(key=lambda c : cell_value(match, c) )
    cell_value_list.reverse()
    our_cells = [ c for c in match.cells.values() if is_ally(match, c) ]
    orders = []
    for cell in our_cells:
        if cell.nb_off>0:
            neighbour_list = [ match.cells[id_] for id_ in cell.links.keys() ]
            neighbour_ally = [ _id for _id in cell.links.keys() if match.cells[_id].owner == match.me and cell_value(match,match.cells[_id]) > cell_value(match,cell)]
            neighbour_foe = [ _id for _id in cell.links.keys() if match.cells[_id].owner != match.me ]
            for c in cell_value_list:
                if c in neighbour_list:
                    if c.owner == match.me and c.nb_off<c.max_off:
                        if cell_value(match,cell)<cell_value(match,c) or (c.unit_needed>cell.unit_needed and cell_value(match,cell)==cell_value(match,c)):
                            if abs(cell.unit_needed) > c.unit_needed and cell_value(match,cell)==cell_value(match,c):
                                orders.append({"from": cell.id, "to": c.id, "percent": to_percent(cell,c.unit_needed)})
                                cell.unit_needed += c.unit_needed
                                c.unit_needed = 0
                            elif len(neighbour_ally)>0:
                                orders.append({"from": cell.id, "to": c.id, "percent": to_percent(cell,cell.nb_off//len(neighbour_ally))})
                                c.unit_needed += cell.nb_off//len(neighbour_ally)
                                cell.unit_needed = 0

                    if c.owner == -1:
                        if len(neighbour_list)==len(neighbour_ally)+1 and len(neighbour_list)>0:
                            orders.append({"from": cell.id, "to": c.id, "percent": to_percent(cell,cell.nb_off)})
                            c.unit_needed += cell.nb_off
                            cell.unit_needed = 0                            
                        if (cell.unit_needed<0 or cell_value(match,cell)<=cell_value(match,c)) and should_i_attack(match,cell,c)> 0:
                            if should_i_attack(match,cell,c)> 0:
                                orders.append({"from": cell.id, "to": c.id, "percent": to_percent(cell,should_i_attack(match,cell,c))})
                                cell.unit_needed += should_i_attack(match,cell,c)
                                c.unit_needed = 0

                    elif c.owner!=match.me and c.owner != -1:
                        if cell.unit_needed<0 or cell_value(match,cell)<=cell_value(match,c) or len(neighbour_foe) == 1 :
                            if cell.nb_off >= unit_to_send(match,cell,c):
                                orders.append({"from": cell.id, "to": c.id, "percent": to_percent(cell,unit_to_send(match,cell,c))})
                                cell.unit_needed += unit_to_send(match,cell,c)
                            elif cell.nb_off < unit_to_send(match,cell,c) and len(neighbour_foe)>0:
                                orders.append({"from": cell.id, "to": c.id, "percent": to_percent(cell,cell.nb_off//len(neighbour_foe))})
                                cell.unit_needed += cell.nb_off//len(neighbour_foe)
    return orders


def strat6(match):
    global logger
    global _has_FileHandler
    global ROUTES

    if not _has_FileHandler:
        _has_FileHandler = True
        fh = logging.FileHandler("test.log".format(), "w")
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
    # Construction des routes
    if  ROUTES.get('NotEmpty'):
        ROUTES.clear()
        logger.debug("strat6 - Building routes")
        build_route_table(match)

    # Listage des cibles
    logger.debug("strat6 - Listing target")
    targets = list_targets(match)
    logger.debug("strat6 - targets : {}".format(targets) )
    logger.debug("strat6 - Listing our cells")
    our_cells = [ c for c in match.cells.values() if c.owner==match.me ]
    # si il y a plus de cible alliée que de cible, on calcul le nombre
    # de cellule qui attaquerons une cell enemie
    nb_targets = len(targets)#len(our_cells)//len(targets)
    #if len(our_cells) > len(targets) or nb_targets<=0:
    #    nb_targets = 1
    logger.debug( "strat6 - Setting {} target(s) by cell".format(nb_targets) )
    target = 0
    
    # Attaque des cibles
    orders = []
    for ind, cell in enumerate(our_cells):
#        if target<=nb_targets and target<len(targets):
#            target = target+1
#        else:
#            target=0
#        target = ind%len(targets)#TODO faire une fonction qui renvoie la plus proche parmi une liste de cell
        target = nearest_target(ind, targets)
        logger.debug( "Targeting cell {}".format( match.cells[target].id ) )
        tmp_target = next_jump_to_target(cell.id, target ) # Fonction qui renvoie le saut suivant pour arriver à la cible avec la distance la plsu courte
        #routes[our_cells].routes[targets[target]].next_jump
        units = max(unit_to_send_(match, cell, match.cells[tmp_target]), 100)
        units = 75#PATCH IMMONDE
        logger.debug( "Sending {} unit(s)".format(units) )
        orders.append( Action(cell, tmp_target, units) )
        logger.debug( "Sending order : {}".format(orders[-1]) )
    return [ o.to_dict() for o in orders ]

if __name__ == "__main__":
    print("Look like there is no syntax error !")
