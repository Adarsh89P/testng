# Plain CV Scanner

A small, self-contained ATS checker and CV builder. Open `index.html` in a browser. Nothing is uploaded; all checks run locally.

## Scan a CV
- Paste text or upload a PDF, DOCX or TXT (PDF and DOCX text extraction loads pdf.js / mammoth from cdnjs).
- Paste a job description to get a keyword match: known skills (Selenium, TestNG, REST Assured, CI/CD, ...) plus terms the posting repeats.
- Score out of 100 from keywords, section headings, contact details, measurable bullets, parse safety and plain language.
- Red-pen proof marks AI-sounding filler in three ways:
  - **swap**: replaced with a plain word (spearheaded → led, leveraged → used)
  - **cut**: removed, adds nothing (successfully, seamless, results-driven)
  - **flag**: needs a rewrite with real facts (passionate about, proven track record, responsible for)
- Clean copy applies the swaps and cuts automatically.

## Build a CV
A form that outputs a single-column CV with standard headings and one date format, the layout parsers read most reliably. It flags slop as you type, and "Scan this CV" sends it to the checker.

## Files
- `app.html`: the page source (published as an artifact; no doctype wrapper)
- `index.html`: the same page wrapped as a standalone HTML document

To extend the slop list, edit `SLOP_DEF` near the top of the script.
