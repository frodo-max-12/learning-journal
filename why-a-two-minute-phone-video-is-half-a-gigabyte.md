# Why a Two-Minute Phone Video Is Half a Gigabyte

**Context:** A 1 minute 54 second video off my phone was **511 MB**. A video of that length on a streaming site is typically 30–60 MB, and my only known method for shrinking it was to upload it and download it back. That felt obviously wrong as a technique, so I asked what was actually going on. The answer is a single number I'd never thought about, and the fix is better than the round-trip on every axis.

---

## 1. The one number: bitrate

File size for video is almost entirely:

```
size ≈ bitrate × duration
```

Resolution, frame rate, and codec all matter only through their effect on the bitrate needed for a given quality. **Bitrate is the thing.**

My phone records 4K HDR at roughly **37.5 megabits per second**. Multiply by 114 seconds and you get 511 MB. There's no mystery — the camera was told to spend that many bits per second and it did.

The real question is *why so many*, and the answer is a deliberate design decision: **that bitrate exists to give editing headroom, not viewing quality.** It's about four times more than you need to *watch* the footage. The extra bits survive colour grading, cropping, stabilization, and re-encoding without accumulating visible artefacts. A phone camera is recording a master, not a deliverable.

Which reframes the comparison I'd started with. A streaming site's 40 MB version isn't a compression miracle. It's the *same footage encoded for viewing rather than editing*, and I was comparing a master to a delivery copy and concluding my file was broken.

---

## 2. What I did instead of the round-trip

Re-encoding locally, using the machine's hardware video encoder:

| version | bitrate | size | reduction |
|---|---|---|---|
| original (as recorded) | 37.5 Mbps | 511 MB | — |
| 4K, re-encoded | 10 Mbps | 141 MB | 3.6× |
| 1080p | 3.5 Mbps | 52 MB | 10× |

Audio copied untouched — no reason to re-encode it, and re-encoding audio is pure quality loss for negligible space.

The whole thing took well under a minute, because the encode ran on **dedicated video-encoding silicon** rather than general-purpose cores. That's a nice concrete instance of specialized hardware: modern chips include a fixed-function block that does one job, and it's why a phone can record 4K without melting.

---

## 3. Why local beats the upload round-trip on every axis

I'd assumed the round-trip was a clever hack. It's worse in four distinct ways:

- **It's a second compression on top of the first.** The platform re-encodes your upload with its own settings; you get *their* trade-off, applied to an already-lossy file, and generation loss accumulates.
- **HDR usually doesn't survive.** Re-downloads are typically standard-range 8-bit. The wide-colour, 10-bit information the phone captured is gone.
- **You upload a personal video to a third party** to perform a transformation that runs locally in thirty seconds.
- **You don't control the quality**, and you can't tune it.

The generalizable version: **when your workaround for a local problem routes through someone else's servers, check whether the local tool exists.** It usually does, it's usually faster, and the round-trip usually degrades something you weren't tracking.

---

## 4. The metadata that has to survive, and how it's checked

The part I'd have got wrong doing this myself is that a video file is not just pixels. It carries:

- **Colour information** — the HDR transfer characteristics and colour space. Drop these tags and the file plays back washed out or oversaturated, because the player no longer knows how to interpret the values.
- **Orientation** — portrait footage is often stored as landscape with a rotation flag. Lose it and your video is sideways.
- **Creation metadata** — timestamps that keep the file sorted correctly in a photo library.
- **A flag that moves the index to the front of the file**, so it starts playing before it's fully downloaded rather than after.

That last one is the same design idea as a zip archive's index placement, inverted. A zip puts its index at the tail because appending matters more than streaming. A video for streaming puts its index at the head because starting playback early matters more than appending. **Same structural decision, opposite answer, both correct for their use case.**

And the verification approach was worth as much as the compression. Rather than eyeballing it: extract matching frames from original and compressed, confirm identical frame counts, and compute an objective similarity measure between them. That catches a real failure mode — a re-encode that silently drops or shifts frames looks fine on casual inspection and is unrecoverable later.

There's a small honest note in that process too: something that *looked* like a frame mismatch turned out to be an artefact of the small comparison thumbnail, and only the objective check settled it. Which is the same lesson as every other measurement in this journal — **compute the number rather than trusting the picture.**

---

## 5. 4K or 1080p?

The genuinely practical question at the end. The answer depends on the screen, and the arithmetic is unforgiving: on a phone display, 4K and 1080p are essentially indistinguishable at normal viewing distance, because the eye can't resolve the extra pixels at that size and distance.

So the rule I settled on: **keep 4K if the footage might be edited or shown on a large display; keep 1080p if it's going to be watched on phones and sent to people.** A 10× size difference for a distinction most viewers can't perceive is an easy trade in most cases — and the 4K re-encode at 141 MB is still there as the archival copy if the answer is "both."

---

## 6. What I took away

**File size questions are bitrate questions.** Once I had `size ≈ bitrate × duration`, everything else — why phone video is huge, why streaming files are small, what a "quality setting" does — became one parameter rather than a set of unrelated facts.

**Recording settings optimize for editing; delivery settings optimize for viewing.** They're different jobs with different correct answers, and comparing a master to a delivery copy is a category error I'd been making without noticing.

**Verify a lossy transformation objectively.** Frame counts and a computed similarity metric catch failures that look fine. The transformation is irreversible, so the check has to happen before you delete the original — which is exactly the situation where it's most tempting to skip it.
