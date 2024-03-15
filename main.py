import csv
import networkx as nx
import pulp as plp
import matplotlib.pyplot as plt

def read_graph_from_csv(file_path):
    """
    Lit un graphe depuis un fichier CSV en utilisant NetworkX.

    :param file_path: Chemin vers le fichier CSV contenant le graphe.
    :return: Un objet Graph de NetworkX.
    """
    G = nx.Graph()
    with open(file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Ajouter une arête avec un poids entre 'Source' et 'Target'
            G.add_edge(row['Source'], row['Target'], weight=float(row['Weight']))
    return G


def find_minimum_dominating_set(G):
    """
    Trouve l'ensemble dominante minimum d'un graphe G.

    :param G: Le graphe NetworkX pour lequel trouver l'ensemble dominante minimum.
    :return: L'ensemble dominante minimum sous forme de liste de sommets.
    """
    prob = plp.LpProblem("MinimumDominatingSet", plp.LpMinimize)
    vertex_vars = plp.LpVariable.dicts("Vertex", G.nodes(), 0, 1, plp.LpBinary)
    prob += plp.lpSum(vertex_vars[i] for i in G.nodes()), "MinimizeDominatingSetSize"
    for i in G.nodes():
        prob += plp.lpSum(vertex_vars[j] for j in G.neighbors(i)) + vertex_vars[i] >= 1, f"DominatingCondition_{i}"
    prob.solve()
    dominating_set = [v for v in G.nodes() if plp.value(vertex_vars[v]) == 1]
    return dominating_set


def draw_and_save_graph_with_dominating_set(G, dominating_set, file_path='graph_with_dominating_set.png'):
    """
    Dessine le graphe G avec l'ensemble dominante minimum mis en évidence et sauvegarde l'image en format PNG.

    :param G: Le graphe NetworkX.
    :param dominating_set: L'ensemble dominante minimum du graphe G.
    :param file_path: Chemin du fichier où sauvegarder l'image du graphe.
    """
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G)  # Positionnement des nœuds

    # Dessiner tous les nœuds
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue', label='Non-dominating Nodes')
    # Mettre en évidence les nœuds dans l'ensemble dominante
    nx.draw_networkx_nodes(G, pos, nodelist=dominating_set, node_size=700, node_color='salmon',
                           label='Dominating Set Nodes')
    # Dessiner les arêtes
    nx.draw_networkx_edges(G, pos)
    # Étiquettes (labels) des nœuds
    nx.draw_networkx_labels(G, pos)

    plt.legend(scatterpoints=1)
    plt.axis('off')
    plt.savefig(file_path)
    plt.show()


if __name__ == "__main__":
    # Chemin vers votre fichier CSV
    file_path = 'mnt/data/graphe.csv'

    # Lecture du graphe depuis le fichier CSV
    G = read_graph_from_csv(file_path)

    # Calcul du minimum dominating set pour le graphe lu
    dominating_set = find_minimum_dominating_set(G)

    # Affichage de l'ensemble dominante minimum
    print("Minimum Dominating Set:", dominating_set)

    # Dessin et sauvegarde du graphe avec l'ensemble dominante minimum mis en évidence
    draw_and_save_graph_with_dominating_set(G, dominating_set, 'graph_with_dominating_set.png')