# What Actually Happens When You Unzip a File

**Context:** I double-clicked a 9.8 GB zip archive, it produced a folder, and I wanted to delete the original — but I hesitated, because I wasn't sure whether the extracted folder was *the files* or somehow still *pointing at* the zip. That hesitation was worth following. The answer is yes, delete it — and the reason why turns into a tour of how compression actually works, including why my particular archive compressed far worse than it should have.

---

## 1. The direct answer

Once extraction completes without error, **the zip and the extracted folder are two independent copies of the same bytes.** Delete either; the other still works.

There is no linkage, no reference, nothing lazy. Extraction reads the compressed bytes, reconstructs the originals, and writes them to disk as ordinary files. The uncertainty I felt comes from the macOS Finder presenting archives semi-transparently — you can peek inside without extracting — which makes it *feel* like the folder might be a view onto the archive. It isn't.

---

## 2. What's actually inside a .zip

A zip is a binary container with three parts:

```
[Local File Header 1][Compressed Data 1]
[Local File Header 2][Compressed Data 2]
...
[Central Directory: index of every entry]
[End of Central Directory record: ~22 bytes, at the very end]
```

Read that structure backwards and the design becomes obvious. The end-of-central-directory record sits at the **tail** and points back to the central directory, which points to each file's local header, which precedes that file's compressed data.

Why put the index at the end? **So you can append to an archive without rewriting it.** Add new entries after the existing data, then rewrite only the index at the tail. If the index lived at the front, adding one file would mean rewriting the entire archive.

It also explains something I'd noticed and never questioned: a zip can be *listed* almost instantly regardless of size, because listing only reads the tail. And it explains why a truncated download of a zip is completely unopenable rather than partially recoverable — losing the last 22 bytes loses the map to everything else.

---

## 3. DEFLATE — two ideas stacked

The compression is DEFLATE, the same algorithm inside gzip and PNG. It's two passes, and each one attacks a different kind of redundancy.

**Pass 1 — LZ77: repeated sequences.** Scan for byte sequences you've already seen and replace later occurrences with a back-reference: *(go back this far, copy this many bytes)*. In a mailbox file there are thousands of repetitions of `From:`, `Content-Type: multipart/mixed`, and MIME boundary strings. Each one after the first collapses to roughly a 3-byte pointer.

**Pass 2 — Huffman coding: uneven frequencies.** Assign shorter bit-codes to more frequent symbols. Common bytes and back-references get 4–6 bit codes; rare ones get 12–15. The classic insight: if `e` is far more common than `q`, spending the same 8 bits on both is waste.

The two are complementary in a way I found satisfying once I saw it. **LZ77 removes repetition across distance; Huffman removes imbalance in frequency.** Neither catches what the other does, and running them in that order matters — LZ77 first produces a stream of literals and back-references whose frequencies are *more* skewed than the original text, giving Huffman more to work with.

---

## 4. The number that told me what was in my file

My archive went 9.8 GB → 6.3 GB. **A 36% reduction.** Plain text usually compresses 60–80%.

That gap is diagnostic, and this is the part I'd have skipped past. Most of my archive was **base64-encoded email attachments.** Base64 packs 6 bits of data into every 8-bit character, producing a near-uniform distribution across a 64-character alphabet with almost no repeated long sequences.

That defeats both passes at once. LZ77 finds few repeats because the byte stream is effectively random. Huffman finds little imbalance because all 64 symbols appear about equally often. There's no structure left to exploit — the encoding already spent it.

So the compression ratio was *reporting the composition of the file*. The plain-text headers and bodies compressed well; the attachment payloads barely compressed at all, and the blended 36% is the weighted average.

The general lesson: **already-encoded or already-compressed data doesn't compress again.** Zipping a folder of JPEGs, MP4s, or another zip buys you almost nothing, because those formats already removed the redundancy. Compression ratio is a measurement of how much structure remains, and a low ratio isn't a failure — it's information.

---

## 5. What I took away

**Reading a file format's *layout* tells you its design priorities.** Index-at-the-tail is a decision in favour of cheap appends and cheap listing, at the cost of fragility if the tail is lost. I'd never have guessed that from using zip files for twenty years; it took thirty seconds of looking at the structure.

**A compression ratio is a measurement, not a score.** I'd been reading it as "how well did the compressor do." It's closer to "how much exploitable structure did this data have" — which makes a disappointing ratio a fact about your data rather than about your tool.

**The hesitation was the right instinct even though the answer was reassuring.** "Can I delete the original?" is exactly the class of question where a wrong assumption is unrecoverable, and where the cost of checking is one question.
