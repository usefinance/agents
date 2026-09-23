# LLMs Beyond Chat: Coding Agents

A presentation for researchers and lecturers at Utrecht School of Economics:
**40 minutes of presentation, 10 minutes of live demonstration, and 10 minutes of Q&A.**

**Live slides:** https://usefinance.github.io/agents/

The opening slide has a QR code linking to the live deck, with matching frames
for the QR at the top left and the Finance Utrecht logo at the top right.

## What the talk covers

- How an agent extends a familiar chat workflow with tools and feedback.
- The model, harness and working loop, explained with one task.
- Research and teaching examples with outputs people can inspect.
- Two kinds of failure: convincing wrong results, and consequential actions
  through terminal or file access.
- Student thesis use and misuse, with Utrecht University's assignment-specific
  AI Index as the policy frame.

The core sequence has 13 visual slides. Slide 14 is the live demo and slide 15 is Q&A.
Five reference slides follow, with sources, current setup links, prompt templates,
demo resources and additional use cases. Product documentation was reviewed on
23 September 2026; model rankings, fixed prices and performance promises are
intentionally omitted from the teaching material.

## Presenting and viewing locally

Run a local web server from the repository root:

    python -m http.server 8000

Use python3 if that is the Python command on your system, then open
http://localhost:8000.

- Arrow keys or Space: navigate.
- O: overview.
- S: presenter view, including slide timings and notes.
- F: fullscreen.
- The footer links directly to Q&A and references.

The deck uses the existing Reveal.js 4.6.1 runtime, now included locally along
with its notes plugin and MIT license. Fonts use the system font stack. Slides,
images and reference demo outputs load without a CDN or font service; external
resource links still need an internet connection. Speaker view needs a local
server or the hosted site and may require allowing a popup.

## Live demonstration

The demo uses real public data from FRED to chart US annual CPI inflation and
the effective federal funds rate since 2019. A coding agent fetches the data,
then writes and runs a Stata analysis. The comparison is descriptive and makes
no causal claim.

- [Presenter guide](demo/README.md): the ten-minute run sheet and fallback.
- [Demo prompt](demo/prompt.txt): a copyable task brief.
- [FRED CSV snapshot](demo/fred/fred_snapshot.csv): saved on 23 September 2026.
- [Download script](demo/fred/fetch.ps1): refreshes the public CSV without an API key.
- [Stata do-file](demo/fred/analyze.do): creates the prepared outputs.
- [Prepared chart](demo/fred/reference/inflation_fedfunds.png),
  [analysis CSV](demo/fred/reference/monthly_analysis.csv),
  [data audit](demo/fred/reference/audit.txt) and
  [methods note](demo/fred/reference/methods.md).

Stata's built-in FRED API command requires a personal key. None is configured
on this workstation, so the live route uses FRED's public CSV download and
imports it into Stata. The saved snapshot makes the prepared result reproducible
if the network is unavailable. The earlier synthetic-firm example remains in
the repository as an optional offline exercise.

## Repository contents

    index.html                         Slide deck, styles and presenter notes
    assets/compustat_sample.csv         Earlier synthetic teaching data
    assets/images/Finance.png           Original Utrecht Finance logo
    assets/images/slides-qr.svg         QR for the public presentation URL
    assets/vendor/reveal/               Pinned runtime and license
    demo/README.md                     Presenter instructions
    demo/prompt.txt                    Live task brief
    demo/fred/                         Public FRED snapshot, Stata analysis and outputs
    demo/reference/                    Earlier synthetic analysis

## Preserved original

Before the update, the original repository was forked to
https://github.com/tchew86/agents.

The original main commit is
[1787a07f94df9b6109a3f1aad057efbb18887c5f](https://github.com/tchew86/agents/tree/1787a07f94df9b6109a3f1aad057efbb18887c5f).
The fork and that commit preserve the earlier Claude Code workshop.

Earlier workshop inspiration: Scott Cunningham's
[mixtapetools](https://github.com/scunning1975/mixtapetools), Mihail Velikov's
[master class](https://github.com/velikov-mihail/edhec-master-class), and Jukka
Sihvonen's [strategic-revision](https://github.com/jusi-aalto/strategic-revision).
