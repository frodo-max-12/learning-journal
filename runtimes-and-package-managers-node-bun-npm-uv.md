# Runtimes and package managers --- Node.js, Bun, npm, and uv from first principles

*Learned on April 2026. I kept encountering these names --- Node.js, npm, Bun, uv --- while setting up tools and following tutorials. They were always mentioned casually, as if everyone already knows what they are. I didn't. The question that started this was embarrassingly basic: "What's the difference between Node.js and npm?" But it led me to understand something fundamental about how modern software is built and run.*

---

## Starting with the word "runtime"

Before I could understand Node.js or Bun, I needed to understand what a "runtime" is, because that word gets thrown around constantly.

A runtime is the program that runs your code. That's it. That's the whole concept.

When you write a Python script, you can't just double-click the `.py` file and have your computer understand it. Your CPU speaks machine code --- ones and zeros. Python is a high-level language that needs to be translated. The **Python runtime** (specifically CPython, the standard implementation) reads your Python code, interprets it line by line, and executes the corresponding machine operations.

The analogy I found helpful: your code is a recipe written in French. The runtime is the French-speaking chef who reads the recipe and actually cooks the food. Without the chef, the recipe is just ink on paper.

Different languages have different runtimes:
- **Python** is run by CPython (or PyPy, or other implementations)
- **Java** is run by the JVM (Java Virtual Machine)
- **JavaScript** is run by... well, that's where the story gets interesting

## The JavaScript problem --- and how Node.js solved it

JavaScript was originally designed to run inside web browsers. Chrome has the V8 engine, Firefox has SpiderMonkey, Safari has JavaScriptCore. These engines are JavaScript runtimes --- they read JS code and execute it.

But JavaScript was trapped inside the browser. You could use it to make web pages interactive, but you couldn't use it to build a server, write a script that processes files, or do anything outside a browser window.

In 2009, Ryan Dahl created **Node.js**. The core idea was: take Chrome's V8 engine (which is excellent at running JavaScript quickly) and wrap it with APIs for things that browsers don't provide --- reading files, starting web servers, accessing the network, running system commands. Suddenly, JavaScript could do everything Python or Java could do.

```
Browser JavaScript:
    V8 engine + DOM APIs (document, window, etc.)
    → Can manipulate web pages
    → Can't touch the filesystem

Node.js:
    V8 engine + system APIs (fs, http, net, path, etc.)
    → Can read/write files
    → Can run web servers
    → Can do anything Python can do
```

When people say "node" (lowercase), they're usually referring to the command-line tool: you type `node server.js` to run a JavaScript file. Node.js is the full project; `node` is the executable.

This is why, when I installed Claude Code on my Mac, the permission dialog said "Node wants to access your files." Claude Code is a JavaScript/TypeScript application that runs on the Node.js runtime. macOS sees the Node.js process --- not Claude Code itself --- requesting filesystem access, because Node.js is the chef doing the actual cooking.

## npm --- the package manager that comes with Node.js

Once JavaScript could run outside the browser, people started building libraries --- reusable pieces of code for common tasks. A web framework, a database driver, a date formatting utility, a testing tool. The JavaScript ecosystem exploded.

**npm** (Node Package Manager) is the tool that manages all these libraries. It does three things:

1. **Installs packages** from a central registry (npmjs.com, which hosts over 2 million packages)
2. **Manages dependencies** --- if package A requires packages B and C, npm installs all of them
3. **Tracks versions** --- your `package.json` file records exactly which packages and versions your project uses

```bash
# Install a package
npm install express    # Downloads "express" and its dependencies

# This creates:
# node_modules/        ← folder with all the downloaded package code
# package.json         ← your project's dependency list
# package-lock.json    ← exact versions of everything installed
```

The `node_modules` folder is notorious in the developer world. Because JavaScript packages tend to have many small dependencies, and those dependencies have their own dependencies, `node_modules` can easily contain thousands of folders and hundreds of megabytes of code. There's a famous joke that `node_modules` is the heaviest object in the universe.

> The key relationship: Node.js is the runtime (runs your code). npm is the package manager (installs other people's code that your code uses). They ship together but do different things.

## Bun --- what if one tool did everything?

Bun arrived in 2023 and took a different philosophy. Instead of being just a runtime or just a package manager, Bun is an all-in-one tool: runtime, package manager, bundler, and test runner in a single executable.

The technical differences from Node.js:

**Different engine.** Node.js uses Google's V8 engine. Bun uses Apple's JavaScriptCore (the engine from Safari). The choice of JSC is part of why Bun is fast --- it's a well-optimized engine that the Bun team found easier to integrate with their performance goals.

**Written in Zig.** Node.js is written in C++. Bun is written in Zig, a modern systems programming language designed for performance. Zig gives Bun fine-grained control over memory allocation and system calls, which contributes to its speed.

**All-in-one design.** Where the Node.js ecosystem has separate tools for each task --- Node for running code, npm for packages, webpack for bundling, Jest for testing --- Bun handles all of these natively. This eliminates the overhead of having multiple tools communicate with each other.

The speed difference is dramatic. Installing packages with Bun can be 10-25x faster than npm. Starting a script with Bun is noticeably faster than Node.js. For developers who run these commands hundreds of times a day, it adds up.

```bash
# With Node.js ecosystem (multiple tools):
node server.js           # Run code (runtime)
npm install express      # Install packages (package manager)
npx webpack              # Bundle code (bundler)
npx jest                 # Run tests (test runner)

# With Bun (one tool):
bun server.js            # Run code
bun install express      # Install packages
bun build ./src          # Bundle code
bun test                 # Run tests
```

Bun is largely compatible with Node.js --- most Node projects run on Bun with minimal or no changes. It implements the same APIs (`fs`, `http`, `path`, etc.) so your code doesn't need to know which runtime is executing it. Think of it like switching from a Toyota to a BMW --- different engine under the hood, but the steering wheel and pedals work the same way.

## uv --- Bun's philosophy, but for Python

uv is in a completely different language ecosystem --- it's for **Python**, not JavaScript. But conceptually, it's doing the same thing Bun did: taking a fragmented set of slow tools and replacing them with one fast tool.

The Python ecosystem traditionally requires multiple tools for what should be simple tasks:

| Task | Traditional Python | With uv |
|---|---|---|
| Install Python itself | pyenv | uv |
| Create isolated environments | virtualenv or venv | uv |
| Install packages | pip | uv |
| Manage project dependencies | pip-tools or poetry | uv |
| Run scripts | python | uv run |

uv replaces all of these. It's written in Rust (another fast systems language, similar in spirit to Zig) by the same team that built `ruff`, the fast Python linter. Like Bun, its defining characteristic is speed --- installing packages with uv is 10-100x faster than pip.

```bash
# Traditional Python workflow:
pyenv install 3.12         # Install Python version
python -m venv .venv       # Create virtual environment
source .venv/bin/activate  # Activate it
pip install flask          # Install a package

# With uv:
uv python install 3.12     # Install Python version
uv init                    # Create project
uv add flask               # Install a package
uv run app.py              # Run your script
```

The parallel to Bun is striking:

| | JavaScript | Python |
|---|---|---|
| Traditional runtime | Node.js | CPython |
| Traditional package manager | npm | pip |
| Fast all-in-one replacement | Bun | uv |
| Written in | Zig | Rust |
| Speed improvement | 10-25x for installs | 10-100x for installs |

## Connecting this to what I already knew

I had previously studied the difference between compilers and interpreters. This fits together neatly.

A **compiler** translates your entire program into machine code before running it (C, Go, Rust). An **interpreter** translates and executes your program line by line (Python, Ruby). JavaScript sits in a middle ground --- engines like V8 use Just-In-Time (JIT) compilation, where they start interpreting but compile frequently-used code paths into machine code on the fly.

The runtime is what *contains* the interpreter or JIT compiler. Node.js contains V8 (which has a JIT compiler). CPython contains the Python interpreter. The runtime is the whole environment --- the engine plus all the system APIs that let your code interact with the world.

```
Your code
    → Runtime (Node.js, Bun, CPython...)
        → Engine (V8, JSC, CPython interpreter...)
            → Machine code
                → CPU
```

## Why this matters for building real projects

When I'm setting up a project --- like the MegaFuse marketplace or the trading desk --- I now understand the layered decisions involved:

1. **What language?** JavaScript/TypeScript or Python (or both)
2. **What runtime?** Node.js or Bun for JS; CPython for Python
3. **What package manager?** npm or Bun for JS; pip or uv for Python
4. **What packages?** Express, React, Flask, whatever the project needs

These aren't independent choices. If you choose Bun, you get the runtime and package manager in one. If you choose Node.js, you probably use npm (though you could also use Yarn or pnpm, two other JavaScript package managers I haven't explored yet).

The trend is clear: the developer tools world is moving toward faster, more integrated solutions. The fragmented "install five tools to do one thing" approach is being replaced by all-in-one tools that are also dramatically faster. Bun and uv are leading this shift in their respective ecosystems, and understanding *why* they're faster (systems languages, integrated design, fewer layers of abstraction) teaches you something about performance engineering in general.

> The pattern: fragmentation creates the need for integration. Slowness creates the need for speed. And the tools that win are the ones that solve both problems at once.

---

*What I studied next: How compilers and interpreters work --- connecting the runtime layer to the execution layer. See [compilers-vs-interpreters.md](compilers-vs-interpreters.md)*
