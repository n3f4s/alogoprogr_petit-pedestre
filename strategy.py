#!/usr/bin/env python3

import cell
import match

def weakest_neighbour_foe(cell, match):
	""" Retourne la cellule enemie adjacente ayant le moins d'unitée défensive
	
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
	""" Retourne la cellule allie adjacente ayant le moins d'unitée défensive
	
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

def distance(begin, end, match, _visited=None):
	"""retourne la distance mimimale entre begin et end
	
	"""
	if not _visited:
		_visited = set()
	if begin == end:
		return 0
	else:
		dist_min=float("inf")
		for id, dist in cell.links.items():
			tmp = match.cells[id]
			if tmp not in _visited:
				_visited.add(tmp)
				dist_tmp = dist+distance(tmp, end, match, _visited)
				if dist_tmp < dist_min:
					dist_min=dist_tmp
		return dist_min

def strategy(match, strat):
	list_strat = {
			"base" : _strat_base,
			"base2" : _strat_base2
			}
	return list_strat[strat](match)

def _strat_base(match):
	orders = []
	for cell in match.cells:
		if cell.owner == match.me:
			weakest = weakest_neighbour_foe(cell, match) or weakest_neighbour_friend(cell, match)
			orders.append({"from": cell.id, "to": weakest.id, "percent": 50})
	return orders


def _strat_base2(match):
	orders = []
	for cell in match.cells:
		if cell.owner == match.me:
			weakest = weakest_neighbour_foe(cell, match)
			if weakest == None:
				weakest = weakest_neighbour_friend(cell, match)
			if #si elles sont pas ds les mv
			orders.append({"from": cell.id, "to": weakest.id, "percent": 50})
	return orders

