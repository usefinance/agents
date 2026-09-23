# Ten-minute live demo: FRED data in Stata

**Question:** How have US CPI inflation and the effective federal funds rate
moved since 2019? This is a descriptive exercise with real public data, not a
test of whether monetary policy caused inflation to change.

The demo uses [CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL) and
[FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS). The former is a monthly
price index; the latter is a monthly interest rate already measured in percent.
The presenter specifies the inflation calculation, while the agent fetches,
inspects, analyzes and checks the series using Stata.

## Before the talk

1. Open this repository from its root folder in a coding agent with file and
   terminal access. Confirm that Stata runs and can create a chart. This
   workstation has Stata/SE 18.
2. Run `demo/fred/fetch.ps1` or use its documented FRED URL to download a fresh
   CSV to `demo/fred/live/fred_latest.csv`. Rehearse the Stata analysis. If the
   network is unavailable, use [the saved FRED snapshot](fred/fred_snapshot.csv).
3. Keep the [prepared chart](fred/reference/inflation_fedfunds.png),
   [analysis CSV](fred/reference/monthly_analysis.csv),
   [audit](fred/reference/audit.txt) and [methods note](fred/reference/methods.md)
   available as a clearly labelled fallback. The live agent should work from
   the prompt and raw CSV without reading the prepared implementation.

Stata's `import fred` command uses FRED's API and requires a personal API key.
No key is configured on this workstation. The main demo therefore downloads
FRED's public CSV over HTTPS and imports it into Stata; it does not use the
keyed API. If you already have a FRED key, Stata's
[official guide](https://www.stata.com/links/stata-basics/import-data-fred/)
shows how to use `import fred`. Keep the key out of scripts and slides.

## Run sheet

| Minute | Show | Ask the audience to notice |
|---|---|---|
| 0–1 | The question and [prompt](prompt.txt). | The person sets the definition and boundaries. |
| 1–3 | Fetch the FRED CSV; inspect series names, dates and missing values. | The agent uses tools and sees the actual data. |
| 3–6 | Write and run a Stata do-file; make a two-line chart. | The agent acts, sees results and can correct errors. |
| 6–8 | Check one inflation value and the missing October 2025 CPI observation. | A real dataset needs a visible audit. |
| 8–10 | Review the do-file, chart, source links and limits. | A useful output is reproducible; the chart alone proves no causal effect. |

If the live run has no usable result at minute 6, say you are switching to a
prepared example. Open the saved chart and audit, then show the reference
do-file. Do not describe those outputs as if the agent produced them live.

## Reproducing the prepared example

From the repository root, run this command in Stata's command window:

```stata
do demo/fred/analyze.do
```

It uses the saved snapshot and writes the PNG, CSV and audit to
`demo/fred/reference/`. To use a freshly downloaded CSV and keep its output
separate:

```stata
do demo/fred/analyze.do demo/fred/live/fred_latest.csv demo/fred/live
```

The public download can be refreshed on Windows from the repository root with
`powershell.exe -NoProfile -File .\demo\fred\fetch.ps1`. The download script
checks the response header before using the CSV. No FRED API key is required.

The saved 23 September 2026 snapshot has 91 paired months from January 2019
through August 2026. CPI is missing for October 2025. Annual CPI inflation
peaks in June 2022 at about 8.98%; in August 2026 it is about 3.35%, beside
an effective federal funds rate of 3.63%. These are snapshot-specific checks,
not expected values for every future download. See the
[methods note](fred/reference/methods.md) for series definitions and limits.

The earlier synthetic-firm example remains in `assets/compustat_sample.csv`
and `demo/reference/` for anyone who needs a fully offline dataset.
