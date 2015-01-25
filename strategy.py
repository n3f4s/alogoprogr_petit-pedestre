#!/usr/bin/env python3

import cell
import match
from util import *
from routage import *
from random import *

"""Module contenant les stratégies
"""


def strategy(match, strat):
	"""Fonction calculant les ordres a donner a un instant t du match

		Argument:
			match :: Match												Match en cour
			strat :: str												Nom de la stratégie a appliquer

		Retour:
			[ {"from" : cell.id, "to" : cell.id, "percent" : int}, ... ] Liste des ordres
	"""
	list_strat = {
			"idle"	 : idle,
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
	} # OK, un peut degeu mais bon

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
                neighbour_list = [ match.cells[id_] for id_ in cell.links.keys() ]
                for c in cell_value_list:
                        if c in neighbour_list:
                                if is_ally(match,c):
                                        if (cell.unit_needed<0 or cell_value(match,cell)<cell_value(match,c)) and c.unit_needed>0:
                                                if abs(cell.unit_needed) > c.unit_needed:
                                                        orders.append({"from": cell.id, "to": c.id, "percent": to_percent(cell,c.unit_needed) })
                                                        cell.unit_needed += c.unit_needed
                                                        c.unit_needed = 0
                                                else:
                                                        orders.append({"from": cell.id, "to": c.id, "percent": to_percent(cell,abs(cell.unit_needed))})
                                                        c.unit_needed += cell.unit_needed
                                                        cell.unit_needed = 0

                                if c.owner == -1:
                                        if cell.nb_off > 0 and should_i_attack(match,cell,c):
                                                if cell.nb_off > c.unit_needed:
                                                        orders.append({"from": cell.id, "to": c.id, "percent": to_percent(cell,c.unit_needed)})
                                                        cell.unit_needed += c.unit_needed
                                                        c.unit_needed = 0
                                                else:
                                                        orders.append({"from": cell.id, "to": c.id, "percent": to_percent(cell,cell.nb_off)})
                                                        c.unit_needed -= cell.nb_off
                                                        cell.unit_needed = 0
                                else:
                                        if cell.unit_needed<0 or cell_value(match,cell)<=cell_value(match,c):
                                                if cell.nb_off > unit_to_send(match,cell,c):
                                                        orders.append({"from": cell.id, "to": c.id, "percent": to_percent(cell,unit_to_send(match,cell,c))})
                                                        cell.unit_needed += unit_to_send(match,cell,c)
                                                        c.unit_needed = 0
        return orders


def strat6(match):
	# Construction des routes
	if not len(ROUTES):
		build_route_table(match)
	
	# Listage des cibles
	targets = list_targets(match)
	our_cells = [ c for c in match.cells.values() if c.owner==match.me ]
	# si il y a plus de cible alliée que de cible, on calcul le nombre
	# de cellule qui attaquerons une cell enemie
	nb_targets = len(our_cells)//len(targets)
	if len(our_cells) > len(targets):
		nb_targets = 1
	target = 0
	
	# Attaque des cibles
	orders = []
	for ind in range(len(our_cells)-1):
		if (ind+1)%nb_targets and target<len(targets)-1:
			target = target+1
		tmp_target = next_jump_to_target(our_cells[ind].id, targets[target] ) # Fonction qui renvoie le saut suivant pour arriver à la cible avec la distance la plsu courte
		#routes[our_cells].routes[targets[target]].next_jump
		units = unit_to_send_(match, our_cells[ind].id, tmp_target) 
		orders.append( Action(our_cells[ind], tmp_target, units) )
		# attaque sans différentiation amis/enemis/neutre ou a mettre dans unit_to_send ???
	return [ o.to_dict() for o in orders ]

if __name__ == "__main__":
	print("Look like there is no syntax error !")
