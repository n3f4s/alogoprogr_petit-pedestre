# -*- coding: utf-8 -*-


"""Robot-joueur de Pooo

    Le module fournit les fonctions suivantes :
        register_pooo(uid)
        init_pooo(init_string)
        play_pooo()

"""

#__version__ = '0.1'
from tkinter import *
import protocol
import match
import graph

## chargement de l'interface de communication avec le serveur
import poooc # order, state, state_on_update, etime

# mieux que des print partout
import logging
# pour faire de l'introspection
import inspect

from strategy import strategy

# string
UUID = None
# { matchid: Match
MATCHES = {}

def register_pooo(uid):
    """Inscrit un joueur et initialise le robot pour la compétition

    :param uid: identifiant utilisateur
    :type uid:  chaîne de caractères str(UUID)

    :Example:

    "0947e717-02a1-4d83-9470-a941b6e8ed07"
    """
    global UUID
    UUID = uid


def init_pooo(init_string):
    """Initialise le robot pour un match

    :param init_string: instruction du protocole de communication de Pooo (voire ci-dessous)
    :type init_string: chaîne de caractères (utf-8 string)


    INIT<matchid>TO<#players>[<me>];<speed>;\
    <#cells>CELLS:<cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>,...;\
    <#lines>LINES:<cellid>@<dist>OF<cellid>,...

    <me> et <owner> désignent des numéros de 'couleur' attribués aux joueurs. La couleur 0 est le neutre.
    le neutre n'est pas compté dans l'effectif de joueurs (<#players>).
    '...' signifie que l'on répète la séquence précédente autant de fois qu'il y a de cellules (ou d'arêtes).
    0CELLS ou 0LINES sont des cas particuliers sans suffixe.
    <dist> est la distance qui sépare 2 cellules, exprimée en... millisecondes !
    /!\ attention: un match à vitesse x2 réduit de moitié le temps effectif de trajet d'une cellule à l'autre par rapport à l'indication <dist>.
    De manière générale temps_de_trajet=<dist>/vitesse (division entière).

    :Example:

    "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
    """
    global MATCHES
    init = protocol.parse_init(init_string)
    strategy_name="strat5"
    MATCHES[init['matchid']] = match.Match(init, lambda match : strategy(match,strategy_name))



def play_pooo():
    """Active le robot-joueur

    """
    global MATCHES
    logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))
    Mafenetre = Tk()
    Canevas = Canvas(Mafenetre, width = 270, height =270, bg ='white')
    Canevas.pack(padx =5, pady =5)
    
    while True:
        # On récupère et parse le nouvel état reçu.
        new_state = poooc.state_on_update()
        new_state = protocol.parse_message(new_state)
        if not new_state:
            continue
        # Si le match est en cours, on le met à jour puis on récupère la
        # stratégie à adopter qu'on encode et envoie.
        matchid = new_state['matchid']
        if matchid in MATCHES:
            if new_state['type'] in ('gameover', 'endofgame'):
                del MATCHES[matchid]
            elif new_state['type'] == 'state':
                current_match = MATCHES[matchid]
                current_match.update(new_state)
                orders = current_match.compute_strategy()
                for order in orders:
                    order = protocol.encode_order(UUID, order)
                    poooc.order(order)
        graph.graph(Canevas,current_match)
        Mafenetre.update()
