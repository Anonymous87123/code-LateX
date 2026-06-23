# Batch 101 Review: solutions #1061-1065

## Scope

- Global solution numbers: #1061-1065
- Source ranges after index rebuild:
  - #1061: lines 44208-44216
  - #1062: lines 44229-44237
  - #1063: lines 44246-44253
  - #1064: lines 44262-44286
  - #1065: lines 44295-44302

## Changes made

- No TeX edits were needed in this batch. Each flagged item was manually reviewed for mathematical correctness, derivation completeness, method consistency, and formula layout.

## Per-solution review

- #1061: correct and complete. The Fourier sine coefficient is formed as \(b_n=\frac1\pi\int_{-\pi}^{\pi}(\pi x+x^2)\sin nx\,dx\). The parity split is valid: \(x^2\sin nx\) is odd and contributes zero, while \(\pi x\sin nx\) is even. Integration by parts gives \(\int_0^\pi x\sin nx\,dx=-\pi(-1)^n/n\), hence \(b_n=-2\pi(-1)^n/n\) and \(b_2=-\pi\). The integration-by-parts chain is a core computation and remains inline because the rendered width is still readable under the current 3/4-line threshold.
- #1062: correct and complete. Existence of the two partial derivatives means the corresponding one-variable difference quotients exist along the coordinate axes. Multiplying the first quotient by \(x-a\) proves \(f(x,b)\to f(a,b)\), and the same argument applies to \(f(a,y)\). The solution also explicitly rejects continuity, differentiability, and the full two-variable limit, so the reasoning matches the standard partial-derivative implication.
- #1063: correct and complete. Writing the surface as \(F=x^2+y^2+z-4=0\) gives normal vector \((2x,2y,1)\). Parallelism to the plane normal \((2,2,1)\), together with the fixed third component, gives \(x=1,\ y=1\), and substitution into the surface gives \(z=2\).
- #1064: correct and complete. Cylindrical coordinates correctly describe the body as \(0\le r\le1,\ r^2\le z\le1\). Symmetry gives \(\bar x=\bar y=0\). The volume is \(\pi/2\), the moment \(M_{xy}\) is \(\pi/3\), and \(\bar z=M_{xy}/V=2/3\). The three displays are retained because they are the volume/moment computation skeleton, not low-status short formulas.
- #1065: correct and complete. Dividing the differential form by \(dx\) gives \(y-\ln x+xy'=0\), hence \(y'+y/x=(\ln x)/x\). On \(x>0\), this is a first-order nonhomogeneous linear equation. The solution also explains why the equation is not nonlinear and ties the classification to the standard form \(y'+P(x)y=Q(x)\).

## Verification

- Batch index:
  - #1061: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #1062: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #1063: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
  - #1064: `display_count=3`, `short_display_count=3`, `inline_long_count=0`
  - #1065: `display_count=0`, `short_display_count=0`, `inline_long_count=0`
- Rendered and inspected:
  - `tmp\pdfs\batch_101_1061_1065_page_final-676.png`
  - `tmp\pdfs\batch_101_1061_1065_page_final-677.png`
- No compile was required because no TeX edits were made after the previous successful build.

## Decision

Batch #1061-1065 is released. The automatic jump-keyword flags in #1061 and #1062 were manually rejected after checking the actual derivations; the #1064 short-display flag was manually accepted because the displays carry the central volume and moment computations.
