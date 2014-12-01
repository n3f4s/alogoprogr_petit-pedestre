import re

REGEX_GENERAL = re.compile(r"""INIT
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

EXAMPLE_MESSAGE = r"""INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"""

def match_protocol(message):
    """Parse le message suivant le protocole donné.

    >>> match_protocol(EXAMPLE_MESSAGE) == {'matchid':\
            '20ac18ab-6d18-450e-94af-bee53fdc8fca', 'nb_players': '6', 'cells':\
            [{'x': '23', 'y': '9', 'radius': '2', 'cellid': '1', 'offsize':\
                '30', 'prod': 'I', 'defsize': '8'}, {'x': '41', 'y': '55',\
                    'radius': '1', 'cellid': '2', 'offsize': '30', 'prod':\
                    'II',\
                    'defsize': '8'}, {'x': '23', 'y': '103', 'radius': '1',\
                        'cellid': '3', 'offsize': '20', 'prod': 'II',\
                        'defsize':\
                        '5'}], 'speed': '1', 'id_us': '2', 'nb_lines': '2',\
                    'nb_cells': '3', 'lines': [{'cellid2': '2', 'dist': '3433',\
                        'cellid1': '1'}, {'cellid2': '3', 'dist': '6502',\
                            'cellid1': '1'}]}
    True
    """
    struct = REGEX_GENERAL.match(message).groupdict()
    cells = [REGEX_CELL.match(s + 'I').groupdict()
             for s in struct['cells'].split('I,')]
    lines = [REGEX_LINE.match(s).groupdict()
             for s in struct['lines'].split(',')]
    struct['cells'] = cells
    struct['lines'] = lines
    return struct


if __name__ == "__main__":
    import doctest
    doctest.testmod()
