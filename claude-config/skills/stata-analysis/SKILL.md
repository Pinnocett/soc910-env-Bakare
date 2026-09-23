---
name: stata-analysis
description: Use for any Stata analysis run — cleaning data, recoding, running models, or producing results tables. Sets up the project folder and writes all code to reproducible do-files. Triggers on "run this in Stata", "write a do file", "clean this data", "run the regression", "analyze this dataset", .dta files, and Stata commands (regress, logit, xtreg, tabulate, summarize).
---

# Stata Analysis

Every analysis run produces two things: a project folder, and do-files that
reproduce the results from raw data. Never hand back loose code in chat alone.

## 1. Project folder

At the start of each analysis, create a folder named for the project:

```
project_name/
├── do_files/
│   └── logs/
└── documentation/
```

`do_files/` holds every .do file and its .log output. `documentation/` holds a
plain description of what the analysis does and any output it produces. Ask for
the project name if it is not obvious; do not invent one.

## 2. Do-files

All code goes in a saved .do file that runs top to bottom from a clean state and
reproduces every result on its own. Number the files in run order:
`01_clean.do`, `02_analyze.do`, `03_tables.do`.

Each do-file follows this shape:

```stata
*==============================================================
* File:    01_clean.do
* Purpose: Clean the raw file and build the analysis dataset
* Input:   raw_data.dta
* Output:  analysis_data.dta, logs/01_clean.log
* Date:    2026-09-22
*==============================================================

clear all
set more off

cd "path/to/project_name/do_files"
log using "logs/01_clean.log", replace

use "raw_data.dta", clear

* Drop respondents under 18 — analysis is adults only
drop if age < 18

* Nativity: 1 = born outside the U.S., 0 = U.S.-born
gen foreign_born = 0
replace foreign_born = 1 if nativity == 2
replace foreign_born = . if nativity == .

save "analysis_data.dta", replace

log close
```

Rules that are not optional:

- **Save under a new filename.** Never `save` over the raw data. A cleaning file
  that overwrites its own input destroys the source the second time it runs.
- **Start clean.** `clear all` and `set more off` at the top, so the file never
  inherits leftover state from the console.
- **Log everything.** `log using ... , replace` at the top, `log close` at the
  bottom.
- **Nothing typed in the console.** If a command mattered to the result, it
  belongs in the do-file.

## 3. Write it plainly

Do not use `global`, `local`, or root-path macros. Spell the commands out so each
line says what it does without the reader scrolling up to substitute a value.

```stata
* Do this
cd "path/to/project_name/do_files"
use "analysis_data.dta", clear
logit uninsured foreign_born age i.sex educ income

* Not this
global root "path/to/project_name"
global covars "age i.sex educ income"
use "$root/analysis_data.dta", clear
logit uninsured foreign_born $covars
```

Other style rules:

- One command per line, in the order they run.
- A short `*` comment above any step whose purpose is not obvious.
- Prefer an explicit `foreach` over a nested macro trick.
- The one exception: a covariate list repeated across five or more models, where
  retyping invites a silent typo. Define it once, immediately above its first
  use, with a comment naming what is in it.

## 4. Document the analysis

Write a short plain-language note into `documentation/` recording what the
analysis does: the data source, the years, the unit of analysis, the sample and
what was excluded from it and on what rule, and how the key variables were
measured. This is a record of the procedure, so that a result can be traced back
to the decisions that produced it.
