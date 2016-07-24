from util import *

import json

with open('./benchmark_data/Sioux_flow.txt') as Sioux_flow:
    Sioux_flow_lines = Sioux_flow.readlines()
Sioux_links = []
i = -1
for line in Sioux_flow_lines:
    i += 1
    if i > 0:
        Sioux_links.append(line.split('\t')[0:2])
numLinks = i

link_list_js = [str(int(Sioux_links[i][0])) + ',' + str(int(Sioux_links[i][1])) for \
                i in range(len(Sioux_links))]

link_list_pk = [str(int(Sioux_links[i][0])) + '->' + str(int(Sioux_links[i][1])) for \
                i in range(len(Sioux_links))]

numNodes = max([int(Sioux_links[i][1]) for i in range(numLinks)])

from collections import defaultdict

node_neighbors_dict = defaultdict(list)

for node in range(numNodes):
    for link in Sioux_links:
        if node == int(link[0]):
            node_neighbors_dict[str(node)].append(int(link[1]))

with open('./benchmark_data/Sioux_trips.txt') as Sioux_trips:
    Sioux_trips_lines = Sioux_trips.readlines()

numZones = int(Sioux_trips_lines[0].split(' ')[3])

od_pairs = []
for i in range(numZones+1)[1:]:
    for j in range(numZones+1)[1:]:
        if i != j:
            od_pairs.append([i, j])
            
numODpairs = len(od_pairs)

# create O-D pair labels
# create a dictionary mapping O-D pairs to labels

import json

OD_pair_label_dict = {}
OD_pair_label_dict_ = {}

label = 1
for i in range(numZones + 1)[1:]:
    for j in range(numZones + 1)[1:]:
        key = (i, j)
        OD_pair_label_dict[str(key)] = label
        OD_pair_label_dict_[str(label)] = key
        label += 1
        
with open('../temp_files/od_pair_label_dict_Sioux.json', 'w') as json_file:
    json.dump(OD_pair_label_dict, json_file)
    
with open('../temp_files/od_pair_label_dict__Sioux.json', 'w') as json_file:
    json.dump(OD_pair_label_dict_, json_file)


OD_pair_label_dict_refined = {}
OD_pair_label_dict_refined_ = {}

label = 1
for i in range(numZones + 1)[1:]:
    for j in range(numZones + 1)[1:]:
        if i != j:
            key = (i, j)
            OD_pair_label_dict_refined[str(key)] = label
            OD_pair_label_dict_refined_[str(label)] = key
            label += 1
        
with open('../temp_files/od_pair_label_dict_Sioux_refined.json', 'w') as json_file:
    json.dump(OD_pair_label_dict_refined, json_file)
    
with open('../temp_files/od_pair_label_dict__Sioux_refined.json', 'w') as json_file:
    json.dump(OD_pair_label_dict_refined_, json_file)
    
    
# create link labels
# create a dictionary mapping directed links to labels
link_label_dict = {}
link_label_dict_ = {}

for i in range(numLinks):
    link_label_dict[str(i)] = link_list_js[i]

for i in range(numLinks):
    link_label_dict_[link_list_js[i]] = i

with open('../temp_files/link_label_dict_Sioux.json', 'w') as json_file:
    json.dump(link_label_dict, json_file)
    
with open('../temp_files/link_label_dict_Sioux_.json', 'w') as json_file:
    json.dump(link_label_dict_, json_file)
    
# create link labels
# create a dictionary mapping directed links to labels
link_label_dict = {}
link_label_dict_ = {}

for i in range(numLinks):
    link_label_dict[str(i)] = link_list_pk[i]

for i in range(numLinks):
    link_label_dict_[link_list_pk[i]] = i

zdump(link_label_dict, '../temp_files/link_label_dict_Sioux_network.pkz')
zdump(link_label_dict_, '../temp_files/link_label_dict_Sioux_network_.pkz')

link_length_list = []
with open('./benchmark_data/Sioux_net.txt', 'r') as f:
    read_data = f.readlines()
    flag = 0
    for row in read_data:
        if ';' in row:
            flag += 1
            if flag > 1:
                link_length_list.append(float(row.split('\t')[4]))

link_label_dict = zload('../temp_files/link_label_dict_Sioux_network.pkz')
link_label_dict_ = zload('../temp_files/link_label_dict_Sioux_network_.pkz')

import networkx as nx

def jacobianSpiess(numNodes, numLinks, numODpairs, od_pairs, link_list_js, link_length_list):
    Sioux = nx.DiGraph()

    Sioux.add_nodes_from(range(numNodes+1)[1:])

    Sioux_weighted_edges = [(int(link_list_js[i].split(',')[0]), int(link_list_js[i].split(',')[1]), \
                             link_length_list[i]) for i in range(len(link_list_js))]

    Sioux.add_weighted_edges_from(Sioux_weighted_edges)

    path = nx.all_pairs_dijkstra_path(Sioux)

    od_route_dict = {}
    for od in od_pairs:
        origi = od[0]
        desti = od[1]
        key = OD_pair_label_dict_refined[str((origi, desti))]
        route = str(path[origi][desti]).replace("[", "").replace(", ", "->").replace("]", "")
        od_route_dict[key] = route

    od_link_dict = {}
    for idx in range(len(od_route_dict)):
        od_link_list = []
        od_node_list = od_route_dict[idx+1].split('->')
        for i in range(len(od_node_list)):
            if i < len(od_node_list) - 1:
                od_link_list.append(link_label_dict_[od_node_list[i] + '->' + od_node_list[i+1]])
        od_link_dict[idx] = od_link_list

    jacob = np.zeros((numODpairs, numLinks))

    for i in range(numODpairs):
        for j in range(numLinks):
            if j in od_link_dict[i]:
                jacob[i, j] = 1

    return jacob

jacob = jacobianSpiess(numNodes, numLinks, numODpairs, od_pairs, link_list_js, link_length_list)
