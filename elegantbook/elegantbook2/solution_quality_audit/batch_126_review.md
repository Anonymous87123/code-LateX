# Batch 126 Review: solutions #1191-1195

## Scope

- Global solution numbers: #1191-1195
- Source ranges after index rebuild:
  - #1191: lines 47214-47231
  - #1192: lines 47237-47263
  - #1193: lines 47269-47283
  - #1194: lines 47289-47297
  - #1195: lines 47305-47335

## Changes made

- #1191: added the reason for using \(\nabla F\times\nabla G\) as a tangent direction to an intersection curve, removed forced inline display style, and displayed the gradient/cross-product and directional-derivative computations.
- #1192: displayed the upper-hemisphere parametrization, keeping the parameter ranges and local identities inline because they are short. The main inertia integral remains the central computation block.
- #1193: displayed the integrating-factor equality chain after visual review showed that it was too dense inline; kept the short transformed equation \((y\sec x)'=1\) inline.
- #1194: reviewed without content edits. The homogeneous solution and resonance ansatz are correct and the inline formulas are short enough.
- #1195: displayed the initial decomposition of the exponential series, the recombined sum function, and the final substituted answer. The short identity \(\sum t^n/n!=e^t-1\) stays inline.

## Per-solution review

- #1191: correct. The curve is the intersection of \(F=x^2+y^2+z^2=6\) and \(G=x+y+z=0\), so a tangent vector is perpendicular to both normals. At \((1,-2,1)\), \(\nabla F=(2,-4,2)\), \(\nabla G=(1,1,1)\), and \(\nabla F\times\nabla G=(-6,0,6)\). The two possible unit tangent directions differ by sign, but \(\nabla u(1,-2,1)\cdot\vec t=0\) for both.
- #1192: correct. For the upper sphere, \(x^2+y^2=a^2\sin^2\varphi\) and \(\mathrm dS=a^2\sin\varphi\,\mathrm d\varphi\,\mathrm d\theta\). Thus \(J_z=2\pi a^4\int_0^{\pi/2}\sin^3\varphi\,\mathrm d\varphi=4\pi a^4/3\).
- #1193: correct. On any interval not crossing \(\cos x=0\), one may take the integrating factor as \(\sec x\) up to a nonzero constant factor. Multiplication gives \((y\sec x)'=1\), hence \(y=(x+C)\cos x\).
- #1194: correct. The characteristic roots of \(y''-y=0\) are \(\lambda=\pm1\). Since the forcing \(4xe^{-x}\) has exponent \(-1\), a simple characteristic root, the particular form must be multiplied by \(x\), giving \(y_p=x(Ax+B)e^{-x}\).
- #1195: correct. With \(t=x/2\), use \(n^2=n(n-1)+n\) to get \(\sum n^2t^n/n!=(t^2+t)e^t\), then add \(e^t-1\). The sum function is \(\left(x^2/4+x/2+1\right)e^{x/2}-1\), and the convergence domain is all real \(x\).

## Verification

- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1099
  - `long_inline_flagged`: 105
  - `short_display_flagged`: 858
  - Remaining short-display flags in this batch were manually reviewed as tangent-vector, parametrization, integrating-factor, or sum-function computation blocks rather than low-status definitions.
- Rendered and inspected:
  - `tmp\pdfs\batch_126_1191_1195_final_v2-712.png`
  - `tmp\pdfs\batch_126_1191_1195_final_v2-713.png`
  - `tmp\pdfs\batch_126_1191_1195_final_v2-714.png`

## Decision

Batch #1191-#1195 is released after content, calculation, method-consistency, and formula-layout review. The second visual pass led to an extra correction for #1193 and #1195, after which the rendered pages no longer show long inline formula crowding in this batch.
