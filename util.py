#!/usr/bin/env python3

from cell  import *
from match import *
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
		self.src = 0  				#cell id
		if isinstance(src, int):
			self.src = src
		elif isinstance(src, Cell):
			self.src = src.id
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
	return match.me == cell.owner

def unit_needed(match, cell):
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
		c_val = match.cells[c]
		if not c_val.owner!=cell.owner:
			nb_unit += c_val.nb_off
	for m in cell.moves:
		if m.owner == match.me:
			nb_unit -= m.nb_units
		else:
			nb_unit += m.nb_units
	return nb_unit - ( cell.nb_off +nb_def )

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
	"""Fonction convertissant un nombre d'unité en pourcentage du nombre d'unité max de la cellule envoyant les unités
	Arguments:
		cell :: Cell Cellule envoyant les unitées
		unit :: Int  Nombre d'unitées à envoyer
	Retour:
		Int          Nombre a envoyer en pourcentage du nombre d'unité maximum de la cellule
	"""
	return (units*100)/cell.max_off

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
		return unit_needed(cell, is_ally(match, cell) )
	else:
		return cell.max_off + Cell.max_def

def distance_to_nearest_enemy(match,cell):
	dist = 0
	for c in match.cell:
		if c.owner != match.me and c.owner != -1:
			if distance(cell,c,match) < dist:
				dist = distance(cell,c,match)
	return dist

def cell_value(match,cell):
	value = 0
	if cell.owner == match.me:
		value = cell.speed_prod-distance_to_nearest_enemy(match,cell)
	else:
		value = cell.speed_prod-1
	return value

def should_i_attack(match,source,target):
	attack = True
	for c in target.link:
		if not is_ally(match,c):
			attack = False
		if source.nb_off == source.max_off:
			attack = True
	return attack

def unit_to_send_(match, src, target):
	units = 0
	if target.owner == match.me:
		units = unit_to_send_ally(match, src, target) 
	elif target.owner == -1:
		units = unit_to_send_neutral(match, src, target) 
	else:
		units = unit_to_send_foe(match, src, target) 
	return units

def unit_to_send_ally(match, src, target):
	src_val = match.cells[src]
	target_val = match.cells[src]
	return min( to_percent(target_val, unit_awating(match, target_val)), 75 )

def unit_to_send_neutral(match, src, target):
	src_val = match.cells[src]
	target_val = match.cells[src]
	unit_sum = target_val.max_def + target_val.max_def
	for neighbour in match.cells[target].links.keys():
		if neighbour != src:
			if match.cells[neighbour].owner == me:
				unit_sum -= match.cells[neighbour].nb_off
			elif match.cells[neighbour].owner != me and match.cells[neighbour].owner != -1:
				unit_sum += match.cells[neighbour].nb_off
	if unit_sum < 0: # Faire verif des déplacements en cour ??
		return 50
	elif unit_sum - src_val.nb_off <= 0:
	# Sinon verifier qu'il y ait assez avec nous
		return 75
	else:
	# Sinon rien envoyer
		return 0

def unit_to_send_foe(match, src, target):
	src_val = match.cells[src]
	target_val = match.cells[src]
	sum_mvt = 0
	for move in src_val.moves:
		if move.owner == me:
			sum_mvt += move.nb_unit
		else:
			sum_mvt -= move.nb_unit
	superiority = (src_val.nb_off*src_val.speed_prod)/( (target_val.nb_def+target_val.nb_def)*target_val.speed_prod )
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
	targets = []
	for cell in match.cells.values():
		if cell.owner != match.me:
			is_attackable = False
			for neighbour_id in cell.links.keys():
				if match.cells[neighbour_id].owner == match.me:
					is_attackable = True
			if is_attackable:
				targets.append(cell.id)
	return targets

def prod(cell):
	prod = 0
	if cell.speed_prod == 1:
		prod = 1/2000
	if cell.speed_prod == 2:
		prod = 1/1500
	if cell.speed_prod == 3:
		prod = 1/1000
	return prod

def unit_to_send(match,source,target):
	return unit_needed(target,match)+ int(source.links(target.id)*prod(target)) + 2
