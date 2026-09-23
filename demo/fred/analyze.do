* Real FRED data example for the coding agents presentation.
* Run from the repository root: do demo/fred/analyze.do
* Optional arguments: do demo/fred/analyze.do input.csv output_directory
version 18.0
clear all
set more off

args input_path output_dir
if `"`input_path'"' == "" local input_path "demo/fred/fred_snapshot.csv"
if `"`output_dir'"' == "" local output_dir "demo/fred/reference"
capture mkdir "`output_dir'"

import delimited using "`input_path'", varnames(1) case(lower) asdouble clear
confirm variable observation_date
confirm variable cpiaucsl
confirm variable fedfunds

capture confirm string variable cpiaucsl
if !_rc destring cpiaucsl, replace force
capture confirm string variable fedfunds
if !_rc destring fedfunds, replace force

generate int month = mofd(date(observation_date, "YMD"))
format month %tm
assert !missing(month)
sort month
isid month
assert cpiaucsl > 0 if !missing(cpiaucsl)
tsset month, monthly

generate double inflation_yoy = 100 * (cpiaucsl / L12.cpiaucsl - 1)
label variable inflation_yoy "CPI inflation, 12-month change (%)"
label variable fedfunds "Effective federal funds rate (%)"

keep if month >= ym(2019,1)
count if missing(inflation_yoy) | missing(fedfunds)
local excluded = r(N)
quietly levelsof observation_date if missing(inflation_yoy) | missing(fedfunds), local(excluded_dates) clean
count if !missing(inflation_yoy, fedfunds)
local included = r(N)
assert `included' >= 12

local first_date = observation_date[1]
quietly summarize month if !missing(inflation_yoy, fedfunds), meanonly
local latest_month = r(max)
quietly levelsof observation_date if month == `latest_month', local(last_date) clean
quietly summarize inflation_yoy if month == `latest_month', meanonly
local latest_inflation = string(r(mean), "%6.2f")
quietly summarize fedfunds if month == `latest_month', meanonly
local latest_rate = string(r(mean), "%6.2f")

twoway (line inflation_yoy month, lcolor(navy) lwidth(medthick) cmissing(n)) ///
       (line fedfunds month, lcolor(maroon) lwidth(medthick)), ///
       title("US inflation and the federal funds rate") ///
       subtitle("Monthly data since 2019") ///
       ytitle("Percent") xtitle("") ///
       xlabel(, format(%tmCY)) ///
       legend(order(1 "CPI inflation, 12-month" 2 "Effective federal funds rate") rows(1) position(6)) ///
       graphregion(color(white)) plotregion(color(white)) ///
       note("Source: FRED (CPIAUCSL, FEDFUNDS). Descriptive comparison; no causal claim.", size(vsmall))
graph export "`output_dir'/inflation_fedfunds.png", width(1800) replace

export delimited observation_date cpiaucsl inflation_yoy fedfunds using ///
    "`output_dir'/monthly_analysis.csv", replace

file open audit using "`output_dir'/audit.txt", write replace
file write audit "Source: FRED CPIAUCSL and FEDFUNDS" _n
file write audit "Input: `input_path'" _n
file write audit "Inflation: 100 * (CPI_t / CPI_t-12 - 1)" _n
file write audit "Sample: `first_date' to `last_date'" _n
file write audit "Paired months: `included'" _n
file write audit "Months with missing series: `excluded'" _n
file write audit "Missing month(s): `excluded_dates'" _n
file write audit "Latest inflation (%): `latest_inflation'" _n
file write audit "Latest federal funds rate (%): `latest_rate'" _n
file write audit "Interpretation: descriptive only; this chart does not identify a causal effect." _n
file close audit

display "FRED_DEMO_COMPLETE: `included' paired months, `first_date' to `last_date'"
