# Methods

This is synthetic teaching data, not evidence about actual firms. Each row is one firm and fiscal year, identified by `gvkey` and `fyear`. Missing or invalid identifiers and duplicate firm-years stop the analysis for review.

Return on assets (ROA) is defined here as `100 * ni / at`: net income divided by **year-end** total assets, expressed in **percent**. This is a chosen definition; using average assets would be a different measure and would require a new specification. The numerator and denominator are assumed to use the same currency units.

Rows with missing, nonnumeric or nonfinite `ni` or `at`, or `at <= 0`, are excluded. Negative net income is retained. Missing values in other fields do not remove a row. There is no imputation, winsorization, weighting or regression. The chart shows the unweighted median of valid firm-level ROA values within each fiscal year, not the ratio of summed net income to summed assets.

Input: 725 rows, 25 firms, 1995–2023. Valid ROA: 725 rows; excluded: 0. Annual sample sizes and medians appear in `yearly_roa.csv`; full missing-value counts and the source SHA-256 fingerprint appear in `diagnostics.json`. CSV medians are rounded to six decimal places; the SVG uses the same unrounded medians.

The series is descriptive. It supports no causal claim and does not establish representativeness of a population. Raw data are never modified.
