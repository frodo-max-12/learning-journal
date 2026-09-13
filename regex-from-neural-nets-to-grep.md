# Regex — From Neural Nets to `grep`, and Why Cmd-F Isn't Using It

**Context:** I'd been using regular expressions without knowing where they came from, and three questions had been quietly bothering me. Is regex actually part of computer science, or just a tool people picked up? What's the difference between `grep` and regex — I'd been using the words interchangeably. And when I hit Cmd-F in a PDF or a browser, is that regex underneath? The answers were more interesting than I expected, and I was wrong about the third one.

---

## 1. It was invented for neural networks, in 1951

Regular expressions were invented by **Stephen Kleene in 1951**, in a paper titled *"Representation of Events in Nerve Nets and Finite Automata."*

He wasn't building a text-search tool. He was working on McCulloch–Pitts neurons — an early mathematical model of neural computation — and needed a notation for **which sets of input strings a finite automaton can recognize.** He called those sets "regular events." That's where the term *regular expression* comes from, and the `*` operator is the **Kleene star**, named after him.

So the origin is pure theory: characterizing the computational power of finite-state machines. No software, no text processing, no files. Mathematics on paper about what a machine with finite memory can and cannot recognize.

That reframes the answer to "is regex part of computer science?" more strongly than I expected. **Regex isn't a tool that theory later explained — it's a piece of theory that later escaped into tooling.** It sits inside automata theory as the notation for the bottom rung of the Chomsky hierarchy: regular languages are exactly the languages a finite automaton can recognize, and regular expressions are exactly the notation for them.

Which also explains the most notorious practical fact about regex — **you can't parse HTML with it.** That's not a limitation of any implementation. Balanced nesting requires unbounded counting, a finite-state machine has no counter, and regular languages therefore cannot express it. The limitation is a theorem from 1951, not a bug from 1998.

---

## 2. How it reached computing — and where `grep` gets its name

**Ken Thompson brought it to computing in 1968**, publishing a regular-expression search algorithm and implementing regex matching in the QED editor, then in `ed`.

And this is the piece that made me laugh. In `ed` you could type:

```
g/re/p
```

meaning **g**lobally search for a **r**egular **e**xpression and **p**rint the matching lines. That command was used so constantly it was pulled out into its own standalone program.

**That's literally where the name `grep` comes from.** It's a command sequence that became a verb.

So the answer to "what's the difference between grep and regex" is now obvious rather than confusing: **regex is the notation; `grep` is one program that reads that notation and applies it to lines of text.** Regex is the language, grep is one of thousands of tools that speak it.

The lineage from there is worth having, because it explains why regex syntax varies between tools: a DFA-based `egrep` for faster matching; a portable C library in 1986 that got copied everywhere; Perl in the late 80s aggressively extending the syntax with backreferences, lookarounds, and non-greedy quantifiers — which is where most "modern" regex syntax comes from; that engine extracted into a standalone library in 1997 that now backs a large share of the tools you use; and a deliberate counter-movement in 2010 rejecting backtracking to guarantee linear time.

---

## 3. The split that actually matters: two ways to implement it

Those last two entries aren't just history. There are **two fundamentally different implementation strategies**, and the difference has bitten the entire internet.

| approach | how it works | worst case | features |
|---|---|---|---|
| **NFA simulation** (Thompson) | compile to an automaton, simulate all reachable states in parallel | linear in input length, always | no backreferences or lookarounds |
| **Backtracking** (Perl-family) | try one path; on failure, back up and try another | can blow up exponentially | full feature set |

The trade-off is real and unavoidable: **the automaton approach is provably fast but feature-limited; backtracking is feature-rich but a denial-of-service risk.**

The canonical demonstration is the pattern `^(a+)+$` matched against a string of a's ending in one `X`. The automaton engine handles it in microseconds. A backtracking engine takes *minutes* on the same short input, because it tries every way of partitioning the a's before concluding failure. Same regex, same input, wildly different outcomes — and this class of bug, catastrophic backtracking, has taken down major internet infrastructure.

Which tells you something practical: **when a regex runs on untrusted input, the engine's implementation strategy is a security property**, not an implementation detail. The engines that guarantee linear time do so by refusing to support backreferences, because backreferences are exactly what pushes the pattern outside regular languages — and once you're outside, the automaton guarantee is gone.

As for "is it written in C?" — historically yes, almost universally, and today it's mixed. The Perl-family backtracking engines are nearly all C. The linear-time engines are C++ and Rust. When you call a regex function in Python you're calling into a C extension; in a browser you're in C++; in `grep` you're in C; in the modern fast search tools you're in Rust.

---

## 4. Cmd-F is not regex — and the reason is interesting

I assumed find-in-page was regex with the syntax hidden. **It's not, almost anywhere.** It's literal substring search with Unicode handling on top.

**In a browser**, find-in-page does Unicode normalization and case folding — so that `café` with a precomposed accent matches `café` with a combining accent — then runs an ordinary substring search, plus DOM walking to visit visible text in document order and skip hidden elements and scripts. There's no regex engine involved. Type `.*` into the find bar and it looks for those three literal characters. That's a test you can run in five seconds, and I did.

**In a PDF, there's a wrinkle that explains a lot of everyday frustration.** A PDF doesn't store text as text. It stores drawing commands — *place glyph #42 at coordinates (305, 700)*. So before searching, the viewer must **reconstruct** a character stream:

1. walk the content stream collecting glyph-and-position tuples,
2. map glyphs to Unicode using the font's embedded table,
3. sort into reading order and infer word and line breaks from coordinate gaps,
4. build a string per page,
5. substring search on that,
6. map matched indices *back* to glyph bounding boxes to draw the highlight.

That pipeline is why Cmd-F sometimes fails on text that's plainly visible: the glyph-to-Unicode table was missing, ligatures weren't decomposed, or a multi-column layout confused the reading-order heuristic. And a scanned PDF with no text layer matches nothing at all, because there are no characters — only pixels.

**In text editors** it varies: simple editors do literal substring search; programmer's editors default to literal with a regex toggle; command-line search tools are regex by default. The pattern across all of them is consistent — **regex is opt-in, literal is the default** — because the overwhelmingly common case is looking for a word, and in a literal search a `.` means a period.

---

## 5. What I took away

**"Where did this come from?" is a genuinely good debugging question.** Knowing regex began as a description of finite automata explains its power *and* its ceiling in one stroke, and turns "you can't parse HTML with regex" from folklore into a theorem.

**Names carry history.** `grep` is a command sequence that became a program. `*` is somebody's surname. Neither is arbitrary, and both were opaque to me until I asked.

**Check assumptions that are cheap to check.** I'd carried "Cmd-F is regex underneath" for years. Testing it took typing two characters into a find bar. The number of beliefs I hold that are one five-second experiment away from being corrected is probably not small.
