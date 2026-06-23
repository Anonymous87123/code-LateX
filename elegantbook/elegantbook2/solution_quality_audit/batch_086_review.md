# Batch 086 Review: solutions #986-990

## Scope

- Global solution numbers: #986-990
- Source ranges after index rebuild:
  - #986: lines 42471-42484
  - #987: lines 42498-42508
  - #988: lines 42514-42537
  - #989: lines 42545-42562
  - #990: lines 42569-42579

## Changes made

- No TeX edits in this batch.

## Per-solution review

- #986: cylindrical-coordinate setup is correct. The solid cone is described by `0<=z<=1`, `0<=r<=z`, `0<=theta<=2pi`; the integrand becomes `r^2` and the Jacobian contributes another `r`, giving `I=pi/10`. The displayed triple integral is the central computation skeleton and is appropriate.
- #987: line-integral decomposition is correct. The first two terms are `d sin(x+y^2)`, and the remaining term is an exact differential in `y`; since both endpoints have `y=0`, the second contribution is zero. Result `I=sin(2pi a)` is correct.
- #988: second-kind surface integral setup is correct. For the lower side of `z=x^2+y^2`, the oriented area vector is `(z_x,z_y,-1)dxdy=(2x,2y,-1)dxdy`. Substitution gives `2x^2y+4y^2-r^4+3r^2`, the odd term integrates to zero on the disk, and the final value is `13pi/6`.
  - Layout decision: one inline formula is script-flagged as long, but the rendered width is below the 3/4-line threshold and the page is readable. It is retained inline rather than mechanically moved to display.
- #989: the sum-function derivation from the sine series is correct. Subtracting `sin x` from `x cos x` produces the coefficient `2n`, so `S(x)=(x cos x-sin x)/2`. The displays are derivation skeletons, not minor substitutions.
- #990: the integral equation is handled correctly. Differentiating gives `f''+f=6sin^2 x=3-3cos 2x`; the homogeneous part and two simple particular solutions give `f=C_1 cos x+C_2 sin x+3+cos 2x`. From `f(0)=0` and the original equation at `x=0`, `f'(0)=1`, so `C_1=-4`, `C_2=1`, and `f(x)=-4cos x+sin x+3+cos 2x`. No layout change needed.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1088
  - `long_inline_flagged`: 120
  - `jump_keyword_flagged`: 579
  - `short_display_flagged`: 821
- Batch index:
  - #986: `display_count=1`, `short_display_count=1`, `inline_long_count=0`
  - #987: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #988: `display_count=1`, `short_display_count=0`, `inline_long_count=1`
  - #989: `display_count=2`, `short_display_count=2`, `inline_long_count=0`
  - #990: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
- Compile check: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` reported the PDF is up-to-date.
- Log scan for fatal errors, warnings, overfull/underfull boxes, missing characters, and undefined controls: no matches.
- Page count: 743.
- Rendered and inspected:
  - `tmp\pdfs\batch_086_986_990\page_final-655.png`
  - `tmp\pdfs\batch_086_986_990\page_final-656.png`

## Decision

Batch #986-990 is released. All five solutions are mathematically correct, sufficiently complete, consistent with the relevant methods, and do not require source edits under the current layout standard.
