# Batch 145 Review: solutions #1286-1290

## Scope

- Global solution numbers: #1286-#1290
- Source ranges after index rebuild:
  - #1286: lines 49371-49393
  - #1287: lines 49402-49422
  - #1288: lines 49428-49453
  - #1289: lines 49459-49468
  - #1290: lines 49477-49506

## Changes Made

- #1286: expanded the Gauss argument on the punctured domain and made the inner-boundary outward normal direction and flux computation explicit.
- #1287: replaced the jumpy transition in the harmonic-number reduction and split the final limiting argument into readable lines.
- #1288: split the Stokes setup into curl, normal direction, dot product, triangle area, and boundary-orientation check.
- #1289: retained the path-independence ODE solution after checking \(P_y=Q_x\), the condition \(\phi(\pi)=1\), and the potential function.
- #1290: replaced the jumpy transition in the work computation and split the normalization plus Lagrange-multiplier setup.

## Formula Layout Decisions

- #1286: kept the punctured-domain Gauss identity and the inner-boundary flux computation as displays because they are the core sign-sensitive steps; short normal-vector statements remain inline.
- #1287: kept the two-line harmonic-number reduction as a display because it is the central summation transformation; shorter partial-fraction and limit statements remain inline.
- #1288: kept the curl determinant and final Stokes integral as displays because they are central computations; the unit normal, dot product, and area explanations stay inline after splitting.
- #1289: kept all formulas inline because the ODE and potential computation are short and read naturally in one compact fill-in solution.
- #1290: kept the line-integral work computation as a display because it is the central derivation of \(W=\xi\eta\zeta\); the Lagrange equations remain inline after being separated into shorter prose.

## Per-Solution Review

- #1286: correct. On \(\Omega_\varepsilon=\Omega\setminus B_\varepsilon\), \(\operatorname{div}\vec F=0\). The inner boundary normal for the punctured domain points into the small ball, so \(\vec n_{\Omega_\varepsilon}=-\vec r/\varepsilon\) and the inner flux is \(-4\pi\), giving the outer flux \(4\pi\).
- #1287: correct. Partial fractions give \(\frac1{4n(4n+2)}=\frac18\frac1{n(2n+1)}\), and \(T_N=2H_N-2H_{2N+1}+2\), so the sum is \((1-\ln2)/4\).
- #1288: correct. \(\nabla\times\vec F=(-2z,-2x,-2y)\), the chosen unit normal is \((1,1,1)/\sqrt3\), and on \(x+y+z=1\) the integrand is \(-2/\sqrt3\); multiplying by area \(\sqrt3/2\) gives \(-1\).
- #1289: correct. Path independence gives \(\phi'(x)+\phi(x)/x=\sin x/x\), hence \((x\phi(x))'=\sin x\). The condition \(\phi(\pi)=1\) gives \(\phi(x)=(\pi-1-\cos x)/x\), and the potential \(U=\phi(x)y\) gives \(I=\pi\).
- #1290: correct. Along \(\vec r(t)=(t\xi,t\eta,t\zeta)\), the work is \(W=\xi\eta\zeta\). Under \(\xi^2/a^2+\eta^2/b^2+\zeta^2/c^2=1\), maximizing \(XYZ\) on \(X^2+Y^2+Z^2=1\) gives \(X=Y=Z=1/\sqrt3\), so \(M=(a/\sqrt3,b/\sqrt3,c/\sqrt3)\) and \(W_{\max}=abc/(3\sqrt3)\).

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1081
  - `long_inline_flagged`: 86
  - `jump_keyword_flagged`: 557
  - `short_display_flagged`: 888
- Batch index check:
  - #1287, #1289, and #1290 are `AUTO_INDEXED_NO_HEURISTIC_FLAG`.
  - #1286 and #1288 remain manual-review items only because their displayed formulas are central sign/orientation computations.
- Batch solution-line check: no source line of length `>=150` inside the #1286-#1290 solution windows.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, `LaTeX Warning`, package warning, undefined-control-sequence, or missing-character hits.
- PDF info: `750` pages.
- Rendered and inspected:
  - `tmp\pdfs\batch_145_1286_1290_final-739.png`
  - `tmp\pdfs\batch_145_1286_1290_final-740.png`
  - `tmp\pdfs\batch_145_1286_1290_final-741.png`
  - `tmp\pdfs\batch_145_1286_1290_final-742.png`

## Decision

Batch #1286-#1290 is released after content, calculation, method-consistency, and formula-layout review. Remaining display flags are intentional central computations; the batch has no long inline formulas and no visual crowding in the rendered pages.
