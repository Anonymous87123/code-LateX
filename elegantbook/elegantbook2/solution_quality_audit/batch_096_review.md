# Batch 096 Review: solutions #1036-1040

## Scope

- Global solution numbers: #1036-1040
- Source ranges after index rebuild:
  - #1036: lines 43577-43590
  - #1037: lines 43596-43608
  - #1038: lines 43623-43634
  - #1039: lines 43647-43656
  - #1040: lines 43670-43677

## Changes made

- #1036: moved the full direction-derivative computation into display form, while keeping the short unit-vector definition inline as \(\nabla f/|\nabla f|\).
- #1037: moved the three curl component computations into display form because the combined inline formula was close to the practical line-width threshold and is the calculation core.
- #1038: changed the long second-kind surface-integral statement in the exercise prompt to display form, and fixed the source spacing in \(\iiint_V 3\,\mathrm{d}V\).
- #1040: normalized the one-sided-limit notation from \(f(0-0),f(0+0)\) to \(f(0-),f(0+)\), and used inline-size fractions for the short final average.

## Per-solution review

- #1036: correct and complete. The gradient is \((4x,2y)\), so \(\nabla f(1,1)=(4,2)\); along the gradient direction, the directional derivative equals \(|\nabla f(1,1)|=2\sqrt5\). The central computation is displayed, while the short unit-vector description remains inline.
- #1037: correct and complete. For \(\mathbf F=(P,Q,R)=(2x-3y,3x-z,y-2x)\), the standard curl formula gives components \(2,2,6\), hence \(2\mathbf i+2\mathbf j+6\mathbf k\). The displayed component line is retained as a real calculation block, not a decorative short display.
- #1038: correct and complete. The integral is the outward flux of \(\mathbf F=(x,y,z)\) through the sphere, \(\nabla\cdot\mathbf F=3\), and Gauss' formula gives \(3\cdot(4\pi R^3/3)=4\pi R^3\). The exercise prompt display is justified because the second-kind surface integral is too long for a clean inline fill-in statement.
- #1039: correct and complete. The integrating factor is \(e^{\sin x}\), yielding \((ye^{\sin x})'=1\), so \(y=(x+1)e^{-\sin x}\) after applying \(y(0)=1\). Its formulas are short enough to remain inline.
- #1040: correct and complete. Since \(0\) is an interior jump point of the period interval, the Fourier series converges to the average of the left and right limits, \((2+1)/2=3/2\), not to \(f(0)=2\). The final average is kept inline with compact fractions.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1091
  - `long_inline_flagged`: 116
  - `jump_keyword_flagged`: 578
  - `short_display_flagged`: 829
- Batch index:
  - #1036: `display_count=1`, `short_display_count=1`, `inline_long_count=0`
  - #1037: `display_count=1`, `short_display_count=1`, `inline_long_count=0`
  - #1038: `display_count=1`, `short_display_count=1`, `inline_long_count=0`
  - #1039: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #1040: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
- The short-display flags in #1036-#1038 were manually reviewed and accepted because each display is a core computation or a long prompt formula. Short definitions, small substitutions, and final compact conclusions remain inline.
- Compile: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan for fatal errors, LaTeX errors, undefined controls, missing characters, overfull/underfull boxes, and real warnings: no matches. The only text match was the package name `infwarerr`.
- Rendered and inspected:
  - `tmp\pdfs\batch_096_1036_1040\page_final-668.png`
  - `tmp\pdfs\batch_096_1036_1040\page_final-669.png`
  - `tmp\pdfs\batch_096_1036_1040\page_final-670.png`

## Decision

Batch #1036-1040 is released. The batch now balances the tightened formula rule with solution correctness: genuinely long/core computations are displayed, short low-status formulas stay inline, and all five answers have been checked for mathematical validity and method consistency.
