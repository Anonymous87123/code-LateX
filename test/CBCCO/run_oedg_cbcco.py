import argparse
import os
import sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Benchmarks.cec2013lsgo.cec2013 import Benchmark as CEC13Benchmark
from Algorithms.CC.CBCC.CBCCO.cbcco import CBCCO


def main():
    parser = argparse.ArgumentParser(description="Run CBCCO with selectable grouping on CEC2013 LSGO")
    parser.add_argument('--func_id', type=int, default=13)
    parser.add_argument('--func_ids', type=int, nargs='+',
                        help='list of function ids to run (overrides --func_id)')
    parser.add_argument('--run_all', action='store_true',
                        help='run all benchmark functions (overrides --func_id/--func_ids)')
    parser.add_argument('--grouping', type=str, default='OEDG', choices=['DG2', 'OEDG'],
                        help='grouping method used inside CBCCO')
    parser.add_argument('--device', default='cpu', choices=['cpu', 'cuda'])
    parser.add_argument('--maxFEs', type=float, default=5e5)
    parser.add_argument('--print_interval', type=int, default=5000,
                        help='print progress every N FEs (0 = no print)')
    parser.add_argument('--out_dir', type=str, default=None,
                        help='directory to store outputs when running multiple functions')
    parser.add_argument('--out', type=str, default=None)
    args = parser.parse_args()

    bench = CEC13Benchmark(device=args.device, output_format='numpy')
    if args.run_all:
        func_ids = list(range(1, bench.get_num_functions() + 1))
    elif args.func_ids:
        func_ids = args.func_ids
    else:
        func_ids = [args.func_id]

    for fid in func_ids:
        f_obj = bench.get_function(fid)
        info = bench.get_info(fid)
        info['fNum'] = fid

        cfg = {
            'maxFEs': args.maxFEs,
            'initial_fEvalNum': 0,
            'overlap_rate': 0.3,
            'cbd_test_generations': 10,
            'optimizer': 'CMAES',
            'grouping': args.grouping.upper(),
        }

        cbcco = CBCCO(f_obj, info, cfg)

        # monkey-patch set_output_values to print phase-aware progress
        if args.print_interval and args.print_interval > 0:
            orig_set_output_values = cbcco.set_output_values

            def set_output_values_with_print():
                orig_set_output_values()
                fe = cbcco.alg['fEvalNum']
                if fe % args.print_interval == 0:
                    bestf = cbcco.alg['bestGlobal']['f']
                    phase = cbcco.alg.get('phase', 'UNKNOWN')
                    try:
                        print(f'[{phase}] f{cbcco.prob["fNum"]} FEs={fe} best={bestf:.5e}')
                    except Exception:
                        print(f'[{phase}] f{cbcco.prob["fNum"]} FEs={fe} best={bestf}')

            cbcco.set_output_values = set_output_values_with_print

        # explicit two-stage run: CBD then CBO
        cbcco.alg['phase'] = 'CBD'
        GS, OS = cbcco._run_cbd()
        cbcco.groups = GS
        cbcco.prob['groups'] = cbcco.groups
        cbcco._init_group_states()

        cbcco.alg['phase'] = 'CBO'
        cbcco._run_cbo()

        best = cbcco.alg['bestGlobal']
        cbcco_fes = cbcco.alg['fEvalNum']
        decomp_fes = getattr(cbcco, 'decomposition_fes', 0)
        decomp_info = getattr(cbcco, 'decomposition_info', {})

        out_name = f"cbcco_{args.grouping.upper()}_F{fid}.txt"
        if args.out_dir:
            os.makedirs(args.out_dir, exist_ok=True)
            out_path = os.path.join(args.out_dir, out_name)
        elif args.out and len(func_ids) == 1:
            out_path = args.out
        elif args.out and len(func_ids) > 1:
            os.makedirs(args.out, exist_ok=True)
            out_path = os.path.join(args.out, out_name)
        else:
            out_path = os.path.join(ROOT, out_name)

        with open(out_path, "w") as f:
            grouping_used = decomp_info.get('method', args.grouping.upper())
            f.write(f"Function: F{fid}\n")
            f.write(f"Grouping_method: {grouping_used}\n")
            if 'subcomponents' in decomp_info:
                f.write(f"Subcomponents: {decomp_info['subcomponents']}\n")
            if 'overlaps' in decomp_info:
                f.write(f"Overlaps: {decomp_info['overlaps']}\n")
            if 'GS_initial' in decomp_info:
                f.write(f"Initial_GS: {decomp_info['GS_initial']}\n")
            if 'OS_initial' in decomp_info:
                f.write(f"Initial_OS: {decomp_info['OS_initial']}\n")
            f.write(f"Decomposition_FEs: {decomp_fes}\n")
            f.write(f"CBCCO_FEs: {cbcco_fes}\n")
            f.write(f"Best_fitness: {best['f']}\n")


if __name__ == '__main__':
    main()
