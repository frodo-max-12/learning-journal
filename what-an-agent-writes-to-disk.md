# What an Agent Writes to Disk — Reading the Dotfiles of a Coding Agent

**Context:** I noticed a pile of folders inside my coding agent's config directory that I'd never opened — snapshots, a JSONL log, rotating backups, 131 empty directories — and asked what each one was. What I expected was housekeeping trivia. What I got was a tour of durable-state design, including one pushback I made that turned out to be a genuine category error on my part, and correcting it taught me more than the tour did.

---

## 1. The snapshot store

The first folder holds file snapshots, organized like this:

```
file-history/
├── <session-uuid>/
│   ├── <filehash>@v1   ← the file before the 1st edit in this session
│   ├── <filehash>@v2   ← after the 1st edit / before the 2nd
│   └── <otherhash>@v1
├── <session-uuid>/     ← empty: no files were edited in that session
└── ...
```

Three conventions, each decodable from the structure:

| pattern | meaning |
|---|---|
| a UUID directory | one conversation session |
| the hash prefix | a deterministic key for a specific file path |
| `@v1`, `@v2`, `@v3` | successive versions of that file *within* the session |

Two things fall out of that layout that I found genuinely informative.

**Empty session directories are the norm.** About half of mine had zero contents — sessions where I only asked questions or read files. The directory gets created at session start and then never written to. That's a design choice: allocate the slot unconditionally, fill it lazily.

**The same hash appearing under two different sessions is a fingerprint.** Because the hash is deterministic from the file path, seeing it in two session folders means the same file was edited across two separate conversations. If you wanted to find every session that touched a given file, you'd hash its path and grep for it — the index you need already exists as a side effect of the naming scheme.

And the reason the unit of storage is *per-session per-version* rather than "latest version of each file" is that **the unit of recovery is a single edit**, not a file. An agent's edit tool writes to disk immediately — there's no "preview, then save" step like a normal editor. Without this store, your only recovery path would be git, assuming the file was tracked and recently committed. The snapshot store covers untracked files, uncommitted changes, and files that aren't in a repository at all.

---

## 2. My pushback, and why it was wrong

My reaction was: *why write versions to disk at all? The model read the file, it has the contents in its context — it can reconstruct the old version.*

That intuition is appealing and it's a category error. Four reasons, and they stack:

**The model never had the whole file.** This is the least obvious and the most important. When an agent does a find-and-replace edit, the *harness* — not the model — opens the file, locates the matching substring, and writes the replacement. The model only ever saw the chunk it quoted. Edit a 6-line function in an 800-line file and 794 of those lines never entered the context at all. The context isn't a complete copy to reconstruct from; it's a sparse, partial view. The snapshot on disk has all 800 lines because the harness wrote them there before applying the change.

**After the write, the old bytes exist nowhere else.** Re-reading the file post-edit gives you current state, not previous state. This is a one-way door in the filesystem, and there's no reflog for arbitrary file edits unless something explicitly wrote the old version somewhere.

**Context is ephemeral; disk is durable.** They're different durability classes:

| event | model context | disk snapshot |
|---|---|---|
| compaction | old content summarized away | untouched |
| session ends | gone | untouched |
| restart / reboot | gone | untouched |
| new conversation tomorrow | can't reach yesterday's context | readable for any past session |

Each of those happens routinely, not exceptionally.

**Model recall is probabilistic; bytes aren't.** Even with context intact, "reconstruct the previous version so we can revert" is approximate recall. You'd get 99.5% of it right and silently change one character in a regex. For a recovery operation, **99.5% is catastrophic** — worse than an outright failure, because a failure is visible and silent drift isn't.

The general rule this instantiates shows up everywhere once you see it:

| system | ephemeral "memory" | durable "state" |
|---|---|---|
| web server | RAM | database |
| bank | teller's open window | general ledger |
| coding agent | model context | on-disk snapshots + the files themselves |

**State must outlive memory, and recovery operations must read from state, not memory.** In-process recall is fast but probabilistic and ephemeral; on-disk state is slower but exact and durable. They do different jobs and you need both.

I've since found this to be the single most portable idea I took from opening these folders — it's the same reason a parsed view of a data source gets written to a database rather than re-derived on demand every time.

---

## 3. The prompt log, and JSONL's actual superpower

Sitting alongside is an append-only log of every prompt ever typed on this machine — the thing that powers up-arrow recall in the input box. Mine holds over a thousand entries in a few hundred KB.

**JSONL** = JSON Lines: one JSON object per line, never wrapped in an array. Append-only.

The schema is small — the prompt text, any pasted attachments, a timestamp, the working directory, and a session ID. But the interesting detail is that **the session ID is missing from the oldest entries and present on newer ones.** The schema was extended in a version upgrade, and the old entries remained valid records.

That's JSONL's real advantage over a single big JSON file or a relational table. Every line is independent, so you can add fields, change types, even introduce nesting in new entries, and nothing already written breaks. Appending is a single `write()` with no need to parse-and-rewrite the whole file, so a crash mid-write costs you one truncated line rather than the document.

The cost is the exact mirror of the benefit: **no enforced schema**. Every consumer has to handle missing fields defensively, and "what shape is this data?" becomes a question about *when* a record was written. That's a real tax, and it's the trade JSONL makes deliberately — it's the format you choose when append-safety and schema evolution matter more than query-time guarantees, which is precisely the situation for a log.

I now read the format choice as a statement of intent. Seeing `.jsonl` tells you someone expected the schema to change and wanted appends to be crash-safe.

---

## 4. Rotating backups — bounded history on purpose

Another folder holds timestamped copies of the main config file. Exactly five of them, each named with a Unix millisecond timestamp, taken roughly every 20–90 minutes while the tool is running. The sixth deletes the oldest.

This is a **ring buffer of snapshots**, and its design accepts a specific limitation: you cannot recover config state from last week. But the 99% case for "roll back my config" is "roll back what just broke," and five snapshots over a few hours covers that completely.

Bounded storage with last-N retention is a small idea that's everywhere once you look — log rotation, CI artifact retention, rolling-update history. The pattern is *deliberately forgetting* so that storage stays constant while the useful window stays covered.

Small practical note that cost me a minute: these files start with a dot, so a plain `ls` shows nothing and the folder looks empty. `ls -a`.

---

## 5. The 131 empty directories

The most interesting folder contained nothing at all. 131 UUID-named subdirectories, every single one empty. Zero files anywhere in the tree, ~12KB total, all of it directory metadata.

The count and the date range implied one directory created per session launch. So: a per-session slot that essentially never gets filled.

The likely reading is that it's a **pre-allocated scratch space** for per-session state — env-var overrides scoped to one session, ephemeral state for hook scripts, runtime context for features that either haven't shipped or that my usage never triggers. The directory is created unconditionally at session start on the theory that it's cheaper to always make it than to check-and-create at the moment of need.

What I liked about this one is that it's a legible negative result. An empty directory tree is evidence — it tells you a code path exists and that you never take it. And "create the slot unconditionally, fill it conditionally" is the same pattern as the empty session folders in §1, which suggests it's a house style rather than an accident.

---

## 6. What the config file reveals about how the tool is built

The main config file is a single JSON document with dozens of top-level keys, and the categories are more interesting than the values:

| category | what it stores |
|---|---|
| identity & account | who you are to the service, subscription state |
| install state & versions | first-run time, startup count, which migrations have run |
| UI preferences | theme, verbosity, display toggles |
| **cached server config** | hundreds of feature flags, pulled from a remote flag service and cached locally |
| connected servers | which integrations are configured |
| project history | every directory the tool has been launched from |
| hint & upsell tracking | booleans and counters gating one-time tips |
| usage telemetry | local counts of feature usage |

Three things I hadn't thought about before reading it:

**Feature flags are cached locally, not fetched per launch.** Flags live in a server-side service, get pulled on sync, and are read from local cache at startup — so the tool doesn't make a network call before it can render. Flips happen server-side and reach you on the next sync. That's why behaviour can change without an update.

**Flag names are deliberately opaque.** They're built from unrelated codewords rather than descriptive names. This is a real A/B-testing convention, not obfuscation for its own sake: a flag named `dark_mode_enabled` tells anyone who sees it exactly what experiment is running, which biases behaviour — engineers code around it, and users who hear about it self-select into a variant. An opaque name reveals nothing, and the mapping to real descriptions lives internally.

**A surprising fraction of the file is hint-suppression state.** Counters and booleans whose only job is remembering that you've already been shown something. That's an entire category of persistent state existing purely so software can avoid repeating itself — obvious in hindsight, and I'd never once considered where "don't show this tip again" is stored.

---

## 7. What I'd generalize

Reading a tool's dotfiles turns out to be one of the higher-yield ways to understand it, because **the on-disk layout is the honest version of the architecture.** Docs describe intent; the directory tree records what the program actually decided to persist, at what granularity, with what retention.

Four transferable patterns came out of one afternoon:

- **Durable state must outlive ephemeral memory** — and recovery reads from state, never from recall.
- **Append-only JSONL** buys crash-safe writes and schema evolution, at the cost of enforced structure.
- **Ring-buffer retention** covers the real recovery window without unbounded growth.
- **Pre-allocate the slot, fill it lazily** — cheap directories, simpler code paths, legible empties.

None of those are agent-specific. They're the reason the folders look the way they do, and I'd have missed all of them if I'd accepted "it's internal housekeeping" as an answer.
