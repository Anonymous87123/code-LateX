import numpy as np


class CCFR2_AEPD:

    def __init__(self, fun, info, cfg):
        self.fun = fun
        self.info = info
        self.cfg = cfg

        dimension = info['dimension']
        self.optimizer = cfg.get('optimizer', 'CMAES').upper()
        if self.optimizer != 'CMAES':
            raise ValueError(f"CCFR2-AEPD currently supports only CMAES optimizer, got {self.optimizer}")

        if 'seed' in cfg and cfg['seed'] is not None:
            np.random.seed(cfg['seed'])

        self.verbose = cfg.get('verbose', False)

        groups = info.get('groups', [])
        self.prob = {
            'betterSign': -1,
            'D': dimension,
            'fNum': info.get('fNum', 1),
            'objN': info.get('objN', 1),
            'lb': np.full(dimension, info['lower'], dtype=float),
            'ub': np.full(dimension, info['upper'], dtype=float),
            'groups': [np.asarray(g, dtype=int) for g in groups]
        }

        initial_fevals = int(info.get('initial_fEvalNum', cfg.get('initial_fEvalNum', 0)))
        must_output_points = np.asarray(info.get('mustOutputPoints', cfg.get('mustOutputPoints', [])), dtype=int)

        self.alg = {
            'outputValues': None,
            'fEvalNumInitial': initial_fevals,
            'fEvalNum': initial_fevals,
            'bestGlobal': None,
            'Max_FEs': int(cfg.get('maxFEs', 3_000_000)),
            'mustOutputPoints': must_output_points,
            'isTerminate': False
        }

        self.group_index_global = None
        self.evol_state_group = []
        self.delta_fit_global = None
        self.delta_fit_regen = None
        self._initialise_group_states()

    def run(self):
        group_count = len(self.prob['groups'])
        if group_count == 0:
            raise ValueError("No variable groups provided for CCFR2-AEPD.")

        self.delta_fit_global = np.full(group_count, np.nan, dtype=float)
        self.delta_fit_regen = np.full(group_count, np.nan, dtype=float)

        self._evolve_groups(list(range(group_count)))

        while not self.alg['isTerminate']:
            if np.all(np.isnan(self.delta_fit_global)):
                rand_threshold = 1.0
                candidate_indices = np.flatnonzero(~np.isnan(self.delta_fit_regen))
            else:
                max_delta = np.nanmax(self.delta_fit_global)
                logical = self.delta_fit_regen > max_delta
                rand_threshold = np.count_nonzero(logical) / logical.size if logical.size else 0.0
                candidate_indices = np.flatnonzero(logical)

            if np.random.rand() < rand_threshold and candidate_indices.size > 0:
                sorted_idx = np.argsort(self.delta_fit_regen[candidate_indices])[::-1]
                selected = candidate_indices[sorted_idx].tolist()
            else:
                available = np.flatnonzero(~np.isnan(self.delta_fit_global))
                if available.size == 0:
                    break
                if np.isclose(np.nanmin(self.delta_fit_global), np.nanmax(self.delta_fit_global), equal_nan=False):
                    selected = available.tolist()
                else:
                    selected = [int(np.nanargmax(self.delta_fit_global))]

            self._evolve_groups(selected)

    def _initialise_group_states(self):
        self.evol_state_group = []
        for group in self.prob['groups']:
            state = {
                'first': True,
                'bestIndiLastRegenPop': None,
                'deltaFitRegenPop': [],
                'unChangeGenNDim': None,
                'threshStdDimInitial': None,
                'regenedPop': False,
                'needRegenPop': False,
                'meanDim': None,
                'stdDim': None,
                'threshStdDim': None,
                # CMA-ES state placeholders
                'sublambda': None,
                'submu': None,
                'subweights': None,
                'submueff': None,
                'subcc': None,
                'subcs': None,
                'subc1': None,
                'subcmu': None,
                'subdamps': None,
                'subpc': None,
                'subps': None,
                'subB': None,
                'subD': None,
                'subC': None,
                'subinvsqrtC': None,
                'subsigma': None,
                'subeigeneval': None,
                'subchiN': None,
                'subxmean': None,
                'iterationNum': 0,
                'subcounteval': 0
            }
            self.evol_state_group.append(state)

    def _evolve_groups(self, indices):
        if not indices:
            return

        for idx in indices:
            self.group_index_global = int(idx)
            self._cmaes_group(self.prob['groups'][idx])

        mask_global = (self.delta_fit_global != 0) & ~np.isnan(self.delta_fit_global)
        mask_regen_zero = (self.delta_fit_regen == 0) & ~np.isnan(self.delta_fit_regen)
        mask_regen_nonzero = (self.delta_fit_regen != 0) & ~np.isnan(self.delta_fit_regen)

        if np.any(mask_global) or np.any(mask_regen_nonzero):
            pool_values = []
            if np.any(mask_global):
                pool_values.append(self.delta_fit_global[mask_global])
            if np.any(mask_regen_nonzero):
                pool_values.append(self.delta_fit_regen[mask_regen_nonzero])

            if pool_values:
                min_value = np.min(np.concatenate(pool_values))
                if np.any(mask_regen_zero):
                    self.delta_fit_regen[mask_regen_zero] = min_value * 0.9

    def _cmaes_group(self, group_dim_index):
        group_dim_index = np.asarray(group_dim_index, dtype=int)
        dim_count = group_dim_index.size

        lb_vec = self.prob['lb'][group_dim_index]
        ub_vec = self.prob['ub'][group_dim_index]

        state = self.evol_state_group[self.group_index_global]

        if state['first']:
            subxmean = lb_vec + (ub_vec - lb_vec) / 2.0
            subsigma = 0.3 * (ub_vec - lb_vec)

            sublambda = 4 + int(np.floor(3 * np.log(dim_count)))
            submu = sublambda / 2.0
            submu_floor = int(np.floor(submu))
            weights = np.log(submu + 0.5) - np.log(np.arange(1, submu_floor + 1))
            weights = weights / np.sum(weights)
            submueff = np.sum(weights) ** 2 / np.sum(weights ** 2)

            subcc = (4 + submueff / dim_count) / (dim_count + 4 + 2 * submueff / dim_count)
            subcs = (submueff + 2) / (dim_count + submueff + 5)
            subc1 = 2 / ((dim_count + 1.3) ** 2 + submueff)
            subcmu = min(1 - subc1, 2 * (submueff - 2 + 1 / submueff) / ((dim_count + 2) ** 2 + submueff))
            subdamps = 1 + 2 * max(0, np.sqrt((submueff - 1) / (dim_count + 1)) - 1) + subcs

            subpc = np.zeros(dim_count)
            subps = np.zeros(dim_count)
            subB = np.eye(dim_count)
            subD = np.ones(dim_count)
            subC = subB @ np.diag(subD ** 2) @ subB.T
            subinvsqrtC = subB @ np.diag(subD ** -1) @ subB.T

            iteration_num = 0
            subcounteval = 0
            subeigeneval = 0
            subchiN = dim_count ** 0.5 * (1 - 1 / (4 * dim_count) + 1 / (21 * dim_count ** 2))
        else:
            sublambda = state['sublambda']
            submu_floor = state['submu']
            weights = state['subweights']
            submueff = state['submueff']
            subcc = state['subcc']
            subcs = state['subcs']
            subc1 = state['subc1']
            subcmu = state['subcmu']
            subdamps = state['subdamps']
            subpc = state['subpc']
            subps = state['subps']
            subB = state['subB']
            subD = state['subD']
            subC = state['subC']
            subinvsqrtC = state['subinvsqrtC']
            subsigma = state['subsigma']
            subeigeneval = state['subeigeneval']
            subchiN = state['subchiN']
            subxmean = state['subxmean']
            iteration_num = state['iterationNum']
            subcounteval = state['subcounteval']

            if state['needRegenPop']:
                subD = np.ones(dim_count)
                subeigeneval = subcounteval
                if self.alg['bestGlobal'] is not None:
                    subxmean = self.alg['bestGlobal']['x'][group_dim_index].copy()
                else:
                    subxmean = lb_vec + (ub_vec - lb_vec) / 2.0
                subsigma = 0.1 * (ub_vec - lb_vec)

                state['deltaFitRegenPop'] = []
                state['unChangeGenNDim'] = None
                state['threshStdDimInitial'] = None
                state['regenedPop'] = True
            else:
                state['regenedPop'] = bool(state['regenedPop'])

        arfitness = np.full(sublambda, np.nan)

        if self.alg['bestGlobal'] is None:
            rand_individual = self.prob['lb'] + (self.prob['ub'] - self.prob['lb']) * np.random.rand(self.prob['D'])
            arx = np.tile(rand_individual.reshape(-1, 1), (1, sublambda))
            self._evaluate_fit(rand_individual)
        else:
            arx = np.tile(self.alg['bestGlobal']['x'].reshape(-1, 1), (1, sublambda))

        best_indi_last_change = self.alg['bestGlobal']['x'].copy() if self.alg['bestGlobal'] is not None else None
        std_delta_fit = None
        delta_fit_set = []
        f_eval_last_best_change = self.alg['fEvalNum']
        fit_last_best_change = self.alg['bestGlobal']['f'] if self.alg['bestGlobal'] is not None else None
        f_eval_before_evol = self.alg['fEvalNum']
        best_fit_before_evol = self.alg['bestGlobal']['f'] if self.alg['bestGlobal'] is not None else None

        while not self.alg['isTerminate']:
            iteration_num += 1

            for k in range(sublambda):
                z = np.random.randn(dim_count)
                mysigma = subB @ (subD * z)
                mysigma = subsigma * mysigma

                limit_mask = np.abs(mysigma) > (ub_vec - lb_vec)
                if np.any(limit_mask):
                    mysigma[limit_mask] = (ub_vec[limit_mask] - lb_vec[limit_mask]) * np.random.randn(np.count_nonzero(limit_mask))

                temp_x = subxmean + mysigma
                out_of_bounds = (temp_x < lb_vec) | (temp_x > ub_vec)
                while np.any(out_of_bounds):
                    idx = np.nonzero(out_of_bounds)[0]
                    local_B = subB[np.ix_(idx, idx)]
                    local_D = subD[idx]
                    new_z = np.random.randn(idx.size)
                    mysigma[idx] = subsigma[idx] * (local_B @ (local_D * new_z))

                    limit_mask = np.abs(mysigma) > (ub_vec - lb_vec)
                    if np.any(limit_mask & out_of_bounds):
                        mask = limit_mask & out_of_bounds
                        mysigma[mask] = (ub_vec[mask] - lb_vec[mask]) * np.random.randn(np.count_nonzero(mask))

                    temp_x[out_of_bounds] = subxmean[out_of_bounds] + mysigma[out_of_bounds]
                    out_of_bounds = (temp_x < lb_vec) | (temp_x > ub_vec)

                arx[group_dim_index, k] = temp_x
                arfitness[k] = self._evaluate_fit(arx[:, k])
                subcounteval += 1

                if self.alg['isTerminate']:
                    break

            if self.alg['isTerminate']:
                break

            if state.get('regenedPop', False):
                best_in_pop = False
                for i in range(sublambda):
                    if np.array_equal(self.alg['bestGlobal']['x'][group_dim_index], arx[group_dim_index, i]):
                        best_in_pop = True
                        break
                if not best_in_pop:
                    worst_idx = int(np.argmax(arfitness))
                    arx[group_dim_index, worst_idx] = self.alg['bestGlobal']['x'][group_dim_index]
                    arfitness[worst_idx] = self.alg['bestGlobal']['f']

            order = np.argsort(arfitness)
            arfitness = arfitness[order]
            elites = order[:submu_floor]

            subxold = subxmean.copy()
            subxmean = arx[group_dim_index][:, elites] @ weights

            subps = (1 - subcs) * subps + np.sqrt(subcs * (2 - subcs) * submueff) * (subinvsqrtC @ ((subxmean - subxold) / subsigma))
            norm_ps_sq = np.sum(subps ** 2)
            hsig_lhs = norm_ps_sq / (1 - (1 - subcs) ** (2 * subcounteval / sublambda))
            subhsig = hsig_lhs / dim_count < (2 + 4 / (dim_count + 1))

            subpc = (1 - subcc) * subpc + subhsig * np.sqrt(subcc * (2 - subcc) * submueff) * ((subxmean - subxold) / subsigma)

            artmp = ((1.0 / subsigma).reshape(-1, 1)) * (arx[group_dim_index][:, elites] - subxold.reshape(-1, 1))
            subC = ((1 - subc1 - subcmu) * subC +
                    subc1 * (np.outer(subpc, subpc) + (1 - subhsig) * subcc * (2 - subcc) * subC) +
                    subcmu * artmp @ np.diag(weights) @ artmp.T)

            subsigma = subsigma * np.exp((subcs / subdamps) * (np.linalg.norm(subps) / subchiN - 1))
            subsigma = np.clip(subsigma, np.finfo(float).tiny, ub_vec - lb_vec)

            if subcounteval - subeigeneval > sublambda / (subc1 + subcmu) / dim_count / 10:
                subeigeneval = subcounteval
                subC = np.triu(subC) + np.triu(subC, 1).T

                if not (np.any(np.isnan(subC)) or np.any(np.isinf(subC))):
                    eigvals, eigvecs = np.linalg.eigh(subC)
                    eigvals = np.clip(np.abs(eigvals), np.finfo(float).tiny, np.finfo(float).max)
                    subD = np.sqrt(eigvals)
                    subB = eigvecs
                    subinvsqrtC = subB @ np.diag(1.0 / subD) @ subB.T

            if self.verbose and self.alg['bestGlobal'] is not None:
                print(f"{self.prob['fNum']}\t{int(self.alg['fEvalNum'])}\t{self.group_index_global}\t{self.alg['bestGlobal']['f']:.10e}")

            stop_evolution = False
            if best_indi_last_change is not None and self.alg['bestGlobal'] is not None:
                changed_dims = np.count_nonzero(best_indi_last_change[group_dim_index] != self.alg['bestGlobal']['x'][group_dim_index])
                non_zero_std = np.count_nonzero(np.std(arx[group_dim_index, :], axis=1, ddof=0) != 0)
                if changed_dims >= non_zero_std:
                    eval_diff = self.alg['fEvalNum'] - f_eval_last_best_change
                    if eval_diff > 0:
                        delta_fit = abs(fit_last_best_change - self.alg['bestGlobal']['f']) / eval_diff
                        delta_fit_set.append(delta_fit)
                        prev_std = std_delta_fit if std_delta_fit is not None else np.inf
                        std_delta_fit = np.std(delta_fit_set, ddof=0) if len(delta_fit_set) > 0 else None
                        if len(delta_fit_set) > 2 and std_delta_fit is not None and std_delta_fit < prev_std:
                            stop_evolution = True
                    best_indi_last_change = self.alg['bestGlobal']['x'].copy()
                    fit_last_best_change = self.alg['bestGlobal']['f']
                    f_eval_last_best_change = self.alg['fEvalNum']

            pop = arx.T
            is_regen_pop = self._determine_regen_pop(pop, group_dim_index)
            state['needRegenPop'] = bool(is_regen_pop)

            if stop_evolution or is_regen_pop:
                eval_diff_total = self.alg['fEvalNum'] - f_eval_before_evol
                if eval_diff_total <= 0:
                    eval_diff_total = 1.0
                delta_fit_total = abs(best_fit_before_evol - self.alg['bestGlobal']['f']) if best_fit_before_evol is not None else 0.0
                state['deltaFitRegenPop'].append([delta_fit_total, eval_diff_total])

                if is_regen_pop:
                    records = np.array(state['deltaFitRegenPop'])
                    numerator = np.sum(records[:, 0])
                    denominator = np.sum(records[:, 1])
                    self.delta_fit_regen[self.group_index_global] = numerator / denominator if denominator > 0 else 0.0
                    self.delta_fit_global[self.group_index_global] = np.nan
                else:
                    self.delta_fit_regen[self.group_index_global] = np.nan
                    self.delta_fit_global[self.group_index_global] = delta_fit_total / eval_diff_total

                break

        state['first'] = False
        state['sublambda'] = sublambda
        state['submu'] = submu_floor
        state['subweights'] = weights
        state['submueff'] = submueff
        state['subcc'] = subcc
        state['subcs'] = subcs
        state['subc1'] = subc1
        state['subcmu'] = subcmu
        state['subdamps'] = subdamps
        state['subpc'] = subpc
        state['subps'] = subps
        state['subB'] = subB
        state['subD'] = subD
        state['subC'] = subC
        state['subinvsqrtC'] = subinvsqrtC
        state['subsigma'] = subsigma
        state['subeigeneval'] = subeigeneval
        state['subchiN'] = subchiN
        state['subxmean'] = subxmean
        state['iterationNum'] = iteration_num
        state['subcounteval'] = subcounteval

    def _determine_regen_pop(self, pop, group_dim_index):
        state = self.evol_state_group[self.group_index_global]
        group_dim_index = np.asarray(group_dim_index, dtype=int)

        pop_subset = pop[:, group_dim_index]
        mean_dim = pop_subset.mean(axis=0)
        std_dim = pop_subset.std(axis=0, ddof=0)

        precision_demand = np.full_like(std_dim, 1e-10)

        if state['threshStdDimInitial'] is None:
            state['threshStdDimInitial'] = np.minimum(np.full_like(std_dim, 1e-3), std_dim * 1e-3)

        if state['unChangeGenNDim'] is None:
            state['unChangeGenNDim'] = np.zeros_like(mean_dim, dtype=float)

        is_stagnant_dim = np.zeros_like(mean_dim, dtype=bool)

        if state['meanDim'] is not None and state['stdDim'] is not None:
            prev_mean = state['meanDim']
            prev_std = state['stdDim']
            for i in range(mean_dim.size):
                if prev_mean[i] == mean_dim[i] and prev_std[i] == std_dim[i]:
                    state['unChangeGenNDim'][i] += 1
                    UN = np.floor(np.sqrt(pop_subset.shape[0])) + 1
                    if state['unChangeGenNDim'][i] >= UN:
                        state['unChangeGenNDim'][i] = UN
                        is_stagnant_dim[i] = True
                else:
                    state['unChangeGenNDim'][i] = 0

        if state['bestIndiLastRegenPop'] is not None:
            state['threshStdDim'] = np.minimum(
                state['threshStdDimInitial'],
                1e-3 * np.abs(state['bestIndiLastRegenPop'] - mean_dim)
            )
        else:
            state['threshStdDim'] = state['threshStdDimInitial'].copy()

        state['threshStdDim'] = np.maximum(precision_demand, state['threshStdDim'])

        is_converged_dim = std_dim <= state['threshStdDim']
        regen_flags = is_converged_dim | is_stagnant_dim

        is_regen_pop = False
        if np.count_nonzero(regen_flags) == mean_dim.size:
            is_regen_pop = True
            state['bestIndiLastRegenPop'] = mean_dim.copy()

        state['meanDim'] = mean_dim
        state['stdDim'] = std_dim
        state['regenPopFlagDim'] = regen_flags

        return is_regen_pop

    def _evaluate_fit(self, individual):
        individual = np.asarray(individual, dtype=float).ravel()
        fitness = self.fun(individual)
        if np.ndim(fitness) == 0:
            fitness_value = float(fitness)
        else:
            fitness_value = np.asarray(fitness, dtype=float).ravel()[0]

        self.alg['fEvalNum'] += 1
        self._update_best_global(individual, fitness_value)
        self._set_output_values()
        self._check_termination()
        return fitness_value

    def _update_best_global(self, x, f):
        if self.alg['bestGlobal'] is None:
            self.alg['bestGlobal'] = {'x': x.copy(), 'f': f}
            return

        if self._is_better(f, self.alg['bestGlobal']['f']) == 1:
            self.alg['bestGlobal']['x'] = x.copy()
            self.alg['bestGlobal']['f'] = f

    def _is_better(self, f1, f2):
        return int(np.sign(f1 - f2) * self.prob['betterSign'])

    def _set_output_values(self):
        if self.alg['outputValues'] is None:
            max_records = min(1001, int(self.alg['Max_FEs']))
            output_points = np.floor(np.linspace(
                self.alg['fEvalNumInitial'] + 1,
                self.alg['Max_FEs'],
                max_records
            )).astype(int)
            if self.alg['mustOutputPoints'].size > 0:
                output_points = np.unique(
                    np.concatenate([output_points, self.alg['mustOutputPoints']])
                )

            self.alg['outputValues'] = np.full((output_points.size, 1 + self.prob['objN']), np.nan)
            self.alg['outputValues'][:, 0] = output_points

        current_index = np.where(self.alg['outputValues'][:, 0] == int(self.alg['fEvalNum']))[0]
        if current_index.size > 0 and self.alg['bestGlobal'] is not None:
            self.alg['outputValues'][current_index[0], 1:] = self.alg['bestGlobal']['f']

        if self.alg['fEvalNum'] >= self.alg['Max_FEs']:
            mask = ~np.isnan(self.alg['outputValues'][:, 0])
            self.alg['outputValues'] = self.alg['outputValues'][mask]

    def _check_termination(self):
        self.alg['isTerminate'] = self.alg['fEvalNum'] >= self.alg['Max_FEs']

