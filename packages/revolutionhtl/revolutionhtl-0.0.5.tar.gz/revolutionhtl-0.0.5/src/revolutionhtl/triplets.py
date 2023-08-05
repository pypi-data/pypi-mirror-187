from . import nxTree as nxt
import networkx as nx
from itertools import chain, product, combinations

def get_triplets(tree, event='event', color= 'color', root_event= 'S'):
    I= {} # Dictionary for induced leafs
    R= set() # set for tree triplets
    for x in nx.dfs_postorder_nodes(tree):
        if nxt.is_leaf(tree, x):
            I[x]= { tree.nodes[x][color] }
        else:
            if x!=tree.root:
                I[x]= set( chain.from_iterable((I[x1] for x1 in tree[x])) ) #### Acomodar esta linea: que no se calcule en la raíz
            if tree.nodes[x][event] == root_event:
                R.update( _get_triples_from_root(tree, x, I) )
    R= [_construct_triplet( X, color ) for X in R]
    return R

def _get_triplets_from_groups(tree, x_out, x_in, I):
    P= combinations( I[x_in], 2 )
    R= set(( (a, frozenset([b,c]))
             for a,(b,c) in product( I[x_out], P ) if a!=b and a!=c
          ))
    return R

def _get_triples_from_root(tree, node, I):
    R= set()
    for x0, x1 in combinations(tree[node], 2):
        R.update( _get_triplets_from_groups(tree, x0, x1, I) )
        R.update( _get_triplets_from_groups(tree, x1, x0, I) )
    return R

def _construct_triplet(topology, color):
    a, (b, c)= topology
    T= nx.DiGraph()
    T.root= 0
    T.add_nodes_from([0,1])
    for i,x in enumerate((a, b, c)):
        T.add_node(i+2, **{color: x})
    T.add_edges_from(( (0,1), (0,2), (1,3), (1,4)))
    return T
