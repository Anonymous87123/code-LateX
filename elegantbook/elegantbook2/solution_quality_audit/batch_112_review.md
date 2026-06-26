# Batch 112 Review: solutions #1121-1125

## Scope

- Global solution numbers: #1121-1125
- Source ranges after index rebuild:
  - #1121: lines 45517-45531
  - #1122: lines 45537-45547
  - #1123: lines 45559-45568
  - #1124: lines 45580-45613
  - #1125: lines 45619-45638

## Changes made

- #1121: added the final quotient \(\bar z=\pi a^3/(2\pi a^2)=a/2\) so the centroid conclusion is not a jump from the surface integral to the coordinate.
- #1122: handled the constant solution \(y=1\) before division by \(\ln y\), stated the interval restriction for \(\cot x\), \(\tan x\), and \(\sec x\), and rewrote the final short formula inline so it does not break awkwardly.
- #1123: made the path-independence criterion explicit by noting continuous partial derivatives on the simply connected plane.
- #1125: expanded the power-series summation into two displayed calculation skeletons: the decomposition of the series and the two exponential-series identities used to compute it.

## Per-solution review

- #1121: correct and complete. Symmetry gives \(\bar x=\bar y=0\); the spherical parametrization gives \(\iint_\Sigma z\,\mathrm dS=\pi a^3\) and area \(2\pi a^2\), so \(\bar z=a/2\). The displayed surface integral is the computation core; the quotient is short and remains inline.
- #1122: correct after the domain and constant-solution handling. The separation step is now made only on \(\ln y\ne0\); \(y=e^{C\sec x}\) is understood on intervals not crossing zeros of \(\sin x\) or \(\cos x\). All formulas are short local steps and were deliberately kept inline.
- #1123: correct and method-consistent. The exactness condition gives \(\varphi'(x)=2x\), hence \(\varphi=x^2\), and the potential \(F=\frac12x^2y^2\) gives the integral \(1/2\). The formulas are below the 3/4-line threshold and remain inline.
- #1124: correct. The solution uses the solid-angle transformation under \((x,y,z)\mapsto(ax,by,cz)\) to obtain \(I=4\pi/(abc)\). The displayed formulas are structural method formulas, not expendable short substitutions.
- #1125: correct and clearer after splitting the long summation chain. The two display formulas are retained because they are the backbone of the sum-function derivation; the final substitution \(t=x^2\) and convergence-domain conclusion remain inline.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1090
  - `long_inline_flagged`: 111
  - `short_display_flagged`: 836, with #1125's new displays manually approved as derivation skeletons.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_112_1121_1125_final-693.png`
  - `tmp\pdfs\batch_112_1121_1125_final-694.png`

## Decision

Batch #1121-#1125 is released after content, calculation, method-consistency, and formula-layout review.
