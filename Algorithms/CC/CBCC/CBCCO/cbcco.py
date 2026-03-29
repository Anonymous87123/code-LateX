import numpy as np

from Algorithms.CC.VI_based_Dec.DG2.dg2 import DG2


class CBCCO:

    def __init__(self, fun, info, cfg):
        self.fun = fun
        self.info = info
        self.cfg = cfg

        D = info['dimension']

        self.prob = {
            'betterSign': -1,
            'D': D,
            'fNum': info.get('fNum', 1),
            'objN': 1,
            'lb': np.ones(D) * info['lower'],
            'ub': np.ones(D) * info['upper'],
            'groups': []
        }

        self.alg = {
            'outputValues': None,
            'fEvalNum': cfg.get('initial_fEvalNum', 0),
            'fEvalNumInitial': cfg.get('initial_fEvalNum', 0),
            'bestGlobal': None,
            'Max_FEs': cfg.get('maxFEs', 1e6),
            'mustOutputPoints': [],
            'isTerminate': False
        }

        self.optimizer = cfg.get('optimizer', 'CMAES')
        self.groupIndexGlobal = 0
        self.evolState_group = {}

        self.overlap_rate = cfg.get('overlap_rate', 0.3)
        self.cbd_test_generations = cfg.get('cbd_test_generations', 100)
        self.grouping_method = cfg.get('grouping', 'DG2').upper()

        self.groups = []
        self.contribution = None
        self.decomposition_fes = 0
        self.decomposition_info = {}

    def run(self):
        GS, OS = self._run_cbd()
        self.groups = GS
        M = len(self.groups)
        if self.contribution is None:
            self.contribution = np.zeros(M, dtype=float)

        self.prob['groups'] = self.groups
        self._init_group_states()

        self._run_cbo()

    def _run_cbd(self):
        method = self.grouping_method
        if method == 'DG2':
            GS, OS = self._build_groups_via_dg2()
            self.decomposition_info = {
                'method': 'DG2',
                'GS_initial': [sorted(list(g)) for g in GS],
                'OS_initial': [{'groups': entry['groups'], 'vars': list(entry['vars'])} for entry in OS],
            }
        elif method == 'OEDG':
            GS, OS = self._build_groups_via_oedg()
        else:
            raise ValueError(f"Unsupported grouping method: {method}")

        GS, OS = self._shared_variable_allocation(GS, OS)
        GS, OS = self._filter_empty_groups(GS, OS)
        GS_final = [sorted(list(g)) for g in GS]
        return GS_final, OS

    def _build_groups_via_dg2(self):
        D = self.prob['D']

        dg2 = DG2(self.fun, self.info)
        _, evaluations, lambda_ = dg2.ism()
        theta = dg2.dsm(evaluations, lambda_)

        adjacency = []
        for i in range(D):
            neighbors = [j for j in range(D) if j != i and theta[i, j] == 1]
            adjacency.append(set(neighbors))

        unassigned = set(range(D))
        GS = []

        while len(unassigned) > 0:
            degrees = {v: len(adjacency[v] & unassigned) for v in unassigned}
            x_hat = min(degrees, key=degrees.get)

            neighbors = adjacency[x_hat] & unassigned
            comp = set([x_hat]) | neighbors

            unassigned -= comp
            GS.append(comp)

        alpha = self.overlap_rate
        changed = True
        while changed:
            changed = False
            M = len(GS)
            for i in range(1, M):
                for j in range(0, i):
                    overlap = GS[i] & GS[j]
                    if not overlap:
                        continue
                    if (len(overlap) / len(GS[i]) >= alpha) or (len(overlap) / len(GS[j]) >= alpha):
                        # Merge j into i
                        GS[i] = GS[i] | GS[j]
                        del GS[j]
                        changed = True
                        break
                if changed:
                    break

        OS = []
        M = len(GS)
        for i in range(1, M):
            for j in range(0, i):
                overlap = GS[i] & GS[j]
                if overlap:
                    OS.append({'groups': (i, j), 'vars': set(overlap)})

        for rec in OS:
            gi, gj = rec['groups']
            vars_ij = rec['vars']
            GS[gi] = GS[gi] - vars_ij
            GS[gj] = GS[gj] - vars_ij

        return GS, OS

    def _build_groups_via_oedg(self):
        from Algorithms.CC.VI_based_Dec.OEDG.oedg import OEDG

        oedg = OEDG(self.fun, self.info, cfg={})
        res = oedg.decompose()
        subcomponents = res['subcomponents']
        overlaps = res['overlaps']
        self.decomposition_fes = getattr(oedg, 'counter', 0)

        comp_sets = [set(comp) for comp in subcomponents]
        var_groups = {}
        for idx, comp in enumerate(comp_sets):
            for v in comp:
                var_groups.setdefault(v, set()).add(idx)

        shared_vars = {v for v, groups in var_groups.items() if len(groups) > 1}

        GS = []
        for comp in comp_sets:
            GS.append(comp - shared_vars)

        os_dict = {}
        for v in shared_vars:
            groups = sorted(list(var_groups.get(v, set())))
            if len(groups) < 2:
                continue
            for i in range(len(groups)):
                for j in range(i + 1, len(groups)):
                    key = (groups[i], groups[j])
                    os_dict.setdefault(key, set()).add(v)

        OS = [{'groups': key, 'vars': vals} for key, vals in os_dict.items()]

        self.decomposition_info = {
            'method': 'OEDG',
            'subcomponents': [sorted(list(comp)) for comp in comp_sets],
            'overlaps': [sorted(list(ov)) for ov in overlaps],
            'GS_initial': [sorted(list(g)) for g in GS],
            'OS_initial': [{'groups': entry['groups'], 'vars': sorted(list(entry['vars']))} for entry in OS],
        }

        return GS, OS

    def _filter_empty_groups(self, GS, OS):
        idx_map = {}
        new_GS = []
        for idx, group in enumerate(GS):
            group_set = set(group)
            if group_set:
                idx_map[idx] = len(new_GS)
                new_GS.append(group_set)

        new_OS = []
        for entry in OS:
            gi, gj = entry['groups']
            if gi in idx_map and gj in idx_map:
                new_OS.append({
                    'groups': (idx_map[gi], idx_map[gj]),
                    'vars': set(entry['vars'])
                })

        return new_GS, new_OS

    def _shared_variable_allocation(self, GS, OS):
        M = len(GS)

        self.prob['groups'] = [sorted(list(g)) for g in GS]
        self._init_group_states()

        contribution = np.zeros(M, dtype=float)
        # use a common baseline context for all groups
        if self.alg['bestGlobal'] is None:
            x_base = self.prob['lb'].copy()
            f_base = self._evaluate_fit_raw(x_base)
            self._set_context(x_base, f_base)
        else:
            x_base = self.alg['bestGlobal']['x'].copy()
            f_base = self.alg['bestGlobal']['f']

        N_test = self.cbd_test_generations
        for i in range(M):
            # reset context to the same baseline before testing each group
            self._set_context(x_base, f_base)
            f0 = f_base
            for _ in range(N_test):
                self.groupIndexGlobal = i
                if self.optimizer == 'CMAES':
                    dimIndexGroup = self.prob['groups'][i]
                    _isStagnant, _delta = self.cmaes_group(dimIndexGroup)
                if self.alg['isTerminate']:
                    break
            f_after = self.alg['bestGlobal']['f']
            contribution[i] = f0 - f_after

        self.contribution = contribution

        for rec in OS:
            gi, gj = rec['groups']
            vars_ij = rec['vars']
            if contribution[gi] > contribution[gj]:
                GS[gi] = GS[gi] | vars_ij
            else:
                GS[gj] = GS[gj] | vars_ij

        return GS, OS

    def _run_cbo(self):
        groups = self.prob['groups']
        M = len(groups)

        self.contribution = np.zeros(M, dtype=float) if self.contribution is None else self.contribution

        if self.alg['bestGlobal'] is None:
            x0 = self.prob['lb'] + (self.prob['ub'] - self.prob['lb']) * 0.5
            f0 = self._evaluate_fit_raw(x0)
            self._set_context(x0, f0)

        while not self.alg['isTerminate']:
            for i in range(M):
                if self.alg['isTerminate']:
                    break
                self.groupIndexGlobal = i
                f_old = self.alg['bestGlobal']['f']
                if self.optimizer == 'CMAES':
                    dimIndexGroup = groups[i]
                    _isStagnant, _delta = self.cmaes_group(dimIndexGroup)
                f_new = self.alg['bestGlobal']['f']
                self.contribution[i] = 0.5 * (self.contribution[i] + (f_old - f_new))

            if self.alg['isTerminate']:
                break

            max_c = np.max(self.contribution)
            if max_c <= 0:
                award_list = []
            else:
                award_list = [i for i in range(M) if (max_c / max(self.contribution[i], 1e-12)) < 2.0]

            if len(award_list) == M:
                award_list = []

            for i in award_list:
                if self.alg['isTerminate']:
                    break
                self.groupIndexGlobal = i
                f_old = self.alg['bestGlobal']['f']
                if self.optimizer == 'CMAES':
                    dimIndexGroup = groups[i]
                    _isStagnant, _delta = self.cmaes_group(dimIndexGroup)
                f_new = self.alg['bestGlobal']['f']
                self.contribution[i] = 0.5 * (self.contribution[i] + (f_old - f_new))

    def _init_group_states(self):
        self.evolState_group = {}
        groupN = len(self.prob['groups'])
        D = self.prob['D']
        for i in range(groupN):
            self.evolState_group[i] = {
                'first': True,
                'unChangeBestIndiGenN': 0,
                'lastbestIndi': np.full(D, np.nan),
                'deltaFit': 0.0,
                'distToBestIndi': None
            }

    def _evaluate_fit_raw(self, x):
        x_arr = np.ascontiguousarray(x, dtype=np.float64)
        y = self.fun(x_arr)
        return float(np.array(y).ravel()[0])

    def _set_context(self, x, f_val):
        self.alg['bestGlobal'] = {'x': x.copy(), 'f': float(f_val)}

    # ------------------------------------------------------------------
    # CMA-ES group optimizer and evaluation (adapted from CCFR3)
    # ------------------------------------------------------------------
    def cmaes_group(self, groupDimIndex):
        with np.errstate(divide='ignore', invalid='ignore'):
            groupDimIndexN = len(groupDimIndex)
            if groupDimIndexN == 0:
                return False, 0.0
            lbvec = self.prob['lb'][groupDimIndex].astype(float)
            ubvec = self.prob['ub'][groupDimIndex].astype(float)

            state = self.evolState_group[self.groupIndexGlobal]
            if state['first']:
                if self.alg['bestGlobal'] is None:
                    subxmean = lbvec + (ubvec - lbvec) / 2.0
                else:
                    subxmean = self.alg['bestGlobal']['x'][groupDimIndex].astype(float)
                subsigma = 0.3 * (ubvec - lbvec)

                sublambda = 4 + int(np.floor(3 * np.log(groupDimIndexN)))
                submu = sublambda / 2.0
                subweights = np.log(submu + 0.5) - np.log(np.arange(1, int(np.floor(submu)) + 1))
                submu = int(np.floor(submu))
                if submu <= 0:
                    submu = 1
                    subweights = np.array([1.0])
                else:
                    subweights = subweights / np.sum(subweights)
                submueff = (np.sum(subweights) ** 2) / np.sum(subweights ** 2)

                subcc = (4 + submueff / groupDimIndexN) / (groupDimIndexN + 4 + 2 * submueff / groupDimIndexN)
                subcs = (submueff + 2) / (groupDimIndexN + submueff + 5)
                subc1 = 2 / ((groupDimIndexN + 1.3) ** 2 + submueff)
                subcmu = min(1 - subc1, 2 * (submueff - 2 + 1 / submueff) / ((groupDimIndexN + 2) ** 2 + submueff))
                subdamps = 1 + 2 * max(0, np.sqrt((submueff - 1) / (groupDimIndexN + 1)) - 1) + subcs

                subpc = np.zeros(groupDimIndexN)
                subps = np.zeros(groupDimIndexN)
                subB = np.eye(groupDimIndexN)
                subD = np.ones(groupDimIndexN)
                subC = subB @ np.diag(subD ** 2) @ subB.T
                subinvsqrtC = subB @ np.diag(subD ** -1) @ subB.T
                subeigeneval = 0
                subchiN = groupDimIndexN ** 0.5 * (1 - 1 / (4 * groupDimIndexN) + 1 / (21 * groupDimIndexN ** 2))

                iterationNum = 0
                subcounteval = 0
                subartmp = None
            else:
                s = state
                sublambda = s['sublambda']
                submu = s['submu']
                subweights = s['subweights']
                submueff = s['submueff']

                subcc = s['subcc']
                subcs = s['subcs']
                subc1 = s['subc1']
                subcmu = s['subcmu']
                subdamps = s['subdamps']
                subartmp = s.get('subartmp', None)

                subpc = s['subpc']
                subps = s['subps']
                subB = s['subB']
                subD = s['subD']
                subC = s['subC']
                subinvsqrtC = s['subinvsqrtC']
                subeigeneval = s['subeigeneval']
                subchiN = s['subchiN']

                subxmean = s['subxmean']
                subsigma = s['subsigma']

                iterationNum = s['iterationNum']
                subcounteval = s['subcounteval']

            arfitness = np.full(sublambda, np.nan)

            D = self.prob['D']
            arx = np.zeros((D, sublambda))
            if self.alg['bestGlobal'] is None:
                randIndi = self.prob['lb'] + (self.prob['ub'] - self.prob['lb']) * np.random.rand(D)
                arx[:, :] = np.tile(randIndi.reshape(-1, 1), (1, sublambda))
                _ = self.evaluate_fit(randIndi)
            else:
                arx[:, :] = np.tile(self.alg['bestGlobal']['x'].reshape(-1, 1), (1, sublambda))

            if self.alg['bestGlobal'] is None:
                self.alg['bestGlobal'] = {'x': np.zeros(D), 'f': float('inf')}

            bestIndiGlobalBefore001 = self.alg['bestGlobal']['x'].copy()
            bestIndiGlobalBefore002 = self.alg['bestGlobal']['x'].copy()
            bestFitGlobalBefore001 = self.alg['bestGlobal']['f']
            bestFitGlobalBeforeEvol = self.alg['bestGlobal']['f']
            fEvalNumBeforeEvol = self.alg['fEvalNum']
            fEvalNumBefore001 = self.alg['fEvalNum']

            state['unChangeBestIndiGenN'] = 0
            deltaFitFinal = 0.0
            isStagnate = False
            stdDeltaFit = 0.0
            deltaFitSet = []
            state['distToBestIndi'] = None

            while not self.alg['isTerminate']:
                iterationNum += 1

                for k in range(sublambda):
                    rand_vec_n = np.random.randn(groupDimIndexN)
                    mysigma = subsigma * (subB @ (subD * rand_vec_n))

                    logicalTemp001 = np.abs(mysigma) > (ubvec - lbvec)
                    if np.any(logicalTemp001):
                        mysigma[logicalTemp001] = ((ubvec[logicalTemp001] - lbvec[logicalTemp001]) *
                                                   np.random.randn(np.sum(logicalTemp001)))

                    tempX = subxmean + mysigma
                    logicalTemp = (tempX < lbvec) | (tempX > ubvec)

                    while np.any(logicalTemp):
                        idxs = np.where(logicalTemp)[0]
                        n_idxs = len(idxs)

                        rand_vec_n_slice = np.random.randn(n_idxs)
                        B_slice = subB[np.ix_(idxs, idxs)]
                        D_slice = subD[idxs]

                        new_sigma = B_slice @ (D_slice * rand_vec_n_slice)

                        mysigma[idxs] = subsigma[idxs] * new_sigma

                        logicalTemp001 = np.abs(mysigma) > (ubvec - lbvec)
                        if np.any(logicalTemp001):
                            mask = logicalTemp & logicalTemp001
                            mysigma[mask] = ((ubvec[mask] - lbvec[mask]) * np.random.randn(np.sum(mask)))

                        tempX[logicalTemp] = subxmean[logicalTemp] + mysigma[logicalTemp]
                        logicalTemp = (tempX < lbvec) | (tempX > ubvec)

                    arx[groupDimIndex, k] = tempX
                    arfitness[k] = self.evaluate_fit(arx[:, k])
                    subcounteval += 1

                    if self.alg['isTerminate']:
                        break

                arindex = np.argsort(arfitness)
                arfitness = arfitness[arindex]
                subxold = subxmean.copy()
                subxmean = arx[groupDimIndex][:, arindex[:submu]] @ subweights

                subps = ((1 - subcs) * subps +
                         np.sqrt(subcs * (2 - subcs) * submueff) * subinvsqrtC @ ((subxmean - subxold) / subsigma))

                subhsig_denom = (1 - (1 - subcs) ** (2 * subcounteval / sublambda))
                subhsig = (np.sum(subps ** 2) / subhsig_denom / groupDimIndexN
                           < 2 + 4 / (groupDimIndexN + 1))

                subpc = ((1 - subcc) * subpc +
                         subhsig * np.sqrt(subcc * (2 - subcc) * submueff) * ((subxmean - subxold) / subsigma))

                subartmp = (1.0 / subsigma).reshape(-1, 1) * (arx[groupDimIndex][:, arindex[:submu]] - subxold.reshape(-1, 1))

                subC = ((1 - subc1 - subcmu) * subC +
                        subc1 * (subpc.reshape(-1, 1) @ subpc.reshape(1, -1) +
                                 (1 - subhsig) * subcc * (2 - subcc) * subC) +
                        subcmu * subartmp @ np.diag(subweights) @ subartmp.T)

                norm_ps = np.linalg.norm(subps)
                subsigma = subsigma * np.exp((subcs / subdamps) * (norm_ps / subchiN - 1))
                tempLogical = np.abs(subsigma) > (ubvec - lbvec)
                if np.any(tempLogical):
                    subsigma[tempLogical] = (ubvec[tempLogical] - lbvec[tempLogical])

                tempLogical = np.abs(subsigma) < np.finfo(float).tiny
                if np.any(tempLogical):
                    subsigma[tempLogical] = np.finfo(float).tiny

                if subcounteval - subeigeneval > sublambda / (subc1 + subcmu) / groupDimIndexN / 10:
                    subeigeneval = subcounteval
                    subC = np.triu(subC) + np.triu(subC, 1).T
                    if not (np.any(np.isnan(subC)) or np.any(np.isinf(subC))):
                        try:
                            eigvals, subB = np.linalg.eigh(subC)
                        except np.linalg.LinAlgError:
                            continue

                        subD = np.sqrt(np.abs(eigvals))

                        subD[subD < np.finfo(float).tiny] = np.finfo(float).tiny
                        subD[subD > np.finfo(float).max] = np.finfo(float).max

                        subinvsqrtC = subB @ np.diag(1.0 / subD) @ subB.T

                stopEvol = False
                if bestIndiGlobalBefore001 is not None:
                    changed_count = np.sum(bestIndiGlobalBefore001[groupDimIndex] != self.alg['bestGlobal']['x'][groupDimIndex])
                    if changed_count == len(groupDimIndex):
                        denom_diff = (self.alg['fEvalNum'] - fEvalNumBefore001)
                        deltaFit001 = (np.abs(bestFitGlobalBefore001 - self.alg['bestGlobal']['f']) / denom_diff)

                        deltaFitSet.append(deltaFit001)
                        stdDeltaFit001 = np.std(deltaFitSet, ddof=1) if len(deltaFitSet) > 1 else stdDeltaFit

                        if len(deltaFitSet) > 2 and stdDeltaFit001 < stdDeltaFit:
                            stopEvol = True

                        stdDeltaFit = stdDeltaFit001
                        bestIndiGlobalBefore001 = self.alg['bestGlobal']['x'].copy()
                        bestFitGlobalBefore001 = self.alg['bestGlobal']['f']
                        fEvalNumBefore001 = self.alg['fEvalNum']

                stopEvol001 = False
                isStagnant = False
                bestIndiIndex = arindex[0]
                pop = arx.T

                if np.sum(bestIndiGlobalBefore002[groupDimIndex] == self.alg['bestGlobal']['x'][groupDimIndex]) == len(groupDimIndex):
                    if state['distToBestIndi'] is None:
                        best_row = pop[bestIndiIndex, groupDimIndex]
                        distToBestIndi = float(np.sum(np.abs(pop[:, groupDimIndex] - best_row)) / max(1, pop.shape[0]))
                        state['distToBestIndi'] = distToBestIndi

                    state['unChangeBestIndiGenN'] += 1
                    UN001 = sublambda

                    if state['unChangeBestIndiGenN'] >= UN001:
                        state['unChangeBestIndiGenN'] = UN001
                        if state['distToBestIndi'] is not None:
                            best_row = pop[bestIndiIndex, groupDimIndex]
                            distToBestIndi = float(np.sum(np.abs(pop[:, groupDimIndex] - best_row)) / max(1, pop.shape[0]))
                            if distToBestIndi <= state['distToBestIndi']:
                                stopEvol001 = True
                                if distToBestIndi == state['distToBestIndi']:
                                    isStagnant = True
                else:
                    state['unChangeBestIndiGenN'] = 0
                    state['distToBestIndi'] = None

                bestIndiGlobalBefore002 = self.alg['bestGlobal']['x'].copy()

                if stopEvol or stopEvol001:
                    if stopEvol001:
                        if isStagnant:
                            deltaFitFinal = 0.0
                        else:
                            denom_diff = (self.alg['fEvalNum'] - fEvalNumBeforeEvol)
                            deltaFitFinal = (np.abs(bestFitGlobalBeforeEvol - self.alg['bestGlobal']['f']) / denom_diff)
                            deltaFitFinal = 0.5 * state['deltaFit'] + 0.5 * deltaFitFinal

                    if stopEvol:
                        denom_diff = (self.alg['fEvalNum'] - fEvalNumBeforeEvol)
                        deltaFitFinal = (np.abs(bestFitGlobalBeforeEvol - self.alg['bestGlobal']['f']) / denom_diff)

                    deltaFitFinal = 0.0 if np.isnan(deltaFitFinal) or np.isinf(deltaFitFinal) else deltaFitFinal
                    break

            state['first'] = False
            state['sublambda'] = sublambda
            state['submu'] = submu
            state['subweights'] = subweights
            state['submueff'] = submueff
            state['subcc'] = subcc
            state['subcs'] = subcs
            state['subc1'] = subc1
            state['subcmu'] = subcmu
            state['subdamps'] = subdamps
            state['subartmp'] = subartmp
            state['subpc'] = subpc
            state['subps'] = subps
            state['subB'] = subB
            state['subD'] = subD
            state['subC'] = subC
            state['subinvsqrtC'] = subinvsqrtC
            state['subeigeneval'] = subeigeneval
            state['subchiN'] = subchiN
            state['subxmean'] = subxmean
            state['subsigma'] = subsigma
            state['iterationNum'] = iterationNum
            state['subcounteval'] = subcounteval

            if np.isnan(deltaFitFinal) or np.isinf(deltaFitFinal):
                deltaFitFinal = 0.0

            state['deltaFit'] = deltaFitFinal
            return isStagnate, deltaFitFinal

    def evaluate_fit(self, pop):
        if pop.ndim == 1:
            x = pop
            x = np.ascontiguousarray(x, dtype=np.float64)
            fit_val = self.fun(x)
            if self.prob['objN'] == 1:
                fit_scalar = float(np.array(fit_val).ravel()[0])
                self.alg['fEvalNum'] += 1
                self.update_best_global(x, fit_scalar)
                self.set_output_values()
                self.is_terminate()
                return fit_scalar
            else:
                fit_arr = np.array(fit_val).ravel().copy()
                self.alg['fEvalNum'] += 1
                self.update_best_global(x, fit_arr)
                self.set_output_values()
                self.is_terminate()
                return fit_arr
        else:
            N = pop.shape[0]
            fits = []
            for i in range(N):
                if self.alg['isTerminate']:
                    break
                val = self.evaluate_fit(pop[i, :])
                fits.append(val)
            if len(fits) == 0:
                return np.nan
            return fits[0] if len(fits) == 1 else np.array(fits)

    def update_best_global(self, x, f):
        if self.prob['objN'] == 1:
            f_val = float(np.array(f).ravel()[0])
        else:
            f_val = np.array(f).ravel().copy()

        if self.alg['bestGlobal'] is None:
            self.alg['bestGlobal'] = {'x': x.copy(), 'f': f_val}
            return

        if self.prob['objN'] == 1:
            if self.is_better(f_val, self.alg['bestGlobal']['f']) == 1:
                self.alg['bestGlobal']['x'] = x.copy()
                self.alg['bestGlobal']['f'] = f_val
        else:
            if self.is_better(f_val[0], self.alg['bestGlobal']['f'][0]) == 1:
                self.alg['bestGlobal']['x'] = x.copy()
                self.alg['bestGlobal']['f'] = f_val

    def is_better(self, f1, f2):
        return int(np.sign(f1 - f2) * self.prob['betterSign'])

    def set_output_values(self):
        if self.alg['outputValues'] is None:
            maxFEs_int = int(self.alg['Max_FEs'])
            outputValuesN = min(501, maxFEs_int)
            outputAtFEs = np.floor(np.linspace(self.alg['fEvalNumInitial'] + 1, maxFEs_int, outputValuesN))
            outputAtFEs = np.union1d(outputAtFEs, self.alg['mustOutputPoints'])
            outputAtFEs = np.array(outputAtFEs, dtype=int)
            outputValuesN = len(outputAtFEs)
            self.alg['outputValues'] = np.full((outputValuesN, 1 + self.prob['objN']), np.nan)
            self.alg['outputValues'][:, 0] = outputAtFEs

        idx = np.where(self.alg['outputValues'][:, 0] == self.alg['fEvalNum'])[0]
        if len(idx) > 0:
            if self.prob['objN'] == 1:
                self.alg['outputValues'][idx[0], 1] = float(self.alg['bestGlobal']['f'])
            else:
                self.alg['outputValues'][idx[0], 1:] = self.alg['bestGlobal']['f']

        if self.alg['fEvalNum'] >= int(self.alg['Max_FEs']):
            self.alg['outputValues'] = self.alg['outputValues'][~np.isnan(self.alg['outputValues'][:, 0]), :]

    def is_terminate(self):
        if self.alg['fEvalNum'] >= self.alg['Max_FEs']:
            self.alg['isTerminate'] = True
        else:
            self.alg['isTerminate'] = False
