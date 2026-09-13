# Document Conversion, and Why OCR Is a Separate Problem

**Context:** I found a tool that converts almost any document format to Markdown and assumed, given when it was built, that a language model was doing the parsing. It isn't. Finding out what it actually does — and then asking the obvious follow-up about scanned PDFs — produced a clean lesson about where machine learning genuinely is required versus where it's the fashionable answer to a solved problem.

---

## 1. It's a dispatcher, not a model

The tool is a **thin wrapper that routes each file type to a dedicated parsing library** and emits Markdown. No model in the default path at all.

| format | what actually parses it |
|---|---|
| PDF | a text-extraction library, plus a table-extraction library |
| DOCX | a converter to HTML, then HTML → Markdown |
| PPTX | a library that walks slides and shapes |
| XLSX | a spreadsheet library |
| HTML | an HTML parser plus a Markdown converter |
| audio | audio handling plus speech recognition |
| images | EXIF metadata, optional OCR |

So for a PDF: one library extracts the text stream, another extracts tables, and the tool does light post-processing — stitching split numbering back together, formatting tables as Markdown grids.

**The honest consequence:** output quality is *exactly* as good as the underlying libraries. It works well on born-digital PDFs with a clean text layer, and degrades to nothing on scanned ones.

That framing — a converter as a **dispatcher over mature format-specific libraries** — is the useful idea. The tool's value isn't parsing. It's the uniform interface and the routing table. Which is a legitimate and underrated kind of software: the hard work is already done in a dozen separate libraries with a dozen separate APIs, and collapsing them behind one call is the whole product.

---

## 2. The question that mattered: what about image PDFs?

If my PDF is a scan, surely machine learning is needed? Yes — and this is exactly where the default path fails.

**On a scanned PDF, the text-extraction library returns essentially nothing.** A scanned PDF has no text layer, only embedded raster images. The tool does not run OCR itself: no bundled engine, no built-in vision model.

**You get an empty or near-empty Markdown file, silently.**

That silent failure is the most useful thing in this entry. Not an error, not a warning — a successful conversion producing nothing, which in a batch pipeline means a file quietly contributing zero and nobody noticing.

I now treat "output is suspiciously small" as a first-class check when converting documents in bulk, because it's the *only* signal this failure produces. It's the same shape as several other silent failures I've run into — a search returning the first match when you needed all of them, an evaluation optimizing the seed lottery. **The failure that produces plausible output is always more expensive than the one that crashes.**

---

## 3. Three ways to get text out of an image, and what each actually is

To handle scanned documents you have to opt into one of three ML-backed paths, and they're genuinely different technologies:

**A vision model per image.** Each embedded image is sent to a multimodal model with a prompt asking for the text. The ML is a general-purpose multimodal model doing visual recognition — flexible, handles messy layouts and handwriting, costs per page.

**A hosted document-intelligence service.** The file goes to a service running trained layout and OCR models — descended from document-understanding architectures rather than being general chat models — which returns structured text, tables, and reading order. The ML is specialized for documents.

**Classical OCR, run yourself first.** A traditional OCR engine — convolutional and recurrent networks, trained specifically for character recognition — adds a text layer to the PDF in place. Then the ordinary text-extraction path works normally.

That last option is the one I'd have skipped, and it's often the right answer: free, local, no data leaving the machine, and it converts the problem back into the solved one. **Rather than making the converter smarter, you make the document conform to what the converter already handles.**

The three form a clear cost/quality ladder:

| approach | ML used | cost | best for |
|---|---|---|---|
| classical OCR first | purpose-built recognition networks | free, local | clean printed text at volume |
| hosted document service | specialized layout + OCR models | per page | complex tables, reading order |
| vision model per page | general multimodal model | highest | handwriting, unusual layouts |

---

## 4. Where the ML boundary actually falls

The clarifying line:

> **Text extraction is a parsing problem. Image-to-text is a recognition problem. Only the second one needs machine learning.**

A born-digital PDF *contains* the characters — they're in the file, encoded, alongside the drawing instructions that position them. Getting them out is fiddly (which is why extraction libraries exist and why PDF text extraction has a reputation) but it's fundamentally decoding.

A scanned PDF contains **pixels**. The characters aren't in the file in any form. Recovering them means inferring symbols from images, which is irreducibly a recognition task.

That's why the tool's "lightweight" positioning is a real design decision rather than a limitation: bundling an OCR engine would mean bundling a model, and they'd rather stay a dispatcher and let you bring the recognition. Knowing *that* is the difference between "this tool is bad at scans" and "this tool has correctly identified where its problem ends."

---

## 5. What I took away

**Check what a tool actually does before assuming the fashionable answer.** My prior was "it's recent, so a model is parsing." It's a routing table over libraries that mostly predate the current era, and that's a better design for the job.

**Silent empty output is a failure mode worth explicitly testing for.** Nothing errors. In bulk processing you find out much later, if at all.

**"Does this need ML?" has a principled answer.** Is the information present in the file and merely awkward to extract, or absent and needing to be inferred? Decoding versus recognition. Almost every "should I use a model here?" question I've faced since sorts cleanly on that distinction.
