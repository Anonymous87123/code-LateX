# Batch 087 Review: solutions #991-995

## Scope

- Global solution numbers: #991-995
- Source ranges after final index rebuild:
  - #991: lines 42589-42597
  - #992: lines 42605-42631
  - #993: lines 42641-42648
  - #994: lines 42655-42665
  - #995: lines 42672-42683

## Changes made

- #992: expanded the minimum-area ellipse solution. The containment condition is now written as the main inequality, then transformed by `s=1+u`; the active inner tangency condition `q'(s)=0` and the resulting relation for `alpha` are shown explicitly. The final substitution was split into shorter inline formulas instead of adding another display.
- #995: moved the final order-swapped integral equality to display form because it is a long answer skeleton.

## Per-solution review

- #991: the continuity proof is correct and complete. On any `[-r,r]` with `0<r<1`, `|a_nx^n|<=a_nr^n<=a_n`; Weierstrass uniform convergence and continuity of each term give continuity on `[-r,r]`, and every point of `(-1,1)` lies in such an interval.
- #992: the optimization is correct. Setting `alpha=1/a^2`, `beta=1/b^2` turns minimizing `pi ab` into maximizing `alpha beta`. The circle boundary is parameterized by `x=1+cos t`, `y=sin t`; with `s=1+cos t`, containment becomes `alpha s^2+beta s(2-s)<=1`. The active inner minimum gives `alpha=(s-1)/s^2`, `beta=1/s`, hence `alpha beta=(s-1)/s^3`, whose maximum on `1<s<=2` occurs at `s=3/2`. The resulting `a=3/sqrt2`, `b=sqrt(3/2)` and minimum area `3sqrt3*pi/2` are correct.
- #993: the undetermined-coefficients form is correct. Since `r=1` is a simple root of the homogeneous characteristic equation and the forcing is a degree-one polynomial times `e^x`, the particular form is `xe^x(Ax+B)`.
- #994: the total differential computation is correct. With `u=x-y`, `v=y-z`, `w=z-x`, collecting `dx`, `dy`, and `dz` gives `(f_1-f_3)dx+(f_2-f_1)dy+(f_3-f_2)dz=0`, hence the displayed answer form for `dz` when `f_3!=f_2`. The final formula is not long enough to require display.
- #995: the order-switching region is correct. From `y^2<=x<=sqrt y` in the unit square, fixed `x` gives `x^2<=y<=sqrt x`; the final equality is now displayed because it is the complete answer skeleton.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1089
  - `long_inline_flagged`: 119
  - `jump_keyword_flagged`: 578
  - `short_display_flagged`: 823
- Batch index after final edit:
  - #991: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #992: `display_count=3`, `short_display_count=3`, `inline_long_count=0`
  - #993: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #994: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #995: `display_count=1`, `short_display_count=1`, `inline_long_count=0`
- Compile: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan for fatal errors, warnings, overfull/underfull boxes, missing characters, and undefined controls: no matches.
- Page count: 744.
- Rendered and inspected:
  - `tmp\pdfs\batch_087_991_995\page_final_v2-656.png`
  - `tmp\pdfs\batch_087_991_995\page_final_v2-657.png`
  - `tmp\pdfs\batch_087_991_995\page_final_v2-658.png`

## Decision

Batch #991-995 is released. The batch now has no long-inline candidates, #992 has a complete optimization chain, and #995 uses display layout only for the genuinely long final equality.
