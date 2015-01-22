#!/usr/bin/env python3

import cell
import match
import util

"""Module contenant les stratégies
"""

def strategy(match, strat):
	"""Fonction calculant les ordres à donner à un instant t du match

		Argument:
			match :: Match												Match en cour
			strat :: str												Nom de la stratégie à appliquer

		Retour:
			[ {"from" : cell.id, "to" : cell.id, "percent" : int}, ... ] Liste des ordres
	"""
	list_strat = {
			"idle"	 : idle
			"base"   : _strat_base,
			"base2"  : _strat_base2,
			"strat3" : _less_worse_strat
			}
	return list_strat[strat](match)

def _strat_base(match):
	"""Strat de base : atttaque l'enemi adjacent le plus faible ou aide l'allié adjacent le plus faible
	"""
	orders = []
	for cell in match.cells:
		if cell.owner == match.me:
			weakest = weakest_neighbour_foe(cell, match) or weakest_neighbour_friend(cell, match)
			orders.append({"from": cell.id, "to": weakest.id, "percent": 50})
	return orders

def _strat_base2(match):
	"""Strat de base amélioré

	N'attaque que si il n'y a pas de mouvement vers la cible ou si les unités attaquants la cible sont à plus de la moitié du trajet.
	Si la cible est allié et qu'elle envoie des unités, alors on ne lui envoie rien
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
			for cell in our_cells\
			if weakest_neighbour_foe(cell, match)!=None and not cells_without_order.remove(cell)\
	} # OK, un peut dégeu mais bon

	while len(cells_without_order) > 0:
		tmp_cell = []
		for cell in cells_without_order:
			target = None
			for id in cells.links.keys():
				if id in cells_with_order.keys():
					# On cible la cell qui est dans les cell ayant déjà un ordre
					target = id
			if target:
				# Si la cell à une cible, on l'ajoute aux celle avc un ordre
				cells_with_order.update( { cell.id : Action(cell, target, 100) } )
				tmp_cell.append(cell)
		# Suppression des cell auquels on a donner un ordre pandant la boucle
		cells_without_order.pop(tmp_cell)
	return [ act.to_dict() for act in cells_with_order.values() ]


def idle(match):
    """ Ne rien faire (une stratégie d'avenir). """
    return []

def strat4(match):
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
	cells_targeted = []
	orders = []
	for cell in our_cells[:len(our_cells)//2]:
		tmp = []
		for neighbour_id in cell.links.keys():
			neighbour_cell = match.cells[neighbour_id]
			if neighbour_cell not in cells_targeted:
				if neighbour_cell in foe_cells[:len(foe_cells)//2]:
					tmp.append( (
								unit_needed(
									neighbour_cell,
									lambda c : c.owner!=-1 and c.owner!=me
									) ),
								neighbour_cell
								)
				elif neighbour_cell in neutral_cells[:len(neutral_cells)//2]:
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
		tmp.sort(key=lambda t : t[0])
		orders.append( Action(cell,tmp[-1][-1],50) )# Faire un calcul pour le pourcentage à envoyer ??
		cells_targeted.append(tmp[-1][-1])
	return [ o.to_dict() for o in orders ]



	for cell in foe_cells:
		for neighbour_id in cell.links.keys:
			neighbour_cell = match.cells[neighbour_id]
			if neighbour_cell.owner == match.me and neighbour_id not in cells_with_order and neighbour_cell not in our_cells[len(our_cells)//2:]:
				cells_with_order.append(neighbour)
				orders.append( Action(neighbour, cell, 50))








