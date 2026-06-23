# Batch 076 Review: Global Solutions #936-940

Scope: `elegantbook2.tex` global solutions #936-940, PDF pages 640-642.

## Changes Made

- #936: Fixed the double-integral solution layout and the broken display punctuation. The inner integral and the final one-variable computation are now explicit, so the answer is not a compressed jump from setup to result.
- #939: Expanded the tangent-plane solution. The revision states the surface normal, the two given plane normals, the cross product direction, the proportional-normal condition, the quadratic equation for the tangent point, and the final two tangent planes.

## No-Edit Decisions

- #937: Rechecked the closed curve integral. Since \(P_y=Q_x\) on the simply connected plane, the form is exact; the potential-function check also shows a closed curve integral of \(0\). The existing formulas are short enough to remain inline.
- #938: Rechecked the power-series substitution \(t=(x-1)/x=1-1/x\). The convergence condition \(-1\le t<1\) gives \(x\ge 1/2\), so the interval \([1/2,+\infty)\) is correct. Short endpoint and inequality steps remain inline.
- #940: Rechecked the inverse-function method for the ODE. With \(x=x(y)\), \(y'=1/x'\) and \(y''=-x''/(x')^3\), giving \(x''-4x=e^{2y}\); the implicit general solution and constant solutions are both accounted for.

## Self-Check

- Correctness: #936-#940 were recalculated; the answers are \(\frac{4}{15}(3^{5/2}-2^{5/2}-1)\), \(0\), \([1/2,+\infty)\), \(x+y-\frac{1+\sqrt2}{2}=0\) and \(x+y-\frac{1-\sqrt2}{2}=0\), and \(x=C_1e^{2y}+C_2e^{-2y}+\frac14ye^{2y}\) with constant solutions \(y=C\).
- Completeness: #936 now includes both integration stages; #939 now includes the geometric normal-vector condition and tangent-point calculation. #937, #938, and #940 already contain the necessary exactness, endpoint, and inverse-function reasoning.
- Method consistency: #937 uses exact differentials; #938 follows the standard known series \(\sum t^n/n\); #939 uses tangent-plane normals and cross products; #940 uses the standard exchange of dependent and independent variables for equations involving powers of \(y'\).
- Formula layout: No new display was introduced for small substitutions or short endpoint checks. Displays are kept only where they carry a structural equality chain, a cross-product/proportionality condition, or a final pair of tangent-plane equations.

## Verification

- Rebuilt `solution_quality_audit/solution_index.csv`; total solutions remain 1322 and total auto-flagged count is 1087.
- Batch index after edits: #936-#940 all have `inline_long_count = 0`.
- `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan for `Overfull \hbox`, `Underfull \hbox`, LaTeX/package warnings, undefined control sequences, fatal errors, and `!` errors returned no matches.
- `pdfinfo` page count is 742.
- Rendered and visually inspected pages 640-642 at 180 dpi; no crowding, overlap, clipped text, dangling page-bottom text, or inappropriate formula promotion/compression found.
