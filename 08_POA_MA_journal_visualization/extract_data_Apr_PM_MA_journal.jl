using JSON

demandsDict = Dict()
# get ground trueth demands, indexed by 0
demandsDict[0] = iniDemand("../data_original/journal_trips_Apr_PM.txt")
# get initial demands, indexed by 1
demandsDict[1] = iniDemand("../data_original/journal_trips_Apr_PM.txt", 1)

numNodes, numLinks, numODpairs, capacity, free_flow_time, ta_data_Apr_PM = paraNetwork("MA_journal_Apr_PM")
link_label_dict, link_label_dict_, link_length_dict = furInfo()

start_node = ta_data_Apr_PM.start_node
end_node = ta_data_Apr_PM.end_node

#load OD pair labels
odPairLabel = readstring("../temp_files/od_pair_label_dict_MA_journal_refined.json")
odPairLabel = JSON.parse(odPairLabel)

odPairLabel_ = readstring("../temp_files/od_pair_label_dict__MA_journal_refined.json")
odPairLabel_ = JSON.parse(odPairLabel_)

#load node-link incidence
nodeLink = readstring("../temp_files/node_link_incidence_MA_journal.json");
nodeLink = JSON.parse(nodeLink);