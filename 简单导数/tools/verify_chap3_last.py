"""Numerical certificate for the last example in chapters/chap3.tex.

The script verifies the final inequality after it has been converted to
a one-parameter comparison.  Put

    a = 1 - u^2, 0 < u < sqrt(1/2),
    phi(x) = x^2 exp(-x) - a^2 exp(-a) log(x),
    c = a exp(-a).

If x1 < x2 < x3 are the three roots of phi(x)=c and x4 < x5 are the two
critical points of phi, set

    P = x1*x2*x3, Q = x2*x3,
    p(z) = (z-x1)(z-x2)(z-x3),
    s(z) = -(phi(z)-c)/p(z).

The target inequality is equivalent to

    E(u) = B*(-p(Q))/(A*p(P))*s(Q) - s(P) > 0,

where A=x2+x3+x4 and B=2*x1+x5.  This avoids the cancellation in the
original expression, whose value is O((1-a)^2) near a=1.

This is a reproducible high-precision certificate, not a symbolic proof
assistant.  It deliberately checks the original expression, the converted
gap, and the part (1) expression on the same mesh.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import mpmath as mp

PADE_DELTA = "0.002"
PADE_P = (
    "0.033301316220612484",
    "-0.096664059426495058",
    "0.073382508893037546",
    "-0.0028292673804696938",
    "0.0021781090213382421",
)
PADE_Q = (
    "1",
    "-0.94084008085698978",
    "0.21490565384106852",
    "-0.07461774302075376",
    "0.035115112305247637",
)


@dataclass(frozen=True)
class Values:
    u: mp.mpf
    a: mp.mpf
    x1: mp.mpf
    x2: mp.mpf
    x3: mp.mpf
    x4: mp.mpf
    x5: mp.mpf
    part1_scaled: mp.mpf
    target_scaled: mp.mpf
    gap: mp.mpf
    gap_derivative: mp.mpf
    order_margin: mp.mpf


def bisect_root(fun, lo: mp.mpf, hi: mp.mpf, rounds: int = 120) -> mp.mpf:
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
        fmid = fun(mid)
        if flo * fmid <= 0:
            hi = mid
            fhi = fmid
        else:
            lo = mid
            flo = fmid
    return (lo + hi) / 2


def roots_and_criticals(a: mp.mpf) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    def f(x: mp.mpf) -> mp.mpf:
        return x * x * mp.exp(a - x) - a * a * mp.log(x) - a

    def fp(x: mp.mpf) -> mp.mpf:
        return mp.exp(a - x) * (2 * x - x * x) - a * a / x

    x4 = bisect_root(fp, mp.mpf("1e-40"), mp.mpf(1))
    x5 = bisect_root(fp, mp.mpf(1), mp.mpf(2) - mp.mpf("1e-40"))
    x1 = bisect_root(f, mp.exp(-10 / a), a)
    x2 = bisect_root(f, a, mp.mpf(1))

    hi = mp.mpf(2)
    while f(hi) > 0:
        hi *= 2
    x3 = bisect_root(f, mp.mpf(1), hi)
    return x1, x2, x3, x4, x5


def evaluate(u: mp.mpf) -> Values:
    u = mp.mpf(u)
    a = 1 - u * u
    au = -2 * u
    x1, x2, x3, x4, x5 = roots_and_criticals(a)

    m = a * a * mp.exp(-a)
    c = a * mp.exp(-a)
    ma = a * (2 - a) * mp.exp(-a)
    ca = (1 - a) * mp.exp(-a)

    def phi(x: mp.mpf) -> mp.mpf:
        return x * x * mp.exp(-x) - m * mp.log(x)

    def h(x: mp.mpf) -> mp.mpf:
        return phi(x) - c

    def hx(x: mp.mpf) -> mp.mpf:
        return mp.exp(-x) * (2 * x - x * x) - m / x

    def ha(x: mp.mpf) -> mp.mpf:
        return -ma * mp.log(x) - ca

    def hxx(x: mp.mpf) -> mp.mpf:
        return mp.exp(-x) * (x * x - 4 * x + 2) + m / (x * x)

    x1a = -ha(x1) / hx(x1)
    x2a = -ha(x2) / hx(x2)
    x3a = -ha(x3) / hx(x3)
    x4a = (ma / x4) / hxx(x4)
    x5a = (ma / x5) / hxx(x5)

    x1u = x1a * au
    x2u = x2a * au
    x3u = x3a * au
    x4u = x4a * au
    x5u = x5a * au

    p = lambda z: (z - x1) * (z - x2) * (z - x3)
    f = lambda z: z * z * mp.exp(a - z) - a * a * mp.log(z) - a

    P = x1 * x2 * x3
    Q = x2 * x3
    Pu = P * (x1u / x1 + x2u / x2 + x3u / x3)
    Qu = Q * (x2u / x2 + x3u / x3)

    A = x2 + x3 + x4
    B = 2 * x1 + x5
    Au = x2u + x3u + x4u
    Bu = 2 * x1u + x5u

    pP = p(P)
    pQ = p(Q)
    sP = -h(P) / pP
    sQ = -h(Q) / pQ
    ratio = B * (-pQ) / (A * pP)
    gap = ratio * sQ - sP

    def p_log_u(z: mp.mpf, zu: mp.mpf) -> mp.mpf:
        return zu * (1 / (z - x1) + 1 / (z - x2) + 1 / (z - x3)) - (
            x1u / (z - x1) + x2u / (z - x2) + x3u / (z - x3)
        )

    pP_log_u = p_log_u(P, Pu)
    pQ_log_u = p_log_u(Q, Qu)
    hPu = hx(P) * Pu + ha(P) * au
    hQu = hx(Q) * Qu + ha(Q) * au
    sP_u = -hPu / pP - sP * pP_log_u
    sQ_u = -hQu / pQ - sQ * pQ_log_u
    ratio_u = ratio * (Bu / B - Au / A + pQ_log_u - pP_log_u)
    gap_derivative = ratio_u * sQ + ratio * sQ_u - sP_u

    target = A * f(P) + B * f(Q)
    part1 = x4 * f(x5) + x5 * f(x4)
    order_margin = min(x4 - x1, x2 - x4, 1 - x2, x5 - 1, x3 - x5, P - x1, x2 - P, Q - x5, x3 - Q)

    return Values(
        u=u,
        a=a,
        x1=x1,
        x2=x2,
        x3=x3,
        x4=x4,
        x5=x5,
        part1_scaled=-part1 / (u**4),
        target_scaled=target / (u**4),
        gap=gap,
        gap_derivative=gap_derivative,
        order_margin=order_margin,
    )


def pade_value_and_derivative(u: mp.mpf) -> tuple[mp.mpf, mp.mpf]:
    u_max = mp.sqrt(mp.mpf("0.5"))
    z = 2 * u / u_max - 1
    p = [mp.mpf(c) for c in PADE_P]
    q = [mp.mpf(c) for c in PADE_Q]

    numerator = sum(p[i] * z**i for i in range(len(p)))
    denominator = sum(q[i] * z**i for i in range(len(q)))
    numerator_z = sum(i * p[i] * z ** (i - 1) for i in range(1, len(p)))
    denominator_z = sum(i * q[i] * z ** (i - 1) for i in range(1, len(q)))

    value = numerator / denominator
    derivative_z = (numerator_z * denominator - numerator * denominator_z) / (denominator * denominator)
    derivative_u = derivative_z * (2 / u_max)
    return value, derivative_u


def pade_sturm_check() -> tuple[int, int, str, str]:
    import sympy as sp

    z = sp.symbols("z")
    p = [sp.Rational(c) for c in PADE_P]
    q = [sp.Rational(c) for c in PADE_Q]
    delta = sp.Rational(PADE_DELTA)
    numerator = sum(p[i] * z**i for i in range(len(p)))
    denominator = sum(q[i] * z**i for i in range(len(q)))
    shifted_numerator = sp.expand(numerator - delta * denominator)

    denominator_poly = sp.Poly(denominator, z)
    shifted_poly = sp.Poly(shifted_numerator, z)
    denominator_roots = sp.polys.polytools.count_roots(denominator_poly, -1, 1)
    shifted_roots = sp.polys.polytools.count_roots(shifted_poly, -1, 1)
    denominator_endpoint = min(denominator_poly.eval(-1), denominator_poly.eval(1))
    shifted_endpoint = min(shifted_poly.eval(-1), shifted_poly.eval(1))

    if denominator_roots != 0 or denominator_endpoint <= 0:
        raise RuntimeError("Pade denominator is not certified positive")
    if shifted_roots != 0 or shifted_endpoint <= 0:
        raise RuntimeError("Pade shifted numerator is not certified positive")

    return (
        int(denominator_roots),
        int(shifted_roots),
        sp.N(denominator_endpoint, 20).__str__(),
        sp.N(shifted_endpoint, 20).__str__(),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dps", type=int, default=80)
    parser.add_argument("--step", default="0.0005")
    parser.add_argument("--edge", default="0.0001")
    args = parser.parse_args()

    mp.mp.dps = args.dps
    step = mp.mpf(args.step)
    edge = mp.mpf(args.edge)
    u_max = mp.sqrt(mp.mpf("0.5"))

    min_gap = mp.inf
    min_target_scaled = mp.inf
    min_part1_scaled = mp.inf
    min_order_margin = mp.inf
    max_gap_derivative = mp.mpf(0)
    min_pade_error_gap = mp.inf
    max_pade_error = mp.mpf(0)
    max_pade_error_derivative = mp.mpf(0)
    worst_gap: Values | None = None
    worst_pade: tuple[Values, mp.mpf, mp.mpf] | None = None

    u = edge
    count = 0
    while u <= u_max - edge:
        values = evaluate(u)
        count += 1
        if values.gap < min_gap:
            min_gap = values.gap
            worst_gap = values
        min_target_scaled = min(min_target_scaled, values.target_scaled)
        min_part1_scaled = min(min_part1_scaled, values.part1_scaled)
        min_order_margin = min(min_order_margin, values.order_margin)
        max_gap_derivative = max(max_gap_derivative, abs(values.gap_derivative))

        pade_value, pade_derivative = pade_value_and_derivative(u)
        pade_error_gap = values.gap - pade_value + mp.mpf(PADE_DELTA)
        if pade_error_gap < min_pade_error_gap:
            min_pade_error_gap = pade_error_gap
            worst_pade = (values, pade_value, pade_derivative)
        max_pade_error = max(max_pade_error, abs(values.gap - pade_value))
        max_pade_error_derivative = max(max_pade_error_derivative, abs(values.gap_derivative - pade_derivative))
        u += step

    if worst_gap is None:
        raise RuntimeError("empty scan")
    if worst_pade is None:
        raise RuntimeError("empty Pade scan")

    # The gap has the endpoint limit 1/(4e) as u -> 0+.
    endpoint_gap = 1 / (4 * mp.e)
    derivative_guard = mp.mpf("1.0")
    mesh_lower_gap = min(min_gap, endpoint_gap) - derivative_guard * step / 2
    pade_derivative_guard = mp.mpf("0.001")
    mesh_lower_pade_error_gap = min_pade_error_gap - pade_derivative_guard * step / 2
    sturm = pade_sturm_check()

    print(f"mp.dps = {mp.mp.dps}")
    print(f"mesh points = {count}")
    print(f"u range = [{mp.nstr(edge, 12)}, {mp.nstr(u_max - edge, 12)}]")
    print(f"step = {mp.nstr(step, 12)}")
    print(f"endpoint gap limit 1/(4e) = {mp.nstr(endpoint_gap, 30)}")
    print(f"min gap E = {mp.nstr(min_gap, 30)} at u = {mp.nstr(worst_gap.u, 20)}, a = {mp.nstr(worst_gap.a, 20)}")
    print(f"max sampled |E'| = {mp.nstr(max_gap_derivative, 30)}")
    print(f"mesh lower gap with |E'|<=1 guard = {mp.nstr(mesh_lower_gap, 30)}")
    print(f"Pade delta = {PADE_DELTA}")
    print(
        "Pade Sturm roots in [-1,1]: "
        f"denominator={sturm[0]}, shifted_numerator={sturm[1]}"
    )
    print(
        "Pade endpoint lower values: "
        f"denominator={sturm[2]}, shifted_numerator={sturm[3]}"
    )
    print(f"max sampled |E-R| = {mp.nstr(max_pade_error, 30)}")
    print(f"max sampled |(E-R)'| = {mp.nstr(max_pade_error_derivative, 30)}")
    print(
        "min E-R+delta = "
        f"{mp.nstr(min_pade_error_gap, 30)} at u = {mp.nstr(worst_pade[0].u, 20)}"
    )
    print(
        "mesh lower E-R+delta with |(E-R)'|<=0.001 guard = "
        f"{mp.nstr(mesh_lower_pade_error_gap, 30)}"
    )
    print(f"min target/(1-a)^2 = {mp.nstr(min_target_scaled, 30)}")
    print(f"min -part1/(1-a)^2 = {mp.nstr(min_part1_scaled, 30)}")
    print(f"min order/location margin = {mp.nstr(min_order_margin, 30)}")
    print(
        "worst roots = "
        + ", ".join(mp.nstr(x, 20) for x in (worst_gap.x1, worst_gap.x2, worst_gap.x3, worst_gap.x4, worst_gap.x5))
    )

    if max_gap_derivative >= derivative_guard:
        raise SystemExit("FAILED: sampled derivative exceeded the guard")
    if mesh_lower_gap <= 0:
        raise SystemExit("FAILED: gap lower bound is not positive")
    if max_pade_error_derivative >= pade_derivative_guard:
        raise SystemExit("FAILED: sampled Pade error derivative exceeded the guard")
    if mesh_lower_pade_error_gap <= 0:
        raise SystemExit("FAILED: Pade error envelope is not positive")
    if min_target_scaled <= 0:
        raise SystemExit("FAILED: original target check is not positive")
    if min_part1_scaled <= 0:
        raise SystemExit("FAILED: part (1) check is not positive")
    if min_order_margin <= 0:
        raise SystemExit("FAILED: required order/location margin is not positive")
    print("PASS")


if __name__ == "__main__":
    main()
