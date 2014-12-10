import re

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

REGEX_CELL = re.compile(r"""(?P<cellid>\d+)
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

REGEX_LINE = re.compile(r"""(?P<cellid1>\d+)
                            @
                            (?P<dist>\d+)
                            OF
                            (?P<cellid2>\d+)
                            """,
                        re.VERBOSE)

REGEX_GENERAL_STATE = re.compile(r"""
                                     """,
                                 re.VERBOSE)

EXAMPLE_INIT = r"INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
EXAMPLE_STATE = r"STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3"
EXAMPLE_ORDER = r"[0947e717-02a1-4d83-9470-a941b6e8ed07]MOV33FROM1TO4"

def parse_init(message):
    """Parse le message suivant le protocole donné.

    >>> parse_init(EXAMPLE_INIT) == {'matchid':\
            '20ac18ab-6d18-450e-94af-bee53fdc8fca', 'nb_players': '6', 'cells':\
            [{'x': '23', 'y': '9', 'radius': '2', 'cellid': '1', 'offsize':\
                '30', 'prod': 'I', 'defsize': '8'}, {'x': '41', 'y': '55',\
                    'radius': '1', 'cellid': '2', 'offsize': '30', 'prod':\
                    'II',\
                    'defsize': '8'}, {'x': '23', 'y': '103', 'radius': '1',\
                        'cellid': '3', 'offsize': '20', 'prod': 'I',\
                        'defsize':\
                        '5'}], 'speed': '1', 'id_us': '2', 'nb_lines': '2',\
                    'nb_cells': '3', 'lines': [{'cellid2': '2', 'dist': '3433',\
                        'cellid1': '1'}, {'cellid2': '3', 'dist': '6502',\
                            'cellid1': '1'}]}
    True
    """
    struct = REGEX_GENERAL_INIT.match(message).groupdict()
    cells = [REGEX_CELL_INIT.match(s + 'I').groupdict()
            for s in struct['cells'][:-1].split('I,')]
    lines = [REGEX_LINE_INIT.match(s).groupdict()
             for s in struct['lines'].split(',')]
    struct['cells'] = cells
    struct['lines'] = lines
    return struct

def parse_state(message):
    #TODO : écrire la fonction !
    pass

def encode_order(user_id, order):
    """Encode l'ordre suivant le protocole donné.

    >>> encode_order("0947e717-02a1-4d83-9470-a941b6e8ed07", {'from': 1, 'to': 4,\
                                                              'percent': 33})
    '[0947e717-02a1-4d83-9470-a941b6e8ed07]MOV33FROM1TO4'
    """
    return "[{user_id}]MOV{percent}FROM{from}TO{to}".format(user_id=user_id, **order)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
