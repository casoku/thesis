from Util.automata_util import * 

LTL = 'F p | F g'

automata = LTL_to_automata(LTL, 'small')
bdict = automata.get_dict()

show_automata(automata)