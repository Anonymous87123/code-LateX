# Batch 115 Review: solutions #1136-1140

## Scope

- Global solution numbers: #1136-1140
- Source ranges after index rebuild:
  - #1136: lines 45865-45883
  - #1137: lines 45891-45903
  - #1138: lines 45921-45939
  - #1139: lines 45951-45971
  - #1140: lines 45977-45998

## Changes made

- #1136: added the missing substitution check \(u=1+4r^2\) and the intermediate radial integral value \(149/60\), instead of jumping directly from the polar integral to the final mass.
- #1137: added the constant-\(C=0\) note so the implicit solution explicitly covers the special solutions \(x=1\) and \(y=-2\) that can be lost during separation.
- #1138: rewrote the path-independent integral solution around the standard \(P_y=Q_x\) criterion, displayed only the differential-equation skeleton and final endpoint evaluation, and kept the short \(P,Q\) definitions inline after visual review.
- #1139: added the missing boundary-singularity qualification for \(0\in\Sigma\), clarified the small-sphere orientation argument, and kept the short vector-field definition inline while retaining the long flux computation as display.
- #1140: promoted the two long summation chains to displayed computation skeletons, while leaving the short final expression for \(s(x)\) inline because it stays below the long-inline threshold in the rendered page.

## Per-solution review

- #1136: correct and complete. The surface element \(dS=\sqrt{1+4x^2+4y^2}\,dxdy\) and polar reduction are consistent with the surface-integral method. The substitution gives \(\int_0^{\sqrt2}r^3\sqrt{1+4r^2}\,dr=149/60\), hence \(M=149\pi/30\).
- #1137: correct. Separation gives \(y-2\ln|y+2|=x+\ln|x-1|+C\), and exponentiation gives \((x-1)(y+2)^2=C e^{y-x}\). Allowing \(C=0\) records the singular solutions rather than silently discarding them.
- #1138: correct and method-consistent. On \(x>0\), path independence gives \(P_y=Q_x\), hence \((x\varphi(x))'=\cos x\). The condition \(\varphi(\pi/2)=0\) gives \(\varphi(x)=(\sin x-1)/x\), and the potential \(F=y\varphi(x)\) gives the integral value \(-1\).
- #1139: correct with the added domain qualification. Away from the origin the field is divergence-free. If \(0\notin\Omega\), the flux is \(0\); if \(0\in\Omega\), excising a small sphere and tracking the inner normal gives \(4\pi\). If \(0\in\Sigma\), the usual surface integral is not defined.
- #1140: correct. Setting \(t=x^3\) reduces the series to \(3\sum nt^n/n!+\sum t^n/n!\), with \(\sum nt^n/n!=te^t\), so \(s(x)=(3x^3+1)e^{x^3}\) and the convergence domain is all real \(x\).

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1091
  - `long_inline_flagged`: 109
  - `short_display_flagged`: 840, with #1136, #1138, #1139, and #1140 displays manually reviewed as computation skeletons or final case structure.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_115_1136_1140_final_v2-697.png`
  - `tmp\pdfs\batch_115_1136_1140_final_v2-698.png`
  - `tmp\pdfs\batch_115_1136_1140_final_v2-699.png`

## Decision

Batch #1136-#1140 is released after content, calculation, method-consistency, and formula-layout review.
