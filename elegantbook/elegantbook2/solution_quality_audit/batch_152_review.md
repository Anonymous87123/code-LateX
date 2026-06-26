# Batch 152 Review: solutions #1321-1322

## Scope

- Global solution numbers: #1321-#1322
- Source ranges after index rebuild:
  - #1321: lines 50177-50192
  - #1322: lines 50211-50234

## Changes Made

- #1321: split the compressed one-line proof into the even-function derivative step, Taylor expansion step, \(O(1/n^2)\) substitution step, and absolute comparison step. Added the explicit absolute-value comparison needed for absolute convergence.
- #1322: removed the jump keyword, converted the long inline summation formulas to display math, and shortened the final conclusion so the target inequality is not awkwardly broken across a line.

## Formula Layout Decisions

- #1321: the Taylor expansion remains displayed because the inline version broke awkwardly at a plus sign in the rendered PDF; it is the central estimate for the proof. The \(O(1/n^2)\) and comparison formulas remain inline because they are short local statements.
- #1322: the two displayed formulas are the termwise-integrated series and the resulting alternating series, both central and too wide/tall for comfortable inline placement. The final bound adjustment is kept inline in prose.

## Per-Solution Review

- #1321: correct. Since \(f\) is even and differentiable near \(0\), \(f'(0)=0\). Taylor's formula gives \(f(x)-1=O(x^2)\), so \(f(1/n)-1=O(n^{-2})\). The absolute comparison with \(\sum n^{-2}\) proves absolute convergence.
- #1322: correct. The Weierstrass test gives uniform convergence and hence continuity of \(F\). Uniform convergence justifies termwise integration on \([0,\pi/2]\). The sine values leave an alternating series with decreasing absolute terms, giving the stated two-sided bound.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1066
  - `long_inline_flagged`: 77
  - `jump_keyword_flagged`: 546
  - `short_display_flagged`: 887
- Batch index check:
  - #1321 and #1322 remain heuristic `短display待判定` items only because the retained displays are manually judged necessary.
- Batch solution-line check: no source line of length `>=150` inside the #1321-#1322 solution windows.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, `LaTeX Warning`, package warning, undefined-control-sequence, or missing-character hits.
- PDF info: `750` pages, A4.
- Rendered and inspected:
  - `tmp\pdfs\batch_152_1321_1322_final_v2-749.png`
  - `tmp\pdfs\batch_152_1321_1322_final_v2-750.png`

## Decision

Batch #1321-#1322 is released after content, calculation, method-consistency, and formula-layout review. The last batch now follows the corrected rule: short local formulas stay inline, while genuinely long or structurally central formula chains are displayed.
