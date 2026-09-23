#!/usr/bin/env python3
"""Reproduce the workshop demo with Python's standard library only."""

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[2]


def number(value):
    """Missing, malformed and nonfinite values are not valid numbers."""
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (ValueError, TypeError):
        return None


def chart(summaries, output):
    width, height = 960, 540
    left, right, top, bottom = 92, 38, 112, 96
    plot_w, plot_h = width - left - right, height - top - bottom
    values = [r["median_roa_pct"] for r in summaries if r["median_roa_pct"] is not None]
    if not values:
        raise ValueError("No valid ROA observations to plot.")
    low, high = min(0, math.floor(min(values))), max(0, math.ceil(max(values)))
    if low == high:
        high += 1
    years = [r["fyear"] for r in summaries]

    def x(year):
        return left + (year - years[0]) * plot_w / max(1, years[-1] - years[0])

    def y(value):
        return top + (high - value) * plot_h / (high - low)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title description">',
        '<title id="title">Median return on assets by fiscal year</title>',
        '<desc id="description">Synthetic teaching data. ROA equals net income divided by end-of-year total assets, multiplied by 100. Each dot is a yearly median; the CSV provides exact values and sample sizes.</desc>',
        '<rect width="960" height="540" fill="#faf9f6"/>',
        '<g font-family="Arial, sans-serif" fill="#183a3c">',
        '<text x="92" y="43" font-size="25" font-weight="700">Median return on assets</text>',
        '<text x="92" y="73" font-size="16">Synthetic teaching data · net income / year-end assets × 100</text>',
        '<text x="92" y="100" font-size="13">ROA (%)</text>',
    ]
    for i in range(6):
        value = low + i * (high - low) / 5
        yy = y(value)
        svg.extend([
            f'<line x1="{left}" y1="{yy:.2f}" x2="{width-right}" y2="{yy:.2f}" stroke="#dbe3de"/>',
            f'<text x="{left-14}" y="{yy+5:.2f}" text-anchor="end" font-size="14">{value:.1f}</text>',
        ])
    for year in years:
        if year == years[0] or year == years[-1] or year % 5 == 0:
            svg.append(f'<text x="{x(year):.2f}" y="{height-bottom+28}" text-anchor="middle" font-size="14">{year}</text>')
    # Circles show available medians; separate polylines avoid bridging missing years.
    segment = []
    for row in summaries + [{"median_roa_pct": None}]:
        if row["median_roa_pct"] is None:
            if segment:
                points = " ".join(segment)
                svg.append(f'<polyline points="{points}" fill="none" stroke="#24776f" stroke-width="3"/>')
                segment = []
        else:
            segment.append(f'{x(row["fyear"]):.2f},{y(row["median_roa_pct"]):.2f}')
    for row in summaries:
        if row["median_roa_pct"] is not None:
            xx, yy = x(row["fyear"]), y(row["median_roa_pct"])
            svg.append(f'<circle cx="{xx:.2f}" cy="{yy:.2f}" r="3.5" fill="#24776f"><title>{row["fyear"]}: {row["median_roa_pct"]:.3f}%; n={row["valid_roa_rows"]}</title></circle>')
    svg.extend([
        '<text x="507" y="500" text-anchor="middle" font-size="14">Fiscal year</text>',
        '<text x="92" y="527" font-size="12">Source: assets/compustat_sample.csv · descriptive example; no causal interpretation</text>',
        '</g></svg>',
    ])
    output.write_text("\n".join(svg) + "\n", encoding="utf-8")


def run(source, output):
    raw = source.read_bytes()
    with source.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        required = {"gvkey", "fyear", "ni", "at"}
        if not required.issubset(columns):
            raise ValueError(f"Missing required columns: {sorted(required - set(columns))}")
        rows = list(reader)
    if not rows:
        raise ValueError("The input dataset has no observations.")
    keys = []
    for row in rows:
        if not (row.get("gvkey") or "").strip():
            raise ValueError("A firm identifier is missing; inspect before proceeding.")
        try:
            year = int(row["fyear"])
        except (ValueError, TypeError):
            raise ValueError("A fiscal year is missing or invalid; inspect before proceeding.") from None
        keys.append((row["gvkey"].strip(), year))
    duplicates = sum(count - 1 for count in Counter(keys).values())
    if duplicates:
        raise ValueError(f"Found {duplicates} duplicate firm-year rows; resolve explicitly before calculating medians.")

    counts = Counter(year for _, year in keys)
    by_year = defaultdict(list)
    exclusions = Counter({"missing_or_invalid_ni": 0, "missing_or_invalid_at": 0, "nonpositive_at": 0})
    excluded_rows = 0
    for row, (_, year) in zip(rows, keys):
        income, assets = number(row["ni"]), number(row["at"])
        reasons = []
        if income is None:
            reasons.append("missing_or_invalid_ni")
        if assets is None:
            reasons.append("missing_or_invalid_at")
        elif assets <= 0:
            reasons.append("nonpositive_at")
        if reasons:
            exclusions.update(reasons)
            excluded_rows += 1
        else:
            # Same units for ni and at; keep losses and apply no winsorization.
            by_year[year].append(100 * income / assets)

    summaries = [
        {"fyear": year, "source_rows": counts[year], "valid_roa_rows": len(by_year[year]),
         "excluded_rows": counts[year] - len(by_year[year]),
         "median_roa_pct": median(by_year[year]) if by_year[year] else None}
        for year in sorted(counts)
    ]
    diagnostics = {
        "source": source.name,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "source_rows": len(rows),
        "unique_firms": len({firm for firm, _ in keys}),
        "unique_firm_years": len(set(keys)),
        "duplicate_firm_year_rows": duplicates,
        "first_fiscal_year": min(counts),
        "last_fiscal_year": max(counts),
        "missing_by_column": {column: sum(not (r.get(column) or "").strip() for r in rows) for column in columns},
        "exclusion_reasons_may_overlap": dict(exclusions),
        "excluded_rows": excluded_rows,
        "valid_roa_rows": sum(len(values) for values in by_year.values()),
    }
    output.mkdir(parents=True, exist_ok=True)
    with (output / "yearly_roa.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summaries[0]))
        writer.writeheader()
        for row in summaries:
            writer.writerow({**row, "median_roa_pct": "" if row["median_roa_pct"] is None else f'{row["median_roa_pct"]:.6f}'})
    (output / "diagnostics.json").write_text(json.dumps(diagnostics, indent=2) + "\n", encoding="utf-8")
    chart(summaries, output / "yearly_roa.svg")
    (output / "methods.md").write_text(
        "# Methods\n\n"
        "This is synthetic teaching data, not evidence about actual firms. "
        "Each row is one firm and fiscal year, identified by `gvkey` and `fyear`. "
        "Missing or invalid identifiers and duplicate firm-years stop the analysis for review.\n\n"
        "Return on assets (ROA) is defined here as `100 * ni / at`: net income divided by "
        "**year-end** total assets, expressed in **percent**. This is a chosen definition; "
        "using average assets would be a different measure and would require a new specification. "
        "The numerator and denominator are assumed to use the same currency units.\n\n"
        "Rows with missing, nonnumeric or nonfinite `ni` or `at`, or `at <= 0`, are excluded. "
        "Negative net income is retained. Missing values in other fields do not remove a row. "
        "There is no imputation, winsorization, weighting or regression. "
        "The chart shows the unweighted median of valid firm-level ROA values within each fiscal year, "
        "not the ratio of summed net income to summed assets.\n\n"
        f"Input: {len(rows)} rows, {diagnostics['unique_firms']} firms, "
        f"{diagnostics['first_fiscal_year']}–{diagnostics['last_fiscal_year']}. "
        f"Valid ROA: {diagnostics['valid_roa_rows']} rows; excluded: {excluded_rows}. "
        "Annual sample sizes and medians appear in `yearly_roa.csv`; full missing-value counts "
        "and the source SHA-256 fingerprint appear in `diagnostics.json`. CSV medians are "
        "rounded to six decimal places; the SVG uses the same unrounded medians.\n\n"
        "The series is descriptive. It supports no causal claim and does not establish "
        "representativeness of a population. Raw data are never modified.\n",
        encoding="utf-8",
    )
    if source.read_bytes() != raw:
        raise RuntimeError("The source dataset changed during execution.")
    print(json.dumps(diagnostics, indent=2))
    print(f"Wrote yearly_roa.csv, yearly_roa.svg, diagnostics.json and methods.md to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "assets" / "compustat_sample.csv")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "outputs")
    args = parser.parse_args()
    run(args.input.resolve(), args.output.resolve())
