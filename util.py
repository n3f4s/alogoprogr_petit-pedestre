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
	def __init__(self, src, dest, percent_unit):
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
		return { 'from':self.src , 'to':self.dest, 'percent':self.units_sent}
