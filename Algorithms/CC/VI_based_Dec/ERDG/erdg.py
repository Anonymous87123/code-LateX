import numpy as np


class ERDG:
    def __init__(self, fun, info, cfg):
        self.fun = fun
        self.info = info
        self.cfg = cfg
        self.counter = 0  # number of function evaluations used inside ERDG

    def _eval(self, x):
        """Evaluate fun(x) and update local evaluation counter."""
        y = self.fun(x)
        self.counter += 1
        # ensure scalar float
        return float(np.array(y).ravel()[0])

    def combine(self, list_of_lists):
        """
        Merge singletons into 'seps' and keep others as 'nonseps',
        following the convention used in RDG2/RDG3.
        """
        single_element_combined = []
        remaining_lists = []

        for sublist in list_of_lists:
            if len(sublist) == 1:
                single_element_combined.extend(sublist)
            else:
                remaining_lists.append(sublist)

        subspaces = {
            'seps': single_element_combined,   # list of indices
            'nonseps': remaining_lists        # list of lists of indices
        }
        return subspaces

    def decompose(self):
        """
        Run ERDG decomposition and return subspaces:
            {'seps': [...], 'nonseps': [[...], ...]}
        """
        D = self.info['dimension']

        # support scalar or vector lower/upper bounds
        lb = np.ones(D) * self.info['lower']
        ub = np.ones(D) * self.info['upper']

        # initial point p1 = lower bound
        p1 = lb.copy()
        y1 = self._eval(p1)

        # MATLAB: sub1 = 1; sub2 = 2:dim  (1-based)
        # here 0-based
        sub1 = [0]
        sub2 = list(range(1, D))

        seps = []       # singleton separable indices
        nongroups = []  # non-separable groups (lists of indices)

        eps_val = np.finfo(float).eps
        muM = eps_val / 2.0

        def gamma(n):
            return (n * muM) / (1.0 - n * muM)

        def INTERACT(sub1_in, sub2_in, p1_local, p2_local, y_local):
            """
            Inputs:
                sub1_in, sub2_in : lists of indices (0-based)
                p1_local, p2_local : full-D vectors (numpy arrays)
                y_local : length-4 list [y1, -y2, -y3 or nan, y4 or nan]
            Returns:
                sub1_out (list), y_out (length-4 list)
            """
            nonsep_flag = True
            y001 = list(y_local)

            # If any of y3, y4 are nan, evaluate them.
            if np.any(np.isnan(y001)):
                p3 = p1_local.copy()
                p4 = p2_local.copy()

                mids = (ub[sub2_in] + lb[sub2_in]) / 2.0
                for ii, idx in enumerate(sub2_in):
                    p3[idx] = mids[ii]
                    p4[idx] = mids[ii]

                y3 = self._eval(p3)
                y4 = self._eval(p4)
                y001[2] = -y3
                y001[3] = y4

                Fmax = np.sum(np.abs(y001))
                epsilon = gamma(np.sqrt(D) + 2) * Fmax
                delta_diff001 = abs(np.sum(y001))
                if delta_diff001 <= epsilon:
                    nonsep_flag = False

            if nonsep_flag:
                if len(sub2_in) == 1:
                    sub1_out = sorted(set(sub1_in) | set(sub2_in))
                    return sub1_out, y001
                else:
                    k = len(sub2_in) // 2
                    sub2_1 = sub2_in[:k]
                    sub2_2 = sub2_in[k:]

                    left_y = [y001[0], y001[1], np.nan, np.nan]
                    sub1_1, y002 = INTERACT(sub1_in, sub2_1, p1_local, p2_local, left_y)

                    delta_diff_diff = np.sum(y001) - np.sum(y002)
                    if delta_diff_diff != 0:
                        if len(sub1_1) == len(sub1_in):
                            right_y = y001
                        else:
                            right_y = [y001[0], y001[1], np.nan, np.nan]
                        sub1_2, _ = INTERACT(sub1_in, sub2_2, p1_local, p2_local, right_y)
                        sub1_out = sorted(set(sub1_1) | set(sub1_2))
                        return sub1_out, y001
                    else:
                        return sub1_1, y001

            return sub1_in, y001

        # main loop
        while len(sub2) > 0:
            # construct p2 = p1 with p2(sub1) = ub(sub1)
            p2 = p1.copy()
            for idx in sub1:
                p2[idx] = ub[idx]

            y2 = self._eval(p2)

            # y = [y1, -y2, nan, nan] as in MATLAB
            y = [y1, -y2, np.nan, np.nan]
            sub1_a, _ = INTERACT(sub1, sub2, p1, p2, y)

            if len(sub1_a) == len(sub1):
                # sub1 does not interact with sub2
                if len(sub1) == 1:
                    seps.append(sub1[0])
                else:
                    nongroups.append(list(sub1))

                # move to next starting variable
                sub1 = [sub2[0]]
                sub2 = sub2[1:]
            else:
                sub1 = sub1_a
                sub2 = [s for s in sub2 if s not in sub1]

            if len(sub2) == 0:
                if len(sub1) <= 1:
                    seps.append(sub1[0])
                else:
                    nongroups.append(list(sub1))

        # build raw groups: non-separable groups followed by singleton groups
        groups001 = []
        for g in nongroups:
            groups001.append(g)
        for s in seps:
            groups001.append([s])

        # convert to {'seps', 'nonseps'} format
        subspaces = self.combine(groups001)
        return subspaces

