# Obsidian and LLM-Powered Knowledge Bases

## What is Obsidian?

Obsidian is a free, local-first note-taking app that stores everything as plain **markdown (.md) files** in a regular folder on your computer. Unlike Notion or Google Docs, your data never lives on someone else's server — it's just files on your disk.

### Why markdown matters
- Markdown is a simple text format (headers with `#`, bold with `**`, links with `[text](url)`)
- Because it's plain text, any tool can read/edit it — you're never locked in
- Git can track changes to markdown files, so you get version history for free

### Key Obsidian concepts

**Vault** — A vault is just a folder that Obsidian opens. Every `.md` file inside it becomes a note. You create a vault by pointing Obsidian at any folder on your computer (File → Open folder as vault).

**Wikilinks** — The killer feature. You link notes together using `[[double brackets]]`:
```markdown
See [[other-note-name]] for details.
```
When you click these links, Obsidian navigates to that note. This creates a web of interconnected knowledge, not a flat list of files.

**Graph View** — Obsidian can visualize all your notes and their links as an interactive network graph (`Cmd+G` on Mac). Notes that link to each other appear connected. This lets you literally *see* how your knowledge connects — clusters of related ideas become visible.

**Backlinks** — If Note A links to Note B, Obsidian automatically shows you in Note B that Note A references it. You don't have to maintain these manually — Obsidian does it for you.

## The Andrej Karpathy Workflow

Andrej Karpathy (former Tesla AI director, OpenAI researcher) recently shared how he uses LLMs to build personal knowledge bases. The insight is that LLMs are great at *compiling and organizing* knowledge, not just answering questions.

### The architecture

```
raw/          ← Dump source material here (articles, papers, notes)
    ↓
  [LLM compiles]
    ↓
wiki/         ← LLM-maintained wiki articles with cross-links
    ↓
  [LLM queries]
    ↓
outputs/      ← Generated reports, slides, charts
```

### How it works, step by step

**1. Ingest** — You save articles, papers, web clippings into a `raw/` folder. The Obsidian Web Clipper browser extension can convert any webpage to markdown with one click.

**2. Compile** — You ask an LLM (like Claude) to read everything in `raw/` and build organized wiki articles in `wiki/`. The LLM creates:
- Summary articles for each concept
- Cross-links between related topics (`[[wikilinks]]`)
- An index file listing everything
- Categories and organization

**3. Query** — Once the wiki is big enough (~100 articles, ~400K words in Karpathy's case), you can ask the LLM complex questions. It researches across the wiki and generates thorough answers. Karpathy noted that simple index files + summaries work surprisingly well — you don't necessarily need fancy RAG (Retrieval Augmented Generation).

**4. Output** — Instead of just text answers, the LLM can generate:
- Markdown reports (viewed in Obsidian)
- Slide decks (Marp format, rendered via Obsidian plugin)
- Charts (matplotlib images)
- These outputs get "filed back" into the wiki, so your explorations compound.

**5. Lint** — Periodically run LLM "health checks" over the wiki to:
- Find inconsistencies across articles
- Fill in missing data (using web search)
- Suggest new connections between topics
- Propose new articles to write

### Why this is powerful

The key insight is that **the LLM writes and maintains all wiki content — you rarely touch it directly**. Your role is:
- Feeding in raw sources
- Asking questions
- Directing what topics to explore

This inverts the traditional note-taking model. Instead of you organizing knowledge, the LLM does it, and you *navigate* and *query* the result.

## Technical Details

### How Obsidian stores data
```
~/Documents/my-vault/           ← This is your vault (just a folder)
├── .obsidian/                  ← Obsidian settings (themes, plugins, etc.)
├── raw/                        ← Your folder structure
│   ├── article-1.md
│   └── article-2.md
├── wiki/
│   ├── index.md
│   ├── topic-a.md
│   └── topic-b.md
└── outputs/
    └── report-1.md
```

Everything is just folders and `.md` files. You can:
- Git version control the whole vault
- Open the files in any text editor (VS Code, vim, etc.)
- Back them up however you want (Dropbox, iCloud, etc.)
- Move the folder to another computer and open it in Obsidian there

### Useful keyboard shortcuts (Mac)
| Shortcut | Action |
|----------|--------|
| `Cmd+G` | Open Graph View |
| `Cmd+O` | Quick open (search for any note) |
| `Cmd+P` | Command palette (search for any action) |
| `Cmd+E` | Toggle edit/preview mode |
| `Cmd+N` | New note |
| `Cmd+Click` | Open link in new tab |

### Obsidian plugins worth knowing about
- **Web Clipper** — Browser extension to save web pages as markdown
- **Marp** — Render markdown as slide presentations
- **Dataview** — Query your notes like a database
- **Graph Analysis** — Enhanced graph view with clustering

## How This Connects to What I've Learned

This builds on several things from my learning journal:

- **[[version-control-with-git-and-github]]** — The vault is just files, so you can git track everything
- **[[terminal-first-principles-and-package-management]]** — You can manipulate vault files from the terminal
- **[[ai-agent-loop-tools-and-orchestration]]** — The LLM agent loop (observe → think → act) is exactly how the knowledge base compilation works: the LLM reads files, decides what articles to create, writes them, then iterates

## Key Takeaway

The most interesting shift is from "LLM as question-answerer" to "LLM as knowledge compiler." Instead of asking one-off questions and getting one-off answers, you build a persistent, growing knowledge base that compounds over time. Every query you run, every source you add, makes the whole system more useful.
