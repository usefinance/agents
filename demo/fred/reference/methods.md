# FRED example: methods and limits

The public FRED CSV snapshot was downloaded on **23 September 2026** from
`https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL%2CFEDFUNDS`.
Its SHA-256 is `7333dc7ac8b1e778daf78222f3b32c8feb819307ca9e72488fb98f9df71ab890`.
FRED may revise historical observations, so a fresh download can change the
numbers. The saved snapshot makes the prepared example reproducible.

- [CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL): monthly, seasonally
  adjusted Consumer Price Index for All Urban Consumers: All Items, from the US
  Bureau of Labor Statistics. Units: index, 1982–84 = 100.
- [FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS): monthly effective
  federal funds rate, from the Federal Reserve Board of Governors. Units:
  percent; monthly average of daily rates. It is not the policy target rate.

Inflation is `100 × (CPI_t / CPI_t−12 − 1)`. The figure shows that annual CPI
inflation and the effective federal funds rate changed markedly between 2019
and 2026. It is a **descriptive comparison**. The two lines do not establish
that one series caused movements in the other.

The snapshot yields 91 months with both rates from January 2019 through August
2026. CPIAUCSL is missing for October 2025 in the downloaded CSV; the chart
keeps the gap visible and the audit names it. Inflation peaks in June 2022 at
8.98% (rounded). The last paired month, August 2026, has 3.35% CPI inflation
and a 3.63% effective federal funds rate. These outputs were checked by an
independent calculation from the raw CSV.
