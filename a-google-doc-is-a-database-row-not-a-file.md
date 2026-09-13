# A Google Doc is a database row, not a file

---

## The mental model I had to give up

My mental picture of a Google Doc was this: somewhere on Google's servers, there's a folder for my account, and inside it there's a file called something like `my_essay.gdoc`. When I open it in my browser, the server reads that file from disk and shows it to me. Same as a Word document on my laptop, just stored on Google's hardware instead of mine.

That mental model is wrong. Once I saw the correct picture, a huge amount of how Gmail, Notion, Linear, Instagram, and every other "cloud app" works suddenly made sense.

## What I got right

I had assumed "ultimately it's stored on Google's hard disk somewhere." **That part is true.** Databases live on hard disks too. PostgreSQL data lives in files under `/var/lib/postgresql/data/`. SQLite is literally a single `.db` file on disk. There's no ethereal storage — bits live on disks somewhere.

The question isn't *whether* it's on a hard disk. It's: **what shape are the bits in, and how do you access them?**

That's where "file" and "database row" diverge.

## The two models, side by side

**File model (my original mental picture):**

```
/users/you/google-drive/
    my_essay.gdoc          ← one file, the whole document
    project_plan.gdoc
```

Open the file → server reads the whole thing from disk → sends to browser → browser renders → I type → browser sends new content → server overwrites the file. Same as Word on my laptop.

**Database-row model (what's actually happening):**

Imagine Google's server has tables roughly like this:

```sql
CREATE TABLE documents (
    doc_id UUID PRIMARY KEY,
    owner_user_id UUID,
    title TEXT,
    created_at TIMESTAMP
);

CREATE TABLE paragraphs (
    paragraph_id UUID PRIMARY KEY,
    doc_id UUID,
    position INT,
    content TEXT,
    style_id UUID
);

CREATE TABLE edit_operations (
    op_id UUID PRIMARY KEY,
    doc_id UUID,
    user_id UUID,
    timestamp TIMESTAMP,
    op_type TEXT,
    op_payload JSONB
);

CREATE TABLE permissions (
    doc_id UUID,
    user_id UUID,
    role TEXT
);

CREATE TABLE comments (
    comment_id UUID,
    doc_id UUID,
    paragraph_id UUID,
    author_id UUID,
    body TEXT
);
```

My "Google Doc" — the one thing that *feels* like a single document — is actually:

- **One row** in `documents` (title, owner, ID).
- **Many rows** in `paragraphs` (one per paragraph, ordered by `position`).
- **Many rows** in `edit_operations` (one for every keystroke anyone has ever made).
- **Some rows** in `permissions` and `comments`.

There is **no file anywhere on Google's disks called `my_essay.gdoc`**. The document doesn't exist as a single object. It exists as a *pattern of rows scattered across multiple tables*, linked by `doc_id`.

(Google's actual internal architecture uses a database system called Spanner. The principle is the same — structured tables with rows.)

## What happens when I open a doc

When I load `docs.google.com/document/d/abc123`, the server runs roughly:

```sql
-- Am I allowed?
SELECT role FROM permissions WHERE doc_id = 'abc123' AND user_id = 'alice';

-- Document metadata
SELECT * FROM documents WHERE doc_id = 'abc123';

-- All paragraphs in order
SELECT * FROM paragraphs WHERE doc_id = 'abc123' ORDER BY position;

-- Comments
SELECT * FROM comments WHERE doc_id = 'abc123';
```

It **assembles** the result into a JSON payload, sends to my browser, and the browser's JavaScript renders the document. The rendering is generated fresh, on the spot, from the database state at that moment.

When I type a character, my browser sends an `edit_operation` row:

```sql
INSERT INTO edit_operations (doc_id, user_id, timestamp, op_type, op_payload)
VALUES ('abc123', 'alice', NOW(), 'insert', '{"position": 42, "text": "x"}');
```

That row is also broadcast to anyone else currently viewing the doc, so their browsers update in real time.

## Why this architecture enables what Google Docs can do

Every Google Docs feature stops feeling like magic once you see the underlying data model:

| Feature | Why it works |
|---|---|
| **Real-time collaboration** | Each keystroke is a row in `edit_operations`. Multiple users append rows simultaneously; the server merges them. A file would corrupt if two people wrote at once. |
| **Infinite version history** | Every edit, forever, is a row. Want to see the doc as of last Tuesday? Replay operations up to that timestamp. |
| **Granular permissions** | "Share with Sagar as commenter" is one `INSERT INTO permissions`. With a file, you'd only have OS-level permissions — no "can comment but not edit." |
| **Comments anchored to text** | A comment row has a `paragraph_id`. When the paragraph moves, the comment follows (shared foreign key). With a file, a comment would be at a byte offset that breaks when text shifts. |
| **"Last edited by Sagar 2 min ago"** | Query the most recent `edit_operations` row, look up the user. With a file, you'd only know "the file was modified." |

None of these fall out naturally from a file architecture. They fall out naturally from rows.

## So where does the "download as .docx" file come from?

When I click Download → .docx, the server:

1. Runs those queries to assemble the doc.
2. Walks the assembled structure and **generates a brand-new `.docx`** (writes XML, zips it up) from the database content.
3. Sends it to my browser.

That `.docx` is an **export** — a snapshot, computed on demand. It's not the canonical document. If I edit it and re-upload, Google has to parse it and *insert new rows back into the database*. This is why exports sometimes lose things (comments may not translate cleanly, image positioning may shift). The translation between representations is lossy.

## The right reframe

- **Word `.docx` on my laptop**: the file *is* the document. Word is just a viewer for that file.
- **Google Doc**: the database state *is* the document. The Google Docs web app is just a viewer for that database state. There is no underlying file to point at.

## The same pattern is everywhere once you see it

This isn't unique to Google Docs. It's the architecture of almost every modern web app:

- **Outlook (old days)**: emails were `.eml` files on disk. **Gmail today**: emails are rows in Google's mail database. No `email_12345.eml` file exists anywhere.
- **Photos on your hard drive**: each is a file. **Instagram photos**: each is a row referencing a media blob, plus rows for likes, comments, hashtags, geotags.
- **A song on your hard drive**: one `.mp3`. **A Spotify track**: a row pointing to an audio blob, plus rows for the playlists it's in, your play history, related artists.

Every "thing" in a modern cloud app — a tweet, a Slack message, a Linear ticket, a Notion page, a Salesforce account — is a small constellation of rows across tables, assembled on demand into what you see.

## What this implies for ownership

The architectural shift has a practical consequence.

When I had a `.doc` file on my laptop in 2005, I owned it. I could copy it, back it up, open it in any compatible software, keep it forever even if Microsoft went out of business. The file was the document.

When I have a Google Doc in 2025, I don't own it in the same sense. I can export it — but the export is a derivative, often lossy. The canonical document lives in Google's database. If my account gets disabled, if Google shuts down Docs, if a government compels Google to hand over my data, the document is no longer mine in the way a local file would be.

This isn't an argument against cloud apps — the collaboration features are genuinely transformative. But it's worth being clear-eyed about the trade: the convenience of "no file management" comes at the cost of "no real ownership." For documents I want to last decades, I still prefer formats that exist as files I control.

## The transferable principle

The shift from "file" to "database row" is bigger than document formats. It's the shift from **artefacts I own** to **services I access**. Most of computing in 2025 has made that shift. The benefits (collaboration, infinite history, instant sync, granular permissions) are real. The costs (vendor lock-in, no offline canonical copy, dependence on the service running) are also real.

A useful frame: ask whether the thing you're working with is *a file you own* or *a view onto a database someone else owns*. Both can be the right choice. Conflating them — assuming a Google Doc behaves like a Word file — leads to surprises that range from "comments didn't survive the export" to "all my work disappeared when my account got disabled."

---

*What I studied next: [Google Spanner and the CAP theorem](google-spanner-and-the-cap-theorem.md) — the database technology that makes "your Google Doc is a row in our database" actually work across continents.*
