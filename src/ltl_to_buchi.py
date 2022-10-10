from Util.automata_util import * 

LTL = 'F g & G ! r3'

automata = LTL_to_automata(LTL, 'small')
bdict = automata.get_dict()

show_automata(automata)