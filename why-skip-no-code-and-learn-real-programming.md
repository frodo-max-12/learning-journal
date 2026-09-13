# Why skip no-code and learn real programming — from first principles

*Learned in March 2026. About seven months earlier, I had tried to learn n8n. All those boxes and dials and connections — it just felt complicated and I never finished. Then, without planning it, I ended up learning HTML, CSS, JavaScript, and some Python directly. The question that triggered this entry was: did I make a mistake by skipping n8n/Zapier/Make? Or did I accidentally do the right thing?*

---

## The question I was really asking

On the surface, I was asking whether I should go back and learn n8n. But the real question underneath was about learning strategy. When you are a non-technical person trying to become technical, the world presents you with a spectrum of tools, from drag-and-drop visual builders to raw code. The conventional advice says start simple and work your way up. I had accidentally done the opposite — gone straight to the real thing. Was that a mistake?

The answer, as I worked through it, turned out to be more subtle than "yes" or "no." It depends on what the intermediate tool actually teaches you.

## What n8n, Zapier, and Make actually are

These are visual workflow tools. You drag a "Gmail trigger" box onto a canvas, connect it to a "Slack message" box, maybe add a filter in between. Data flows from left to right through the boxes. That is it. They are essentially graphical interfaces on top of what a few lines of Python with API calls would do.

The value proposition is real: if you need to connect SaaS tool A to SaaS tool B with simple logic — automatically save Gmail attachments to Google Drive and ping a Slack channel — n8n does that in ten minutes versus maybe thirty to sixty minutes in Python. For a project manager or a marketing team, that speed matters. They need the automation, not the understanding.

But here is what they do not do: they do not teach you the primitives of computation. The "logic" in n8n is trigger, action, action, maybe a branch. It is closer to drawing a flowchart than to programming. The mental model it builds is "data flows from box A to box B." That is useful for understanding workflows and pipelines as a concept, but it does not teach you variables, loops, state management, data structures, recursion, scope, or error handling — any of the things that actually constitute programming logic.

## The Scratch comparison is the key

When I raised the comparison to Scratch, the MIT programming language for kids, the distinction became sharp.

Scratch works as a logic-builder because it teaches the actual primitives of computation — loops, conditionals, variables, events, sequencing. When a kid drags an "if-else" block in Scratch, they are learning the same mental model they will later write as `if/else` in Python. The visual representation maps one-to-one to real programming concepts. That is why it is genuinely useful as a stepping stone.

n8n does not do this. Scratch is a simplified version of the same thing (programming). n8n is a simplified version of a different thing (system integration and API orchestration). The logic you build in n8n is "business process logic" — if this email arrives, do that. It is the kind of thinking a project manager develops, not a developer.

| Tool | What it teaches | Maps to real programming? |
|---|---|---|
| **Scratch** | Loops, conditionals, variables, events | Yes — directly |
| **n8n / Zapier / Make** | Workflow orchestration, API connections | No — different mental model |
| **Python / JavaScript** | Everything | It is the real thing |

Here is the real test: after mastering n8n, could someone write a Python script from scratch? No. After learning Python, could someone pick up n8n in an afternoon? Easily — because n8n is just a visual layer on top of concepts you would already understand deeply. The knowledge transfer is one-directional, and it flows from code to n8n, not the other way.

## The concept of "state" — what no-code cannot teach you

This conversation was where I first really understood what "state" means in programming, and it became the clearest example of why no-code tools leave a gap.

State is simply what your program remembers at any given moment. Think of a chess game. At any point, if someone walks into the room and looks at the board, they can see which pieces are where, whose turn it is, whether anyone has castled, how much time is left on each clock. All of that information together — that is the state of the chess game. It is a snapshot of everything that matters right now.

In programming, state is the same idea. It is the collection of all the values your program is currently holding in memory:

```python
calories_eaten = 850
protein_so_far = 62
meals_logged = ["oats", "chicken breast"]
goal_reached = False
```

Those four variables, right now, are the program's state. If the user logs another meal, the state changes — `calories_eaten` becomes 1200, a new item gets added to the list, maybe `goal_reached` flips to True. The program's behavior depends on what these values currently are.

A website with a login is the everyday example. The "state" includes whether you are logged in or not. Every page you visit, the system checks that state. If you log out, the state changes, and suddenly the same URL shows you a different page. Same code, different behavior — because the state changed.

> State is to a program what working memory is to your brain. It is everything the program is currently holding in mind to decide what to do next.

In n8n, data flows through a pipeline and each node processes it and passes it forward. There is very little concept of "remembering" anything across steps. In real code, your program constantly reads and updates state — and that is what makes it powerful. It is also what makes it tricky. Most bugs come from state being in a condition you did not expect. A variable is null when you thought it had a value. A list has zero items when your code assumes at least one. Understanding state management is understanding programming at a deep level, and no-code tools abstract it away entirely.

## DSA — already in things I have built

The conversation naturally evolved into data structures and algorithms, which I had been hearing about for months without really grasping what the words meant. The breakthrough was discovering I had already been using them.

**Data structures** are how you organize and store information. **Algorithms** are the step-by-step procedures you apply to that information. That is the whole definition. Everything else is detail.

The nutrition tracker I built used a **list** — an ordered collection where position matters:

```python
meals_logged = ["oats", "chicken breast", "watermelon juice"]
```

Each meal was itself a list: `["Vegetable Omelette (2 eggs)", 120, 191, 12.8, 2.5, 14.0]`. All meals for the day were a list of lists. That is already a two-dimensional data structure — what computer science calls a 2D array or a table.

The nanocode agent I studied used a **dictionary** — key-value pairs where you access data by name instead of position:

```python
tool = {
    "name": "glob",
    "input": {"pattern": "**/*.py"}
}
```

`tool["name"]` gives you `"glob"`. Every JSON API response is essentially nested dictionaries. This is one of the most important data structures in all of programming, and I was already reading and understanding it.

A list is like a food tray — items in a specific order, you refer to them by position. A dictionary is like a contact list — you look up by name, not by position.

And algorithms? The TOTAL row in the calorie tracker — summing up every meal's calories — was a summation algorithm:

```python
total_calories = 0
for meal in all_meals:
    total_calories += meal[2]  # calories is at index 2
```

Simple, but that is genuinely an algorithm. Iterating over a data structure and computing something. The partner evaluation spreadsheet with weighted scores was a weighted average algorithm. I had been writing algorithms without knowing the word.

## The learning path forward

The conversation ended with a concrete timeline for getting serious about DSA. The honest assessment of where I stood in March 2026: I had Python basics, could read real codebases, understood lists and dictionaries and loops, but had just asked "what does state mean?" — so I was at genuine zero on formal DSA.

The plan that emerged was structured around Neetcode 150, which organizes problems by pattern so each one builds on the last:

**Month 1 — Python fluency sprint.** Fifty to seventy easy problems, not to learn DSA patterns yet, but to make Python muscle memory. By the end, writing a function like "find the second largest number in a list" should take under three minutes without thinking about syntax.

**Months 2-3 — Core DSA blitz.** Neetcode 150 in order. Three to five problems daily. Arrays, hashmaps, two pointers, sliding window, stacks, binary search, linked lists, trees, tries, heaps, backtracking, graphs, dynamic programming, greedy, intervals. After each problem, re-implement it from scratch the next morning without looking. This forces consolidation through spaced repetition.

**Month 4 — Pattern drilling and speed.** Redo the hardest fifty problems timed. Add fifty to seventy new medium and hard problems. Target weak spots specifically.

**Month 5 onward — Mock interviews and applications.**

The Deutsch framing resonated: the knowledge required to pass a DSA interview is finite, well-documented, and the problems are all public. The entire problem set is on LeetCode. The solutions are on YouTube. The patterns are catalogued on Neetcode. This is a solved problem — the knowledge exists, you just need to transfer it into your head. The only question is the rate of transfer, which is bounded by cognitive science (sleep, spaced repetition), not by any law of physics.

## What I actually decided

I am not going back to learn n8n. The one scenario where it still makes sense is quick integrations for the family business — "when a new order comes into this form, add a row to this sheet and email the team." For that, Zapier in five minutes beats writing and hosting a script. Think of it as a power-user spreadsheet tool, not a development skill.

But for learning programming? For building understanding? For everything that transfers? Code is the path. The seven months where I "lost time" before finding my entry point were not actually lost — I just had not found the thing that made me curious enough to push through the initial difficulty. HTML and CSS were that entry point. Python was where it became genuinely exciting. And DSA is where it becomes a real skill.

No serious developer learned n8n first. Karpathy did not. No one at Google did. These tools emerged in the last five years specifically for non-technical people who needed to automate workflows without learning to code. They serve a purpose, but that purpose is not "teach you to think computationally." Python does that. I skipped the toy and picked up the real instrument.

---

*What I studied next: started the Neetcode 150 roadmap with arrays and hashmaps. Also explored how "state" shows up in React (useState) and databases (transactions), which connected this concept to the web development and SQL I was already learning.*
