import os
import time
import argparse
import torch


def get_options(args=None):

    parser = argparse.ArgumentParser(description="LSGO-platform") 

    # Basic settings
    parser.add_argument('--device', default='cpu', choices=['cpu','cuda'], help='device to use ')

    # CC settings

    # VI_based_Dec settings
    parser.add_argument('--batch_size', type=int, default=5096, help='batch size for ISM') # DG2_parallel

    
    # # CMAES (basic_env) settings
    # parser.add_argument('--backbone', default='cmaes', choices=['cmaes'], help='backbone algorithm')
    # parser.add_argument('--m', type=int, default=10, help='number of subgroups')
    # parser.add_argument('--subspace_dim', type=int, default=100, help='dimensionality of the subspace')
    # parser.add_argument('--sigma', type=float, default=2, help='sigma for cmaes')
    # parser.add_argument('--sub_popsize', type=int, default=20, help='population size of each subgroup')
    # parser.add_argument('--max_fes', type=int, default=1.02e6, help='maximum number of function evaluations')
    # parser.add_argument('--subFEs', type=int, default=1000, help='minimum number of iterations for each subgroup')
    # parser.add_argument('--output_init_cma_info', type=bool, default=False, help='output the initial cma info')
    # parser.add_argument('--initFEs', type=int, default=1000, help='number of iterations for initialization')
    
    opts = parser.parse_args(args)

    return opts