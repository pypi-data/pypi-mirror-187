from .nxTree import copy_tree, is_leaf, induced_colors
from itertools import product, combinations
import networkx as nx
from bmgedit import BMGEditing
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

def build_graph(G, method='louvain', objective='cost', color_attr= None):
    """
    ARG1: method - this param will be use to select the method
    """
    if color_attr != None:
        G1= G.copy()
        for x in G:
            G1.nodes[x]['color']= G.nodes[x][color_attr]
    else:
        G1= G

    solver = BMGEditing.BMGEditor(G1, binary=True)
    solver.build(method, objective)

    hug_free= solver.get_bmg(extract_triples_first=False)

    for x in G:
        hug_free.nodes[x]['accession']= G.nodes[x]['accession']
        hug_free.nodes[x]['species']= G.nodes[x]['species']

    return hug_free

def _addN(T,idx, tree, n):
    T.add_node(idx, **(tree.nodes[n].copy()))

def get_augmented_tree(tree, geneAttr, speciesAttr):
    """
    Constructs the color intersection graph
    Schaller et. al. 2020:
    Complete characterization of incorrect orthology assiments in BMGs
    """

    T= nx.DiGraph() #<
    T.root= 0
    _addN(T, 0, tree, 0) #<
    w_idx= 1 #<
    mu= {1 : 0} #< node x in tree --> corresponding dad in T

    for node in list(nx.dfs_preorder_nodes(tree, source= 1)):

        _addN(T, w_idx, tree, node) #<
        T.add_edge(mu[node], w_idx) #<
        for child in tree[node]:
            mu[child]= w_idx
        current= w_idx
        w_idx+= 1

        if (not is_leaf(tree, node)) and (node != tree.root):
            CIG= get_CIG(tree, node, speciesAttr)
            CC= list(nx.connected_components(CIG))
            if len(CC)>1:
                T.nodes[current][geneAttr]= 'S' #<
                for cc in (X for X in CC if len(X)>1):
                    _create_redundant_node(T, w_idx, current, tree, node, cc, mu, geneAttr, speciesAttr) #<
                    w_idx+= 1
            else:
                T.nodes[current][geneAttr]= 'P'
    T.nodes[T.root][geneAttr]= None
    return T

def get_CIG(tree, node, speciesAttr):
    """
    Color Intersection Graph
    """
    children= set(tree[node])
    CIG= nx.Graph()
    CIG.add_nodes_from(children)
    for v0,v1 in combinations(children, 2):
        colors0= induced_colors(tree, v0, speciesAttr)
        colors1= induced_colors(tree, v1, speciesAttr)
        if not colors0.isdisjoint(colors1):
            CIG.add_edge(v0, v1)
    return CIG

def _create_redundant_node(T, w_idx, current, tree, node, cc, mu, geneAttr, speciesAttr):
    T.add_node(w_idx, **{geneAttr: 'P', speciesAttr: None})
    T.add_edge(current, w_idx)
    for child in cc:
        mu[child]= w_idx

####################
#                  #
# Standalone usage #
#                  #
####################

if __name__ == "__main__":
    import argparse
    from .parse_prt import create_cBMG
    from .in_out import read_tl_digraph, write_digraphs_list

    parser = argparse.ArgumentParser(prog= 'hug_free',
                                     description='Converts a digraph into a BMG.',
                                    )

    # Parameters for input graph
    ############################

    parser.add_argument('edges_list',
                        type= str,
                        help= '.tsv file containing best matches. (See input formats)'
                       )

    parser.add_argument('-og', '--orthogroup',
                        type= str,
                        required=False,
                        help= 'Column in the edges_list specifying orthogroups.',
                        default= None,
                       )

    parser.add_argument('-f', '--filter_orthogroups',
                        type= str,
                        required=False,
                        help= '.tsv file describing which orthogroups are alrready cBMGs.',
                        default= None,
                       )
    

    parser.add_argument('-o', '--output_prefix',
                        type= str,
                        required=False,
                        help= 'prefix used for output files (default "prt_revolutionhtl").',
                        default= 'tl_project.hug_free',
                       )

    args= parser.parse_args()

    # Process data
    ##############

    print('Reading hit graphs...')
    G= read_tl_digraph(args.edges_list, og_col= 'OG')
    print('Computing hug-free graphs...')
    G1= G.progress_apply(lambda X: build_graph(X, color_attr= 'species'))
    write_digraphs_list(G, args.output_prefix, n_attrs= ['accession', 'species'])
    print(f'Hug-free graphs successfully writen to {args.output_prefix}.tsv')
