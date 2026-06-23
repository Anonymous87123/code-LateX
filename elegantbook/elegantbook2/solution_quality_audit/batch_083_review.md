# Batch 083 Review (#971--975)

## Scope

- Reviewed solutions #971--975 in `elegantbook2.tex`.
- Corresponding rendered pages inspected: PDF pages 650--653, logical pages 600--603.

## Changes Made

- #975: Expanded the exact-differential solution. The path-independence condition is now shown through \(P_y=Q_x\), the resulting ODE
  \((x\varphi(x))'=\sin x\), the determination of \(C=\pi-1\), and the potential-function check.
- #975: After a first expansion, compressed short endpoint and final-answer formulas back inline. The solution now keeps only the two core display blocks: the differential-equation derivation and the potential-function verification.

## Mathematical Review

- #971: On \(\Sigma:x^2+y^2+z^2=a^2\), the integrand is \(a^2\), so the integral is \(a^2\cdot4\pi a^2=4\pi a^4\). Correct.
- #972: Since the power series centered at \(x=1\) converges at \(x=-1\), it converges absolutely at every point closer to the center, including \(x=2\). The conclusion is absolute convergence. Correct.
- #973: The transformation \((\xi,\eta)=(x^2-y^2,2xy)\) is handled by the chain rule; the first-order and mixed terms cancel, giving \(z_{xx}+z_{yy}=4(x^2+y^2)(f_{\xi\xi}+f_{\eta\eta})=0\). Correct.
- #974: Spherical coordinates in the first octant give \(1\le r\le2,\ 0\le\varphi,\theta\le\pi/2\). The angular factors and radial substitution \(u=r^2\) lead to \(I=\frac{\pi}{8}\left(\frac2e-\frac5{e^4}\right)\). Correct.
- #975: The path-independence condition gives \(x\varphi'(x)+\varphi(x)=\sin x\), hence \(\varphi(x)=(\pi-1-\cos x)/x\). With \(\Phi=y\varphi(x)\), the integral from \((1,0)\) to \((\pi,\pi)\) is \(\pi\). Correct.

## Formula Layout Check

- #971--975 all have `inline_long_count=0` after rebuilding the index.
- #974's two short-display candidates are retained because they are the triple-integral setup and radial integral skeleton.
- #975 has one short-display candidate remaining, but it is the core conversion from \(P_y=Q_x\) to the ODE for \(\varphi\); short endpoint values and final answer remain inline.

## Verification

- Rebuilt index with `python solution_quality_audit\build_solution_index.py`.
- Ran `latexmk -xelatex -interaction=nonstopmode -halt-on-error elegantbook2.tex`; compile completed successfully.
- Scanned `elegantbook2.log` for errors, overfull/underfull boxes, LaTeX/package warnings, missing characters, and undefined control sequences; no matches.
- Confirmed PDF page count remains 743.
- Rendered and visually inspected:
  - `tmp\pdfs\batch_083_971_975\page_final-650.png`
  - `tmp\pdfs\batch_083_971_975\page_final-651.png`
  - `tmp\pdfs\batch_083_971_975\page_final-652.png`
  - `tmp\pdfs\batch_083_971_975\page_final-653.png`

## Batch Result

#971--975 are closed for this pass: calculations and conclusions are correct, #975 no longer skips the exactness-to-potential-function reasoning, and formula layout follows the current inline/display standard.
