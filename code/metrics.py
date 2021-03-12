import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

def get_numerical_descriptors(graph_path):
    """
    Reads a Pajek graph files and calculates the 
    following metrics of the graph:
    - Number of nodes
    - Number of edges
    - Minimum node degree
    - Maximum node degree
    - Average node degree
    - Assortativity
    - Average path length
    - Diameter

    Returns those values in a list.
    """
    # Read Graph
    G = nx.Graph(nx.read_pajek(graph_path))

    # Simple operations
    results = []
    results.append(nx.number_of_nodes(G))
    results.append(nx.number_of_edges(G))

    degrees = nx.degree(G)
    results.append(min(degrees, key = lambda t: t[1])[1])
    results.append(max(degrees, key = lambda t: t[1])[1])
    results.append(mean(map(lambda t: t[1],degrees)))

    results.append(nx.average_clustering(G))
    results.append(nx.degree_assortativity_coefficient(G))
    results.append(nx.average_shortest_path_length(G))
    results.append(nx.diameter(G))

    return results


def plot_degree_distribution(graph_path, powerlaw = False):
    """
    Plots the probability degree function for the given graph
    and the complementary cumulative degree function
    """
    # Read Graph
    G = nx.Graph(nx.read_pajek(graph_path))
    # Get degree distribution
    distribution = nx.degree_histogram(G)
    edges = nx.number_of_edges(G)
    distribution = list(map(lambda t: t/edges ,distribution))
    # Get the Cumulative degree distribution
    cumulative = distribution.copy()
    cumulative.reverse()
    cumulative = np.cumsum(cumulative).tolist()
    cumulative.reverse()

    # Plot the PDF
    fig, axs = plt.subplots(nrows=1, ncols=2)
    ax = axs[0]
    ax.plot(distribution, 'bo', distribution)
    if powerlaw:
        ax.set_yscale('log')
        ax.set_xscale('log')
    ax.set_title('PDF')
    
    # Plot the CCDF
    ax = axs[1]
    ax.plot(cumulative, 'ro', cumulative)
    if powerlaw:
        ax.set_yscale('log')
        ax.set_xscale('log')
    ax.set_title('CCDF')
    
    fig.suptitle(graph_path)

    plt.show()

#Print results in latex table format
def print_results(name):
    print(name,end=' & ')
    print(*get_numerical_descriptors(name), sep= ' & ',end='\\\\ \n')

# for i in ['simpledistros.net']:
#     print_results(i)
#     print('\\hline')


# Plot the graphs degree distribution
plot_degree_distribution('simpledistros.net', True)
