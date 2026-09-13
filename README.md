# Learning Journal - Computer Science from First Principles

I'm teaching myself computer science from first principles, and documenting it as I go.

Every entry in this journal starts from "what is this, actually?" and builds up from there. I don't memorize - I try to understand *why* things work the way they do.

**Start here:** [Problem-First Learning - How I Actually Learn a Technical Subject](problem-first-learning-how-i-actually-learn.md) - the method behind every entry below: meet the problem before the solution, break things on purpose, follow the pushback, and compute the ground truth whenever a small exact answer is available.

---

## Computer Architecture & Hardware

How computers actually work - from transistors to memory hierarchies to what's physically inside a GPU.

- [Why CPU, RAM, and Storage Exist](computer-architecture-why-cpu-ram-and-storage-exist.md) - the speed mismatch problem, SRAM vs DRAM at circuit level, automata theory
- [Compilers vs Interpreters - How Code Becomes Machine Instructions](compilers-vs-interpreters-how-code-becomes-machine-instructions.md) - what happens between `print("hello")` and the CPU executing it
- [OS, Hardware, Processes, and the CS Curriculum](cs-big-picture-os-hardware-processes-turing-curriculum.md) - subprocess, fork/exec, Activity Monitor, the M5 chip, Turing's universality
- [HBM and AI Accelerators - What's Inside a GPU Package](hbm-and-ai-accelerators-whats-inside-a-gpu-package.md) - Blackwell internals, HBM stacks, why Nvidia captures more value than memory makers
- [Why Circuits Need Discrete Components Alongside Chips](why-circuits-need-discrete-components-alongside-chips.md) - CMOS logic, parasitic capacitance, decoupling capacitors, ESD protection
- [What "Compute" Actually Means - From Physical Servers to EC2](what-compute-actually-means-from-physical-servers-to-ec2.md) - what is physically happening in a cloud server, virtualisation, hypervisors, what a CPU actually does
- [Inside a 74181 ALU - From Schematic to Silicon](inside-a-74181-alu-from-schematic-to-silicon.md) - package vs die vs schematic vs layout, bipolar transistors, bond wires, how a block diagram becomes a 2D city on silicon
- [Why SRAM Costs 1000× More Than DRAM](why-sram-costs-1000x-more-than-dram.md) - the vertical capacitor that makes DRAM dense, why the two are made in incompatible fabs, the per-wafer cost arithmetic, and the two entirely different phenomena both called "leakage"
- [Wafer-Scale Computing - Why Nvidia Doesn't Just Build One Big Chip](wafer-scale-computing-why-nvidia-doesnt-build-one-big-chip.md) - defeating yield with homogeneity and redundancy, the reticle limit as a physical wall, why binning is worth more than it looks, and how the rack became the new wafer
- [Mainframes - Scale-Up in a Scale-Out World](mainframes-scale-up-in-a-scale-out-world.md) - hardware redundancy in one box vs software resilience across many cheap ones, why the cloud is the mainframe's architectural opposite rather than its descendant, and why elasticity is the product you're actually buying
- [The Memory Hierarchy - From Registers to Spinning Disks](the-memory-hierarchy-from-registers-to-spinning-disks.md) - the forty-million-fold span from register to disk seek, why cache is hardware-managed and registers aren't, the floating-gate trick that makes flash non-volatile, and why a machine with a fast SSD still needs a small NOR chip to boot
- [EEPROM and the Lineage of Rewritable Memory](eeprom-and-the-lineage-of-rewritable-memory.md) - mask ROM to PROM to the UV-erasable chip with a quartz window to electrical erasure, why one tunneling mechanism explains non-volatility and wear and slow writes together, and why flash is EEPROM's child rather than its replacement

## Theory of Computation

The foundational ideas of CS - what computation is, what's computable, and why it matters.

- [Turing, Church, and the Halting Problem](theory-of-computation-turing-church-and-the-halting-problem.md) - the Entscheidungsproblem, Turing machines, lambda calculus, what "computable" means
- [Turing's 1936 Paper, Deutsch's Lens, and Classifying ICs as Universal or Not](turings-1936-paper-deutsch-lens-universality-threshold-and-classifying-ics-as-universal-or-not.md) - reading the original paper, Deutsch's universality-as-physics reframing, which real-world ICs are universal, why GPUs exist if CPUs are also universal
- [Von Neumann Machines and Self-Replicating Systems](von-neumann-machines-and-self-replicating-systems.md) - universal constructors, the DNA parallel, self-replicating code
- [Bayesian Reasoning - Why 99% Accurate Doesn't Mean What You Think](bayesian-reasoning-why-99-percent-accurate-doesnt-mean-what-you-think.md) - base rates, Bayes' theorem, updating beliefs with evidence
- [What Computation Actually Is](what-computation-actually-is.md) - implication becoming physical, the two-layer lock between mechanism and meaning, universality as a generic property of rule-systems
- [State - The Concept Behind All of Computing](state-the-concept-behind-all-of-computing.md) - what "state" actually is, why every system from a counter to a database to a neural net has it, how state is the substrate that makes computation visible
- [The Dominoes-Adder Paradox - Determined vs Known](the-dominoes-adder-paradox-determined-vs-known.md) - the gap between logically determined and epistemically available, computational irreducibility, why running rules is genuinely productive work
- [Deutsch on Free Will and Universal Explainers](deutsch-on-free-will-and-universal-explainers.md) - agency caused by reasons, knowledge creation as unpredictable in principle, locally narrow / globally universal
- [You Are the Program, Not the Computer](you-are-the-program-not-the-computer.md) - identity as pattern, atom replacement, self-modifying programs, identity as verb not noun
- [Identity, Copies, Uploads, and the Fork Problem](identity-copies-uploads-and-the-fork-problem.md) - qualitative vs numerical sameness, gradual-replacement argument, Parfit on continuity without privilege
- [The Four Strands of *The Fabric of Reality*](the-four-strands-of-the-fabric-of-reality.md) - quantum, computation, evolution, epistemology - why each is irreducible and the cloth needs all four
- [Physics and Computation - Locked, Not Nested](physics-and-computation-locked-not-nested.md) - Landauer's principle, Church-Turing-Deutsch, layered honesty about what "physics requires computation" actually means
- [The Physical Limits of Computation](the-physical-limits-of-computation.md) - Lloyd's ultimate laptop, why the speed bound comes from energy and the memory bound from surface area, why the memory bound bites first, and Tipler's Omega Point as the one fully specified escape
- [Wolfram vs Deutsch - Is Universality a Ceiling or a Doorway?](wolfram-vs-deutsch-a-ceiling-or-a-doorway.md) - same theorem, opposite conclusions; the flat region above the line vs the jump to universality; where the disagreement becomes technical rather than temperamental; and why irreducibility and explicability may not be the same axis
- [Popper - On the Sources of Knowledge and of Ignorance](popper-on-the-sources-of-knowledge-and-of-ignorance.md) - how empiricism and rationalism share the premise worth attacking, why manifest truth breeds a conspiracy theory of ignorance, the regress that kills justification by source, and replacing "what are the best sources?" with "how do we detect error?"
- [Universal Explainers vs Universal Turing Machines](universal-explainers-vs-universal-turing-machines.md) - a universal executor vs a universal creator of knowledge, jumps to universality as one repeated structure, why the substrate has been solved since 1936 and the program hasn't, and which half is a theorem and which a conjecture
- [Wealth as a Repertoire of Physical Transformations](wealth-as-a-repertoire-of-physical-transformations.md) - wealth as capacity rather than stockpile, why knowledge is the binding constraint, non-rivalry as the reason the frontier stays scarce, and what agents compete over once transformations are cheap
- [Information, Knowledge, Explanatory Knowledge](information-knowledge-explanatory-knowledge.md) - three nested circles with a criterion at each boundary, why a gene is knowledge but not explanatory knowledge, hard-to-vary as the innermost ring, and where language models sit on the map

## AI & Machine Learning

Understanding how modern AI systems actually work - not just using them, but knowing what's inside.

- [How Transformers Work - Attention Is All You Need](how-transformers-work-attention-is-all-you-need.md) - self-attention, parallel processing vs sequential generation, "lost in the middle"
- [Model Distillation - How Small Models Learn from Big Ones](model-distillation-how-small-models-learn-from-big-ones.md) - soft labels, temperature scaling, the DeepSeek controversy
- [Neurosymbolic AI - Type 1 vs Type 2 Abstraction](neurosymbolic-ai-type1-vs-type2-abstraction.md) - Chollet's framework, neural vs symbolic, "never let Type 1 make a financial decision"
- [Chollet's Case Against Intelligence Explosion](chollets-case-against-intelligence-explosion.md) - No Free Lunch theorem, diminishing returns of recursive self-improvement
- [Training vs Inference - The Economics of AI Compute](training-vs-inference-the-economics-of-ai-compute.md) - why labs that don't own silicon eventually run out of money, why chip generations split into separate training and inference designs
- [Headless Browsers and AI-Agent Browsing](headless-browsers-and-ai-agent-browsing.md) - what a browser actually does (7-layer stack), what "headless" means, why Lightpanda exists, why Browser Use / Stagehand need an LLM API key
- [Landscape of AI Browser Agents](landscape-of-ai-browser-agents.md) - five categories, 40+ projects mapped, where SDK frameworks / purpose-built browsers / MCP servers / computer-use agents / vision overlays each fit in the stack
- [Building a Local NotebookLM - Semantic Search From Scratch](building-a-local-notebooklm-semantic-search-from-scratch.md) - chunking books with overlap, embeddings as meaning-geometry, why SQLite + a numpy matrix is the entire database, and the one matrix multiply that *is* the search engine
- [RAG vs Long Context - The Economics of Retrieval](rag-vs-long-context-the-economics-of-retrieval.md) - what loading a whole library into a million-token window costs per question, prompt-cache economics, and how the failure modes swap instead of disappearing
- [Local Models with Ollama, Hooks, and the Plugin I Uninstalled](local-models-with-ollama-hooks-and-the-plugin-i-uninstalled.md) - what 12B parameters actually costs in RAM, why quantization is what makes local inference possible at all, unified memory and the cold-start tax, Claude Code hooks vs CLAUDE.md vs skills vs plugins, and the free/private/no-local-load trilemma that killed the tool
- [The Bitter Lesson - Search and Learning as Compute Pumps](the-bitter-lesson-search-and-learning-as-compute-pumps.md) - what "scales with computation" actually means, search paying at decision time vs learning paying in advance, and why "scale is all you need" is a weaker claim than the essay makes
- [Pretraining, SFT, RLHF, RLVR - the Four Stages](the-training-pipeline-pretraining-sft-rlhf-rlvr.md) - what each stage deposits and what it costs, why you can't fine-tune in knowledge that wasn't pretrained in, and reading the coding-agent capability cliff as a map of which stage ran out
- [Why Generating a Token Is a Memory Problem, Not a Compute Problem](why-generating-a-token-is-a-memory-problem-not-a-compute-problem.md) - capacity vs bandwidth vs compute, the 300x gap between moving the weights and multiplying them, why quantization's real win is bytes-per-token, and why batching is nearly free
- [NLP From the Bottom Up](nlp-from-the-bottom-up.md) - seven layers where each exists because the previous one broke: subword tokenization, meaning as geometry, why attention is quadratic by definition, and the honest open question at the top
- [ML, Deep Learning, and RL - Three Words That Cut Along Different Axes](ml-deep-learning-and-rl-three-words-different-axes.md) - a field, a method, and a problem setup mistaken for three siblings; why "deep RL" is a compound of two independent choices; and why boosted trees still win on tabular data
- [Why It's Called an "Embedding" - and the Latent Space Question](why-its-called-an-embedding-and-the-latent-space-question.md) - embedding as the mathematical act of placing a structureless set inside a structured space, why the geometry has to be learned, and why two brains have no shared latent space to talk in
- [Q, K, V - Attention as a Matching Engine](q-k-v-attention-as-a-matching-engine.md) - reading attention as retrieval with soft weights, why softmax is what makes matching learnable, what the scaling factor is protecting, and the architecture diagram as a menu rather than a model
- [What's Actually in a Modern GPT Training Script](whats-actually-in-a-modern-gpt-training-script.md) - the gap between the 2017 paper and shipped code: RMSNorm, grouped-query attention, RoPE, QK-norm and sliding windows, each a fix for a named failure, and how much of "architecture" turns out to be memory-movement optimization
- [A Global Workspace in a Model, and Deutsch's Three Kinds of Ideas](a-global-workspace-in-a-model-and-deutschs-three-kinds-of-ideas.md) - mapping an interpretability result onto explicit / conscious-inexplicit / unconscious ideas, why later-verbalizable isn't the same as explicit, gradient descent as error correction on unconscious structure, and the visible reasoning trace as the only channel available

## Reinforcement Learning

Learning by trial and reward - worked from tabular algorithms upward, with the textbook results checked against exact solvers rather than taken on trust.

- [Why Reinforcement Learning Exists - What Random Search on CartPole Taught Me](why-reinforcement-learning-exists-random-search-on-cartpole.md) - 200 blind guesses beating a hand-written controller, the policy as a knife cutting state space, the winner's curse, and the three gifts CartPole gives you that every real problem takes away
- [Q-Learning vs SARSA - and the Textbook Figure That's Partly an Artifact](q-learning-vs-sarsa-and-the-textbook-figure-thats-partly-an-artifact.md) - the one line separating on-policy from off-policy, a DP solver as ground truth, why an agent can't un-learn a fear it no longer tests, and four bugs that produce a plausible learning curve instead of a crash
- [Value Functions - and Why Every Symbol in the Equation Has to Be There](value-functions-and-why-discounting-has-to-be-there.md) - the value function as NPV, the three jobs γ is doing at once, the 1/(1−γ) planning horizon, and why states have no value without a policy attached
- [How a Value Seeps Backward - TD Learning Through Tic-Tac-Toe](how-a-value-seeps-backward-td-learning-through-tic-tac-toe.md) - simulating the update by hand, why game 1 changes exactly one number, afterstates, and watching a table know it has won several moves before it has
- [Bandits, Exploration vs Exploitation, and Deutsch's Objection](bandits-exploration-vs-exploitation-and-deutschs-objection.md) - bandits as RL with the sequential part removed, regret and Thompson sampling, a medieval Italian legal procedure hiding in the name, and why the fixed option set is the assumption doing all the work
- [Does RLVR Count as "Learning from Experience"?](does-rlvr-count-as-learning-from-experience.md) - why the human-data/experience split isn't where I thought it was, design time vs runtime as the real gap, and the two dual failures of gradient descent (catastrophic forgetting and loss of plasticity) that make continual learning unsolved
- [Where Reward Comes From in Evolution](where-reward-comes-from-in-evolution.md) - three different things bundled as "reward", why a bacterium following a gradient isn't learning, the 302-neuron worm that is, and why a deployed model sits on the bacterium's side of that line

## AI Agent Craft

How agents are actually built - the loop, what persists to disk, what autonomy means, and what the context window really costs.

- [What a Harness Actually Is - the Model Has No Hands](what-a-harness-actually-is.md) - the model as a stateless function, the whole agent loop in ~40 lines, harness vs agent vs model (the swap test and the repo test), and why "harness" comes from software testing while "agent" comes from economics
- [Is Cron the Only Way to Make an Agent Autonomous?](is-cron-the-only-way-to-make-an-agent-autonomous.md) - time-triggered vs event-triggered vs continuous, what kind of system a human is, and the reframe that the real axis is *what generates the next action* - with the model as an expensive subroutine a cheap program decides to call
- [What an Agent Writes to Disk](what-an-agent-writes-to-disk.md) - reading a coding agent's dotfiles as architecture: per-edit snapshots, why "the model can just remember it" is a category error, JSONL's schema-evolution superpower, ring-buffer retention, and 131 deliberately empty directories
- [What's Actually in a Context Window](whats-actually-in-a-context-window.md) - what loads before you type anything, progressive disclosure (index eagerly, content lazily), why the filesystem is invisible by default, and the difference between drafting for free and rewind-and-resend at 4× the tokens
- [Why Markdown Costs Fewer Tokens Than HTML](why-markdown-costs-fewer-tokens-than-html.md) - scaffolding vs content, why tokenizers are doubly punishing on class attributes, what client-side rendering does to a fetched page, and markup as instructions for a renderer that a model isn't
- [The Cost Model of Agent Work - Capex vs Opex](the-cost-model-of-agent-work-capex-vs-opex.md) - authoring cost paid once vs runtime cost paid every run, why reading the input dominates the bill, the three-run break-even, and when writing a script is actively the wrong move
- [Designing a File-Based Memory System for an Agent](designing-a-file-based-memory-system-for-an-agent.md) - persistent recall on a fixed always-loaded budget, the description as a retrieval key rather than documentation, silent non-retrieval as the failure mode, and why the index line and the file's own summary should differ
- [How an Always-On Agent Stays Alive](how-an-always-on-agent-stays-alive.md) - three layers of autonomy, the restart paradox and the detached child that solves it, and why the heartbeat layer is the whole difference between an agent and a cron job
- [The Accidental A/B Test - Framing Effects in Model Answers](the-accidental-ab-test-framing-effects-in-model-answers.md) - the same question asked two ways, sycophancy and its overcorrection, the human vocabulary for the same tendency, and using two framings as a cheap instrument for separating knowledge from counterweighting
- [AI Agent Loop, Tools, and Orchestration](ai-agent-loop-tools-and-orchestration.md) - what agents are, the goal/think/tools/observe loop, sub-agents
- [Multi-Agent Orchestration and Sub-Agent Architecture](multi-agent-orchestration-and-subagent-architecture.md) - agent teams, sub-agent types, settings

## Cloud Infrastructure

How the cloud actually works - the companies, the chips, and the services they sell.

- [Why AI Datacenters Are Measured in Megawatts](why-ai-datacenters-are-measured-in-megawatts.md) - why a watt is the only unit that survives generational churn, what a grid interconnect actually buys you, the five compounding reasons it takes 4–7 years, why software companies are restarting nuclear plants, and how India's constraint has a different shape
- [Hyperscalers Explained - The Pyramid of Cloud Computing](hyperscalers-explained-the-pyramid-of-cloud-computing.md) - what a hyperscaler is, the eight companies that qualify, the tiers below them, why they behave so differently from everyone else
- [Why Hyperscalers Build Their Own Chips - and Why Intel Lost](why-hyperscalers-build-their-own-chips-and-why-intel-lost.md) - Axion, Graviton, Maia, MTIA, Apple silicon - the structural reasons software companies now design better chips than Intel
- [The Four Foundational AWS Services - EC2, S3, Lambda, RDS](the-four-foundational-aws-services-ec2-s3-lambda-rds.md) - what each service solves, when to use which, pricing comparisons, how they compose
- [Containers, Docker, and Kubernetes - From First Principles](containers-docker-kubernetes-from-first-principles.md) - the chain of problems that produced modern cloud-native infrastructure, plus what ECS and EKS actually are

## Programming Concepts

Core ideas that cut across all programming languages.

- [Functional Programming - Pure Functions, Immutability, and Monads](functional-programming-pure-functions-immutability-and-monads.md) - referential transparency, Option/Either, the Red Book
- [Why Skip No-Code and Learn Real Programming](why-skip-no-code-and-learn-real-programming.md) - why n8n/Zapier don't build programming logic, state, DSA through own projects
- [Runtimes and Package Managers - Node, Bun, npm, uv](runtimes-and-package-managers-node-bun-npm-uv.md) - what a "runtime" actually means, how the JS/Python tooling ecosystems relate
- [Parsing a PDF into CSV - Regex vs pdfplumber](parsing-a-pdf-into-csv-regex-vs-pdfplumber.md) - walking through a real parser, what regex is and when it earns its keep, why working at the right layer beats heroic reconstruction
- [Regex - From Neural Nets to `grep`](regex-from-neural-nets-to-grep.md) - invented in 1951 to describe finite automata, why `g/re/p` became a program name, automaton vs backtracking engines as a security property, and the five-second test showing Cmd-F isn't regex
- [The FFT - Why Splitting the Problem in Half Changes Everything](the-fft-why-splitting-in-half-changes-everything.md) - the DFT as a matrix-vector product with exploitable structure, the even/odd split, the butterfly that gets two outputs from one multiplication, and the 2×2 that organizes the whole Fourier family
- [The Abstraction Ladder - RAM, Arrays, and Hash Maps](the-abstraction-ladder-ram-arrays-hashmaps.md) - RAM is literally one giant array, why an array is the thinnest possible software convention rather than hardware, thin vs thick abstraction instead of hardware vs software, and where every other data structure sits on the ladder
- [Rust and the Trade-Off It Dissolved](rust-and-the-tradeoff-it-dissolved.md) - who frees the memory, ownership moving the bookkeeping to compile time, why the GIL is downstream of reference counting, and safety-vs-speed as a question about when the cost is paid
- [Why MATLAB Still Exists](why-matlab-still-exists.md) - certification, vendor liability and an irreplaceable simulation toolchain as the things that keep a tool alive, and the two capabilities that separate NumPy from a deep-learning framework

## Networking & Protocols

How computers talk to each other - from the physical cable up through modern AI tool protocols.

- [Two Machines, One Cable, Two Different Answers - the OSI Model Made Concrete](two-machines-one-cable-the-osi-model-made-concrete.md) - two honest reports that contradict each other because each reads a different layer, why a connector is not a protocol, all seven layers against one running transfer, and encapsulation as the mechanism underneath

- [The Physical Internet - From USB-C to Submarine Fiber and Satellites](the-physical-internet-from-usb-c-to-submarine-fiber-and-satellites.md) - USB-C vs Ethernet vs fiber tradeoffs, submarine cable anatomy and resilience, PoE as copper's killer feature, capacity math (~1 exabit/sec cables vs ~800 Tbps satellites at full Starlink build), and why broadcast satellite TV works but unicast satellite internet doesn't
- [Ports, IP Addresses, and Localhost - from First Principles](ports-ip-addresses-and-localhost-from-first-principles.md) - the apartment building analogy, why one program per port, well-known ports
- [TCP/IP Protocols and How MCP Fits In](tcp-ip-protocols-and-how-mcp-fits-in.md) - ARPANET history, TCP mechanics, the layered stack, application-layer protocols
- [MCP vs CLI - How AI Tools Connect to the World](mcp-vs-cli-how-ai-tools-connect-to-the-world.md) - Model Context Protocol, JSON-RPC, why MCP and CLI are complementary

## Databases & SQL

How data is stored, queried, and managed.

- [Advanced SQL - CTEs, Unions, and Analytical Queries](advanced-sql-ctes-unions-and-analytical-queries.md) - Common Table Expressions, NULLIF, GROUP BY ALL, the SA360 dashboard
- [Database Locking, Transactions, and Why ERP Systems Break](database-locking-transactions-and-why-erp-systems-break-anonymized.md) - locks, transactions, deadlocks, isolation levels, why concurrent writes break enterprise systems
- [A Google Doc Is a Database Row, Not a File](a-google-doc-is-a-database-row-not-a-file.md) - the mental shift from "file on a server" to "rows across tables", what that enables (live collaboration, infinite history, granular permissions), and why your `.docx` export is a derivative
- [Google Spanner and the CAP Theorem](google-spanner-and-the-cap-theorem.md) - how Google built a globally consistent SQL database using GPS receivers and atomic clocks, the TrueTime API, why the "fundamental" CAP trade-off dissolved, and the open-source children (CockroachDB, YugabyteDB, TiDB)
- [SQLite vs PostgreSQL - One Architectural Fact](sqlite-vs-postgresql-one-architectural-fact.md) - in-process library vs socket server, and how concurrency, typing, security and ops all fall out of it; two opposite origin stories still visible in the software; and why migration difficulty is set in week one
- [Trigram Matching, and When Vector Search Isn't Worth It](trigram-matching-and-when-vector-search-isnt-worth-it.md) - surface-form vs semantic difference as the question that picks the tool, why a trigram index accelerates a leading-wildcard LIKE, and a pushback that produced a sharper answer than either starting position
- [Where Relational Databases Struggle - and the Four Kinds of NoSQL](where-relational-databases-struggle-and-the-four-nosqls.md) - scale, varying structure and nested data as one trade seen three ways; document, key-value, column-family and graph each defined by the guarantee it abandoned; and SQL as a language vs an engine that speaks it
- [What a Database Actually Looks Like on Disk](what-a-database-actually-looks-like-on-disk.md) - a table is literally a file, 8 KB pages and why that number matches the layer underneath, indexes as a read/write trade, and Codd's separation of logical structure from physical storage as the idea the whole stack serves
- [Redis - a Data-Structure Server, Not a Cache](redis-a-data-structure-server-not-a-cache.md) - key-to-structure instead of key-to-blob, why that removes a read-modify-write race, single-threaded execution as a feature, and durability as an explicit setting
- [Every Click in a Database GUI Is Generating SQL](every-click-in-a-database-gui-is-generating-sql.md) - a table has no inherent row order, why sorting is a read, what the query log teaches, pagination needing two queries, and a schema you can query
- [Why Databases Exist - Asking What a Spreadsheet Can't Do](why-databases-exist-the-spreadsheet-question.md) - finding the exact point the spreadsheet breaks, the join as a native operation vs one you fake with lookups, a foreign key as a rule rather than a note, and the 1979 coincidence that put both tools on shelves the same year

## Web Development

Frontend architecture and how the browser works.

- [Frontend Architecture - HTML, CSS, JS, and Frameworks](frontend-architecture-html-css-js-and-frameworks.md) - identifying languages by syntax, React/Vue/Angular, the evolution from jQuery to modern frameworks
- [How Search Engines Work - from Crawling to Ranking](how-search-engines-work-from-crawling-to-ranking.md) - inverted indexes, TF-IDF, BM25, PageRank, Google vs Bing index sizes
- [Ingesting Web Content - REST APIs vs Scraping](ingesting-web-content-rest-apis-vs-scraping.md) - check for an API before writing a scraper: WordPress's wp-json endpoint, regex scraping as the fallback, and building an idempotent, re-runnable corpus fetcher
- [What `/v1/` Is Doing in a URL - and the Stack From Raw HTTP to a GUI](api-versioning-and-the-http-sdk-cli-gui-stack.md) - versioning as a promise about breakage, why a decade on v1 is evidence of good design, and the four layers (raw HTTP → SDK → CLI → GUI) where each adds convenience and removes flexibility
- [GraphQL vs REST - Who Decides What Comes Back](graphql-vs-rest-you-decide-what-comes-back.md) - the server choosing the response vs the client describing it, why one endpoint replaces many, over-fetching and the N+1 round trip, and what GraphQL gives up in caching and load predictability
- [OAuth, Scopes, and How an API Knows Who You Are](oauth-scopes-and-how-an-api-knows-who-you-are.md) - six concepts hiding behind "log in", why credentials identify the app and not you, why requesting every scope fails outright, and reading each error code as a diagnosis
- [When the Official API Can't Do It - Reverse-Engineering an Internal Endpoint](when-the-official-api-cant-do-it-internal-endpoints.md) - why a public API is only the subset a company chose to expose, borrowing a rotating key out of a page instead of holding one, impersonating a first-party mobile client, and exactly what stability you trade for access

## Developer Tools & Workflows

Practical tools and practices every developer should understand.

- [Dev Environment and Toolchain](dev-environment-and-toolchain.md) - terminal, Node.js, npm, git, GitHub CLI, Homebrew
- [Terminal - First Principles and Package Management](terminal-first-principles-and-package-management.md) - flags, package managers, dependencies, silence = success
- [Version Control with Git and GitHub](version-control-with-git-and-github.md) - commits, staging, branches, merge conflicts, rebase
- [Git Blame and GitHub Gists Explained](git-blame-and-github-gists-explained.md) - who changed each line, lightweight code sharing, GitHub Sponsors
- [Git Worktrees, tmux, and Parallel Development](git-worktrees-tmux-and-parallel-development.md) - separate working directories, terminal multiplexing, running parallel agents
- [CI/CD Pipelines and Hugging Face - the ML Developer Workflow](cicd-pipelines-and-hugging-face-the-ml-developer-workflow.md) - continuous integration, Hugging Face as "GitHub for ML", error correction
- [Comparing Browser Automation - Playwright, Selenium, Puppeteer](comparing-browser-automation-playwright-selenium-puppeteer.md) - evolution of browser testing, headless browsers, when to use which
- [What the Colours in Your Editor Actually Mean](what-the-colours-in-your-editor-actually-mean.md) - two systems colouring the same file and how to tell which is talking, colour as a diagnostic that arrives before you run anything, how a linter differs from both, and frames-hold-arrows/objects-hold-values
- [Where Does My Code Actually Run?](where-does-my-code-actually-run.md) - the interface vs the machine doing the work, headless meaning no display attached, why "installed" and "importable" are different claims, and ten-byte files as a sign you're looking at a signpost
- [Reading a Recommender Codebase](reading-a-recommender-codebase.md) - a method for navigating a large unfamiliar repo, the bet to delete every hand-engineered feature, retrieve-to-rank-to-filter, and why filter ordering is an economic argument
- [Filesystems, and Finding Where the Bottleneck Actually Is](filesystems-and-where-the-bottleneck-actually-is.md) - what exFAT gives up to be universal, why journaling is the same write-down-your-intent idea from elsewhere, and how a copy and a parse over the same cable are limited by completely different components
- [How Big Is a Codebase, Really - Monorepos and Folder Conventions](how-big-is-a-codebase-monorepos-and-folder-conventions.md) - two billion lines in one repo and the custom version control it forces, monorepo vs polyrepo as a question about where dependency pain gets paid, and why src/bin/test/scripts is navigation rather than convention

## Document Formats & File Standards

How documents are actually stored - and why each format makes the trade-offs it does.

- [Everything Is Text Underneath - File Formats Demystified](everything-is-text-underneath-file-formats-demystified.md) - XLSX = zipped XML, Protocol Buffers, the automation principle
- [Why PDFs Are Binary, Not Text](why-pdfs-are-binary-not-text.md) - the visual-fidelity design goal, PostScript heritage, draw-commands instead of text, why extraction is hard
- [Three Categories of Document Formats](three-categories-of-document-formats.md) - plain text/MD/HTML vs document packages (.docx) vs cloud documents (Google Doc), and the five axes they trade off on
- [Spotlight, Importers, and Why `grep` Can't Read a .docx](spotlight-importers-and-why-grep-cant-read-a-docx.md) - the index vs the filesystem, how `.mdimporter` plugins unpack a Word file, `contains` vs `matches` tested empirically, and reading a document's internal metadata when the Date Modified column lies
- [What Actually Happens When You Unzip a File](what-happens-when-you-unzip-a-file.md) - why the index lives at the tail, LZ77 and Huffman attacking two different kinds of redundancy, and reading a disappointing compression ratio as a report on what's inside the file
- [Document Conversion, and Why OCR Is a Separate Problem](document-conversion-and-why-ocr-is-a-separate-problem.md) - a converter as a dispatcher over format-specific libraries, silent empty output as the failure mode, and decoding vs recognition as the test for whether you need ML
- [Why a Two-Minute Phone Video Is Half a Gigabyte](why-a-two-minute-phone-video-is-half-a-gigabyte.md) - size as bitrate times duration, recording settings optimizing for editing rather than viewing, the metadata that has to survive a re-encode, and verifying a lossy transform objectively

## Knowledge Management

Tools for organizing what you learn.

- [Obsidian and LLM-Powered Knowledge Bases](obsidian-and-llm-knowledge-bases.md) - vaults, wikilinks, Karpathy's knowledge base workflow
- [Reverse-Engineering macOS App Databases with SQLite](reverse-engineering-macos-app-databases-sqlite.md) - ~/Library, SQL commands, the developer thinking pattern

## Finance Meets Tech

Where quantitative finance concepts connect to programming and math.

- [Options Trading, Black-Scholes, and Implicit Options in Physical Trading](options-trading-black-scholes-and-implicit-options-in-physical-trading.md) - calls and puts from first principles, the 5 inputs to option pricing, semiconductor trading as options

## Industry & Security

Understanding the tech landscape.

- [Cloud Security - CNAPP, Wiz, and Palo Alto](cloud-security-cnapp-wiz-and-palo-alto.md) - the cloud security market, Google's $32B Wiz acquisition, competitive dynamics
