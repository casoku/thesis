import spot
from cairosvg import svg2png
from PIL import Image

def custom_print(aut):
    bdict = aut.get_dict()
    print("Acceptance:", aut.get_acceptance())
    print("Number of sets:", aut.num_sets())
    print("Number of states: ", aut.num_states())
    print("Initial states: ", aut.get_init_state_number())
    print("Atomic propositions:", end='')
    for ap in aut.ap():
        print(' ', ap, ' (=', bdict.varnum(ap), ')', sep='', end='')
    print()
    # Templated methods are not available in Python, so we cannot
    # retrieve/attach arbitrary objects from/to the automaton.  However the
    # Python bindings have get_name() and set_name() to access the
    # "automaton-name" property.
    name = aut.get_name()
    if name:
        print("Name: ", name)
    print("Deterministic:", aut.prop_universal() and aut.is_existential())
    print("Unambiguous:", aut.prop_unambiguous())
    print("State-Based Acc:", aut.prop_state_acc())
    print("Terminal:", aut.prop_terminal())
    print("Weak:", aut.prop_weak())
    print("Inherently Weak:", aut.prop_inherently_weak())
    print("Stutter Invariant:", aut.prop_stutter_invariant())

    for s in range(0, aut.num_states()):
        print("State {}:".format(s))
        for t in aut.out(s):
            print("  edge({} -> {})".format(t.src, t.dst))
            # bdd_print_formula() is designed to print on a std::ostream, and
            # is inconvenient to use in Python.  Instead we use
            # bdd_format_formula() as this simply returns a string.
            print("    label =", spot.bdd_format_formula(bdict, t.cond))
            print("    acc sets =", t.acc)

def LTL_to_automata(ltl_string):
    #Change small to complete to also show terminating transitions
    automata = spot.translate(ltl_string, 'Buchi', 'state-based', 'small')
    return automata

def show_automata(automata_svg):
    spot.setup()
    svg2png(bytestring=automata_svg.show().__dict__["data"], write_to='output.png')
    image = Image.open('output.png')
    image.show()

# automata = spot.translate('F((F c & F d) & F s)', 'Buchi', 'state-based', 'small')
# custom_print(automata)
# show_automata(automata)
#print(spot.translate('F(a & F b)', 'Buchi', 'state-based', 'small').show())

def solve_edge_bool_expression(bdict, automata_edge, map_edge, variables):

    #TODO: evaluate if an edge should be added via boolean logic (i.e. is this edge ever gonna happen?)
    # If not, there is no need to add to the combined model
    print("mapLabel: " + str(map_edge.labels))
    print("automataLabel: " + str(spot.bdd_format_formula(bdict, automata_edge.cond)))

    # rewrite to python logic
    expression = str(spot.bdd_format_formula(bdict, automata_edge.cond)).replace('&', 'and').replace('|', 'or').replace('!', 'not ')

    variables_copy = variables.copy()
    #Replace labels with "True"
    for label in map_edge.labels:
        print("label to replace: " + label)
        if str(label) in variables_copy: 
            variables_copy.remove(str(label))
        expression = str(expression.replace((str(label)) , 'True'))

    #Replace unassigned values with "False"
    for variable in variables_copy:
        print("variable to replace: " + variable)
        expression = str(expression.replace((str(variable)) , 'False'))

    print("expression: " + expression)
    #evaluate expression:
    return bool(eval(expression))

