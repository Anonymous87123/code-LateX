# Batch 091 Review: solutions #1011-1015

## Scope

- Global solution numbers: #1011-1015
- Source ranges after index rebuild:
  - #1011: lines 43019-43039
  - #1012: lines 43046-43060
  - #1013: lines 43070-43082
  - #1014: lines 43089-43098
  - #1015: lines 43109-43127

## Changes made

- #1011: expanded the second-order chain-rule step. The solution now shows \(z_{xx}\) and \(z_{yy}\) separately, then cancels the \(f_\xi\) and \(f_{\xi\eta}\) terms before using \(f_{\xi\xi}+f_{\eta\eta}=0\).
- #1012: corrected the arc-length and radial-factor notation to use \(|a|\). This keeps the answer \(2a^2\) valid even if the circle parameter \(a\) is not assumed positive.
- #1013: moved the long curve-integral expression in the exercise statement to display form. The solution formulas remain inline because they are short endpoint and parameter-substitution statements.
- #1014: split the compressed symmetry argument into short inline sentences. The formulas are not promoted to display because they are short consequences of the shifted sphere \(X=x-a\).
- #1015: moved the long second-kind surface-integral expression in the exercise statement to display form, and replaced the compressed phrase "angular area is \(2\pi\)" with the actual spherical-coordinate angular integral.

## Per-solution review

- #1011: correct and complete. With \(\xi=x^2-y^2,\eta=2xy\), the mixed derivative terms in \(z_{xx}+z_{yy}\) cancel, giving \(4(x^2+y^2)(f_{\xi\xi}+f_{\eta\eta})=0\).
- #1012: correct and complete. The circle \(x^2+y^2=ax\) is parametrized by \(x=a(1+\cos t)/2,\ y=a\sin t/2\); \(\mathrm ds=|a|\,\mathrm dt/2\) and \(\sqrt{x^2+y^2}=|a||\cos(t/2)|\), so \(I=2a^2\).
- #1013: correct and complete. The form decomposes as \(\mathrm d(x/y)+f(x)\mathrm d(xy)\); along \(y=(8-2x)/3,\ x:3\to1\), the endpoint term is \(-4\) and the remaining integral is \(\frac13\int_3^1(8-4x)f(x)\,\mathrm dx\).
- #1014: correct and complete. On the shifted sphere \(X=x-a\), symmetry gives \(\iint_\Sigma X\,\mathrm dS=0\), hence \(\iint_\Sigma x\,\mathrm dS=a\cdot4\pi a^2\) and \(I=8\pi a^4\).
- #1015: correct and complete. Closing the upper hemisphere with the disk gives no bottom flux; Gauss formula reduces the flux to \(3\iiint_\Omega r^2\,\mathrm dV\), whose upper-half-ball value is \(6\pi a^5/5\). The final displayed computation is retained despite the heuristic short-display flag because it is the core multi-step volume integral, not a low-status variable definition or tiny substitution.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1088
  - `long_inline_flagged`: 116
  - `jump_keyword_flagged`: 577
  - `short_display_flagged`: 824
- Batch index:
  - #1011: `display_count=1`, `short_display_count=0`, `inline_long_count=0`
  - #1012: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #1013: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #1014: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #1015: `display_count=1`, `short_display_count=1`, `inline_long_count=0`
- Compile: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan for fatal errors, LaTeX errors, undefined controls, missing characters, overfull/underfull boxes, and real warnings: no matches. The only text match was the package name `infwarerr`.
- Rendered and inspected:
  - `tmp\pdfs\batch_091_1011_1015\page_final-662.png`
  - `tmp\pdfs\batch_091_1011_1015\page_final-663.png`
  - `tmp\pdfs\batch_091_1011_1015\page_final-664.png`

## Decision

Batch #1011-1015 is released. All five solutions are mathematically correct, complete enough for the local methods being used, and aligned with the tightened layout rule: only the genuinely long core formulas were moved to display form, while short computations stayed inline.
