# Coding Agents for Researchers — USE Finance

A presentation for researchers at Utrecht School of Economics:
**40 minutes of presentation, 10 minutes of live demonstration, and 10 minutes of Q&A.**
No live installation is required to attend.

**Live slides:** https://usefinance.github.io/agents/

The opening slide has a QR code linking to the live deck, with matching frames
for the QR at the top left and the Finance Utrecht logo at the top right.

## What the talk covers

- Chat as an interface, and the capabilities that make a workflow agentic.
- Coding agents as a model working inside a harness with context, tools,
  an execution environment and controls.
- A practical cycle: define, inspect, plan, change, run, verify and report.
- Project instructions, reusable skills and MCP connections.
- Research, teaching and communication examples, with concrete checks.
- Execution location, model processing, access boundaries and approvals.

The core sequence has 18 slides. Slide 19 is the live demo and slide 20 is Q&A.
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

The demo creates a reproducible yearly median ROA figure from the synthetic
firm-year CSV already included in this repository. ROA is explicitly defined as
100 × net income / year-end total assets for this teaching example.

- [Presenter guide](demo/README.md): the ten-minute run sheet and review questions.
- [Demo prompt](demo/prompt.txt): a copyable task brief.
- [Reference script](demo/reference/analyze.py): uses only Python's standard library.
- [Prepared chart](demo/reference/outputs/yearly_roa.svg).
- [Prepared table](demo/reference/outputs/yearly_roa.csv).
- [Diagnostics](demo/reference/outputs/diagnostics.json) and
  [methods note](demo/reference/outputs/methods.md).

Run the fallback from the repository root:

    python demo/reference/analyze.py

The live demo should begin from the dataset and prompt in a fresh folder. The
reference implementation is a separately labelled fallback, not material for the
live agent to copy. No package installation is needed for the reference script.

## Repository contents

    index.html                         Slide deck, styles and presenter notes
    assets/compustat_sample.csv         Original synthetic teaching data
    assets/images/Finance.png           Original Utrecht Finance logo
    assets/images/slides-qr.svg         QR for the public presentation URL
    assets/vendor/reveal/               Pinned runtime and license
    demo/README.md                     Presenter instructions
    demo/prompt.txt                    Live task brief
    demo/reference/                    Executable fallback and checked outputs

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
