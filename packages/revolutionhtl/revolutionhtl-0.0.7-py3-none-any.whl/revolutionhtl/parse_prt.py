import pandas as pd
import os
import numpy as np
import networkx as nx
from itertools import chain
from tqdm import tqdm
tqdm.pandas()

from .common_tools import norm_path
from .in_out import create_cBMG, tl_digraph_from_pandas

####################
#                  #
# Some parameters  #
#                  #
####################

from .constants import _df_matches_cols, _default_f

####################
#                  #
# Parse functions  #
#                  #
####################

def parse_prt_best_hits(path, f_value):
    """
    Returns a DataFrame of best hits obtained from proteinortho files
    """
    print('Reading .proteinortho.tsv file and hits directory...')
    # Check if all files are ok
    prt_path= _check_files(path)
    # Load prt orthogroups
    df_prt= parse_prt_orthogroups(prt_path)
    # Load prt hits
    df_hits= parse_prt_hits(path, best_hit_dir= f'proteinortho_cache_{_get_prt_projectname(prt_path)}')
    # Identify best hit scores w.r.t. query_gene and target_species
    w_x_B= max_hit_scores(df_hits)
    # Apply dynamic threshold for best hit selection
    print('Selecting best hits by dynamic threshold...')
    df_best_hits= select_best_hits(df_hits, f_value, w_x_B)
    # Return the subset of hits for each orthogroup
    print('Filtering best hits by orthogroup...')
    F= lambda row: _get_orthogroup_hits(row, df_best_hits)
    return pd.concat( df_prt.progress_apply(F, axis= 1).values )

def parse_prt_orthogroups(orthogroups_file, clear_singletones= True):
    df_prt= pd.read_csv(orthogroups_file, sep= '\t')
    species_cols= list(map(lambda x: x.split('.')[0], df_prt.columns[3:]))
    df_prt.columns= ['Species', 'Genes', 'Alg.-Conn.']+species_cols
    df_prt[species_cols]= df_prt[species_cols].apply(lambda X: X.apply(lambda x: set(x.split(','))))
    df_prt.index.name= 'OG'
    if clear_singletones:
        df_prt= _clean_prt(df_prt)
    return df_prt

def parse_prt_hits(prt_files_path,
                   best_hit_dir= '.',
                   best_hit_file_ext= '.diamond',
                   Query_accession= 'Query_accession',
                   pd_params= dict(names= _df_matches_cols, sep= '\t'),
                  ):
    """
    Returns a DataFrame of hits obtained from proteinortho files
    """
    best_hit_dir= norm_path(norm_path(prt_files_path)+best_hit_dir)

    df= pd.concat((_read_bh_table(f'{best_hit_dir}/{file}',
                                 pd_params,
                                 Query_accession= Query_accession
                                 )
                   for file in os.listdir(best_hit_dir) if file.endswith(best_hit_file_ext)
                  ))
    return df

def _read_bh_table(file, pd_params, Query_accession):
    """
    Para que funcione, el archivo debe ser llamado algo así como: 
    H0.fa.vs.H10.fa.diamond
    """
    species= file.split('/')[-1].split('.')
    species= species[0], species[3]
    df= pd.read_csv(file, **pd_params)
    columns= list(df.columns)
    df['Query_species']= species[0]
    df['Target_species']= species[1]
    return df[ ['Query_species', 'Target_species']+columns ]

def max_hit_scores(df_hits,
                   Query_accession= 'Query_accession',
                   Target_species= 'Target_species',
                   Score= 'Bit_score',
                  ):
    return df_hits.groupby([Query_accession, Target_species])[Score].max()

def select_best_hits(df, f_value, w_x_B, a= 'Query_accession', b= 'Target_accession', species_b= 'Target_species'):
    """
    Obtain the subset of hits that pass the dynamic threshold of proteinortho.
    """
    is_best_hit= lambda row: row.Bit_score >= f_value * w_x_B[ row.Query_accession, row.Target_species ]
    mask= df.progress_apply(is_best_hit, axis= 1)
    return df.loc[mask]

def _get_orthogroup_hits(row, df_hits):
    """
    Input:
    - row: A row from an orthogroups table (.proteinortho.tsv)
    - df_hits: table of best hits (Query_gene -> Target_gene)
    """
    genes= set(chain.from_iterable(row))
    mask= (df_hits.Query_accession.isin(genes)) & (df_hits.Target_accession.isin(genes))
    og_hits= df_hits[ mask ]
    og_hits['OG']= row.name
    return og_hits

def _clean_prt(df_prt):
    mask= df_prt.Species > 1
    species= list(df_prt.columns[3:])
    return df_prt.loc[mask, species]

def read_symBets(prt_graph_path, prt_path):
    # Loads symBets (proteinortho-graph)
    symBets= pd.read_csv(prt_graph_path, sep='\t', comment= '#', names= ['a',
                                                                         'b',
                                                                         'evalue_ab',
                                                                         'bitscore_ab',
                                                                         'evalue_ba',
                                                                         'bitscore_ba',
                                                                        ])

    # Loads proteiortho table containng orthogroups
    df_prt= parse_prt_orthogroups(prt_path)

    # For each ortogroup obtain the orthology relations of all the genes in such orthogroup
    F= lambda x: _get_orthos(x, symBets)
    df_edges= pd.concat( list(df_prt.apply(F, axis= 1)) )

    return df_edges

def _get_orthos(row, symBets):
    orths= pd.concat((_search_orths(row, X, symBets) for X in row.index))
    orths['OG']= row.name
    return orths.set_index('OG').sort_index()

def _search_orths(row, species, symBets):
    mask= lambda x: symBets[ (symBets.a==x) | (symBets.b==x) ]
    return pd.concat(map(mask, row[species]))

####################
#                  #
# General functions#
#                  #
####################

def _check_files(path):
    prt_path= [x for x in os.listdir(path) if x.endswith('.proteinortho.tsv')]
    if len(prt_path)==1:
        prt_path= path + prt_path[0]
    else:
        raise ValueError(f'There is more than one ".proteinortho.tsv" file at {path}')
    return prt_path

def _get_prt_projectname(prt_file):
    return prt_file.split('/')[-1].split('.')[0]

####################
#                  #
# Graph functions  #
#                  #
####################

def parse_prt_project_bmgs(path, f_value):
    df= parse_prt_best_hits(path, f_value)
    X= tl_digraph_from_pandas(df, og_col= 'OG')
    return X

####################
#                  #
# Standalone usage #
#                  #
####################


def _parse(path, f_value, opath):
    df= parse_prt_best_hits(path, f_value)
    df.reset_index().to_csv(opath, sep='\t', index= False)
    print(f'Best hits were successfully written to {opath}')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(prog= 'parse_prt',
                                     description='Converts proteinortho outputs to edges list of best hits.',
                                    )
    # Parameters for input graph
    ############################

    parser.add_argument('prt_path',
                        type= str,
                        help= 'Path to a directory containing proteinortho files. For more information see:'
                       )

    parser.add_argument('-o', '--output_prefix',
                        type= str,
                        required=False,
                        help= 'prefix used for output files (default "prt_revolutionhtl").',
                        default= 'prt_revolutionhtl',
                       )

    parser.add_argument('-f', '--f_value',
                        type= float,
                        required=False,
                        help= f'Number between 0 and 1 (default {_default_f}), defines the adaptative threshhold for best matches: f*max_bit_score. (see proteinortho paper for a deep explanation)',
                        default= _default_f,
                       )

    args= parser.parse_args()

    # Process data
    ##############
    args.prt_path= norm_path(args.prt_path)
    opath= args.output_prefix+'.best_hits.tsv'
    _parse(args.prt_path, args.f_value, opath)


