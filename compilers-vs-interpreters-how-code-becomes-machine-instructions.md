# Compilers vs Interpreters — How Code Becomes Machine Instructions

*Learned on 29 March 2026. Branched off from studying the agent loop — the `#!/usr/bin/env python3` shebang line led to the question: how does Python code actually get executed by the M5 chip?*

---

## The Core Problem

Your M5 chip doesn't understand Python. It doesn't understand C, Java, or any human-readable language. It only understands **machine code** — raw binary instructions like "load this number from memory address X into register 3, add it to register 4, store the result at address Y."

Something has to bridge the gap between `print("hello world")` and the binary instructions the CPU can execute. That bridge is either a **compiler** or an **interpreter** — two different strategies for solving the same problem.

---

## Compilers: Translate Everything Upfront

A compiler reads your entire source code, translates the whole thing into machine code, and produces a **standalone executable file**. After that, the original source code isn't needed — the machine code runs directly on the CPU.

**C works this way.** When you write a C program and run `gcc myprogram.c -o myprogram`, the compiler (`gcc`) reads your C code, translates it all into machine code, and produces a binary file called `myprogram`. When you run `./myprogram`, the CPU is executing raw machine instructions directly. No middleman at runtime. This is why C programs tend to be very fast.

## Interpreters: Translate Line by Line As You Go

An interpreter reads your source code one piece at a time and executes it on the fly, without ever producing a standalone machine code file.

It's like having a human translator in a meeting who listens to one sentence, translates it, then waits for the next sentence — versus a translator who reads the whole document first and hands you a fully translated copy.

## Python Is Interpreted, Not Compiled

When you run `python3 myscript.py`, Python doesn't translate the entire script into machine code upfront. Instead, the Python interpreter (called **CPython**, the standard one) reads your code, converts it to an intermediate format called **bytecode** (simpler but still not machine code), and then a piece of software called the **virtual machine** executes that bytecode instruction by instruction.

So that `#!/usr/bin/env python3` shebang line in the agent loop script? It's pointing to the interpreter. Python needs that interpreter present every time the script runs. A compiled C program doesn't — once compiled, it's self-sufficient.

This is also why Python shows up as a running process in Activity Monitor. That's the Python interpreter sitting in memory, actively interpreting a script. When you run a compiled C program, you'd see the program's own name as the process, not "C."

---

## The Spectrum: It's Not Black and White

The line between compiled and interpreted has gotten blurry. Many languages use a **hybrid approach**:

- **Java** compiles to an intermediate bytecode (not machine code), then the Java Virtual Machine (JVM) runs that bytecode. But the JVM also has a **Just-In-Time (JIT) compiler** that notices which parts of your code run frequently and compiles those hot spots to native machine code on the fly for speed.
- **Python's CPython** is relatively straightforward — compiles to bytecode and interprets it, without much JIT optimization.
- **PyPy** is an alternative Python implementation that uses JIT compilation to make Python code run much faster.

---

## Each Language Has Its Own Compiler or Interpreter

| Language | Tool | Type | Notes |
|----------|------|------|-------|
| **C** | `gcc`, `clang`, MSVC | True compilers → native machine code | `clang` is what your Mac likely uses by default (Apple-developed) |
| **C++** | `g++`, `clang++`, MSVC | Same compilers as C | C++ evolved from C |
| **Python** | CPython (default), PyPy, Jython, IronPython | Interpreter (CPython), JIT interpreter (PyPy) | CPython is the one at `/opt/homebrew/Cellar/python@3.13/` |
| **Java** | `javac` → bytecode, then JVM | Hybrid: compiled to bytecode, then JIT-compiled | Different JVMs: Oracle HotSpot, Eclipse OpenJ9, GraalVM |
| **JavaScript** | V8 (Chrome/Node.js), SpiderMonkey (Firefox), JavaScriptCore (Safari) | Interpreted with sophisticated JIT | V8 is what runs the MegaFuse Next.js project |
| **Rust** | `rustc` | True compiler → native machine code | |
| **Go** | `go build` | True compiler → native machine code | |

---

## The Benchmark: Seeing the Difference in Numbers

A benchmark ran one simple task — calculating π using the Leibniz formula, 100 million iterations — across many languages. Same task, same computer, only the language differs.

| Language | Time (ms) | Notes |
|----------|-----------|-------|
| C++ (g++) | ~161 | Compiled → native machine code |
| C (gcc) | ~161 | Compiled → native machine code |
| Fortran | ~162 | Compiled → native machine code |
| Go | ~163 | Compiled → native machine code |
| Rust | ~164 | Compiled → native machine code |
| Java | ~212 | JVM + JIT — slight overhead, but competitive |
| JavaScript (Node.js) | ~425 | V8 engine with JIT — impressive for interpreted |
| Python (PyPy) | ~964 | Same Python code, but JIT-compiled — 30x faster than CPython |
| **Python (CPython)** | **~28,514** | Pure interpretation — **177x slower than C** |

### What this shows

- **All compiled languages cluster at the top** (~161–164ms) because once compiled, they all produce nearly identical machine code. The CPU doesn't know what language the source was.
- **Python (CPython) is 177x slower than C** — that's the cost of interpretation. Every operation goes through the interpreter.
- **PyPy vs CPython** is striking: same Python code, 30x faster. The language isn't inherently slow — the *implementation* (compiler vs interpreter) determines speed.

### Why anyone uses Python then

For most real-world tasks, the speed difference doesn't matter. If your script takes 0.001 seconds in Python vs 0.000006 seconds in C, you'd never notice. **Developer time matters more than computer time.** Python lets you write in 10 lines what might take 50 in C, with no memory management headaches, no compilation step, and far fewer bugs.

But when performance does matter — training AI models, processing video, running databases — the critical code is written in C/C++/Rust, and **Python just calls into it**. NumPy is "Python" but the actual math happens in compiled C and Fortran underneath. You get Python's ease of use with C's speed.

### Tying it back to Turing and Deutsch

This benchmark is a vivid demonstration of Deutsch's point about universality. Every language computed the **exact same result** — the same value of π. They're all universal computers. The difference is purely in how efficiently the translation from human-readable code to machine instructions happens. **Universality guarantees the same result; it says nothing about speed.**

---

## But Wait — Apps Like Chrome Were Already Compiled Too

Apps like Google Chrome, Wispr Flow, and the Claude desktop app are all compiled programs. The compilation just happened *before they reached you* — on Google's build servers, on the developer's machine, etc. By the time you download Chrome, you're getting the finished machine code binary. That's why Activity Monitor shows "Google Chrome" as the process name, not "C++ interpreter running Chrome."

The difference with Python: you have the raw source code (`.py` files) and the interpretation happens on your machine every time you run the script. With Chrome, you never see the C++ source — you just run the pre-compiled binary.

## Compiled Code Isn't Static — It's Fixed Logic + Changing Input

A compiled binary isn't a fixed set of answers. It's a fixed set of **instructions for how to respond to any situation**. Chrome's compiled code contains logic like: "when the user types a URL, make a network request, parse the HTML, render the page." The logic is baked in; the data it operates on (which URL, which page) is not.

Every app sits in an **event loop** — perpetually cycling, checking for new input (keystrokes, clicks, network responses), updating state in memory, and rendering output. It looks alive because it's constantly reacting. Like a vending machine: the mechanical logic was fixed at the factory, but it responds dynamically to whatever button you press and whatever money you insert.

## JavaScript: An Interpreter Inside a Compiled App

Chrome is compiled C++, but it contains the **V8 JavaScript engine** — because web pages include JavaScript code that Chrome has never seen before. When you visit a website, JS source code arrives over the network and V8 JIT-compiles it to machine code on the fly.

So you get **two nested event loops**: Chrome's C++ event loop (handling windows, networking, processes) and JavaScript's event loop inside each tab (handling button clicks, API callbacks, DOM updates). When you click "Like" on YouTube, the event travels down from macOS → Chrome's C++ → V8 executing YouTube's JavaScript → back to Chrome's networking stack to send the API request.

**Why not just compile websites?** Because the web runs *other people's code you've never seen before*, on *any CPU architecture*. Websites ship portable source code (JS), and every browser's JIT compiler translates it for whatever chip the user has. Same JS, different machine code output, same behavior.

### The pattern at every level

Your computer is layers of this same pattern stacked on top of each other: macOS (compiled, event loop) → Chrome (compiled, event loop) → JavaScript (JIT-compiled, event loop). Each layer is a program sitting in a loop, waiting for input, responding dynamically. The compiled layers serve as foundations for the interpreted layers above. And every layer is doing what Turing described — executing conditional logic on changing input.
