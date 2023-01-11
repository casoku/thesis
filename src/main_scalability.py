from Util.create_env import create_simple_env, create_9_rooms_env
from high_level_model import HLM
from Util.automata_util import num_edges, num_states, LTL_to_automata

import matplotlib.pyplot as plt
import numpy as np
import sys
import time

sys.setrecursionlimit(70000)

simple_env = create_simple_env()
nine_rooms_env = create_9_rooms_env()

simple_HLM = HLM(load_dir='simple_env_small_subtasks')
nine_rooms_HLM = HLM(load_dir='9_rooms_HLM')

# Tasks simple env
LTL_simple1 = 'F g'
LTL_simple2 = 'F(p & F g)'
LTL_simple3 = 'F (g & F( p  & F (g & F start)))'
LTL_simple4 = 'F g & F start & F p & F d1 & F d2'
LTL_simple5 = 'F g & F start & F p & F d1 & F d2 & F d3 & F d4'

# Tasks 9 roon env
LTL_large1 = 'F g & F p & G ! R5'
LTL_large2 = 'F y & F c & F p & F g'
LTL_large3 = 'F (g & F( p  & F (g & F start))) | (F y & (F(g & F y & (F p & (F c & (F g & (F p & F start)))))))'
LTL_large4 = 'F y & F c & F p & F g & F d3'
LTL_large5 = 'F y & F c & F p & F g & F d3 & F d7'

tasks = [LTL_simple1, LTL_simple2, LTL_simple3, LTL_simple4, LTL_simple5, LTL_large1, LTL_large2, LTL_large3, LTL_large4, LTL_large5]
boxplotdataPD = []
boxplotdataMA = []
index = 0
for LTL in tasks:

    if index < 5:
        hlm = simple_HLM
    else:
        hlm = nine_rooms_HLM

    index += 1 
    data_productgraph = []
    data_martin = []
    # Create product automata
    # 50
    for i in range(1):
        automata = LTL_to_automata(LTL)
        automata_num_states = num_states(automata)
        automata_num_edges = num_edges(automata)

        print("Size of automata ({} x {}), (states x edges)".format(automata_num_states, automata_num_edges))
        print("Size of HLM ({} x {}), (states x edges)".format(len(hlm.states), len(hlm.edges)))

        start_time = time.time()
        graph = hlm.create_product_graph(LTL)
        end_time = time.time()
        total_time = end_time - start_time
        data_productgraph.append(total_time)
        print("Creation of Product graph takes:   %s seconds" % total_time)
        #graph.show_graph('product graph')

        #Print size of product graph
        num_of_states = len(graph.get_states())
        num_of_edges = len(graph.get_edges())

        print("size of productgraph: ({} x {}), (states x edges)".format(num_of_states, num_of_edges))

        # Find pareto optimal paths
        start_time = time.time()
        graph.martins_algorithm()
        paths = graph.find_optimal_paths_2()
        end_time = time.time()
        total_time = end_time - start_time
        data_martin.append(total_time)
        print("Finding pareto optimal paths takes:   %s seconds" % total_time)
        print("number of pareto paths found:   %s" % (len(paths)))
    
    boxplotdataPD.append(data_productgraph)
    boxplotdataMA.append(data_martin)

fig = plt.figure(figsize =(10, 7))
 
# Creating plot
plt.boxplot(boxplotdataMA)
plt.ylabel('Time (s)', fontsize = 15)
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        ['Test 1', 'Test 2', 'Test 3', 'Test 4', 'Test 5', 'Test 6', 'Test 7', 'Test 8', 'Test 9', 'Test 10']) 
plt.tick_params(labelsize = 12)
# show plot
plt.show()