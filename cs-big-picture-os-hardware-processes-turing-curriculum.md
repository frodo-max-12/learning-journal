# How Computers Work — Processes, CPU, GPU, and the Layers Underneath

*Learned on 29 March 2026 while studying the agent loop code from shareAI-lab's Learn Claude Code course. Started with `subprocess.run()` in Python and kept asking "but how?" until we reached Turing machines.*

---

## How Python Runs External Commands (`subprocess`)

When you write `subprocess.run(["ls", "-l"])` in Python, it feels like magic — a script reaching outside itself to run another program. But it makes sense once you understand what's happening at the OS level.

When you run a Python script, it becomes a **process** — a running program managed by the operating system. Every process can ask the OS to spawn a **child process**. This is a fundamental OS capability, not something special about Python.

Here's the chain when `subprocess.run(["ls", "-l"])` executes:

1. Your Python script calls `subprocess.run()`
2. Under the hood, `subprocess` asks the OS kernel: "please create a new process and run `ls` in it." On Unix, this uses system calls called `fork()` (clone the current process) and `exec()` (replace the clone with the new program)
3. The OS starts `ls -l` as a separate process running independently alongside your Python script
4. The OS connects the input/output streams (stdin, stdout, stderr) between the two processes, like a pipe
5. `ls` does its thing, writes output, and exits
6. The OS hands that output back to your Python script

Python isn't doing anything extraordinary. It's using the same mechanism that your terminal shell (Bash, Zsh) uses when you type a command. Your shell is itself just a program that spawns child processes. Python, through `subprocess`, does the exact same thing.

This is how almost everything works on your computer — programs launching other programs, forming trees of processes. You can see this tree by running `ps aux` in a terminal. **It's processes all the way down.**

---

## `ps aux` — X-Raying Your Computer

Running `ps aux` gives a snapshot of every process running on your Mac. Each row is one process, and the columns tell you about it:

| Column | Meaning |
|--------|---------|
| USER | Who owns the process |
| PID | Process ID — a unique number the OS assigns |
| %CPU | How much processor it's using right now |
| %MEM | How much memory it's using |
| STAT | Current state: `S` = sleeping/waiting, `R` = actively running, `Ss` = sleeping session leader |
| STARTED | When it launched |
| TIME | Total CPU time used |
| COMMAND | The actual program |

### What you see in the output

- **PID 1 — `/sbin/launchd`**: The root of the entire process tree on macOS. First thing the kernel starts; everything else descends from it.
- **WindowServer**: Draws everything on screen. Usually one of the biggest CPU users.
- **System services**: `coreaudiod` (sound), `bluetoothd`, `locationd`, `mDNSResponder` (network discovery), `trustd` (security certificates), and dozens more — the invisible machinery that makes macOS work.
- **Your apps**: Chrome (with many helper processes — Chrome runs each tab as a separate process), Claude desktop, Terminal, etc.
- **`ps aux` itself**: Shows up in its own output because it was running at the moment it took the snapshot. It has state `R+` (the only one actively Running).

---

## Activity Monitor = GUI Version of `ps aux`

Activity Monitor is just the graphical version of `ps aux`. Both read from the same source — the kernel's process table — and show you the same information, just presented differently.

Activity Monitor gives you: sorting by clicking columns, real-time updates, memory pressure graphs, and the ability to kill processes. `ps aux` gives you a one-time text snapshot that works over SSH on remote servers with no screen, and can be piped into other commands (e.g., `ps aux | grep chrome`).

### The Five Tabs

Each tab isn't just re-sorting — it changes which **metrics** are displayed:

| Tab | What it shows | Bottom panel |
|-----|--------------|--------------|
| **CPU** | % CPU usage, CPU Time per process | CPU usage graph, % idle |
| **Memory** | Memory usage, Threads, Ports | Memory pressure graph, Physical Memory breakdown, Swap |
| **Disk** | Bytes read/written per process | Disk activity |
| **Network** | Data sent/received per process | Network activity |
| **Energy** | Energy impact, whether app prevents sleep | Battery impact |

You can also sort *within* each tab by clicking any column header.

---

## The Four Fundamental Computer Resources

### Memory (RAM)
Your computer's **short-term workspace**. Like a desk — it's where things go while you're actively working on them. When you open an app, it gets loaded into RAM so the CPU can access it quickly. Your Mac has 16 GB. It's fast but temporary — everything in RAM disappears when you shut down.

### CPU (Central Processing Unit)
The **brain** — does the actual thinking and calculating. When your code runs a loop, when Chrome renders a page, when a video gets decoded — that's all CPU work. The "% CPU" column shows how much processing power each process is demanding right now.

### Disk (SSD/Hard Drive)
**Long-term storage**. Everything lives here permanently: your files, apps, the OS itself. Much slower than RAM but persists when you power off. The Disk tab shows bytes read and written.

### Network
Data going in and out over the internet or local network — every web page loaded, every API call, every file synced to iCloud.

### Energy
Battery impact — which apps are draining your battery the most, and whether any app is preventing your Mac from sleeping.

**The flow:** Apps live on **disk**, get loaded into **memory** when you open them, the **CPU** does the actual work, and **network** handles communication with the outside world. These are the four fundamental resources every computer manages.

---

## Your M5 Chip — CPU, GPU, and Neural Engine

Your MacBook Air runs on the **Apple M5** chip. It's a **System on a Chip (SoC)** — the CPU, GPU, Neural Engine, and memory controller are all on a single piece of silicon.

### What is a "core"?

A core is one independent worker that can execute instructions. Think of it like a person at a desk doing tasks. Early CPUs had just one core — one worker doing everything, one task at a time. Multi-core processors put multiple workers on the same chip to work in parallel.

### 10-core CPU

Your M5 has 10 CPU cores split into two types:

- **Performance cores (P-cores)**: Big, fast, power-hungry. Handle heavy lifting — compiling code, processing data, complex logic.
- **Efficiency cores (E-cores)**: Smaller, slower, low power. Handle lightweight background tasks — checking email, syncing iCloud, playing music.

Most of the time your computer is doing easy stuff, so the efficiency cores handle it while the performance cores sleep (saving battery). When something demanding launches, the performance cores wake up. macOS decides which cores to use automatically.

### 10-core GPU

GPU cores are fundamentally different from CPU cores:

- **CPU core** = a brilliant mathematician — solves one complex problem at a time, handles branching logic, decision-making, unpredictable tasks
- **GPU core** = a room full of hundreds of simple calculators all working simultaneously

GPU cores are designed for tasks where you do the **same operation on thousands of pieces of data at once**. The classic example: rendering your screen. Millions of pixels, each needing a color calculation — millions of nearly identical calculations, perfect for parallel processing. This is also why GPUs turned out to be great for AI/ML: training neural networks involves multiplying enormous matrices, which is exactly what GPUs excel at.

### Neural Accelerators (inside each GPU core)

Inside each of the 10 GPU cores, Apple embedded a **Neural Accelerator** — a tiny hardware unit specifically optimized for AI math (matrix multiplications and tensor operations). It's like the difference between cutting bread with a general-purpose knife versus a bread knife — both work, but one is designed for the job.

### 16-core Neural Engine

A completely separate section of the M5 chip, dedicated entirely to **machine learning inference** (running trained AI models). It has 16 cores that do nothing but ML math. It can't render graphics. It can't run Python. It only processes neural network computations — extremely fast and efficiently.

Apple uses the Neural Engine for: Face ID, computational photography, real-time voice transcription (Siri, dictation), on-device text prediction, image recognition in Photos, and Apple Intelligence features.

### Why three separate units that all do "AI"?

| Unit | Strength | Flexibility |
|------|----------|------------|
| CPU | Most flexible — can run any code | Slowest at parallel AI work |
| GPU + Neural Accelerators | Great for large, complex AI models | Medium flexibility |
| Neural Engine | Fastest and most power-efficient for pure ML inference | Least flexible — only specific model types |

macOS and Apple's frameworks (Core ML) automatically route work to the right unit based on the task.

### Technical specs

- Built on **third-generation 3-nanometer technology** (how tiny the transistors are — smaller = more efficient, more transistors packed in)
- **16 GB unified memory** — both CPU and GPU share the same memory pool (no copying data back and forth, which makes things faster and more power efficient)
- Separate **N1 wireless chip** for Wi-Fi 7 and Bluetooth 6

---

## Tying It All to David Deutsch and The Fabric of Reality

### Turing's Universal Computer

In *The Fabric of Reality*, Deutsch starts with Alan Turing's 1936 insight. Turing imagined the simplest possible computing machine: a strip of tape with symbols, a head that reads/writes one symbol at a time, and a set of rules. Absurdly simple.

But Turing proved something astonishing: **this trivial machine, given enough tape and time, can compute anything that is computable.** He then showed you can build a **universal Turing machine** — one that takes a description of any other Turing machine as input and simulates it. A machine that can imitate any machine.

Deutsch builds on this, arguing that a universal computer can simulate any physically possible process — tying computation to the laws of physics themselves. For Deutsch, the universality of computation is one of the **four fundamental strands of reality**, alongside quantum mechanics, epistemology, and evolution.

### Your M5 chip is a Turing machine made real

| Turing's machine | Your MacBook |
|-----------------|--------------|
| A tape (stores symbols) | RAM + SSD (stores data) |
| A head that reads/writes | CPU cores (fetch instructions, execute, write results) |
| A table of rules | Programs — Python, Chrome, macOS |

**The deep insight Deutsch wants you to notice:** It doesn't matter that your M5 has 10 cores and a GPU and a Neural Engine. In terms of *what it can compute*, it's equivalent to Turing's 1936 tape machine. All that hardware just makes it *faster*. It doesn't make it capable of computing anything fundamentally new.

**Every universal computer is equivalent to every other universal computer in terms of what it can compute.** Your M5, a Raspberry Pi, a 1960s room-sized mainframe, Turing's hypothetical tape machine — all in the same computational class. The differences are speed, efficiency, and convenience, not fundamental capability.

### Where Deutsch goes beyond Turing

Deutsch argues that the physical world is such that universal computation is possible within it — and that this is a deep fact about the laws of physics. He proposes that a **quantum computer** would be a stronger kind of universal computer, one that can efficiently simulate quantum physical processes that a classical Turing machine could simulate only with exponential slowdown.

Your M5 is a classical computer. There are physical processes (like quantum interference across many particles) that your MacBook can simulate *in principle* but not *in practice* — they'd take longer than the age of the universe. A quantum computer could do them efficiently. That's the frontier Deutsch is pointing toward.

### The tower of abstraction

Going from Deutsch/Turing all the way up to Activity Monitor:

1. **Physics and logic** (bottom): Turing's proof that universal computation is possible. Deutsch's argument that the laws of physics permit and require universal computers.
2. **Hardware**: Your M5 chip. Billions of transistors at 3nm, implementing logic gates (AND, OR, NOT) that together can perform any computation. CPU, GPU, Neural Engine = specialized arrangements of the same basic logic gates.
3. **Operating System**: macOS. Manages the hardware — decides which core runs which process, allocates memory, handles disk I/O. When you saw 300+ processes in `ps aux`, that's the OS giving each program the illusion it has the whole computer to itself.
4. **Applications**: Chrome, Python, Claude Code, Terminal. Programs running on top of the OS. When Python calls `subprocess.run()`, it asks the OS to create a process. The OS talks to hardware. Hardware executes instructions. All traces back to Turing's logic.
5. **Knowledge creation** (top): What you're actually doing — writing code, learning, having conversations. Deutsch would say this layer is the whole point. Computers are universal explanation machines, extending our ability to create and test explanations about reality.

---

## How This Maps to the Computer Science Curriculum

All of the above is taught in a standard undergrad CS degree, spread across ~8–12 core courses:

### Year 1: Programming Fundamentals
Learn to write code (Python/Java). Loops, functions, data structures. This is where `import os`, `getcwd()`, and writing scripts lives. *CS 101/102.*

### Year 1–2: Data Structures and Algorithms
How to organize data efficiently (arrays, trees, hash tables, graphs) and write procedures that operate on it (sorting, searching). Big O notation — analyzing how fast algorithms run. Often considered the single most important CS course.

### Year 2: Computer Architecture / Computer Organization
How a CPU actually works at the hardware level — logic gates, instruction pipelines, registers, cache, memory addressing. Why a GPU differs from a CPU at the circuit level. Why the Neural Engine exists. **This explains your M5.**
*Textbook: Patterson and Hennessy — Computer Organization and Design*

### Year 2–3: Operating Systems
How the OS manages hardware, processes, memory, files. Everything from `ps aux` and Activity Monitor: process scheduling across 10 cores, virtual memory, swap, how processes communicate, system calls (`fork()`, `exec()`), file systems, permissions, the shebang mechanism.
*Textbooks: Tanenbaum — Modern Operating Systems, or Silberschatz — Operating System Concepts ("the dinosaur book")*

### Year 2–3: Computer Networks
How data travels from browser to server and back. TCP/IP, HTTP, DNS. What happens at each layer of the network stack when Chrome connects to google.com.

### Year 3: Theory of Computation
The most abstract course — connects directly to Deutsch. Turing machines as formal mathematical objects. What can and cannot be computed. The halting problem. Computational complexity (P vs NP). **This is where the deep ideas live.**
*Textbook: Sipser — Introduction to the Theory of Computation*

### Year 3: Databases
How data is stored, organized, and retrieved on disk. SQL, indexing, transactions.

### Year 3: Compilers / Programming Languages
How `print("hello")` in Python gets translated into instructions your M5 can execute. Lexing, parsing, code generation.

### Year 3–4: Distributed Systems
Computation spanning multiple computers. How Google, Netflix, AWS work.

### Year 4: Electives
ML/AI, computer graphics, security, robotics, quantum computing (Deutsch's deeper ideas).

### Self-study path recommendation

Since I have a B.Tech in metallurgy (comfortable with math and engineering thinking):

1. **Harvard's CS50** (free on YouTube/edX) — broad, entertaining overview of the whole landscape
2. **Nand2Tetris** (free) — build a computer from logic gates all the way up to a working OS. Gives the complete picture from hardware to software in one course
3. **Go deeper** into whichever layer fascinates you most with the textbooks above
4. **Keep reading Deutsch** alongside everything — his perspective gives philosophical depth the standard curriculum usually doesn't provide
