#!/usr/bin/env python3

import cell
import match
import util

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
			"strat4" : strat4
			}
	return list_strat[strat](match)

def _strat_base(match):
	"""Strat de base : atttaque l'enemi adjacent le plus faible ou aide l'allie adjacent le plus faible
	"""
	orders = []
	for cell in match.cells:
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
	for cell in match.cells:
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
	cells_without_order = [ cell for cell in match.cells.values() if cell.owner == match.me ]
	cells_with_order = { cell.id : Action(cell, weakest_neighbour_foe(cell, match) , 50 )\
			for cell in cells["our"]\
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
		# Suppression des cell auquels on a donner un ordre pandant la boucle
		cells_without_order.pop(tmp_cell)
	return [ act.to_dict() for act in cells_with_order.values() ]


def idle(match):
    """ Ne rien faire (une stratégie d'avenir). """
    return []

def strat4(match):
	cells = list_cell_by_unit_needed(match)
	cells_targeted = []
	orders = []
	for cell in cells["our"][:len(cells["our"])//2]:
		tmp = possible_action(match, cell, cells_targeted)
		tmp.sort(key=lambda t : t[0])
		unit_to_send = max( 75, to_percent(unit_awating(match, cell), tmp[-1][-1]) )
		orders.append( Action(cell,tmp[-1][-1],50) )# Faire un calcul pour le pourcentage a envoyer ??
		cells_targeted.append(tmp[-1][-1])
	return [ o.to_dict() for o in orders ]

if __name__ == "__main__":
	print("Look like there is no syntax error !")
