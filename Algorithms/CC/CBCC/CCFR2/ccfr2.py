import numpy as np

class CCFR2:
    def __init__(self, fun, info, cfg):
        self.fun = fun
        self.info = info
        self.cfg = cfg

        self.prob = {
            'betterSign': -1,  # -1 for minimization
            'D': info['dimension'],
            'fNum': info.get('fNum', 1),
            'objN': 1,
            'lb': np.ones(info['dimension']) * info['lower'],
            'ub': np.ones(info['dimension']) * info['upper'],
            # Decomposition provided externally
            'groups': info.get('groups', [])
        }

        self.w = cfg.get('w', 0.1)     # Weight for history contribution
        self.GEs = cfg.get('GEs', 100)  # Generations per cycle

        self.alg = {
            'outputValues': None,
            'fEvalNum': cfg.get('initial_fEvalNum', 0),
            'fEvalNumInitial': cfg.get('initial_fEvalNum', 0),
            'bestGlobal': None,  # {'x': ..., 'f': ...}
            'Max_FEs': cfg.get('maxFEs', 3e6),
            'mustOutputPoints': [],
            'isTerminate': False
        }

        groupN = len(self.prob['groups'])
        self.delta_F = np.zeros(groupN)

        self.x_prime_best = [None] * groupN

        self.evolState_group = {}
        for i in range(groupN):
            self.init_cmaes_state(i)

        print(
            f"[DEBUG] CCFR2 init F{self.prob['fNum']}: "f"fEvalNumInitial={self.alg['fEvalNumInitial']}, Max_FEs={self.alg['Max_FEs']}")

    def init_cmaes_state(self, groupIndex):
        group_indices = self.prob['groups'][groupIndex]
        D_sub = len(group_indices)
        lbvec = self.prob['lb'][group_indices]
        ubvec = self.prob['ub'][group_indices]

        # CCFR2 Population Size: Ni = 4 + 3 * ln(Di)
        lam = 4 + int(np.floor(3 * np.log(D_sub)))

        mu = lam / 2.0
        weights = np.log(mu + 0.5) - \
            np.log(np.arange(1, int(np.floor(mu)) + 1))
        mu = int(np.floor(mu))
        weights = weights / np.sum(weights)
        mueff = (np.sum(weights) ** 2) / np.sum(weights ** 2)

        cc = (4 + mueff / D_sub) / (D_sub + 4 + 2 * mueff / D_sub)
        cs = (mueff + 2) / (D_sub + mueff + 5)
        c1 = 2 / ((D_sub + 1.3) ** 2 + mueff)
        cmu = min(1 - c1, 2 * (mueff - 2 + 1 / mueff) /
                  ((D_sub + 2) ** 2 + mueff))
        damps = 1 + 2 * max(0, np.sqrt((mueff - 1) / (D_sub + 1)) - 1) + cs

        xmean = lbvec + (ubvec - lbvec) * 0.5
        sigma = 0.3 * (ubvec - lbvec)  

        self.evolState_group[groupIndex] = {
            'lambda': lam,
            'mu': mu,
            'weights': weights,
            'mueff': mueff,
            'cc': cc,
            'cs': cs,
            'c1': c1,
            'cmu': cmu,
            'damps': damps,
            'xmean': xmean,
            'sigma': sigma,
            'pc': np.zeros(D_sub),
            'ps': np.zeros(D_sub),
            'B': np.eye(D_sub),
            'D': np.ones(D_sub),
            'C': np.eye(D_sub),
            'invsqrtC': np.eye(D_sub),
            'chiN': D_sub ** 0.5 * (1 - 1 / (4 * D_sub) + 1 / (21 * D_sub ** 2)),
            'eigeneval': 0,
            'counteval': 0
        }

    def run(self):
        D = self.prob['D']
        if self.alg['bestGlobal'] is None:
            rand_x = self.prob['lb'] + \
                (self.prob['ub'] - self.prob['lb']) * np.random.rand(D)
            self.evaluate_fit(rand_x)  

        groups = self.prob['groups']
        groupN = len(groups)

        # Main Loop
        while not self.alg['isTerminate']:
            # Round-Robin 
            for i in range(groupN):
                if self.alg['isTerminate']:
                    break
                self.process_group(i)

            if self.alg['isTerminate']:
                break

            while (np.ptp(self.delta_F) > 1e-18) and not self.alg['isTerminate']:
                i = np.argmax(self.delta_F)
                self.process_group(i)

    def process_group(self, group_idx):
        x_best_before = self.alg['bestGlobal']['x'].copy()
        f_best_before = self.alg['bestGlobal']['f']
        fes_before = self.alg['fEvalNum']

        self.run_cmaes_optimizer(group_idx)

        fes_consumed = self.alg['fEvalNum'] - fes_before
        f_best_after = self.alg['bestGlobal']['f']
        improvement = np.abs(f_best_after - f_best_before)

        if fes_consumed > 0:
            real_time_contrib = improvement / fes_consumed
            self.delta_F[group_idx] = self.w * \
                self.delta_F[group_idx] + real_time_contrib
        else:
            self.delta_F[group_idx] = self.w * self.delta_F[group_idx]

        is_stagnant = (improvement == 0)
        if is_stagnant:
            self.delta_F[group_idx] = 0.0

        self.x_prime_best[group_idx] = self.alg['bestGlobal']['x'].copy()

        if fes_consumed > 0:
            try:
                if self.alg['fEvalNum'] <= self.alg['Max_FEs'] + 100:
                    print(
                        f'{self.prob["fNum"]}\t {self.alg["fEvalNum"]}\t {group_idx}\t {self.alg["bestGlobal"]["f"]:.5e}')
            except:
                pass

    def run_cmaes_optimizer(self, group_idx):
        group_indices = self.prob['groups'][group_idx]
        s = self.evolState_group[group_idx]

        lbvec = self.prob['lb'][group_indices]
        ubvec = self.prob['ub'][group_indices]
        D_sub = len(group_indices)

        xmean = s['xmean']
        sigma = s['sigma']  
        pc, ps = s['pc'], s['ps']
        B, D_eig, C = s['B'], s['D'], s['C']
        invsqrtC = s['invsqrtC']
        eigeneval = s['eigeneval']
        counteval = s['counteval']

        lambda_ = s['lambda']
        mu = s['mu']
        weights = s['weights']

        for gen in range(self.GEs):
            if self.alg['isTerminate']:
                break

            arx = np.zeros((D_sub, lambda_))
            fitnesses = np.zeros(lambda_)

            for k in range(lambda_):
                if self.alg['isTerminate']:
                    break

                valid = False
                while not valid:
                    z = np.random.randn(D_sub)
                    dx = B @ (D_eig * z)
                    candidate = xmean + sigma * dx

                    if np.all(candidate >= lbvec) and np.all(candidate <= ubvec):
                        arx[:, k] = candidate
                        valid = True
                    else:
                        candidate = np.clip(candidate, lbvec, ubvec)
                        arx[:, k] = candidate
                        valid = True

                full_x = self.alg['bestGlobal']['x'].copy()
                full_x[group_indices] = arx[:, k]

                fitnesses[k] = self.evaluate_fit(full_x)
                counteval += 1

            if self.alg['isTerminate']:
                break

            arindex = np.argsort(fitnesses)
            xold = xmean.copy()
            xmean = arx[:, arindex[:mu]] @ weights

            # Update Evolution Paths
            sigma_col = sigma.reshape(-1, 1) if sigma.ndim == 1 else sigma

            z_mean = invsqrtC @ ((xmean - xold) / sigma)

            ps = (1 - s['cs']) * ps + np.sqrt(s['cs']
                                              * (2 - s['cs']) * s['mueff']) * z_mean

            hsig_denom = (1 - (1 - s['cs']) ** (2 * counteval / lambda_))
            hsig = (np.linalg.norm(ps)**2 / D_sub < 2 + 4/(D_sub+1))

            pc = (1 - s['cc']) * pc + (1 if hsig else 0) * \
                np.sqrt(s['cc'] * (2 - s['cc']) * s['mueff']) * z_mean

            artmp = (arx[:, arindex[:mu]] - xold.reshape(-1, 1)) / sigma_col

            C = (1 - s['c1'] - s['cmu']) * C \
                + s['c1'] * (pc.reshape(-1, 1) @ pc.reshape(1, -1) + (1 - (1 if hsig else 0)) * s['cc'] * (2 - s['cc']) * C) \
                + s['cmu'] * (artmp @ np.diag(weights) @ artmp.T)

            sigma = sigma * np.exp((s['cs'] / s['damps'])
                                   * (np.linalg.norm(ps) / s['chiN'] - 1))

            sigma = np.minimum(sigma, ubvec - lbvec)
            sigma = np.maximum(sigma, 1e-10)

            # Decomposition
            if counteval - eigeneval > lambda_ / (s['c1'] + s['cmu']) / D_sub / 10:
                eigeneval = counteval
                C = np.triu(C) + np.triu(C, 1).T
                try:
                    eigvals, eigvecs = np.linalg.eigh(C)
                    eigvals = np.sqrt(np.abs(eigvals))
                    B = eigvecs
                    D_eig = eigvals
                    invsqrtC = B @ np.diag(1.0 /
                                           np.clip(D_eig, 1e-12, None)) @ B.T
                except np.linalg.LinAlgError:
                    pass

        s['xmean'] = xmean
        s['sigma'] = sigma
        s['pc'] = pc
        s['ps'] = ps
        s['B'] = B
        s['D'] = D_eig
        s['C'] = C
        s['invsqrtC'] = invsqrtC
        s['eigeneval'] = eigeneval
        s['counteval'] = counteval

    def evaluate_fit(self, x):

        if self.alg['fEvalNum'] >= self.alg['Max_FEs']:
            self.alg['isTerminate'] = True
            return np.inf

        x = np.ascontiguousarray(x, dtype=np.float64)
        fit_val = self.fun(x)

        if hasattr(fit_val, '__len__'):
            f_scalar = float(fit_val[0])
        else:
            f_scalar = float(fit_val)

        self.alg['fEvalNum'] += 1

        if self.alg['bestGlobal'] is None:
            self.alg['bestGlobal'] = {'x': x.copy(), 'f': f_scalar}
        else:
            is_better = (
                np.sign(f_scalar - self.alg['bestGlobal']['f']) * self.prob['betterSign']) == 1
            if is_better:
                self.alg['bestGlobal']['x'] = x.copy()
                self.alg['bestGlobal']['f'] = f_scalar

        self.set_output_values()

        if self.alg['fEvalNum'] >= self.alg['Max_FEs']:
            self.alg['isTerminate'] = True

        return f_scalar

    def set_output_values(self):
        if self.alg['outputValues'] is None:
            maxFEs_int = int(self.alg['Max_FEs'])
            outputValuesN = min(501, maxFEs_int)
            outputAtFEs = np.floor(np.linspace(
                self.alg['fEvalNumInitial'] + 1, maxFEs_int, outputValuesN))
            outputAtFEs = np.union1d(outputAtFEs, self.alg['mustOutputPoints'])
            outputAtFEs = np.array(outputAtFEs, dtype=int)
            outputValuesN = len(outputAtFEs)
            self.alg['outputValues'] = np.full((outputValuesN, 2), np.nan)
            self.alg['outputValues'][:, 0] = outputAtFEs

        idx = np.where(self.alg['outputValues'][:, 0]
                       == self.alg['fEvalNum'])[0]
        if len(idx) > 0:
            self.alg['outputValues'][idx[0], 1] = float(
                self.alg['bestGlobal']['f'])

        if self.alg['fEvalNum'] >= int(self.alg['Max_FEs']):
            self.alg['outputValues'] = self.alg['outputValues'][~np.isnan(
                self.alg['outputValues'][:, 0]), :]

    def is_terminate(self):
        if self.alg['fEvalNum'] >= self.alg['Max_FEs']:
            self.alg['isTerminate'] = True
        else:
            self.alg['isTerminate'] = False
