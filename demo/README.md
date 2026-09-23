# A ten-minute coding agent demo

Use the same task to show what the model contributes, what the harness lets it do, and what the researcher must review. The dataset is synthetic and may be shown publicly.

## Before the talk

- Open the repository in one coding agent with file and terminal access.
- Confirm that Python 3 is available. The reference solution uses only its standard library; no package installation, API key or network request is needed.
- Rehearse once in a clean working folder. Keep `assets/compustat_sample.csv` unchanged and create new live work under `demo/live/`.
- Keep the prepared [chart](reference/outputs/yearly_roa.svg), [table](reference/outputs/yearly_roa.csv), [diagnostics](reference/outputs/diagnostics.json) and [methods](reference/outputs/methods.md) open as a fallback.
- The `reference/` folder is a presenter backup. For a fresh live demonstration, tell the agent to work from the data and prompt without reading it, or copy only the CSV to a clean demo workspace and adjust the input path below.

## Copyable prompt

```text
Create a small reproducible analysis of assets/compustat_sample.csv.
This is synthetic teaching data. Preserve the raw file and put all new work
under demo/live/. Work from the dataset and these instructions without
reading demo/reference/.

1. Inspect the columns, row count, unique firms, fiscal-year range,
   duplicate firm-years, and missing values. Stop and ask if identifiers
   are invalid or firm-years are duplicated.
2. Define ROA as 100 * ni / at, using year-end total assets and reporting
   percent. Keep negative income. Exclude only rows where ni or at is
   missing, not numeric, or not finite, or where at <= 0. Do not drop rows
   just because another column is missing. Do not impute or winsorize.
3. Use Python's standard library only. Write and execute a reusable script.
   Create a CSV of each year's row count, valid sample size, exclusions,
   and median firm-level ROA; an SVG line chart using those same medians;
   a diagnostics file; and a short methods note. Label the data synthetic.
4. Check row counts, unique keys, exclusion counts, and the agreement
   between chart and table. Confirm the raw data did not change.
5. Show me the outputs, commands you ran, and the files you changed.
   Explain assumptions and limitations. Do not make causal claims.

Before editing, give me a brief plan and identify any choices that need
my judgment. Then carry out the specified analysis.
```

The request to stop on duplicate keys is deliberate: the researcher should choose how to resolve them. The supplied file has no duplicates, so this does not interrupt the prepared workflow.

## Presenter run sheet

| Minute | Action | What to point out |
|---|---|---|
| 0–1 | Show the raw CSV and paste the prompt. | The user specifies the measure, sample rules and deliverables. The model interprets the task. |
| 1–3 | Read the plan and input inspection. | The harness provides actual files, tools and an execution environment. |
| 3–6 | Let the agent write and run the analysis. | Watch a tool call and its result. If an error occurs, let the agent inspect it and try a correction. |
| 6–8 | Check the chart, table and missing-value report; request one small revision if time allows. | Multiplication by 100 produces percent. Missing cash-flow and depreciation fields should not shrink the ROA sample. |
| 8–10 | Review changed files, run instructions and a manual numerical check, then return to Q&A. | A usable result includes repeatable code. The researcher still judges definitions, interpretation and the research design. |

If the agent has no usable output at minute 6, say that you are switching to a prepared example, open the fallback outputs and show the reference command. A live tool failure is useful only if it fits within the ten-minute slot.

## Review questions

- Did the agent use **year-end assets**, as requested, or silently substitute average assets?
- Does the chart show the **median of firm-level ratios**, rather than the ratio of totals?
- Are loss-making observations retained?
- Did unrelated missing `dpc` or `oancf` values cause unnecessary exclusions?
- Do each year's valid observations plus exclusions equal its source row count?
- Do the plot's labels, units, medians and sample sizes agree with the table?
- Is the source file unchanged, and can someone rerun the analysis from the script?
- Which claims would need a different research design or actual data?

## Prepared result and numerical checks

The supplied file has **725 rows**, **25 firms**, **725 unique firm-years**, and fiscal years **1995–2023**. Each year has **25 observations**. There are no duplicate keys, missing `ni`/`at`, nonnumeric `ni`/`at`, or nonpositive assets, so all 725 rows enter the ROA calculation. `dpc` is missing in 15 rows and `oancf` in 23 rows; neither field is used here.

As a simple row-level check, the first record has `ni = 1530.3` and `at = 34965.82`, so its ROA is `100 * 1530.3 / 34965.82 = 4.376560%` (rounded). This individual observation is not the yearly median. The annual medians are `4.206320%` for 1995 and `3.475039%` for 2023. All 29 yearly medians were independently recalculated using decimal arithmetic and the thirteenth sorted value of each 25-observation sample, and checked against the table and SVG points.

The diagnostics include the SHA-256 of the exact input. When using a revised dataset, recompute expectations rather than treating these totals as universal acceptance criteria.

## Fallback commands

From the repository root, run whichever Python command is installed:

```bash
python demo/reference/analyze.py
```

On systems where Python 3 is named `python3`:

```bash
python3 demo/reference/analyze.py
```

To reproduce into a separate folder:

```bash
python demo/reference/analyze.py --output demo/live-fallback/outputs
```

Open `demo/reference/outputs/yearly_roa.svg` in a browser and `yearly_roa.csv` in a text editor or spreadsheet application. The script prints the diagnostics and writes all four outputs. The default input is resolved from the script's location, so running it does not depend on the current shell directory.

The prepared implementation is one possible correct solution. The live agent may organize its code and files differently; assess its definitions, numerical results and reproducibility.
