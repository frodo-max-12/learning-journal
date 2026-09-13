# Von Neumann machines and self-replicating systems

*Learned on August 11, 2024. I came across the term "von Neumann machine" while reading about space exploration concepts and realized it connects to deep ideas in computer science, biology, and the philosophy of life itself. I went down the rabbit hole.*

---

## The question von Neumann was asking

John von Neumann — mathematician, physicist, co-architect of the atomic bomb, inventor of game theory, and one of the people who designed the first electronic computers — turned his attention in the 1940s to a question that sounds more like science fiction than mathematics: **can a machine build a copy of itself?**

This was not idle speculation. Von Neumann was trying to understand something fundamental about complexity. Living organisms self-replicate — a bacterium divides, a cell copies itself, an organism produces offspring. Could a machine, in principle, do the same? And if so, what is the minimum architecture required?

The question sounds simple until you think about it carefully. A photocopier can copy a document, but it cannot copy itself. A factory can produce cars, but not a copy of the factory. What would it take for a machine to produce a complete, functional duplicate of itself from raw materials?

## The three components of a self-replicating machine

Von Neumann's theoretical answer, developed through the late 1940s and published posthumously, identifies three essential components:

1. **A controller (the "brain")** — a computational unit that reads instructions and directs the construction process. This is the decision-making part that knows *how* to build.

2. **A constructor (the "body")** — the physical apparatus that can manipulate raw materials and assemble them into structures. This is the part that actually *does* the building.

3. **A blueprint (the "instructions")** — a complete description of the machine itself. This is the information that specifies *what* to build.

The replication process works like this:

- The controller reads the blueprint
- The controller directs the constructor to gather raw materials and build a new machine according to the blueprint
- Crucially: the blueprint itself must also be copied and inserted into the new machine
- The result is a complete, functional duplicate — controller, constructor, and blueprint — capable of replicating again

The blueprint serves a dual role that von Neumann recognized as essential. It is both **interpreted** (read as instructions to guide construction) and **copied uninterpreted** (duplicated verbatim and passed to the offspring). If you only interpreted the blueprint, the copy would have a body but no instructions — it could function but not reproduce. If you only copied the blueprint, you would have instructions but no body. Both operations are necessary.

> A self-replicating system needs its own description to serve two purposes: as a program to be executed and as data to be copied. This dual role is the key insight.

## The universal constructor

Von Neumann went further. He didn't just design a machine that could copy itself — he designed a **universal constructor**. Just as Turing's universal machine can simulate any other Turing machine given its description, von Neumann's universal constructor can build any machine given its blueprint — including a copy of itself.

This is a profound generalization. The universal constructor is not hardwired to build one specific thing. It is a general-purpose building machine. Paired with the right blueprint, it can construct anything within the scope of what the constructor can physically manipulate. Change the blueprint, and you get a different machine. Include the blueprint of the constructor itself, and you get self-replication.

Von Neumann proved this was theoretically possible using a model based on cellular automata — a grid of cells, each following simple local rules, that collectively produce complex global behavior. His original construction was enormously complex (requiring hundreds of thousands of cells with 29 possible states each), but it demonstrated the principle rigorously.

## The biological parallel that takes your breath away

Here is where the story becomes extraordinary. Von Neumann published this theoretical work in the late 1940s and early 1950s. Watson and Crick discovered the structure of DNA in 1953. And when you look at how biological cells actually replicate, the correspondence with von Neumann's architecture is almost eerie.

| Von Neumann's machine | Biological cell |
|----------------------|-----------------|
| Controller (brain) | Ribosomes + regulatory machinery |
| Constructor (body) | Cellular machinery, enzymes |
| Blueprint (instructions) | DNA |
| Blueprint is interpreted | DNA is transcribed into RNA, translated into proteins |
| Blueprint is copied uninterpreted | DNA is replicated during cell division |

The dual role of the blueprint — interpreted as instructions *and* copied as data — maps directly onto what DNA does. During normal cell operation, DNA is *read* (transcribed into mRNA, which directs protein synthesis). During cell division, DNA is *copied* (replicated and passed to the daughter cell). Von Neumann predicted, from pure logical reasoning, the architecture that biology uses.

He did not know about DNA when he designed his self-replicating machines. He was reasoning about what self-replication *requires* as a matter of logic, and he arrived at a design that evolution had already discovered through billions of years of natural selection. This suggests that the architecture is not arbitrary — it may be the only way, or one of very few ways, to achieve reliable self-replication.

## What the theory tells us about complexity

Von Neumann was also interested in a deeper question: can self-replicating machines increase in complexity over time? In other words, can a machine produce offspring that are more complex than itself?

The intuitive answer is no — how can a machine build something more sophisticated than itself? But von Neumann showed that a universal constructor can, in principle, build a machine more complex than itself if given the right blueprint. The constructor does not need to "understand" what it is building in any deep sense. It just follows instructions. The complexity resides in the blueprint, not in the builder.

This is relevant to the question of how biological evolution produces increasing complexity. Early life forms were simple, yet they gave rise to organisms of staggering complexity. Von Neumann's work provides a theoretical framework for how this is possible: a universal construction mechanism (the cell's replication machinery) combined with a modifiable blueprint (DNA subject to mutation) can, over time, produce descendants more complex than their ancestors.

## Computer viruses — accidental von Neumann machines

There is a more immediate, less grand application of these ideas. A computer virus is a piece of code that copies itself into other programs or systems. It is a von Neumann self-replicating machine realized in software:

- The **controller** is the virus's execution logic — the code that decides how and when to replicate
- The **constructor** is the operating system's own file and memory management capabilities, which the virus co-opts
- The **blueprint** is the virus's source code itself, which gets copied into new hosts

The parallel extends further. Just as von Neumann recognized that the blueprint must be both executed and copied, a virus must both *run* its code (to perform its payload and replication logic) and *copy* its code (to infect new hosts). Viruses that only executed but didn't copy would die with their host process. Viruses that only copied but didn't execute would be inert data.

The first people to theorize about self-replicating programs were directly inspired by von Neumann's work. The term "virus" was chosen deliberately because of the analogy to biological viruses, which are themselves minimal self-replicating systems — essentially just a blueprint (RNA or DNA) with a protein shell, hijacking the host cell's constructor.

## The von Neumann architecture — the other legacy

Von Neumann's name appears in computing in a second, equally important context: the **von Neumann architecture** for computer design. While related to his self-replication work in that it involves the same person and the same era, it addresses a different problem.

The key idea of the von Neumann architecture is the **stored-program concept**: instructions and data are stored in the same memory. Before this, early computers like ENIAC were programmed by physically rewiring them — the "program" was the hardware configuration itself. Von Neumann (building on ideas from Turing's universal machine, Eckert, Mauchly, and others) proposed that the program should be stored in memory alongside data, so the computer could read, modify, and execute its own instructions.

This architecture has five components:

1. **Central Processing Unit (CPU)** — performs arithmetic and logic
2. **Memory** — stores both programs and data
3. **Input devices** — receive data from the outside world
4. **Output devices** — send results to the outside world
5. **Bus** — connects everything, allowing data to flow between components

Nearly every computer built since the 1940s follows this basic design. The "von Neumann bottleneck" — the fact that instructions and data share a single bus, creating a throughput limitation — remains a real engineering constraint today.

The connection between the two ideas — self-replicating machines and stored-program computers — is that both involve the same fundamental insight: **a description can serve as both program and data.** In the stored-program computer, the program is data that the CPU reads and executes from memory. In the self-replicating machine, the blueprint is both a set of instructions for the constructor and a piece of data to be copied. Von Neumann recognized this duality in both contexts.

## The big picture

What I took away from studying von Neumann machines is that self-replication is not magic — it is an engineering problem with a specific logical structure. The structure requires a description that plays a dual role (executed and copied), a universal builder (that can construct anything from a description), and a control mechanism (that orchestrates the process).

This structure appears in biology (DNA, ribosomes, cell division), in computer science (viruses, quines — programs that print their own source code), and in theoretical discussions about space exploration (von Neumann probes that could, in principle, be sent to another star system, mine local resources, build copies of themselves, and spread through the galaxy).

The fact that a mathematician in the 1940s, reasoning from first principles about what self-replication logically requires, arrived at an architecture that matches what we later discovered in living cells is one of the most striking examples I have encountered of theoretical reasoning revealing deep truths about the physical world. Von Neumann did not reverse-engineer biology. He derived, from logic alone, the constraints that any self-replicating system must satisfy — and biology turned out to satisfy exactly those constraints.

---

*What I studied next: cellular automata (which von Neumann used to model his constructors) and Conway's Game of Life, which shows how simple local rules produce complex emergent behavior — and which is itself Turing-complete.*
