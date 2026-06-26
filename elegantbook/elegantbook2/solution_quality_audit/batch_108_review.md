# Batch 108 Review: solutions #1101-1105

## Scope

- Global solution numbers: #1101-1105
- Source ranges after index rebuild:
  - #1101: lines 45046-45060
  - #1102: lines 45061-45076
  - #1103: lines 45077-45092
  - #1104: lines 45093-45106
  - #1105: lines 45107-45123

## Changes made

- #1102: expanded the explanation with two concrete counterexamples. The first shows that the two partial derivatives may exist while the function is discontinuous; the second shows that continuity at a point need not give the partial derivative. The piecewise counterexample is kept in display form because it is the structural definition of the example, not a minor inline calculation.
- #1104: promoted the long Green-formula computation chain from inline math to display math. This is a genuine long formula chain, near the layout threshold and central to the method, so display math improves readability without over-promoting a minor formula.
- #1105: expanded the option-by-option comparison argument, keeping the short asymptotic and comparison formulas inline because none is close to the 3/4 text-width threshold.

## Per-solution review

- #1101: correct, clear, and method-consistent. It states the standard second-order linear ODE form, explains that coefficients may depend only on the independent variable, and rules out A as first-order, C as nonlinear in $y''$, and D as nonlinear in $y$.
- #1102: correct and now sufficiently explicit. The solution separates the two logical directions: partial derivatives only test coordinate-axis limits, while continuity requires all paths; continuity also does not guarantee the coordinate-axis difference quotient. Formula layout is appropriate: the piecewise definition remains displayed, while the short derivative and path checks remain inline.
- #1103: correct and clear. The gradient normal and the normal to $z=0$ give the acute angle through $\cos\theta=1/\sqrt2$. The inline cosine calculation is moderately long but below the 3/4 text-width threshold and reads naturally in the sentence, so it should not be split mechanically.
- #1104: correct and now better laid out. Green's formula gives $2\operatorname{Area}(D)=2\pi ab$ for the counterclockwise ellipse. The direction note prevents the common sign error, and the long computation chain is displayed.
- #1105: correct and clearer than the compressed version. A, C, and D are shown convergent by standard asymptotic or exponential-series comparisons, while B diverges since $1/\ln n>1/n$ eventually. The short comparison formulas are left inline.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1090
  - `long_inline_flagged`: 112
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_108_1101_1105_strict_final-687.png`
  - `tmp\pdfs\batch_108_1101_1105_strict_final-688.png`
  - `tmp\pdfs\batch_108_1101_1105_strict_final-689.png`

## Decision

Batch #1101-#1105 is released after the #1102, #1104, and #1105 edits and strict formula-layout recheck.
