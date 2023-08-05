from . import nxTree as nxt
from .triplets import get_triplets
from .build_st_n import BUILDst_N
from .nhxx_tools import read_nhxx, get_nhx

import networkx as nx
import pandas as pd

def reconciliate(Tg, Ts, gene_attr= 'genes', species_attr= 'species', event_attr= 'event'):
    """
    The input trees must be planted, where the LCA of all the leafs have int label '1'
    """
    # Check if species tree displays the gene tree
    Rg= get_triplets(Tg, event=event_attr, color= species_attr) + [ nxt.subtree(Ts, 1) ]
    Trr= BUILDst_N(Rg, color_attr= species_attr)
    # Obtain reconciliation map
    mu= get_reconciliation_map(Tg, Ts, event_attr= event_attr, species_attr= species_attr)
    # Resolve gene tree
    T, mu_s, mu_inv= resolve(Tg, Ts, mu, event_attr, [species_attr], Tg_root= 1)
    return T, mu_s, mu_inv

def resolve(Tg, Ts, mu, event_attr, copy_attrs= [], Tg_root= None):
    # Initialize output objects
    if Tg_root==None:
        Tg_root= Tg.root
    T= nx.DiGraph()
    T.root= 0
    T.add_node(0, **{event_attr: 0})
    n= 1
    dad_dict= {Tg_root : 0}
    mu_s= {}
    mu_inv= {y:{'S':[],'P':[],'X':[],'.':[]} for y in Ts}
    # Given is a universal parameter for all functions
    given= Tg, Ts, T, mu, event_attr, copy_attrs, mu_s, mu_inv, dad_dict
    # Segregate all the nodes
    for x0 in nx.dfs_preorder_nodes(Tg, Tg_root):
        symbol= Tg.nodes[x0][event_attr]
        if symbol=='S':
            resolve_node= _resolve_s
        elif symbol=='P':
            resolve_node= _resolve_p
        elif nxt.is_leaf(Tg, x0):
            resolve_node= _resolve_l
        else:
            raise ValueError(f'unknown event "{symbol}"')
        n= resolve_node(x0, n, dad_dict[x0], *given)
    return T, mu_s, mu_inv

def get_reconciliation_map(Tg, Ts, event_attr= 'event', species_attr= 'species'):
    mu= {Tg.root: Ts.root}
    Q= nxt.BFS_graph(Tg, Tg.root)
    Q.pop(0)
    for x in Q:

        if nxt.is_leaf(Tg, x):
            y= nxt.LCA_color(Ts, {Tg.nodes[x][species_attr]}, color_attr= 'species')

        else:
            x_species= nxt.induced_colors(Tg, x, color_attr= species_attr)
            y= nxt.LCA_color(Ts, x_species, color_attr= 'species')

        mu[x]= y
    return mu

def recon_2_text(mu):
    text_mu= 'Tg_node\tTs_node\n'
    text_mu+= '\n'.join(('\t'.join(map(str, x)) for x in mu.items()))
    return text_mu

##################
#                #
# Internal usage #
#                #
##################

def _resolve_s(x0, n, dad, *given):
    # Obtain constant arguments
    Tg, Ts, T, mu, event_attr, copy_attrs, mu_s, mu_inv, dad_dict= given
    # Resolve
    L= {mu[x1] for x1 in Tg[x0]}
    d, Xi, Kappa= _inherit(mu[x0], L, n, dad, *given)##################### Quitar Xi
    # Update dad_dict
    for x1 in Tg[x0]:
        _update_ddict(x0, x1, *given)
    return n+d

def _resolve_p(x0, n, dad, *given):
    Tg, Ts, T, mu, event_attr, copy_attrs, mu_s, mu_inv, dad_dict= given
    # Resolve
    y0= mu[x0]
    _add_node(n, 'P', y0, dad, *given)
    d= 0
    n1= n+1
    for x1 in Tg[x0]:
        y1= mu[x1]
        if y0==y1:
            dad_dict[x1]= n
        else:
            d, Xi, Kappa= _inherit(y0, {y1}, n1, n, *given)
            n1+= d
            _update_ddict(x0, x1, *given)

    return n1

def _resolve_l(x0, n, dad, *given):
    Tg, Ts, T, mu, event_attr, copy_attrs, mu_s, mu_inv, dad_dict= given
    _add_leaf(n, Tg.nodes[x0][event_attr], mu[x0], dad, *given)
    T.nodes[n].update({attr : Tg.nodes[x0][attr] for attr in copy_attrs})
    return n+1

def _update_ddict(x0, x1, *given):
    Tg, Ts, T, mu, event_attr, copy_attrs, mu_s, mu_inv, dad_dict= given
    y= mu[x1]
    if y!=mu[x0]:
        y= nxt.get_dad(Ts, mu[x1])
    dad_dict[x1]= mu_inv[y]['S'][-1]

def _inherit(roh, lamb, n, dad, *given):
    """
    _inherit(roh, lamb, n, dad, *given)

    Simulates the process of inheriting a gene throug a sub-species tree defined by roh and lamb;
    rho is a node in the species tree, and lamb is a list of nodes y in the species tree such that
    rho >= y.
    The subtree is the subgraph of Ts induced by all the nodes y' such that 
    roh >= y' > y,
    and also the node roh.

    This function creates the node n on the genes tree as son of dad.
    Creates all the necessary descendants of n, usign as a guide the sub-species tree defined by roh and lab.
    Such descendants may be of type speciation and loss.

    Input:
    - roh: Node of the species tree where the process starts.
    - lamb: Set of nodes {y0, y1, ...} of the species tree where the process ends.
    - n: Nodo to create in the gene tree, corresponds to the speciation at roh.
    - dad: dad of n in the genes tree.
    """
    Tg, Ts, T, mu, event_attr, copy_attrs, mu_s, mu_inv, dad_dict= given
    # Inherit
    d= 0
    Xi, Kappa= _ancestry_graph(roh, lamb, *given)
    Q= [(roh, dad)]
    while len(Q)>0:
        n1= n+d
        y, dad= Q.pop(0)
        _add_node(n1, 'S', y, dad, *given)
        d+= 1 + _add_losses(y, Xi, n1, *given)
        Q+= [(y1, n1) for y1 in Kappa[y]]
    return d, Xi, Kappa

def _add_node(n, phi, y, dad, *given):
    """
    Agrega un nodo al árbol de genes, y guarda su información.

    Input:
    - n: nodo a crear.
    - phi: símbolo del nodo ('S', 'P', 'X', '.').
    - y: Nodo al que mapea n por el mapeo mu_s.
    - dad: Papa de n.
    """
    Tg, Ts, T, mu, event_attr, copy_attrs, mu_s, mu_inv, dad_dict= given
    # Add node and edge
    T.add_node(n, **{event_attr: phi})
    T.add_edge(dad, n)
    mu_s[n]= y
    mu_inv[y][phi]+= [n]

def _add_leaf(n, label, y, dad, *given):
    Tg, Ts, T, mu, event_attr, copy_attrs, mu_s, mu_inv, dad_dict= given
    # Add node and edge
    T.add_node(n, **{event_attr: label})
    T.add_edge(dad, n)
    mu_s[n]= y
    mu_inv[y]['.']+= [n]

def _ancestry_graph(y0, lamb, *given):
    Tg, Ts, T, mu, event_attr, copy_attrs, mu_s, mu_inv, dad_dict= given
    Kappa_nodes= {y0}
    Q= list(lamb-Kappa_nodes)
    while len(Q)>0:
        y= Q.pop(0)
        y_dad= nxt.get_dad(Ts, y)
        if y_dad not in Kappa_nodes:
            Kappa_nodes.add(y_dad)
            Q+= [y_dad]
    Xi_nodes= Kappa_nodes.union(lamb)
    # Create graphs
    Kappa= nx.induced_subgraph(Ts, Kappa_nodes)
    Xi= nx.induced_subgraph(Ts, Xi_nodes)
    return Xi, Kappa

def _add_losses(y, Xi, n, *given):
    Tg, Ts, T, mu, event_attr, copy_attrs, mu_s, mu_inv, dad_dict= given
    d= 0
    for y1 in set(Ts[y]) - set(Xi[y]):
        _add_node(n+1+d, 'X', y1, n, *given)
        d+= 1
    return d

####################
#                  #
# Standalone usage #
#                  #
####################

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog= 'reconciliate',
                                     description='Maps and resolves gene trees against species trees',
                                    )
    # Parameters for input graph
    ############################

    parser.add_argument('gene_trees',
                        type= str,
                        help= 'file containing gene trees in newick format.'
                       )

    parser.add_argument('species_tree',
                        type= str,
                        help= 'file containing a species tree in newick format.'
                       )

    parser.add_argument('-o', '--output_prefix',
                        type= str,
                        required=False,
                        help= 'prefix used for output files (default "tl_project").',
                        default= 'tl_project',
                       )

    args= parser.parse_args()

    # Process data
    ##############
    with open (args.gene_trees) as F:
        Tg= read_nhxx(F.readline().strip())
    with open (args.species_tree) as F:
        Ts= read_nhxx(F.readline().strip(), name_attr= 'species')

    Tr, mu, mu_inv= reconciliate(Tg, Ts, gene_attr= 'genes',
                                 species_attr= 'species',
                                 event_attr= 'label',
                                )

    nhx_r, text_mu= recon_2_text(Tr, mu)

    with open(f'{args.output_prefix}.resolved_tree.nhx', 'w') as F:
        F.write(nhx_r)
    with open(f'{args.output_prefix}.reconciliation_map.nhx', 'w') as F:
        F.write(text_mu)

    keys= ['S', 'P', 'X', '.']
    aux= pd.Series(mu_inv).apply(lambda X: pd.Series([','.join(map(str, X[k])) for k in keys])).reset_index()
    aux.columns= ['Ts_node'] + keys
    aux.to_csv(f'{args.output_prefix}.inverse_map.nhx' , sep= '\t', index= False)
