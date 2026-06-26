# Batch 144 Review: solutions #1281-1285

## Scope

- Global solution numbers: #1281-#1285
- Source ranges after index rebuild:
  - #1281: lines 49257-49291
  - #1282: lines 49297-49305
  - #1283: lines 49314-49321
  - #1284: lines 49327-49339
  - #1285: lines 49346-49364

## Changes Made

- #1281: removed the duplicated closing word, replaced the jumpy transition around the \(w\)-substitution, and made the final multiplication by \(a/2\) explicit.
- #1282: retained the Fourier sine-coefficient computation after checking parity, integration by parts, and the value \(b_3=2/3\).
- #1283: split the compressed ODE solution into homogeneous solution, trial particular solution, substitution, and coefficient comparison.
- #1284: retained the displayed mixed partial derivative after checking the chain-rule order \(z_x\) then \(y\)-differentiation.
- #1285: replaced the jumpy transition before the transformed rectangular integral and retained the Jacobian computation.

## Formula Layout Decisions

- #1281: retained the antiderivative formula and definite integral evaluation as displays because they are the central long computation; shorter substitutions remain inline.
- #1282: kept the coefficient computation inline because the formulas are short and flow with the prose.
- #1283: kept the undetermined-coefficients equations inline after splitting the explanatory text.
- #1284: kept the final mixed-partial formula as a display because it is the requested result and is too dense for inline placement.
- #1285: kept the Jacobian determinant as a display because it is the core change-of-variables step; the transformed integral remains compact inline.

## Per-Solution Review

- #1281: correct. With \(\rho=t\) and \(\mathrm{d}s=a\sqrt{1+t^2+t^4}\,\mathrm{d}t\), the substitutions \(s=t^2\) and \(w=s+1/2\) give the stated mass.
- #1282: correct. For \(f(x)=x\), \(b_n=2(-1)^{n+1}/n\), hence the \(\sin3x\) coefficient is \(2/3\).
- #1283: correct. The particular solution \(e^x(Ax+B)\) gives \(2A=3,\ 2A+2B=0\), so \(y_p=\frac32(x-1)e^x\).
- #1284: correct. Differentiating \(z_x=(y+1/y)\cos w\) with respect to \(y\) gives the displayed expression.
- #1285: correct. The map \(u=x^2+y^2,\ v=y^2-x^2\) has determinant \(8xy\), and the first-quadrant region maps to \(9\le u\le16,\ 1\le v\le9\), giving \(7\).

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1083
  - `long_inline_flagged`: 90
  - `jump_keyword_flagged`: 559
  - `short_display_flagged`: 888
- Batch index check:
  - #1282, #1283, and #1285 are `AUTO_INDEXED_NO_HEURISTIC_FLAG`.
  - #1281 and #1284 remain manual-review items only because their displayed formulas are central computations.
- Batch solution-line check: no source line of length `>=150` inside the #1281-#1285 solution windows.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, `LaTeX Warning`, package warning, undefined-control-sequence, or missing-character hits.
- PDF info: `750` pages.
- Rendered and inspected:
  - `tmp\pdfs\batch_144_1281_1285_final-738.png`
  - `tmp\pdfs\batch_144_1281_1285_final-739.png`

## Decision

Batch #1281-#1285 is released after content, calculation, method-consistency, and formula-layout review. Remaining display flags are intentional central computations; the batch has no long inline formulas and no visual crowding in the rendered pages.
