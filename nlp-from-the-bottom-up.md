# NLP From the Bottom Up — Seven Layers, Each Motivated by the Last One Failing

**Context:** I wanted to learn natural language processing properly, and asked for it built the way Nand2Tetris builds a computer — from the bottom, no black boxes. What came out was a ladder of seven steps where **each one exists because the previous one failed in a specific way.** That ordering is the entry; the individual facts are available anywhere, and the sequence is what made them stick.

---

## 0. Text is just numbers, and meaning isn't in the symbols

The starting point, which sounds trivial and isn't: a computer has no text. It has integers. `A` is 65 because a table says so.

The consequence is the whole problem statement of the field. **Nothing about the number 65 is more "A-like" than 66.** The symbol carries no meaning; meaning is entirely in the relationships between symbols and the world, and none of that survives the encoding.

So every layer above is an attempt to reconstruct, from statistics over symbols, something that behaves like the meaning the encoding threw away.

---

## 1. Tokenization — choosing the atoms

**The failure it addresses:** work character by character and each unit carries almost no meaning, so the model must learn everything from scratch. Work word by word and your vocabulary is unbounded — every typo, name, and inflection is a new word, and any word you didn't see in training is a hole.

**The fix:** subword tokenization. Common words stay whole; rare words shatter into reusable pieces.

Watching this run is what made it click. Feed it a sentence and you get something like:

```
token ##ization  makes  pre ##process ##ing  un ##break ##able
```

`makes` is common enough to stay intact. `tokenization`, `preprocessing`, and `unbreakable` fragment into pieces that recur across thousands of other words.

That's the resolution of the dilemma: **a fixed-size vocabulary that can still represent any string.** You never meet an unknown word, because worst case you spell it out of fragments.

And it explains behaviour I'd noticed and not understood — why models are sometimes strange about arithmetic, spelling, and rare proper nouns. Those are exactly the cases where the tokenizer's chosen atoms don't line up with the units the task actually operates on.

---

## 2. Embeddings — meaning becomes geometry

**The failure it addresses:** token IDs are still arbitrary. ID 4,821 is no closer to a synonym than to an unrelated word.

**The fix:** represent each token as a vector, positioned so that **distance means similarity**.

The demonstration that convinced me was vector arithmetic actually resolving:

```
king − man + woman  →  queen
paris − france + italy  →  rome
```

The second is the more interesting one, because it shows the geometry encoding a *relation* — "capital of" — as a **direction** rather than a location. Subtracting France from Paris isolates the capital-of relationship as a vector, and adding it to Italy walks you to Rome.

That's the reframe worth keeping: **meaning becomes geometry.** Not a lookup table of definitions, but a space where directions correspond to relationships. Once you accept that, similarity search, clustering, and retrieval stop being separate techniques and become "do geometry in this space."

---

## 3. One word, many meanings

**The failure:** a single fixed vector per word can't handle *bank* meaning riverside and *bank* meaning financial institution. The embedding has to be some blurry average of both, which is right for neither.

That minimal pair is the entire motivation for the next step. You don't need a complicated example — two sentences using one word differently, and a static embedding is stuck.

---

## 4. Attention — every word looks at every other

**The fix:** compute each word's representation *in context*, by letting every word attend to every other word and take a weighted blend.

The widget that made this concrete: a sentence containing "it," where flipping the final word changes what "it" refers to. Click "it," change `thirsty` to `fresh`, and watch the attention re-aim from *cat* to *milk* — real weights, recomputed.

Which is the whole idea in one observation. **The representation of "it" is not fixed. It's constructed from the sentence, so the same token gets a different vector in a different context.**

And it explains why attention costs what it does. Every word attending to every other word is quadratic in sequence length — that single design choice is the reason context windows are expensive, why long-context efficiency is a research area, and why the cost of doubling the input more than doubles.

---

## 5. Predicting the next token is the one task

**The unifying move:** translation, summarization, question answering, classification — all of them become *predict what comes next*.

The demo here was an honest n-gram model that had genuinely counted its corpus, so you could click a prediction, extend the sentence, and watch it **back off** to shorter context when it hadn't seen your prefix before.

Seeing a real n-gram model do this is a better introduction than starting from transformers, because you can see exactly where it fails: it has no notion of similarity between contexts. An unseen prefix is *unseen*, full stop — even if it's nearly identical to something in the corpus. Which is precisely the gap embeddings and attention fill, so the ladder closes on itself.

---

## 6. Scale — and the honest open question

**The bold conjecture:** to predict text well enough, at enough scale, you are *forced* to model the world the text describes. Compression approaches understanding. Prediction at scale isn't imitation of language, it's the acquisition of whatever the language encodes.

**The objection:** genuine knowledge growth is *creating new explanatory conjectures*, not interpolating within existing text. On this view a system trained to predict a corpus can recombine what's in it and cannot reach past it, however large it gets.

Nobody has settled which is right, and I'd rather have the tension than a confident answer. Both are live positions held by serious people, the disagreement is about mechanism rather than vocabulary, and it's the same fault line that runs under every argument about what these systems are.

---

## 7. Why the ordering was the lesson

Each rung exists because the previous one broke:

| step | what broke | what it forced |
|---|---|---|
| raw bytes | symbols carry no meaning | some representation of similarity |
| characters | too little meaning per unit | larger atoms |
| words | unbounded vocabulary, unknown words | subword tokenization |
| token IDs | arbitrary, no similarity structure | embeddings |
| static embeddings | one vector per word, ambiguity unresolved | context |
| context | how much should each word matter? | attention |
| a fixed task | too narrow to be general | next-token prediction as the universal task |

That's the same structure as everything else that's taught me anything: **the solution is only comprehensible after you've felt the failure it answers.** Presented as a list of techniques, NLP is seven arbitrary things to memorize. Presented as a chain of failures, each step is the obvious response to the previous one, and there's almost nothing left to remember.

---

## 8. What I took away

**Subword tokenization is a genuinely elegant compromise**, and it explains a whole class of odd model behaviour — arithmetic, spelling, rare names — as a mismatch between the atoms the tokenizer chose and the units the task needs.

**"Meaning becomes geometry" is the load-bearing idea.** Relations as directions, not just similarity as distance. Every retrieval and semantic-search system I've looked at is doing arithmetic in that space.

**Attention's cost is the direct consequence of its definition.** Everything attending to everything is quadratic. That isn't an implementation inefficiency to be optimized away; it's what the mechanism *is*, which is why long context is expensive in a way that won't simply be engineered out.
