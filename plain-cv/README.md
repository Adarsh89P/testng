# Plain CV Scanner

A self-contained ATS checker and CV builder. Open `index.html` in a browser. Nothing is uploaded; all checks run locally.

## Pick an ATS
The "Scan as" dropdown has 52 profiles: enterprise systems (Workday, Taleo, SuccessFactors, iCIMS, ...), tech and startup systems (Greenhouse, Lever, Ashby, ...), small-business tools, staffing agency systems (Bullhorn, Ceipal, ...), Indian systems and job portals (Naukri, Darwinbox, Keka, Zoho Recruit, TurboHire, foundit, ...), UK/EU/AU systems, LinkedIn and Indeed, and USAJOBS.

Each profile sets:
- **matching**: exact keywords, keywords with word forms, AI/semantic (related skills get partial credit), or mostly human review
- **parser strictness**: how hard tables, columns, text boxes and header/footer contact details are penalised
- **screening questions**: how much knockout fit (years, degree, notice period, work authorisation) counts
- **safest upload format**: Word or PDF

Vendors don't publish their scoring. Profiles are built from vendor documentation and recruiter reports, so the score is a guide, not a guarantee. "Compare across all ATS profiles" scores the same CV against every profile.

## Scan a CV
- Paste text or upload PDF, DOCX or TXT. DOCX uploads are also inspected for tables, text boxes, columns, images and contact details in headers/footers.
- Keyword match against a job description; click a missing keyword to add it to your Skills line.
- Red-pen proof of AI-sounding filler (swap / cut / flag). Every fix can be changed or replaced with your own wording.

## Side preview
Next to the CV editor, a live preview renders the exact file the main download gives you, page by page, with an Updated / Original toggle. In PDFs the changed lines are highlighted. Word files are drawn with docx-preview, so Word itself may differ slightly in bullets and spacing.

## Download in your own format
Edit any word or line in the CV box (or use the slop fixes and keyword chips). The download is **your uploaded file with only that text changed**; it is never rebuilt.

- **Word (.docx)**: the tool diffs the uploaded text against your edited text and changes only those words inside the original runs. Fonts, sizes, colours, bold/italic, bullets, tables, headers and spacing stay as they were. Deleted lines are removed; new lines copy the formatting of the line above (a new bullet stays a bullet).
- **PDF**: the tool reads each page's content stream, decodes the text with the PDF's own font tables, and rewrites a changed line from the first changed word to the end of that line segment, using the same embedded font, size and position. Bold and other styles carry over per word, right-aligned dates keep their place, and a longer line is squeezed slightly instead of overflowing. The old text is really removed, so an ATS reads the new wording; every download is re-read to check. Limits: a PDF can't take extra lines, removed lines leave a gap, and if the embedded font lacks a letter you typed, that letter is drawn in the closest standard font (Helvetica/Times/Courier) and you're told which.
- **Other formats**: rebuilt clean-layout Word/PDF, plain text, and a change list.

## Build a CV
Form-based builder with live slop marking, per-ATS tips, and Word/PDF/TXT downloads.

## Files
- `app.html`: page source (published as an artifact; no doctype wrapper)
- `index.html`: the same page as a standalone HTML document

Libraries load on demand from cdnjs: pdf.js 3.11.174, JSZip 3.10.1, pdf-lib 1.17.1, and docx-preview 0.3.5 from jsDelivr.
To extend the slop list edit `SLOP_DEF`; to add an ATS add a `P(...)` line to `PROFILES`.
