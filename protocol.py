""" Module chargé de parser et encoder les communications avec le serveur. """

import re
import itertools
import logging

LOGGER = logging.getLogger('parsing')

REGEX_GENERAL_INIT = re.compile(r"""INIT
                                    (?P<matchid>[0-9a-f\-]+)  # UUID du match
                                    TO
                                    (?P<nb_players>\d+)
                                    \[(?P<id_us>\d+)\]
                                    ;
                                    (?P<speed>\d+)
                                    ;
                                    (?P<nb_cells>\d+)
                                    CELLS
                                    (:(?P<cells>.*))?
                                    ;
                                    (?P<nb_lines>\d+)
                                    LINES
                                    (:(?P<lines>.*))?
                                    """,
                                re.VERBOSE)

REGEX_CELL_INIT = re.compile(r"""(?P<cellid>\d+)
                                 \(
                                 (?P<x>\d+),(?P<y>\d+)
                                 \)
                                 '
                                 (?P<radius>\d+)
                                 '
                                 (?P<offsize>\d+)
                                 '
                                 (?P<defsize>\d+)
                                 '
                                 (?P<prod>I+)
                                 """,
                             re.VERBOSE)

REGEX_LINE_INIT = re.compile(r"""(?P<cellid1>\d+)
                                 @
                                 (?P<dist>\d+)
                                 OF
                                 (?P<cellid2>\d+)
                                 """,
                             re.VERBOSE)

REGEX_GENERAL_STATE = re.compile(r"""STATE
                                     (?P<matchid>[0-9a-f\-]+)  # UUID du match
                                     IS
                                     (?P<nb_players>\d+)
                                     ;
                                     (?P<nb_cells>\d+)
                                     CELLS
                                     (:(?P<cells>.*))?
                                     ;
                                     (?P<nb_moves>\d+)
                                     MOVES
                                     (:(?P<moves>.*))?
                                     """,
                                 re.VERBOSE)

REGEX_CELL_STATE = re.compile(r"""(?P<cellid>\d+)
                                  \[
                                  (?P<owner>-?\d+)
                                  \]
                                  (?P<offunit>\d+)
                                  '
                                  (?P<defunit>\d+)
                                  """,
                              re.VERBOSE)

REGEX_MOVE_STATE = re.compile(r"""(?P<direction>\<|\>)
                                  (?P<units>\d+)
                                  \[
                                  (?P<owner>\d+)
                                  \]
                                  @
                                  (?P<timestamp>\d+)
                                  """,
                              re.VERBOSE)

REGEX_GAMEOVER = re.compile(r"""GAMEOVER
                                \[
                                (?P<winner>\d+)
                                \]
                                IN
                                (?P<matchid>[0-9a-f\-]+)
                                """,
                            re.VERBOSE)

REGEX_ENDOFGAME = re.compile(r"""ENDOFGAME
                                 (?P<matchid>[0-9a-f\-]+)
                                 """,
                             re.VERBOSE)

EXAMPLE_INIT = r"INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
EXAMPLE_STATE = r"STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"
EXAMPLE_ORDER = r"[0947e717-02a1-4d83-9470-a941b6e8ed07]MOV33FROM1TO4"
EXAMPLE_GAMEOVER = r"GAMEOVER[2]IN20ac18ab-6d18-450e-94af-bee53fdc8fca"
EXAMPLE_ENDOFGAME = r"ENDOFGAME20ac18ab-6d18-450e-94af-bee53fdc8fca"

def parse_register(message):
    """ Retourne l'UUID du joueur."""
    return message[3:]

def parse_init(message):
    """ Parse le message suivant le protocole donné.

    >>> parse_init(EXAMPLE_INIT) == \
            {'matchid': '20ac18ab-6d18-450e-94af-bee53fdc8fca',\
             'nb_players': 6,\
             'cells': [{'x': 23, 'y': 9, 'radius': 2, 'cellid': 1,\
                        'offsize': 30, 'prod': 'I', 'defsize': 8},\
                       {'x': 41, 'y': 55, 'radius': 1, 'cellid': 2,\
                        'offsize': 30, 'prod': 'II', 'defsize': 8},\
                       {'x': 23, 'y': 103, 'radius': 1, 'cellid': 3,\
                        'offsize': 20, 'prod': 'I', 'defsize': 5}],\
             'speed': 1,\
             'id_us': 2,\
             'lines': [{'cellid2': 2, 'dist': 3433, 'cellid1': 1},\
                       {'cellid2': 3, 'dist': 6502, 'cellid1': 1}]}
    True
    """
    LOGGER.debug('Reçu  :' + message)
    struct = REGEX_GENERAL_INIT.match(message).groupdict()
    struct['cells'] = struct['cells'] or ''
    struct['lines'] = struct['lines'] or 'I'
    cells = [REGEX_CELL_INIT.match(s + 'I').groupdict()
             for s in struct['cells'][:-1].split('I,')]
    lines = [REGEX_LINE_INIT.match(s).groupdict()
             for s in struct['lines'].split(',')]
    struct['cells'] = cells
    struct['lines'] = lines
    # Suppression de champs inutiles
    del struct['nb_cells'], struct['nb_lines']
    # str -> int pour les champs numériques. la regex garrantit que ce sont des
    # nombre.
    _intify(struct, ['nb_players', 'speed', 'id_us'])
    for cell in struct['cells']:
        _intify(cell, ['x', 'y', 'radius', 'cellid', 'offsize', 'defsize'])
    for line in struct['lines']:
        _intify(line, ['cellid1', 'cellid2', 'dist'])
    LOGGER.debug('Parsé :' + str(struct))
    return struct

def parse_message(message):
    """ Parse le message en identifiant son type. """
    try:
        if message.startswith('GAMEOVER'):
            return parse_gameover(message)
        elif message.startswith('ENDOFGAME'):
            return parse_endofgame(message)
        elif message.startswith('STATE'):
            return parse_state(message)
        else:
            LOGGER.warning('Protocole inconnu : ' + message)
            return None
    except Exception as e:
        LOGGER.error('Pas de correspondance trouvée pour ' + message)
        LOGGER.debug(e)
        return None

def parse_state(message):
    """ Parse le message suivant le protocole donné.

    >>> parse_state(EXAMPLE_STATE) == \
               {'moves': [\
                   {'to': 1, 'owner': 2, 'from': 2, 'units': 5, 'timestamp': 232},\
                   {'to': 2, 'owner': 2, 'from': 1, 'units': 6, 'timestamp': 488},\
                   {'to': 2, 'owner': 1, 'from': 1, 'units': 3, 'timestamp': 4330},\
                   {'to': 1, 'owner': 1, 'from': 3, 'units': 10, 'timestamp': 2241}],\
                'cells': [\
                    {'defunit': 4, 'owner': 2, 'offunit': 12, 'cellid': 1},\
                    {'defunit': 2, 'owner': 2, 'offunit': 15, 'cellid': 2},\
                    {'defunit': 6, 'owner': 1, 'offunit': 33, 'cellid': 3}],\
                'nb_players': 2,\
                'matchid': '20ac18ab-6d18-450e-94af-bee53fdc8fca',\
                'type': 'state'}
    True
    """
    LOGGER.debug('Reçu  : ' + message)
    struct = REGEX_GENERAL_STATE.match(message).groupdict()
    struct['cells'] = struct['cells'] or ''
    cells = [REGEX_CELL_STATE.match(s).groupdict()
             for s in struct['cells'].split(',')]
    moves = struct['moves'].split(',') if struct['moves'] else []
    # l'itertool est là pour transformer [[x]] en [x]
    moves = list(itertools.chain(*[_parse_moves(move) for move in moves]))
    struct['cells'] = cells
    struct['moves'] = moves
    struct['type'] = 'state'
    # suppression de champs inutiles
    del struct['nb_moves'], struct['nb_cells']
    # str -> int pour les champs numériques. la regex garrantit que ce sont des
    # nombre.
    _intify(struct, ['nb_players'])
    for cell in struct['cells']:
        _intify(cell, ['defunit', 'owner', 'offunit', 'cellid'])
    for move in struct['moves']:
        _intify(move, ['to', 'owner', 'from', 'units', 'timestamp'])
    LOGGER.debug('Parsé : ' + str(struct))
    return struct

def _parse_moves(moves):
    (left, moves, right) = re.match(r"(\d+)(.*)(\d+)", moves).groups()
    moves = [REGEX_MOVE_STATE.match(s).groupdict()
             for s in moves.split("'")
             if s]
    for move in moves:
        if move['direction'] == '>':
            move['from'] = left
            move['to'] = right
        else:
            move['from'] = right
            move['to'] = left
        del move['direction']
    return moves

def encode_order(user_id, order):
    """ Encode l'ordre de déplacement suivant le protocole donné.

    >>> encode_order("0947e717-02a1-4d83-9470-a941b6e8ed07", {'from': 1, 'to': 4,\
                                                              'percent': 33})
    '[0947e717-02a1-4d83-9470-a941b6e8ed07]MOV33FROM1TO4'
    """
    LOGGER.debug('Reçu  : ' + user_id + ', ' + str(order))
    result = "[{user_id}]MOV{percent}FROM{from}TO{to}".format(user_id=user_id, **order)
    LOGGER.debug('Encodé : ' + result)
    return result

def parse_gameover(message):
    """ Parse un message de gameover.

    >>> parse_gameover(EXAMPLE_GAMEOVER) == {'type': 'gameover', 'winner': 2,\
            'matchid': '20ac18ab-6d18-450e-94af-bee53fdc8fca'}
    True
    """
    LOGGER.debug('Reçu  : ' + message)
    struct = REGEX_GAMEOVER.match(message).groupdict()
    struct['type'] = 'gameover'
    _intify(struct, ['winner'])
    LOGGER.debug('Parsé : ' + str(struct))
    return struct

def parse_endofgame(message):
    """ Parse un message de gameover.

    >>> parse_endofgame(EXAMPLE_ENDOFGAME) == {'type': 'endofgame', 'matchid':\
            '20ac18ab-6d18-450e-94af-bee53fdc8fca'}
    True
    """
    LOGGER.debug('Reçu  : ' + message)
    struct = REGEX_ENDOFGAME.match(message).groupdict()
    struct['type'] = 'endofgame'
    LOGGER.debug('Parsé : ' + str(struct))
    return struct

def _intify(struct, keys):
    """ Transforme les valeurs str en int.

    >>> _intify({1: '1', 2: '2', 3: '3'}, [1, 3]) == {1: 1, 2: '2', 3: 3}
    True
    """
    for key in keys:
        struct[key] = int(struct[key])
    return struct


if __name__ == "__main__":
    import doctest
    doctest.testmod()
