# Batch 121 Review: solutions #1166-1170

## Scope

- Global solution numbers: #1166-1170
- Source ranges after index rebuild:
  - #1166: lines 46586-46597
  - #1167: lines 46608-46640
  - #1168: lines 46657-46676
  - #1169: lines 46682-46698
  - #1170: lines 46707-46716

## Changes made

- #1166: reviewed and retained the displayed spherical-coordinate integral as the central computation skeleton. No edit was needed.
- #1167: corrected the punctured-region boundary-normal explanation. The inner boundary normal for the punctured region is \(-\nu_\varepsilon\), giving inner-boundary flux \(4\pi\) and hence \(I+4\pi=0\). Also changed one short display-style inline formula back to normal inline math.
- #1168: changed several low-status display-style inline fractions to normal inline math. These estimates and line-test computations are below the 3/4-line threshold and do not deserve separate displays.
- #1169: moved the Maclaurin expansion chain into display math. This is a long answer-forming series chain and was visually cramped as inline math.
- #1170: changed the short differential identities from display-style inline math to normal inline math. The proof remains a compact exact-differential argument.

## Per-solution review

- #1166: correct. On the sphere \(x^2+y^2+z^2=4\), \(z=2\cos\varphi\) and the cap cut by \(z=\sqrt2\) corresponds to \(0\le\varphi\le\pi/4\). With \(\mathrm{d}S=4\sin\varphi\,\mathrm{d}\varphi\,\mathrm{d}\theta\), the integral equals \(4\pi\).
- #1167: correct after the orientation clarification. The field \(\mathbf F=(P-M)/|P-M|^3\) has \(\operatorname{div}\mathbf F=0\) away from \(P\). If \(P\) is outside the enclosed region, Gauss gives \(I=0\). If \(P\) is inside, the punctured region has inner flux \(4\pi\), so the original outer flux is \(I=-4\pi\).
- #1168: correct. For \(\alpha>3/2\), the estimate \(|f(x,y)|\le Cr^{2\alpha-2}\) gives \(|f(x,y)-f(0,0)|/r\to0\), and the coordinate-axis partial derivatives are zero. Along \(y=x>0\), the quotient is proportional to \(x^{2\alpha-3}\), so differentiability fails for \(\alpha\le3/2\). Thus the condition is \(\alpha>3/2\).
- #1169: correct. Factoring \(1-3x+2x^2=(1-x)(1-2x)\) and applying \(\ln(1-t)=-\sum t^n/n\) gives \(-\sum_{n=1}^{\infty}(1+2^n)x^n/n\), valid where both \(|x|<1\) and \(|2x|<1\), i.e. \(|x|<1/2\).
- #1170: correct. Since \(f\) is continuous, an antiderivative \(F\) exists, and \(f(x^2-y^2)(x\,\mathrm{d}x-y\,\mathrm{d}y)=\frac12\,\mathrm{d}F(x^2-y^2)\). The integral of an exact differential around a closed curve is zero.

## Verification

- Rebuilt index: `python solution_quality_audit\build_solution_index.py`
  - `total_solutions`: 1322
  - `auto_flagged`: 1095
  - `long_inline_flagged`: 109
  - `short_display_flagged`: 846, with #1166, #1167, and #1169 manually reviewed as necessary computation or answer-skeleton displays.
- Compiled: `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex` completed successfully.
- Log scan: no `Overfull`, `Underfull`, LaTeX warning, package warning, undefined-control-sequence, or missing-character hits.
- Rendered and inspected:
  - `tmp\pdfs\batch_121_1166_1170_final_v1-705.png`
  - `tmp\pdfs\batch_121_1166_1170_final_v1-706.png`
  - `tmp\pdfs\batch_121_1166_1170_final_v1-707.png`

## Decision

Batch #1166-#1170 is released after content, calculation, method-consistency, and formula-layout review. The only new display is the long Maclaurin expansion chain in #1169; short estimates and exact-differential identities remain inline.
