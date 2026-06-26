# Batch 151 Review: solutions #1316-1320

## Scope

- Global solution numbers: #1316-#1320
- Source ranges after index rebuild:
  - #1316: lines 50033-50047
  - #1317: lines 50061-50075
  - #1318: lines 50088-50100
  - #1319: lines 50110-50123
  - #1320: lines 50146-50160

## Changes Made

- #1316: returned the short transformed flux formula to inline form, and expanded the fourth-moment computation using spherical coordinates so the displayed formula now carries real computational content.
- #1317: split the one-line derivative calculation into separate \(u_1\) and \(u_2\) parts, removed the jump keyword, and shortened the final conclusion to avoid repeating the problem's full differential expression.
- #1318: manually reviewed the displayed decomposition of the differential form and kept it because the built-up fractions would be crowded inline.
- #1319: manually reviewed the displayed final expansion and kept it because it is the final answer with a summation and convergence condition.
- #1320: split the long diagonalization proof into shorter sentences while keeping the short local formulas inline.

## Formula Layout Decisions

- #1316: the intermediate formula \(I=\iint_\Sigma (x^4+y^4+z^4)/a^2\,\mathrm dS\) is inline. The spherical-coordinate fourth-moment calculation remains displayed because it contains two definite integrals and the evaluated constant.
- #1317: all derivative identities are short local formulas and remain inline; the final answer is written simply as \(0\).
- #1318: the differential-form decomposition remains displayed. Although the heuristic marks it as short, it contains three built-up fractions and is the central method split.
- #1319: the power-series expansion remains displayed as the final result; forcing it inline would make the summation formula and condition harder to read.
- #1320: diagonalization, norm preservation, and the bounding inequality remain inline because each formula is short and local to the proof sentence.

## Per-Solution Review

- #1316: correct. On the sphere, \(\sqrt{x^2+y^2+z^2}=a\) and the outer normal is \((x,y,z)/a\), so the flux reduces to a sum of fourth moments. The spherical-coordinate computation gives \(\iint_\Sigma x^4\,\mathrm dS=4\pi a^6/5\), and symmetry gives \(I=12\pi a^4/5\).
- #1317: correct. For \(u_1=yf(x/y)\) and \(u_2=xg(y/x)\), the two second-derivative contributions each vanish in the combination \(x u_{xx}+y u_{xy}\), so the requested value is \(0\).
- #1318: correct. The integrand is \(\mathrm d(\frac12\ln(x^2+y^2))+\mathrm d\theta\). The endpoint logarithmic values agree, and the polar angle changes from \(\pi\) to \(0\), giving \(I=-\pi\).
- #1319: correct. With \(t=(x-1)/(x+1)\), \(x=(1+t)/(1-t)\), so \(\ln x=\ln(1+t)-\ln(1-t)=2(t+t^3/3+t^5/5+\cdots)\). The condition \(|t|<1\) corresponds to \(x>0\).
- #1320: correct. Since \(M\) is real symmetric, orthogonal diagonalization reduces the quadratic form on the unit sphere to a convex combination of eigenvalues, so the extrema are the smallest and largest eigenvalues.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1066
  - `long_inline_flagged`: 78
  - `jump_keyword_flagged`: 547
  - `short_display_flagged`: 885
- Batch index check:
  - #1317 and #1320 are `AUTO_INDEXED_NO_HEURISTIC_FLAG`.
  - #1316, #1318, and #1319 remain heuristic `短display待判定` items, but each was visually and mathematically reviewed and kept for the reasons above.
- Batch solution-line check: no source line of length `>=150` inside the #1316-#1320 solution windows.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, `LaTeX Warning`, package warning, undefined-control-sequence, or missing-character hits.
- PDF info: `750` pages, A4.
- Rendered and inspected:
  - `tmp\pdfs\batch_151_1316_1320_final-748.png`
  - `tmp\pdfs\batch_151_1316_1320_final-749.png`
  - `tmp\pdfs\batch_151_1316_1320_final-750.png`

## Decision

Batch #1316-#1320 is released after content, calculation, method-consistency, and formula-layout review. Short/local formulas were kept inline, while the retained displays are central, structured formulas whose inline form would be less readable.
