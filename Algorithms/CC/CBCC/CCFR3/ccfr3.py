import numpy as np

class CCFR3:
    def __init__(self, fun, info, cfg):
        self.fun = fun
        self.info = info
        self.cfg = cfg

        # problem and algorithm state
        self.prob = {
            'betterSign': -1,  # -1 for minimization
            'D': info['dimension'],
            'fNum': info.get('fNum', 1),
            'objN': 1,
            'lb': np.ones(info['dimension']) * info['lower'],
            'ub': np.ones(info['dimension']) * info['upper'],
            'groups': info.get('groups', [])
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

        # Initialize evolution states for each group
        groupN = len(self.prob['groups'])
        for i in range(groupN):
            self.evolState_group[i] = {
                'first': True,
                'unChangeBestIndiGenN': 0,
                'lastbestIndi': np.full(self.prob['D'], np.nan),
                'deltaFit': 0.0,
                'distToBestIndi': None
            }

    def run(self):
        groups = self.prob['groups']
        groupN = len(groups)
        deltaFit = np.zeros(groupN)

        while not self.alg['isTerminate']:
            sortIndex = np.argsort(-deltaFit)
            for i in range(groupN):
                groupIndex = sortIndex[i]
                self.groupIndexGlobal = groupIndex

                if self.optimizer == 'CMAES':
                    deltaFit000 = self.evolution_group_cmaes(groupIndex, groups)

                deltaFit[groupIndex] = deltaFit000

                if self.alg['isTerminate']:
                    break

            logical001 = (deltaFit == 0)
            if np.sum(~logical001) > 0:
                deltaFit[logical001] = np.min(deltaFit[~logical001]) * 0.9

            for i in range(groupN):
                self.evolState_group[i]['deltaFit'] = deltaFit[i]

            while (len(deltaFit) == 1 or np.min(deltaFit) != np.max(deltaFit)):
                groupIndexMax = np.argmax(deltaFit)
                groupIndex = groupIndexMax
                self.groupIndexGlobal = groupIndex

                if self.optimizer == 'CMAES':
                    deltaFit000 = self.evolution_group_cmaes(groupIndex, groups)

                deltaFit[groupIndex] = deltaFit000

                if deltaFit[groupIndex] == 0 and np.any(deltaFit != 0):
                    deltaFit[groupIndex] = np.min(deltaFit[deltaFit != 0]) * 0.9

                self.evolState_group[groupIndex]['deltaFit'] = deltaFit[groupIndex]

                if self.alg['isTerminate']:
                    break

    def evolution_group_cmaes(self, groupIndex, groups):
        dimIndexGroup = groups[groupIndex]
        isStagnate, deltaFit001 = self.cmaes_group(dimIndexGroup)
        return deltaFit001

    def cmaes_group(self, groupDimIndex):
        """
        CMA-ES for a group of indices (FINAL CORRECTED version)
        
        This version:
        1. Uses np.linalg.eigh (CRITICAL: matches MATLAB's symmetric eig, guarantees real results)
        2. Removes try...except (CRITICAL: matches MATLAB's boundary logic)
        3. Removes denom safeguards (CRITICAL: matches MATLAB's inf/nan propagation)
        4. Uses '==' for stagnation (CRITICAL: matches MATLAB's float compare)
        """
        # CHANGED: Wrap main logic in errstate to replicate MATLAB's handling of inf/nan
        with np.errstate(divide='ignore', invalid='ignore'):
            groupDimIndexN = len(groupDimIndex)
            lbvec = self.prob['lb'][groupDimIndex].astype(float)
            ubvec = self.prob['ub'][groupDimIndex].astype(float)

            state = self.evolState_group[self.groupIndexGlobal]
            if state['first']:
                subxmean = lbvec + (ubvec - lbvec) / 2.0
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
                    # NOTE: Python's randn(N) is (N,) array. MATLAB's randn(N,1) is (N,1) matrix.
                    # This is fine, np operators handle (N,N) @ (N,) correctly.
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

                        # CHANGED: Removed try-except block to match MATLAB
                        # This logic MUST NOT crash.
                        
                        # Generate the random vector, ensuring it's (N,)
                        rand_vec_n_slice = np.random.randn(n_idxs) 
                        
                        # B(logical, logical) in MATLAB
                        B_slice = subB[np.ix_(idxs, idxs)] # Use np.ix_ for robust slicing
                        # D(logical) in MATLAB
                        D_slice = subD[idxs] 
                        
                        # (N,N) @ ((N,) * (N,)) -> (N,N) @ (N,) -> (N,)
                        # This logic is sound for n_idxs >= 1
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

                # CHANGED: Removed 'denom' safeguard
                subps = ((1 - subcs) * subps +
                         np.sqrt(subcs * (2 - subcs) * submueff) * subinvsqrtC @ ((subxmean - subxold) / subsigma))
                
                subhsig_denom = (1 - (1 - subcs) ** (2 * subcounteval / sublambda))
                subhsig = (np.sum(subps ** 2) / subhsig_denom / groupDimIndexN
                           < 2 + 4 / (groupDimIndexN + 1))
                
                subpc = ((1 - subcc) * subpc +
                         subhsig * np.sqrt(subcc * (2 - subcc) * submueff) * ((subxmean - subxold) / subsigma))

                # CHANGED: Removed 'denom' safeguard
                subartmp = (1.0 / subsigma).reshape(-1, 1) * (arx[groupDimIndex][:, arindex[:submu]] - subxold.reshape(-1, 1))
                
                subC = ((1 - subc1 - subcmu) * subC +
                        subc1 * (subpc.reshape(-1, 1) @ subpc.reshape(1, -1) +
                                 (1 - subhsig) * subcc * (2 - subcc) * subC) +
                        subcmu * subartmp @ np.diag(subweights) @ subartmp.T)

                # adapt step size sigma
                norm_ps = np.linalg.norm(subps)
                subsigma = subsigma * np.exp((subcs / subdamps) * (norm_ps / subchiN - 1))
                tempLogical = np.abs(subsigma) > (ubvec - lbvec)
                if np.any(tempLogical):
                    subsigma[tempLogical] = (ubvec[tempLogical] - lbvec[tempLogical])
                
                tempLogical = np.abs(subsigma) < np.finfo(float).tiny
                if np.any(tempLogical):
                    subsigma[tempLogical] = np.finfo(float).tiny

                # update eigen decomposition if needed
                if subcounteval - subeigeneval > sublambda / (subc1 + subcmu) / groupDimIndexN / 10:
                    subeigeneval = subcounteval
                    subC = np.triu(subC) + np.triu(subC, 1).T # Enforce symmetry
                    if not (np.any(np.isnan(subC)) or np.any(np.isinf(subC))):
                        # CHANGED: Use eigh()! This is the correct Python equivalent
                        # for MATLAB's eig() on a symmetric matrix.
                        # It guarantees real results.
                        try:
                            eigvals, subB = np.linalg.eigh(subC)
                        except np.linalg.LinAlgError:
                            # Eigendecomposition failed, skip update
                            continue # Go to next iteration

                        # Replicate MATLAB's abs() and sqrt(diag())
                        # abs() is good practice even if eigh guarantees real
                        subD = np.sqrt(np.abs(eigvals))
                        
                        subD[subD < np.finfo(float).tiny] = np.finfo(float).tiny
                        subD[subD > np.finfo(float).max] = np.finfo(float).max
                        
                        # Re-calculate subinvsqrtC (subB.T is correct for real matrix)
                        subinvsqrtC = subB @ np.diag(1.0 / subD) @ subB.T

                # print progress
                bestf_print = self.alg['bestGlobal']['f']
                try:
                    print(f'{self.prob["fNum"]}\t {self.alg["fEvalNum"]}\t {self.groupIndexGlobal}\t {bestf_print:.5e}')
                except Exception:
                    print(f'{self.prob["fNum"]}\t {self.alg["fEvalNum"]}\t {self.groupIndexGlobal}\t {bestf_print}')

                # stopping criterion based on improvements
                stopEvol = False
                if bestIndiGlobalBefore001 is not None:
                    changed_count = np.sum(bestIndiGlobalBefore001[groupDimIndex] != self.alg['bestGlobal']['x'][groupDimIndex])
                    if changed_count == len(groupDimIndex):
                        # CHANGED: Removed denom_diff safeguard
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
                pop = arx.T  # pop shape: lambda x D

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
                                # CHANGED: Use exact float comparison (==) to match MATLAB
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
                            # CHANGED: Removed denom_diff safeguard
                            denom_diff = (self.alg['fEvalNum'] - fEvalNumBeforeEvol)
                            deltaFitFinal = (np.abs(bestFitGlobalBeforeEvol - self.alg['bestGlobal']['f']) / denom_diff)
                            deltaFitFinal = 0.5 * state['deltaFit'] + 0.5 * deltaFitFinal

                    if stopEvol:
                        # CHANGED: Removed denom_diff safeguard
                        denom_diff = (self.alg['fEvalNum'] - fEvalNumBeforeEvol)
                        deltaFitFinal = (np.abs(bestFitGlobalBeforeEvol - self.alg['bestGlobal']['f']) / denom_diff)
                    
                    # Handle potential nan/inf from division by zero
                    deltaFitFinal = 0.0 if np.isnan(deltaFitFinal) or np.isinf(deltaFitFinal) else deltaFitFinal
                    
                    break

            # save state
            state['first'] = False
            # ... (rest of state saving)
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

            # Final check to ensure we don't return nan/inf
            if np.isnan(deltaFitFinal) or np.isinf(deltaFitFinal):
                deltaFitFinal = 0.0

            return isStagnate, deltaFitFinal

    def evaluate_fit(self, pop):
        """Evaluate fitness of a vector (or matrix rows). Return scalar (single objective) or array."""
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
            # pop: N x D
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
        """Normalize f and update best """
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

    def erdg(self):
        """
        Run ERDG grouping (translated from MATLAB). Uses self.evaluate_fit(...) so
        f-evals are counted in self.alg['fEvalNum'] automatically.
        Returns: (groups_list, fEvalConsumed) where groups_list is list of lists of 0-based indices.
        """
        D = self.prob['D']
        lb = self.prob['lb'].astype(float)
        ub = self.prob['ub'].astype(float)

        start_fes = int(self.alg.get('fEvalNum', 0))

        # prepare p1 = lb * ones(1, D)
        p1 = lb.copy()
        # evaluate y1
        y1 = self.evaluate_fit(p1)  # this updates self.alg['fEvalNum']
        # ensure scalar
        y1 = float(np.array(y1).ravel()[0])

        # MATLAB: sub1 = 1; sub2 = 2:dim  (1-based)
        sub1 = [0]
        sub2 = list(range(1, D))

        seps = []         # store singleton separable indices
        nongroups = []    # store non-sep groups (lists)

        # define INTERACT as nested function so it can call self.evaluate_fit and modify FEs implicitly
        eps_val = np.finfo(float).eps
        muM = eps_val / 2.0
        def gamma(n):
            return (n * muM) / (1.0 - n * muM)

        def INTERACT(sub1_in, sub2_in, p1_local, p2_local, y_local):
            """
            Inputs:
                sub1_in, sub2_in: lists of indices (0-based)
                p1_local, p2_local: full-D vectors (numpy arrays)
                y_local: list/array length 4 where some entries might be np.nan
            Returns:
                sub1_out (list)
                y_out (length-4 list)
            Note: FEs are accumulated via calls to self.evaluate_fit(...)
            """
            nonsepFlag = True
            y001 = list(y_local)  # copy

            # if any nan in y_local, we need to evaluate y3,y4
            if np.any(np.isnan(y001)):
                p3 = p1_local.copy()
                p4 = p2_local.copy()
                # set positions indexed by sub2 to midpoint
                mids = (ub[sub2_in] + lb[sub2_in]) / 2.0
                for ii, idx in enumerate(sub2_in):
                    p3[idx] = mids[ii]
                    p4[idx] = mids[ii]
                y3 = self.evaluate_fit(p3)
                y4 = self.evaluate_fit(p4)
                y3 = float(np.array(y3).ravel()[0])
                y4 = float(np.array(y4).ravel()[0])
                y001[2] = -y3
                y001[3] = y4

                Fmax = np.sum(np.abs(y001))
                epsilon = gamma(np.sqrt(D) + 2) * Fmax
                deltaDiff001 = abs(np.sum(y001))
                if deltaDiff001 <= epsilon:
                    nonsepFlag = False

            if nonsepFlag:
                if len(sub2_in) == 1:
                    # union(sub1, sub2)
                    sub1_out = list(sorted(set(sub1_in) | set(sub2_in)))
                    return sub1_out, y001
                else:
                    k = len(sub2_in) // 2
                    sub2_1 = sub2_in[:k]
                    sub2_2 = sub2_in[k:]

                    # prepare y for left child: [y1, y2, nan, nan]
                    left_y = [y001[0], y001[1], np.nan, np.nan]
                    sub1_1, y002 = INTERACT(sub1_in, sub2_1, p1_local, p2_local, left_y)

                    deltaDiffDiff = np.sum(y001) - np.sum(y002)
                    if deltaDiffDiff != 0:
                        # decide which y to pass to right child
                        if len(sub1_1) == len(sub1_in):
                            # left child is separable
                            right_y = y001
                        else:
                            right_y = [y001[0], y001[1], np.nan, np.nan]
                        sub1_2, _ = INTERACT(sub1_in, sub2_2, p1_local, p2_local, right_y)
                        sub1_out = list(sorted(set(sub1_1) | set(sub1_2)))
                        return sub1_out, y001
                    else:
                        return sub1_1, y001
            # if not nonsepFlag
            return sub1_in, y001

        # main while loop
        while len(sub2) > 0:
            # construct p2 = p1 with p2(sub1)=ub(sub1)
            p2 = p1.copy()
            for idx in sub1:
                p2[idx] = ub[idx]
            y2 = self.evaluate_fit(p2)
            y2 = float(np.array(y2).ravel()[0])

            # MATLAB has y = [y1 -y2 nan nan]
            y = [y1, -y2, np.nan, np.nan]
            sub1_a, y_ret = INTERACT(sub1, sub2, p1, p2, y)

            if len(sub1_a) == len(sub1):
                # sub1 does not interrelate with sub2
                if len(sub1) == 1:
                    seps.append(sub1[0])
                else:
                    nongroups.append(list(sub1))
                # move sub1 to first element of sub2
                sub1 = [sub2[0]]
                sub2 = sub2[1:]
            else:
                sub1 = sub1_a
                # remove elements in sub1 from sub2
                sub2 = [s for s in sub2 if s not in sub1]

            if len(sub2) == 0:
                if len(sub1) <= 1:
                    seps.append(sub1[0])
                else:
                    nongroups.append(list(sub1))

        # build groups001: nongroups first then seps as singleton lists
        groups001 = []
        for g in nongroups:
            groups001.append(g)
        for s in seps:
            groups001.append([s])

        # compute consumed FEs
        end_fes = int(self.alg.get('fEvalNum', 0))
        consumed = end_fes - start_fes

        return groups001, consumed
