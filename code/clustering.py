import networkx as nx
from networkx.algorithms.community import label_propagation_communities, greedy_modularity_communities, asyn_fluidc

graph_name = 'simpledistros.gml'
number_subreddits = 6
infomap_clu = 'simpledistros.clu'

G = nx.read_gml(graph_name)
G = nx.convert_node_labels_to_integers(G,first_label=1)

# Get the label propagation clustering
print('Label propagation clustering...')
lpa_gen = label_propagation_communities(G)
partition = []
for community in lpa_gen:
    part = sorted(community)
    partition.append(part)
partition = tuple(partition)
for v in G:
    for i in range(len(partition)):
        if v in partition[i]:
            G.node[v]['lpa'] = i
            continue

# Get the modularity clustering
print('Modularity clustering...')
comp = greedy_modularity_communities(G)
partition = []
for community in comp:
    part = sorted(community)
    partition.append(part)
for v in G:
    for i in range(len(partition)):
        if v in partition[i]:
            G.node[v]['mod'] = i
            continue

# Get the Infomap clustering
print('Infomap clustering...')
with open(infomap_clu) as f:
    content = f.readlines()
content = content[2:] # remove the first two lines
content = [x.split() for x in content]
content = [(int(x[0]), int(x[1])) for x in content]
for x in content:
    G.node[x[0]]['map'] = x[1]


nx.write_gml(G, graph_name)
