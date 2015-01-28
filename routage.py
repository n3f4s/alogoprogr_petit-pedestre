#!/usr/bin/env python3

from match import *

class Route_table:
    """Classe représentant une table de routage
    Attributs:
        self.cell_id :: Int    ID de la cell possédant cette table de routage
        self.routes  :: list   Liste des lignes de la table de routage.
    """
    def __init__(self, id):
        self.cell_id = id #id
        self.routes = []

class Route_line:
    """Classe représentant une ligne de la table de routage
    Attributs:
        self.dest      :: Int    ID de la cell à laquelle on veut se rendre
        self.next_jump :: Int    ID de la cell adjacente où il faut aller pour se rendre à destination
        self.dist      :: Int    Distance à la destination en nombre de saut
    """
    def __init__(self, dest, next_jump, dist, prod_speed):
        self.dest = dest #id
        self.next_jump = next_jump #id
        self.dist = dist
        self.prod_speed = prod_speed

# Table de routage, de la forme { ID de la cell : Route_table }
ROUTES = {}

def build_route_table(match):
    """Fonction initialisant la table de routage ROUTES

    Argument : match :: Match   Match en cour
    """
    tmp = {}
    for cell_id,cell_val in match.cells.items():
        tmp = send_route(match, cell_id,cell_id,cell_id,0, cell_val.speed_prod)
        for id,route in tmp.items():
            if not ROUTES.get(id):
                ROUTES[id] = Route_table(id)
            ROUTES[id].routes.append(route)

def next_jump_to_target(cell, target):
    """Renvoie l'ID de la cellule suivante sur le chemin vers target
    Argument:
        cell   :: Int   Id de la cell
        target :: Int Id de la target
    Retour: 
        Int           Id du saut suivant
    """
    ROUTES[cell].routes.sort(key=lambda r : r.dist )
    return ROUTES[cell].routes[0].next_jump

def send_route(match, id, src, last_jump, dist, prod_speed, _visited = None):
    """Initialise la table de routage

    Cette fonction visite les cellules en mettant à jour leurs table de routage

    Argument:
        match      :: Match   Match en cour
        id         :: Int     ID de la cellule qu'on visite
        src        :: Int     ID de la cellule par laquelle on a commencé
        last_jump  :: Int     ID de la dernière cellule que l'on a visité
        dist       :: Int     Distance à la cellule src
        prod_speed :: Int     Vitesse de production de la cellule src
        
    Retour:
        { id_cell : route_line(src,...) }
    """
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
    return _visited
