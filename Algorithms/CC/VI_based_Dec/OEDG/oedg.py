import numpy as np


class OEDG:
    def __init__(self, fun, info, cfg):
        self.fun = fun
        self.info = info
        self.cfg = cfg

        self.n = int(info['dimension'])
        self.lower = float(info['lower'])
        self.upper = float(info['upper'])

        self.x_ll = np.ones(self.n) * self.lower
        self.f_ll = None
        self.counter = 0

    # ----- basic helpers -----
    def _eval(self, x):
        y = self.fun(x)
        self.counter += 1
        return float(np.array(y).ravel()[0])

    @staticmethod
    def _gamma(d):
        muM = np.finfo(float).eps / 2.0
        return (d * muM) / (1.0 - d * muM)

    def _interaction(self, sub1, sub2):
        """RDG2-style 4-point finite-difference test between two variable sets."""
        if not sub2:
            return False

        x_ul = np.ones(self.n) * self.lower
        x_ul[sub1] = self.upper
        f_ul = self._eval(x_ul)

        mid = 0.5 * (self.lower + self.upper)
        x_lm = np.ones(self.n) * self.lower
        x_um = x_ul.copy()
        x_lm[sub2] = mid
        x_um[sub2] = mid
        f_lm = self._eval(x_lm)
        f_um = self._eval(x_um)

        d1 = self.f_ll - f_ul
        d2 = f_lm - f_um

        eps = self._gamma(self.n ** 0.5 + 2.0) * (
            abs(self.f_ll) + abs(f_ul) + abs(f_lm) + abs(f_um)
        )
        return abs(d1 - d2) > eps

    # ----- INTERACT / INTERACT-OV -----
    def _interact_rec(self, sub1, sub2):
        if not self._interaction(sub1, sub2):
            return sub1, sub2
        if len(sub2) == 1:
            return sub1 + sub2, []

        k = len(sub2) // 2
        left, right = sub2[:k], sub2[k:]
        s1_l, rem_l = self._interact_rec(sub1.copy(), left)
        s1_r, rem_r = self._interact_rec(sub1.copy(), right)
        sub1_new = sorted(list(set(s1_l + s1_r)))
        rem_new = sorted(list(set(rem_l + rem_r)))
        return sub1_new, rem_new

    def _interact(self, seeds, all_idx):
        sub1 = list(seeds)
        sub2 = [i for i in all_idx if i not in sub1]
        sub1_new, rem = self._interact_rec(sub1, sub2)
        return sorted(sub1_new), sorted(rem)

    def _interact_ov_rec(self, group, other, out):
        """Recursive INTERACT-OV: prune non-interacting halves, descend to vars that still interact."""
        if not group or not other:
            return
        if not self._interaction(group, other):
            return
        if len(group) == 1:
            out.append(group[0])
            return
        k = len(group) // 2
        self._interact_ov_rec(group[:k], other, out)
        self._interact_ov_rec(group[k:], other, out)

    def _interact_ov(self, sub_idx, other_idx):
        ov = []
        if not sub_idx or not other_idx:
            return ov
        self._interact_ov_rec(sorted(list(sub_idx)), sorted(list(other_idx)), ov)
        return sorted(set(ov))

    # ----- Stage I: initial grouping -----
    def _stage_one(self):
        all_idx = list(range(self.n))
        V1 = set(all_idx)
        N = []
        OV = []
        rng = np.random.default_rng()
        total = self.n
        progress_step = max(1, total // 10)

        while V1:
            xi = int(rng.choice(list(V1)))
            X1, _ = self._interact([xi], all_idx)
            X1_set = set(X1)
            remain = [i for i in all_idx if i not in X1_set]
            XOV = set(self._interact_ov(X1, remain))
            N.append(sorted(list(X1_set)))
            OV.append(XOV)
            V1 -= X1_set

        return N, OV

    # ----- Stage II: refinement (SUD + SD) -----
    def _has_inter(self, v, S):
        return bool(S) and self._interaction([v], list(S))

    def _sud(self, i, N, OV):
        OVi = OV[i]
        if not OVi:
            return False
        M = len(N)
        for j in range(M):
            if j == i or not OV[j]:
                continue
            Xs = OVi & OV[j]
            if not Xs:
                continue
            Xr = OVi - Xs
            if Xr:
                for v in Xs:
                    if not self._has_inter(v, Xr):
                        return True
            if Xs:
                for v in Xr:
                    if not self._has_inter(v, Xs):
                        return True
        return False

    def _sd(self, i, N, OV, H):
        Ni = set(N[i])
        OVi = set(OV[i])
        Xd = (OVi & H) or (Ni - OVi)
        if not Xd:
            return N, OV, False

        # try each candidate in Xd at most once (shuffled order)
        rng = np.random.default_rng()
        candidates = list(Xd)
        rng.shuffle(candidates)

        X1 = set()
        for xd in candidates:
            sub1, _ = self._interact([xd], sorted(list(Ni)))
            X1 = set(sub1)
            if 0 < len(X1) < len(Ni):
                break

        if len(X1) == 0 or len(X1) == len(Ni):
            return N, OV, False

        N.append(sorted(list(X1)))
        OV.append(set())
        new_idx = len(N) - 1

        X2 = Ni - X1
        OV_between = set(self._interact_ov(sorted(list(X1)), sorted(list(X2))))
        Ni_updated = Ni - X1 - OV_between

        if Ni_updated:
            OVi_updated = set(self._interact_ov(sorted(list(Ni_updated)), list(range(self.n))))
        else:
            OVi_updated = set()
        OV1_updated = set(self._interact_ov(sorted(list(X1)), list(range(self.n))))

        OV[new_idx] = OV1_updated
        OV[i] = OVi_updated
        N[i] = sorted(list(Ni_updated))
        return N, OV, True

    def _stage_two(self, N, OV):
        cnt = {}
        for ov in OV:
            for v in ov:
                cnt[v] = cnt.get(v, 0) + 1
        H = {v for v, c in cnt.items() if c >= 2}

        k = len(N)
        i = 0
        while i < k:
            if self._sud(i, N, OV):
                N, OV, changed = self._sd(i, N, OV, H)
                if changed:
                    k = len(N)
                else:
                    i += 1  # prevent infinite loop if SD made no split
            else:
                i += 1

        N2 = []
        OV2 = []
        for comp, ov in zip(N, OV):
            if comp:
                N2.append(sorted(list(set(comp))))
                OV2.append(set(ov))
        return N2, OV2

    # ----- public -----
    def decompose(self):
        self.counter = 0
        self.f_ll = self._eval(self.x_ll.copy())

        N, OV = self._stage_one()
        N_ref, OV_ref = self._stage_two(N, OV)

        return {
            'subcomponents': N_ref,
            'overlaps': OV_ref,
        }
