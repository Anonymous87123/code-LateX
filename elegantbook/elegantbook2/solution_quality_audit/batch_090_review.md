# Batch 090 Review: solutions #1006-1010

## Scope

- Global solution numbers: #1006-1010
- Source ranges after index rebuild:
  - #1006: lines 42927-42934
  - #1007: lines 42940-42951
  - #1008: lines 42961-42976
  - #1009: lines 42982-42992
  - #1010: lines 43004-43009

## Changes made

- #1009: moved the Green formula identity into display form. This is the main method step for the line-integral problem and removes a long compressed inline formula; the short derivative, area, and sign-change conclusions remain inline.

## Per-solution review

- #1006: the nonhomogeneous linear ODE argument is correct. Differences of any two particular solutions solve the corresponding homogeneous equation; `x^2` and `e^x` are independent, and `y=3` is a particular solution, so the general solution is `3+C_1x^2+C_2e^x`.
- #1007: the implicit differential computation is correct. With `u=x-y`, `v=y-z`, `w=z-x`, collecting terms gives `(F_1-F_3)dx+(F_2-F_1)dy+(F_3-F_2)dz=0`, hence the stated `dz`.
- #1008: the gradient and directional derivative are correct. At `P(2,0,1)`, `grad f=(4/5,0,2/5)`, so the derivative along the gradient direction equals `|grad f|=2sqrt5/5`. The gradient display is appropriate.
- #1009: Green formula and orientation are correct. Counterclockwise gives `2*pi ab`; the stated clockwise orientation reverses sign, so the answer is `-2*pi ab`.
- #1010: the Fourier sine-series interpretation is correct. The sine series is the odd 2-periodic extension of `sin(pi x^2)`; `-1/2` is a continuity point, so `S(-1/2)=-sin(pi/4)=-sqrt2/2`.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1089
  - `long_inline_flagged`: 116
  - `jump_keyword_flagged`: 578
  - `short_display_flagged`: 824
- Batch index:
  - #1006: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #1007: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #1008: `display_count=1`, `short_display_count=1`, `inline_long_count=0`
  - #1009: `display_count=1`, `short_display_count=1`, `inline_long_count=0`
  - #1010: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
- Compile: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan for fatal errors, warnings, overfull/underfull boxes, missing characters, and undefined controls: no matches.
- Page count: 744.
- Rendered and inspected:
  - `tmp\pdfs\batch_090_1006_1010\page_final-660.png`
  - `tmp\pdfs\batch_090_1006_1010\page_final-661.png`
  - `tmp\pdfs\batch_090_1006_1010\page_final-662.png`

## Decision

Batch #1006-1010 is released. All five solutions are mathematically correct and complete; #1009's previously dense Green formula line has been fixed.
