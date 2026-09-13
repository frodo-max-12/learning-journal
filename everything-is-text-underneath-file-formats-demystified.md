# Everything is text underneath -- file formats demystified

*Learned on March 7, 2026. I was poking around at how Excel files work and discovered you can literally unzip an .xlsx file and read the XML inside. That small surprise unraveled into a foundational insight about how computers represent everything -- and how AI tools interact with structured data.*

---

## The moment it clicked

I unzipped an Excel file.

That sounds like a small thing, but it genuinely startled me. I had always thought of an .xlsx file as a single, opaque binary object -- something only Microsoft Excel could read. A black box. You double-click it, the spreadsheet appears, and whatever happens in between is not your concern.

Then I learned that an .xlsx file is actually a zip archive. You can rename it from `budget.xlsx` to `budget.zip`, unzip it, and inside you will find a folder structure full of XML files. Human-readable XML files. The cell values, the formulas, the formatting -- all of it, described in structured text.

If cell A1 is colored blue, somewhere in the XML you will find something like:

```xml
<color rgb="FF0000FF"/>
```

That is not machine code. That is not binary. It is a string of characters that says "the color is blue" in a format both humans and machines can parse. The bold text in cell B3? A tag that says `<b/>`. The formula in C5? The literal text `SUM(A1:A4)` sitting in an XML element.

Everything I thought was opaque and proprietary was just text wearing a costume.

## What is a file format, really?

This realization opened up a bigger question. If Excel files are just zipped XML, what are other file formats? The answer, which I have come to think of as one of the most important foundational insights in computing, is: **almost everything is structured text**.

A PDF file contains a text-based description of page layouts, fonts, and content positions. An HTML file is literally a text document with tags that a browser interprets visually. A JSON file is text structured as key-value pairs. A PNG image file has a header (metadata in a defined text-like structure) followed by compressed pixel data. Even a compiled executable program started as text (source code) that a compiler transformed into machine instructions.

The file extension -- .xlsx, .pdf, .html, .json -- is really just a label that tells the operating system which program to use when opening the file. The file itself is data, structured according to some documented format. Change the extension, and you change which program tries to read it, but the content is the same bytes.

| File type | What it looks like | What is inside |
|---|---|---|
| **.xlsx** | A spreadsheet with cells, colors, formulas | Zipped XML files describing rows, columns, styles |
| **.docx** | A formatted Word document | Zipped XML files describing paragraphs, styles, images |
| **.html** | A web page | Text with tags: `<h1>Title</h1>`, `<p>Content</p>` |
| **.json** | Structured data | Text with key-value pairs: `{"name": "Alice"}` |
| **.csv** | A simple spreadsheet | Plain text, values separated by commas |
| **.pdf** | A printed-looking document | Text-based page description language |

> **See also:** [Why PDFs Are Binary, Not Text](why-pdfs-are-binary-not-text.md) — I later learned PDFs are actually binary files containing compressed streams of drawing commands (not text in the usual sense). The "everything is text" principle still mostly holds across formats, but PDFs are the interesting exception that deserved a deeper look.

The pattern is the same everywhere. Some format is more complex than others (PDF is notoriously messy), but the principle holds: at the bottom of every file format is a structured representation that, with the right knowledge, you can read and manipulate as text.

## But wait -- Google Sheets is different

My natural next question was: does Google Sheets work the same way? If I open a Google Sheet, is there an XML file somewhere on Google's servers that I could theoretically unzip and read?

No. And the reason why is instructive.

Google Sheets is a cloud-native application. There is no single file sitting on a disk the way an .xlsx file sits on your computer. When you work in Google Sheets, your data and formatting are stored on Google's servers -- specifically on their distributed file systems (originally GFS, now Colossus) -- and the "file" you interact with in your browser is really a live connection to that backend.

Google uses a data serialization format called **Protocol Buffers** (protobuf) internally. Unlike XML or JSON, which are text-based and human-readable, protobuf is a compact binary format designed for speed and efficiency. Google processes billions of operations across millions of spreadsheets; the overhead of parsing verbose XML for every cell edit would be enormous. Protobuf gives them the performance they need.

But the underlying principle still holds. When you interact with Google Sheets through the Google Sheets API, what you get back is JSON:

```json
{
  "values": [
    ["Name", "Revenue", "Region"],
    ["Acme Traders", "12000000", "Maharashtra"],
    ["Globex Supply", "8500000", "Gujarat"]
  ]
}
```

And when you ask about cell formatting:

```json
{
  "backgroundColor": {
    "red": 0,
    "green": 0,
    "blue": 1
  }
}
```

It is the same blue as the Excel XML `FF0000FF`, just described in a different notation. Text describing structure. The representation changes, but the principle does not.

When you export a Google Sheet, it gets converted on the fly into whatever format you choose -- .xlsx, .csv, .pdf. Google Sheets does not "contain" XML files the way an Excel file does, but at the API boundary, everything becomes structured text.

## Why this matters for working with AI

This is where the "everything is text" insight connects directly to what I am learning about AI tools and automation.

Large language models -- Claude, GPT, Gemini -- are fundamentally text-processing systems. They take text in and produce text out. They cannot natively "see" an Excel spreadsheet the way your eyes see a grid of cells on a screen. But they can absolutely work with the structured text representations that lie underneath those visual presentations.

When I connect Claude to Google Sheets via MCP (the Model Context Protocol I learned about in a separate conversation), here is what actually happens:

1. I ask Claude something like "find all suppliers with revenue over 1 crore"
2. Claude calls the Google Sheets MCP tool, which hits the Sheets API
3. The API returns the spreadsheet data as structured JSON text
4. Claude reads that JSON, understands the structure, and answers my question

Claude never "opens" the spreadsheet. It reads the text representation. And because the text representation contains all the information -- the values, the formulas, the formatting -- Claude can do anything with it that a human could do while looking at the visual spreadsheet, sometimes more efficiently.

This is why the "everything is text" principle is not just an interesting trivia fact. It is the foundational reason AI tools can interact with the digital world at all. Every integration, every automation, every MCP server works because the data it connects to can be expressed as structured text.

## The practical implication: multiple paths to automation

Understanding this opened up a practical question for me. If I want an LLM to work with my spreadsheets -- analyzing data, generating reports, automating repetitive tasks -- there are several paths, and they correspond to different levels of directness:

**Path 1 -- Copy and paste (simplest).** I select the data in my spreadsheet, copy it, paste it into Claude. What gets pasted is text -- usually tab-separated values. Claude reads it, analyzes it, gives me answers. I copy the output back. This works today, immediately, with zero setup. The "everything is text" principle is what makes this possible: the clipboard converts the visual grid into text, and the LLM works with text natively.

**Path 2 -- API / Apps Script (medium).** I write code (or have Claude write code) that programmatically reads the spreadsheet via the Google Sheets API, sends the data to an LLM API as text, gets back structured text, and writes it back into the sheet. Google Apps Script is particularly convenient here because it runs inside the Google ecosystem with no external setup required. The "middle layer" of code is what converts between the spreadsheet's internal representation and the text the LLM needs.

**Path 3 -- MCP (most automated).** I connect the LLM to the spreadsheet via an MCP server. Now I just talk to Claude naturally -- "update the Q3 projections based on last month's actuals" -- and Claude handles the API calls, the data parsing, and the writing-back autonomously. The MCP server is the bridge between Claude's text world and the spreadsheet's structured data.

Each path is a different point on the automation spectrum, but they all work because of the same underlying reality: the spreadsheet data can be expressed as text, and the LLM can process text. The visual interface I see when I open Google Sheets is a convenience for human eyes. Under the hood, it is text all the way down.

## The deeper principle

What struck me most about this learning is how general the principle is. It is not just about spreadsheets.

Images are grids of numbers. Music is streams of numerical samples. Bold text is just a flag in a data structure. A video is a sequence of compressed image frames. A 3D model is a list of vertex coordinates and face definitions. Every complex digital artifact, no matter how rich it appears to human senses, is ultimately represented as structured data that can be expressed as text.

This is why programming is so powerful. When you learn to work with text representations directly -- reading them, transforming them, generating them -- you gain a kind of x-ray vision into the digital world. The visual surfaces (the spreadsheet grid, the formatted document, the rendered web page) are human-friendly projections of the underlying reality. The text is the reality.

> The moment I unzipped that .xlsx file and saw readable XML, my mental model of "what a file is" shifted permanently. Files are not opaque boxes that only their native applications can understand. They are structured descriptions, written in documented formats, readable by anything that knows the format.

For someone coming from a non-technical background, this was one of those "the veil lifts" moments. I had been interacting with computers for twenty-plus years as a consumer of visual interfaces, never realizing that everything those interfaces showed me was a rendering of text-based descriptions underneath. Learning this changes how you think about automation, about data, and about what is possible when you start treating information as the structured text it actually is.

The practical version of this philosophy: if something exists on a computer, it can be read as text. If it can be read as text, an LLM can process it. If an LLM can process it, it can be automated. The entire chain from "opaque file" to "automated workflow" rests on the single insight that there are no truly opaque files -- just text you have not learned to read yet.

---

*What I studied next: [Options, Black-Scholes, and implicit options in physical trading](options-trading-black-scholes-and-implicit-options-in-physical-trading.md), where a news story about SEBI banning Jane Street led me to discover that my semiconductor trades already have options structures embedded in them.*
