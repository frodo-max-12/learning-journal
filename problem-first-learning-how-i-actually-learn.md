# Problem-First Learning — How I Actually Learn a Technical Subject

**Context:** I asked how networking is taught in a computer science degree, got a good answer, and then realized the answer wasn't going to work for me. So I described my own style instead — introduce the *problem* first, then show me why someone invented the thing that solved it. Stating that explicitly changed the recommendations completely, and it made me articulate a method I'd been using without naming. This entry is that method, with networking as the worked example.

---

## 1. How the subject is normally taught

Worth knowing, because it's what you'll get by default.

Most universities teach networking as **one core course plus a fan of electives**. The single foundational course — usually just "Computer Networks," taken in the third or fourth year — is where about 90% of a student's networking education happens, and it's remarkably standardized because it tracks the dominant textbooks. Everything after it (security, wireless, distributed systems, datacenter networking) is modular specialization.

The core course is organized around the protocol stack, and the one real pedagogical choice is **direction**:

- **Top-down** — start at the application layer, with the web and email that students already use, and descend toward the wire. Motivation-first, and now the dominant style.
- **Bottom-up** — start at the physical and link layer and build up.

Either way the content is the same ladder: fundamentals and layering → application (HTTP, DNS, sockets, CDNs) → transport (UDP, reliable delivery, TCP, congestion control) → network (IP addressing, subnetting, NAT, routing algorithms, BGP) → link (error detection, media access, Ethernet, ARP) → physical and wireless → cross-cutting security.

And the part that actually matters: **the labs are where the learning happens.** The recurring set is socket programming, packet capture and analysis, and — the important one — **implementing a reliable transport protocol from scratch over an unreliable one.** That last lab is the dividing line between knowing the vocabulary and understanding the subject. The best-regarded course in the field is famous precisely because its semester-long lab is *build a working TCP/IP stack.*

The canon is unusually stable, too. One accessible top-down textbook to *learn* from, one legendary byte-level reference to *understand* the wire, and a free systems-tradeoffs book as a third perspective — that pairing is what most engineers credit.

---

## 2. Why that wasn't going to work for me

None of it is bad. It just doesn't match how I actually absorb things, and I know that because I've measured it against a case where learning worked unusually well.

I watched an entire computer-science video series and loved every episode. When I asked myself *why*, the answer was specific:

> She introduces the **problem** first, then the invention that solved it.

The example I gave: switches. Without switches, everyone transmitting to everyone else causes congestion and collisions — *therefore* switches were invented. The device is introduced as **the answer to a difficulty you have already felt.**

Compare the default: "A switch is a layer-2 device that forwards frames based on MAC addresses, maintaining a forwarding table populated by learning source addresses." Every word true. Nothing in it tells you why anyone bothered.

Saying that out loud changed the recommendations entirely, and pointed at a series that derives an entire network from scratch, where every step asks *"okay, this creates a new problem — how do we solve it?"* The arc runs: send a bit over a wire → but how does the receiver know where bits start? → but how do two machines address each other? → but what if both transmit at once? → and so on, up through addressing, routing, and reliable delivery.

**Each invention exists because the previous step created a problem.** That's a curriculum ordered by *necessity* rather than by layer.

---

## 3. Why problem-first works, stated properly

I don't think this is only a preference, and I'd want to defend it as more than taste.

**It supplies the thing memory needs.** A definition is an isolated fact. A problem-and-solution pair is a *relationship*, and it comes with a reason attached. I don't have to remember what a switch is; I have to remember that shared media collide, and the switch follows.

**It makes the design space visible.** If you're told the answer first, you never see the alternatives. If you feel the problem first, you naturally ask *"couldn't we have done it differently?"* — and that question is where the actual engineering lives. Almost every entry in this journal that taught me something has that shape: the interesting content was in the trade-off, and the trade-off is invisible unless you know what was being traded against.

**It gives you a test for whether you understood.** If I can state the problem a thing solves, I understand it. If I can only state what it *is*, I've memorized a definition. That's a check I can run on myself, which definition-first learning doesn't offer.

**And it protects against the biggest failure mode of learning with an AI assistant**, which is getting an answer before you've felt the question. It's very easy to accumulate correct explanations of things you never needed explained. Problem-first is the discipline that keeps the answers attached to something.

---

## 4. The corollaries I actually run

**Break the thing before reading about the fix.** The most useful learning I've done this year came from making a method fail on purpose — starving an evaluation until it lied about its own result, or removing a property from an environment until a simple approach collapsed. Meeting the solution *after* the failure means the solution has somewhere to attach. Meeting it before means memorizing.

**Follow the pushback.** A surprising number of the things I actually learned started with "wait, that doesn't sound right" — *static RAM shouldn't leak*, *why store file versions on disk when the model has them*, *surely this is memory as well as time*. Roughly half the time I was wrong in an informative way, and the other half the explanation was imprecise. Both outcomes beat accepting the first answer.

**Prefer the source that was there.** Reading the original paper, the actual repository, or the raw file format beats reading a summary. Summaries are compressions made for someone else's purposes, and the detail they dropped is often the detail I needed.

**Compute the ground truth when you can.** Where a small exact answer is available — a solver, an arithmetic check — get it, and check the impressive method against it. Almost every genuine finding I've had came from having a number to disagree with.

**Say what you already know.** The single highest-leverage input in that networking exchange was one paragraph describing how I learn. It changed the recommendation more than any follow-up question would have. When working with someone — or something — that adapts, describing your own state is worth more than asking a better question.

---

## 5. What I'd tell someone doing the same thing

Take the standard curriculum as a **map, not a route**. It tells you what the territory contains and roughly how experts carve it up, which is genuinely valuable — I now know what a networking course covers and which textbook does what. But the *order* it proposes is optimized for a lecture hall with a fixed schedule and no ability to answer individual questions, and I have none of those constraints.

So: use the syllabus to know what exists, then learn it in the order your own questions generate — and do the lab. In every subject there's one exercise that separates vocabulary from understanding. For networking it's implementing reliable transport yourself. Find that exercise and do it, even if you skip half the syllabus around it.

The thing I'd most want to preserve from all of this is smaller than a method: **the failures are the curriculum.** Every entry in this journal that I'd defend came from something not working — a claim that didn't survive checking, an intuition that turned out to be a definition that had aged, a method that collapsed when I removed one of its assumptions. The polished explanation was never the point. It was the thing that broke on the way there.
