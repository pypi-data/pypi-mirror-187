need_params= {0: ['prt_path'],
              1: ['hit_list'],
              2: [],
             }

def check_args(args):
    d_args= vars(args)
    s0, s1= sorted(args.steps)
    missed= {}
    for step in [s0]:
        for param in need_params[step]:
            if d_args[param] == None:
                missed[step]= missed.get(step, []) + [param]

    if len(missed)>0:
        raise MissedData(f'{missed}')

    return s0, s1

def assign_id(T, idAttr= 'node_id'):
    for x in T:
        T.nodes[x][idAttr]= x


from .reconciliation import reconciliate, recon_2_text
from .error import InconsistentTrees
from tqdm import tqdm

def aux(Tg, Ts):
    try:
        Tr, mu_s, mu_inv= reconciliate(Tg, Ts, gene_attr= 'genes', species_attr= 'species', event_attr= 'label')
        return Tr, mu_s
    except InconsistentTrees:
        return '*'

def reconciliate_many(gTrees, Ts):
    recons= [aux(Tg, Ts) for Tg in tqdm(gTrees)]
    return recons

if __name__ == "__main__":
    from .in_out import read_tl_digraph, write_digraphs_list
    from .constants import _df_matches_cols, _default_f
    from .hug_free import build_graph, get_augmented_tree
    from .error import MissedData, ParameterError
    from .parse_prt import _parse
    from .common_tools import norm_path
    from .cBMG_tools import analyze_digraphs_list
    from .nhxx_tools import read_nhxx, get_nhx
    import pandas as pd
    import argparse
    import os

    parser = argparse.ArgumentParser(prog= 'revolutionhtl',
                                     description='Bioinformatics tool for the reconstruction of evolutionaty histories.',
                                    )
    # Parameters
    ############

    parser.add_argument('-steps',
                        help= 'list of steps to run (default: 1 2 3).',
                        type= int,
                        nargs= '*',
                        default= [1, 2, 3]
                       )

    parser.add_argument('-prt_path',
                        help= 'path to a directory containing proteinortho output files.',
                        type= str,
                        default = './',
                       )

    parser.add_argument('-gene_trees',
                        help= '.tsv file containing a .nhx for each line at column "tree"',
                        type= str,
                       )

    parser.add_argument('-species_tree',
                        help= '.nhx file containing a species tree.',
                        type= str,
                       )

    parser.add_argument('-hit_list',
                        help= '.tsv file containing hits.',
                        type= str,
                       )

    parser.add_argument('-og', '--orthogroup_column',
                        help= 'column in -hit_list and -gene_trees specifying orthogroups (default: OG).',
                        type= str,
                        default= 'OG',
                       )

    parser.add_argument('-o', '--output_prefix',
                        help= 'prefix used for output files (default "tl_project").',
                        type= str,
                        default= 'tl_project',
                       )

    parser.add_argument('-rod', '--recon_output_dir',
                        help= 'directory for reconciliation maps.',
                        type= str,
                        default= './',
                       )

    parser.add_argument('-f', '--f_value',
                        help= f'number between 0 and 1 used for the adaptative threshhold for best matches selection: f*max_bit_score. (default {_default_f}, see proteinortho paper for a deep explanation)',
                        type= float,
                        default= _default_f,
                       )

    args= parser.parse_args()

    if not args.recon_output_dir.endswith('/'):
        args.recon_output_dir+= '/'

    ################
    # Process data #
    ################

    print('\nREvolutionH-tl')

    allowed_steps= {0, 1, 2, 3}
    bad_steps= set(args.steps) - allowed_steps
    if len(bad_steps) > 0:
        raise ParameterError(f'Only steps 0, 1, 2, and 3 are allowed to be used in the parameter -steps. ')
    else:
        args.steps= sorted(set(args.steps))

    print(f'Running steps {", ".join(map(str, args.steps))}')

    # 0. Convert proteinortho output to a best-hit list
    #################################################
    if 0 in args.steps:
        print("\nStep 0: Convert proteinortho output to a best-hit list")
        print("----------------------------------------------------")
        if args.prt_path==None:
            raise MissedData('Step 0 needs a value for the parameter -prt_path')

        args.prt_path= norm_path(args.prt_path)
        opath= args.output_prefix+'.best_hits.tsv'
        _parse(args.prt_path, args.f_value, opath)
        print('This file will be used as input for step 1.')
        args.hit_list= opath

    # 1. Conver best hit graphs to cBMGs
    ####################################
    if 1 in args.steps:
        print("\nStep 1: Conver best-hit graphs to cBMGs")
        print("---------------------------------------")
        if args.hit_list==None:
            raise MissedData('Step 1 needs a value for the parameter -hit_list')

        print('Reading hit graphs...')
        G= read_tl_digraph(args.hit_list, og_col= args.orthogroup_column)
        print('Editing to best match graphs (cBMGs)...')
        G1= G.progress_apply(lambda X: build_graph(X, color_attr= 'species'))
        opath= f'{args.output_prefix}.cBMGs.tsv'
        write_digraphs_list(G1, opath)#, n_attrs= ['gene', 'species'])
        print(f'Best match graphs successfully written to {opath}')
        print('This file will be used as input for step 2.')
        args.hit_list= opath

    # 2. Conver cBMGs to gene trees
    ###############################
    if 2 in args.steps:
        print("\nStep 2: Reconstruct gene trees")
        print("------------------------------")
        if args.hit_list==None:
            raise MissedData('Step 2 needs a value for the parameter -hit_list')

        print('Reading best match graphs...')
        G= read_tl_digraph(args.hit_list, og_col= args.orthogroup_column)

        print('Reconstructing gene trees...')
        df= analyze_digraphs_list(G, species_attr= 'species', gene_attr= 'accession')

        print('Labeling gene tree nodes with evolutionary events...')
        df.tree= df.tree.progress_apply( lambda x: get_augmented_tree(x, 'accession', 'species') )
        df.tree= df.tree.apply(lambda x: get_nhx(x, root= 1, name_attr= 'accession'))

        opath= f'{args.output_prefix}.gene_trees.tsv'
        df.to_csv(opath, sep='\t', index= False)
        print(f'Gene trees successfully written to {opath}')
        print('This file will be used as input for step 3.')
        args.gene_trees= opath

    # 3. Reconciliate gene trees and species tree
    ##############################################
    if 3 in args.steps:
        print("\nStep 3: Reconciliation of gene species trees")
        print("-------------------------------------------")
        if args.gene_trees==None:
            raise MissedData('Step 2 needs a value for the parameter -gene_trees')
        if args.species_tree==None:
            raise MissedData('Step 2 needs a value for the parameter -species_tree')
        if not os.path.isdir(args.recon_output_dir):
            raise ValueError(f'-recon_output_dir {args.recon_output_dir}: : No such directory')

        print('Reading trees...')
        gTrees= pd.read_csv(args.gene_trees, sep= '\t').set_index(args.orthogroup_column).tree.apply(read_nhxx)
        with open(args.species_tree) as F:
            sTree= read_nhxx(''.join( F.read().strip().split('\n') ),
                             name_attr= 'species')
            assign_id(sTree)

        print('Reconciling trees...')
        recons= reconciliate_many(gTrees, sTree)

        # Write resolved trees
        df_r= pd.DataFrame([(idx, X) if X == '*' else (idx, X[0])
                            for idx, X in zip(gTrees.index, recons)],
                           columns= [args.orthogroup_column, 'Tree'])
        df_r.Tree.apply(lambda x: x if x=='*' else assign_id(x))
        df_r.Tree= df_r.Tree.apply(lambda x: x if x=='*' else get_nhx(x, name_attr= 'label', root= 1))

        opath= f'{args.output_prefix}.resolved_trees.tsv'
        df_r.to_csv(opath, sep= '\t', index= False)
        print(f'Resolved gene trees were successfully written to {opath}')

        # Write mu maps
        for idx, X in zip(gTrees.index, recons):
            if X!='*':
                text_mu= recon_2_text(X[1])
                opath= f'{args.recon_output_dir}{args.output_prefix}.{idx}.reconciliation_map.tsv'
                with open(opath, 'w') as F:
                    F.write(text_mu)
        print(f'Reconciliation maps were successfully written at {args.recon_output_dir}')

        # Write labeled species tree
        nhx_s= get_nhx(sTree, name_attr= 'species', root= 1)
        opath= f'{args.output_prefix}.labeled_species_tree.nhxx'
        with open(opath, 'w') as F:
            F.write(nhx_s)
        print(f'Indexed species tree successfully written to {opath}')
#


















