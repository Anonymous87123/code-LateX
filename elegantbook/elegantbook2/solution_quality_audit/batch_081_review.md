# Batch 081 Review (#961--965)

## Scope

- Reviewed solutions #961--965 in `elegantbook2.tex`.
- Corresponding rendered pages inspected: PDF pages 648--650, logical pages 598--600.

## Changes Made

- #962: Moved the four-tetrahedron-volume product from a long inline formula to a displayed computation:
  \[
    V=\frac16\cdot\frac{a^2}{x_0}\cdot\frac{b^2}{y_0}\cdot\frac{c^2}{z_0}
    =\frac{a^2b^2c^2}{6x_0y_0z_0}.
  \]
  This formula is both central to the optimization argument and visually long enough to justify display treatment.
- #964: Rephrased the chain-rule solution into shorter sentences while keeping the formulas inline. The derivative relation itself is not long enough to require a displayed equation, so this fixes the dense source/rendered paragraph without over-promoting short formulas.

## Mathematical Review

- #961: The Weierstrass-test proof is correct. For \(x\in[0,+\infty)\), \(0\le1-e^{-nx}\le1\) and \(n^2+x^2\ge n^2\), so the terms are bounded by \(1/n^2\); the comparison series converges.
- #962: The tangent plane, intercepts, volume formula, reduction to maximizing \(XYZ\) under \(X^2+Y^2+Z^2=1\), and Lagrange multiplier conclusion \(X=Y=Z=1/\sqrt3\) are correct. The boundary discussion rules out smaller boundary volume.
- #963: Dividing by \(\mathrm{d}x\) gives \(y'+y/x=(\ln x)/x\) on \(x>0\), hence the equation is first-order linear nonhomogeneous. Option B is correct.
- #964: With \(g(t)=f(t,t)\), \(g(0)=0\), \(g'(0)=a+b\), so \(\varphi'(0)=a+b(a+b)\). Option B is correct.
- #965: Green's formula is applied with \(P=-x^2y,\ Q=xy^2\); \(Q_x-P_y=x^2+y^2\), and the polar integral gives \(\pi a^4/2\). Option A is correct.

## Formula Layout Check

- #961--965 all have `inline_long_count=0` after rebuilding the index.
- The new display in #962 is intentional despite being counted as a short-display candidate: it is the key volume computation and was visually cramped as inline math.
- Short definitions and simple endpoint/option conclusions remain inline.

## Verification

- Rebuilt index with `python solution_quality_audit\build_solution_index.py`.
- Ran `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex`; compile completed successfully.
- Scanned `elegantbook2.log` for errors, overfull/underfull boxes, LaTeX/package warnings, missing characters, and undefined control sequences; no matches.
- Confirmed PDF page count remains 743.
- Rendered and visually inspected:
  - `tmp\pdfs\batch_081_961_965\page_final-648.png`
  - `tmp\pdfs\batch_081_961_965\page_final-649.png`
  - `tmp\pdfs\batch_081_961_965\page_final-650.png`

## Batch Result

#961--965 are closed for this pass: the solutions are mathematically correct, derivations are sufficiently explicit for their problem types, and formula layout follows the current \(3/4\textwidth\) long-inline standard.
