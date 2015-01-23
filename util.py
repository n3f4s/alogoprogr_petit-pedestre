#!/usr/bin/env python3

import cell
import match

"""Module contenant les fonctions nécéssaires au calcul des stratégies
"""

def weakest_neighbour_foe(cell, match):
	""" Retourne la cellule enemie adjacente ayant le moins d'unitée défensive
	
	Argument : 
		cell	:: Cell 	Objet Cell pour lequel on veut la cellule enemie
		match	:: Match	Match en cours

	Retour:
		Cell ou None		cellule enemie adjacente ayant le moins d'unitée défensive ( ou None si la cellule passée en paramêtre n'a pas de cellule enemie adjacente)
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
		cell	:: Cell 	Objet Cell pour lequel on veut la cellule enemie
		match	:: Match	Match en cours

	Retour:
		Cell ou None		cellule enemie adjacente ayant le moins d'unitée défensive ( ou None si la cellule passée en paramètre n'a pas de cellule alliée adjacente)
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

	Argument:
		begin	:: Cell 	Cellule à partir de laquelle il faut calculer la distance
		end		:: Cell		Cellule jusqu'à laquelle il faut calculer la distance
		match	:: Match	Match en cours

	Retour:
		Int					Distance minimale entre les cellules (en nombre de saut) begin et end
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


def time_remaining_per_cent(match, mvt, dest):
	"""Fonction retournant le temps restant à un groupe d'unité pour arriver à la cible en pourcentage du temps maximum de trajet

	Argument:
		match 	:: Match 	Match en cours
		mvt 	:: Movement Mouvement dont il faut calculer le temps restant pour arriver à ça cible
		dest 	:: Cell 	Cellule cible des unités en mouvement
	
	Retour:
		Int 				Temps restant (en pourcentage) aux unités pour arriver à leurs cible
	"""
	total_time = match.cells[mvt.source].links[dest.id]
	return (mvt.time_remaining/total_time)*100

class Action:
	"""Classe servant à faciliter l'envoi d'ordre
	"""
	def __init__(self, src, dest, percent_unit):
		"""Constructeur de la classe Action
		Argument:
			src			 :: int ou Cell	Source du mouvement
			dest		 :: int ou Cell	Destination du mouvement
			percent_unit :: int			pourcentage d'unité à envoyer
		"""
		self.dest = 0  				#cell id
		if isinstance(dest, int):
			self.dest = dest
		elif isinstance(dest, Cell):
			self.dest = dest.id
		self.dest = 0  				#cell id
		if isinstance(dest, int):
			self.dest = dest
		elif isinstance(dest, Cell):
			self.dest = dest.id
		self.units_sent = percent_unit 	# nombre d'unité à envoyer

	def to_dict(self):
		"""Fonction renvoyant le mouvement sous forme d'un dictionnaire

		Retour:
			[ {"from" : cell.id, "to" : cell.id, "percent" : int}, ... ] Liste des ordres
		"""
		return { 'from':self.src , 'to':self.dest, 'percent':self.units_sent}

def is_ally(match, cell):
	"""Fonction renvoyant vrai si la cellule appartient au joueur

	Argument:
		match	:: Match	Match en cour
		cell	:: Cell		Cellule dont on doit verifier si elle nous appatient
	Retour:
		Bool				True si la cellule appartient au joueur, False sinon
	"""
	return me == cell.owner

def unit_needed(cell, mine):
	"""Fonction renvoyant le nombre d'unité que la cellule à besoin

	Cette fonction calcul la "menace" de la cellule en ajoutant le nombre d'unité enemis en déplacements vers cette cellule ainsi que les unité offensives des cellules enemies adjacentes et soustrait le nombre d'unité offensive des unités alliés adjacentes ainsi que le nombre d'unité des déplacement alliés vers cette cellule

	Argument:
		cell :: Cell		Cellule pour laquelle il faut calculer la "menace"
		mine :: Function	Fonction renvoyant vrai si la cellule appartient au propriétaire de la cellule cell
	
	Retour
		Int					"Menace" calculé selon le calcul ci-desssus
	"""
	nb_unit = 0
	for c in cell.links.keys():
		if not mine(c.owner):
			nb_unit += c.nb_off
	for m in cell.moves:
		if mine(m.owner):
			nb_unit -= m.nb_units
		else:
			nb_unit += m.nb_units
	return nb_unit - ( cell.nb_off +nb_def )

def neighbour_foe(match, cell):
	return [ c for c in cell.links if not is_ally(match, cell) ]

def list_cell_by_unit_needed(match):
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
	tmp = []
	for neighbour_id in cell.links.keys():
		neighbour_cell = match.cells[neighbour_id]
		if neighbour_cell not in cells_targeted:
			if neighbour_cell in cells["foe"][:len(cells["foe"])//2]:
				tmp.append( (
					unit_needed(
						neighbour_cell,
						lambda c : c.owner!=-1 and c.owner!=me
						) ),
					neighbour_cell
					)
			elif neighbour_cell in cells["neutral"][:len(cells["neutral"])//2]:
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
	return (units*100)/cell.max_off

def unit_awating(match, cell):
	if cell.owner == match.me:
		return unit_needed(cell, is_ally(match, cell) )
	else:
		return cell.max_off + Cell.max_def

def distance_to_nearest_enemy(match,cell):
	dist = 0
	for c in match.cell:
		if c.owner != match.me and c.owner != -1:
			if distance(cell,c,match) < dist:
				dist = distance(cell,c,match)
	return dist # C'est ça qu'il faut retourner ??

def cell_value(match,cell):
	value = 0 # Porté des variables !!!!
	if cell.owner == match.me:
		value = cell.speed_prod-distance_to_nearest_enemy(match,cell)
	else:
		value = cell.speed_prod-1
	return value # ??
