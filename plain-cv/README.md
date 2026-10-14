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

## Download
- **Word, original layout** (DOCX uploads): edits only the text inside the uploaded file, so fonts, spacing, tables and design stay as they were.
- **Word / PDF, clean layout**: single-column, ATS-safe rebuild.
- **Plain text**, and for PDF uploads a **change list** to apply in the source file. PDFs aren't edited in place: covering words leaves the old text in the file, where an ATS still reads it.

## Build a CV
Form-based builder with live slop marking, per-ATS tips, and Word/PDF/TXT downloads.

## Files
- `app.html`: page source (published as an artifact; no doctype wrapper)
- `index.html`: the same page as a standalone HTML document

Libraries load on demand from cdnjs: pdf.js 3.11.174, mammoth 1.6.0, JSZip 3.10.1, pdf-lib 1.17.1.
To extend the slop list edit `SLOP_DEF`; to add an ATS add a `P(...)` line to `PROFILES`.
