# Independent Review

- Qualification use: `FAILURE_FIXTURE_ONLY`
- Original validator result: `PASS/0`
- Review finding: "必须牢记" was rotated to the empty coaching shell "遇到这类题，必须注意", and the original empty ending became "由此可以得出结论". TeX and formulas were preserved, but the requested removal of coaching and formulaic closure was incomplete.
- Rule basis: `NOTE-HUM-16` preserves the concrete correction "不要直接套公式" while removing motivational wording; `LEX-CONCLUDE-01` already owns compulsory conclusion shells.
- Regression action: add a narrow COURSE coaching pattern and the observed conclusion-shell variants; require this exact before/after pair to return `REVIEW/2`.
- Post-fix status: covered by lexical scanner and unified-validator regression tests. This artifact does not qualify the generator.
