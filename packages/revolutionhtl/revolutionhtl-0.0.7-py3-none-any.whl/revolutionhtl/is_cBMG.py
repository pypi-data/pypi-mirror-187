from .cBMG_tools import analyze_digraphs_list
from .common_tools import norm_path
import pandas as pd

####################
#                  #
# Standalone usage #
#                  #
####################

if __name__ == "__main__":

    import argparse
    import os
    from .parse_prt import parse_prt_project_bmgs
    from .in_out import read_tl_digraph

    parser = argparse.ArgumentParser(prog= 'is_cBMG',
                                     description='Determines if a directed graph is a coloured Best Match Graph (cBMG).',
                                    )
    # Parameters for input graph
    ############################

    parser.add_argument('edges_list',
                        type= str,
                        #required=False,
                        help= '.tsv file containing directed edges.'
                       )

    parser.add_argument('-F', '--edges_format',
                        type= str,
                        required=False,
                        help= 'Format of the edges list (default "prt"). For more information see:...',
                        choices= ['prt', 'tl'], # 'prt_pre_parse'
                        default= 'tl',
                       )

    parser.add_argument('-o', '--output_prefix',
                        type= str,
                        required=False,
                        help= 'prefix used for output files (default "tl_iscBMG").',
                        default= 'tl_iscBMG',
                       )

    args= parser.parse_args()

    # Input data
    #############
    print('Reading hit list...')
    if args.edges_format=='prt':
        args.edges_list= norm_path(args.edges_list)
        #> Añadir opción para guardar o no tabla parseada
        G= parse_prt_project_bmgs(args.edges_list, f_value= 0.9)
    elif args.edges_format=='tl':
        G= read_tl_digraph(args.edges_list, og_col= 'OG')
    else:
        #> Leer tabla de aristas parseada
        raise ValueError(f'Edges format "{args.edges_format}" not valid.')

    # Analyze
    #########
    print('Analyzing hit graphs...')
    df= analyze_digraphs_list(G)
    opath= args.output_prefix + '.csv'
    df.to_csv(opath, sep='\t', index= False)
    print(f'Output successfully writen to {opath}')

