#!/usr/bin/env python3

from match import *

class Route_table:
	def __init__(self, id):
		self.cell_id = id #id
		self.routes = []

class Route_line:
	def __init__(self, dest, next_jump, dist, prod_speed):
		self.dest = dest #id
		self.next_jump = next_jump #id
		self.dist = dist
		self.prod_speed = prod_speed

ROUTES = {}

def build_route_table(match):
	# Devrait marcher
	tmp = {}
	for cell_id,cell_val in match.cells.items():
		tmp = send_route(match, cell_id,cell_id,cell_id,0, cell_value.speed_prod)
		for id,route in tmp.items():
			if not ROUTES.get(id):
				ROUTES[id] = Route_table(id)
			ROUTES[id].routes.append(route)

def next_jump_to_target(cell, target):
	# cell :: Int Id de la cell
	# target :: Int Id de la target
	# Retour :: Int Id du saut suivant
	ROUTES[cell].routes.sort(key=lambda r : r.dist )
	return ROUTES[cell].routes[0].next_jump

def send_route(match, id, src, last_jump, dist, prod_speed, _visited = None):
	# Devrait marcher
	# On envoit son adresse au cell adjacente (au lieu de demander les cells suivantes )
	if not _visited:
		_visited = {}
	if src == id:
		_visited[id] = None
	else:
		_visited[id] = Route_line(src, last_jump, dist, prod_speed)
	for neighbour in match.cells[id].links.keys():
		if neighbour not in _visited.keys():
			_visited.update( send_route(match,neighbour,src,id,dist+1,match.cells[id].speed_prod,_visited) )
	# forme du retour:
	# { id_cell : route_line(src,...) }
	return _visited


# pre : création de la table de routage
# phase 1 : séléction des cibles
# 		- cibles avec le plus de prod ( parmi neutre et enemis)
# 		- nombre de cibles fonction du nombre de nos cellules
# phase 2 : attaque
#		- si cell neutre:
#			- si il y a une cellule enemis qui peut l'attaquer:
#				- si on a le double (220%) des units adverses, on attaque
#				- si on au moins assez pour prendre l'unité + unité de la cell enemis
#				- sinon, on attent que l'enemis attaque
#			- sinon, on attaque
#		- sinon si cell enemis, on attaque si on a assez de cell
# 		- sinon on cherche la cell allié adjacente la plus faible
