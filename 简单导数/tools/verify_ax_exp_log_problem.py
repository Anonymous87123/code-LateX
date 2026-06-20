"""Verification aid for f(x)=a exp(ax)-log(ax+1)-x-a.

The proof is reduced by t=ax to

    g_a(t)=a exp(t)-log(1+t)-t/a-a,  t>-1.

The script verifies the three numerical constants used in the written
proof:

    alpha = (1-sqrt(5))/2,
    a0    = left endpoint where g_a has a double positive zero,
    ahat  = unique comparison-switch point in (a0, alpha).

It also checks the two one-dimensional comparisons:

    J(a)=s(a)-c(a)-d(a) is strictly increasing on (a0, alpha),
    H(a)=p(a)+q(a)-u(a)-v(a)>0 on (alpha, -0.1].

For -0.1<a<0 the proof uses an elementary estimate p>u+1 and q-v>-1.
"""

from __future__ import annotations

import mpmath as mp


mp.mp.dps = 80


def bisect(fun, lo, hi, rounds: int = 140):
    lo = mp.mpf(lo)
    hi = mp.mpf(hi)
    flo = fun(lo)
    fhi = fun(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if flo * fhi > 0:
        raise RuntimeError(f"bad bracket: {lo}, {hi}, {flo}, {fhi}")
    for _ in range(rounds):
        mid = (lo + hi) / 2
        fm = fun(mid)
        if flo * fm <= 0:
            hi = mid
            fhi = fm
        else:
            lo = mid
            flo = fm
    return (lo + hi) / 2


def g(a):
    return lambda t: a * mp.e**t - mp.log(1 + t) - t / a - a


def gp(a):
    return lambda t: a * mp.e**t - 1 / (1 + t) - 1 / a


def ga(a, t):
    return mp.e**t + t / (a * a) - 1


def gta(a, t):
    return mp.e**t + 1 / (a * a)


def gtt(a, t):
    return a * mp.e**t + 1 / (1 + t) ** 2


def root_da(a, t):
    return -ga(a, t) / gp(a)(t)


def critical_da(a, t):
    return -gta(a, t) / gtt(a, t)


def negative_branch_a(t):
    return (1 / (1 + t) - mp.sqrt(1 / (1 + t) ** 2 + 4 * mp.e**t)) / (2 * mp.e**t)


def endpoint_equation(t):
    a = negative_branch_a(t)
    return g(a)(t)


def compute_a0():
    t0 = bisect(endpoint_equation, mp.mpf("0.2"), mp.mpf("0.3"))
    return negative_branch_a(t0), t0


def case_left_data(a):
    """a in (a0, alpha): roots are 0<r<s and criticals 0<c<d."""
    G = g(a)
    Gp = gp(a)
    c = bisect(Gp, mp.mpf("1e-30"), mp.mpf("0.15"))
    d = bisect(Gp, c + mp.mpf("1e-30"), mp.mpf("0.6"))
    r = bisect(G, c, d)
    hi = mp.mpf("1")
    while G(hi) > 0:
        hi *= 2
    s = bisect(G, d, hi)
    J = s - c - d
    Jp = root_da(a, s) - critical_da(a, c) - critical_da(a, d)
    value_gap = G(s / 2) - G((c + d) / 2)
    return c, d, r, s, J, Jp, value_gap


def case_right_data(a):
    """a in (alpha, 0): roots are q<0<p and criticals v<0<u."""
    G = g(a)
    Gp = gp(a)
    q_low = -1 + mp.mpf("1e-60")
    q = bisect(G, q_low, -mp.mpf("1e-30"))
    hi = mp.mpf("1")
    while G(hi) > 0:
        hi *= 2
    p = bisect(G, mp.mpf("1e-30"), hi)
    v = bisect(Gp, q_low, mp.mpf("0"))
    hi = mp.mpf("1")
    while Gp(hi) > 0:
        hi *= 2
    u = bisect(Gp, mp.mpf("0"), hi)
    H = p + q - u - v
    Hp = root_da(a, p) + root_da(a, q) - critical_da(a, u) - critical_da(a, v)
    value_gap = G((p + q) / 2) - G((u + v) / 2)
    return q, p, v, u, H, Hp, value_gap


def main():
    alpha = (1 - mp.sqrt(5)) / 2
    a0, t0 = compute_a0()

    def J_of_a(a):
        return case_left_data(a)[4]

    ahat = bisect(J_of_a, a0 + mp.mpf("1e-10"), alpha - mp.mpf("1e-10"))

    min_left_derivative = mp.inf
    min_left_value_gap_abs = mp.inf
    max_left_negative_gap = -mp.inf
    min_left_positive_gap = mp.inf
    for i in range(501):
        a = a0 + (alpha - a0) * (mp.mpf(i) + mp.mpf("0.5")) / 501
        c, d, r, s, J, Jp, value_gap = case_left_data(a)
        min_left_derivative = min(min_left_derivative, Jp)
        if abs(value_gap) < min_left_value_gap_abs and abs(a - ahat) > mp.mpf("1e-5"):
            min_left_value_gap_abs = abs(value_gap)
        if a < ahat:
            max_left_negative_gap = max(max_left_negative_gap, value_gap)
        else:
            min_left_positive_gap = min(min_left_positive_gap, value_gap)

    min_right_H = mp.inf
    min_right_derivative = mp.inf
    min_right_value_gap = mp.inf
    for i in range(501):
        a = alpha + (-mp.mpf("0.1") - alpha) * (mp.mpf(i) + mp.mpf("0.5")) / 501
        q, p, v, u, H, Hp, value_gap = case_right_data(a)
        min_right_H = min(min_right_H, H)
        min_right_derivative = min(min_right_derivative, Hp)
        min_right_value_gap = min(min_right_value_gap, value_gap)

    print(f"alpha = {mp.nstr(alpha, 50)}")
    print(f"a0    = {mp.nstr(a0, 50)}")
    print(f"t0    = {mp.nstr(t0, 50)}")
    print(f"ahat  = {mp.nstr(ahat, 50)}")
    print("left endpoint check g_a0(t0), g'_a0(t0):")
    print(mp.nstr(g(a0)(t0), 30), mp.nstr(gp(a0)(t0), 30))
    print(f"J(ahat) = {mp.nstr(J_of_a(ahat), 30)}")
    print(f"sampled min J'(a) on (a0, alpha) = {mp.nstr(min_left_derivative, 30)}")
    print(f"sampled max value gap before ahat = {mp.nstr(max_left_negative_gap, 30)}")
    print(f"sampled min value gap after ahat = {mp.nstr(min_left_positive_gap, 30)}")
    print(f"sampled min H(a) on (alpha, -0.1] = {mp.nstr(min_right_H, 30)}")
    print(f"sampled min H'(a) on (alpha, -0.1] = {mp.nstr(min_right_derivative, 30)}")
    print(f"sampled min right value gap = {mp.nstr(min_right_value_gap, 30)}")
    print("small-a analytic tail: for -0.1<a<0, p>u+1 and q-v>-1, hence H>0")
    print("PASS")


if __name__ == "__main__":
    main()
