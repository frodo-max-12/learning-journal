# Why It's Called an "Embedding" — and Whether We Could Ever Talk in Latent Space

**Context:** I'd been using the word "embedding" for a while without asking why it's called that. The answer turned out to be a precise mathematical term rather than jargon — and once I had it, a much bigger question I'd been carrying about brain interfaces and shared "latent space" answered itself. The second question is a good test of whether you actually understood the first.

---

## 1. What an embedding does

A token is a discrete symbol — really just an integer id pointing into a vocabulary. The network can't do arithmetic on the symbol "cat," or on the id 8423. It *can* do arithmetic on a vector of real numbers.

So the embedding step converts symbols into the continuous, trainable form the rest of the model computes with: **discrete id in, dense vector out.**

---

## 2. Why that word

The name comes from the mathematical sense of *embedding*: **a map that places the points of one space inside another, larger space while preserving structure.**

You're taking a discrete set — a vocabulary of tens of thousands of tokens, points with **no inherent notion of distance or direction** — and embedding it into a continuous high-dimensional space, where distance and direction now *mean something*.

That's the whole justification for the term, and it's exact rather than metaphorical. Before the embedding, asking "how far is `cat` from `dog`?" is a meaningless question — they're two ids, and the fact that 8423 and 8424 are adjacent integers says nothing. After training, related tokens land near each other and directions capture relationships, so the **geometry carries semantic information the bare ids never had.**

The pairing that makes it stick: you *embed* a structureless set into a structured space, and the structure is what you gain.

---

## 3. Why it has to be learned

There's no obvious "correct" vector for "cat." Nobody can write one down.

So the model starts with **random vectors and adjusts them by gradient descent** until the positions are useful for predicting text. The embedding table isn't a designed lookup — it's a learned one, and the geometry is a *byproduct* of being good at the prediction task.

Which is the part I find genuinely surprising every time: nobody specified that related words should be near each other. That structure emerged because it's useful for prediction, and it turned out to be useful for a hundred other things too.

---

## 4. The question that tests all of it

Having understood that, I asked something I'd been wondering about separately: **could humans one day communicate directly in latent space through a neural interface?**

The romantic version — I think at you, you feel exactly what I feel — runs into an obstacle that no amount of hardware fixes:

> **There is no shared latent space between two brains.**

When a neural network has a latent space, **every copy of that network shares the same learned geometry**, so an embedding produced by one instance is meaningful to another. That's what makes vectors portable at all.

Brains aren't like that. My neural pattern for "dog" — which neurons, firing in what pattern — was shaped by my particular genetics and my particular life. Yours is different. **Piping my raw cortical activity into your head wouldn't read as "dog"; it would read as noise.** Each brain speaks a private code.

That's not a hardware limitation. It's a consequence of exactly the fact from §3: **the geometry is learned, so it's specific to the learner.** Two models trained separately don't share an embedding space either — you can't take a vector from one and feed it to another. The same fact that makes embeddings powerful within a system makes them non-transferable between systems.

---

## 5. What could work instead

Not direct transfer — **a learned bridge.** An AI intermediary that both people train against, mapping each person's idiosyncratic neural code to and from a common artificial latent space.

Which is less telepathy and more: *we each learn to speak a shared machine interlingua, and the machine translates in real time.* Plausible in principle, and still very hard.

There's also a hardware asymmetry worth knowing, separate from the representation problem: **reading neural activity is far easier than writing it.** Current interfaces decode motor intention — a user moving a cursor by way of spikes in motor cortex. Making someone *experience* a specific concept means precisely stimulating the right neurons to evoke that percept, and the state of the art there is crude, roughly at the level of producing dots of light.

The existing brain-to-brain demonstrations are real and tiny: a 2018 experiment linked three people via EEG and magnetic stimulation to cooperatively play a Tetris-like game, transmitting essentially **one bit** — rotate or don't. A genuine proof of concept, and nowhere near sharing a thought.

---

## 6. What I took away

**The word was doing precise work and I'd been reading it as jargon.** "Embedding" names a specific mathematical operation — placing a structureless set inside a structured space — and knowing that turns the technique from a trick into an instance of something general.

**Learned geometry is private geometry.** The same property that lets vectors from one model be compared meaningfully is what stops them meaning anything to a different model — or a different brain. Every "shared representation" claim should be checked against *shared by construction, or merely similar?*

**And the answer to a speculative question came from the definition.** I didn't need new facts about neuroscience to see the obstacle. I needed to notice that "latent space" means *this network's learned coordinate system*, and that two independently trained systems don't have the same one. The question dissolved into the definition, which is usually the sign that the definition was the thing worth learning.
