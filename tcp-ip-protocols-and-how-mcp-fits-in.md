# TCP/IP, protocols, and how MCP fits in — from first principles

**Context:** After understanding ports and IP addresses (see `ports-ip-addresses-and-localhost-from-first-principles.md`), the next natural question is: *what is TCP/IP, what does "protocol" actually mean, and how does Claude's Model Context Protocol (MCP) fit into this family?* This journal covers the broader networking picture that CS students learn in their Year 2–3 Networks course.

---

## 1. What does "protocol" even mean?

Before computing, **protocol** was a diplomatic word. It came from Greek *prōtokollon* — literally "the first glued-on page" of an ancient scroll, which carried authentication info. By the 1500s it meant the formal rules diplomats followed when ambassadors from different countries met:

> "Don't speak before being introduced. Address the French ambassador as 'Your Excellency.' Offer gifts in this order. Sign the treaty left-to-right."

Why did diplomats need all that? Because **two parties who have never met, from different cultures, speaking different languages, need pre-agreed rules** — otherwise every meeting devolves into chaos. Nobody would know who speaks first, what words are rude, how to confirm agreement. The protocol is the *rules of the conversation*, agreed on in advance, so the conversation itself can happen.

That is exactly — *exactly* — what a protocol is in computing.

> **A protocol is a pre-agreed set of rules about how two programs talk to each other: how to start a conversation, how to structure messages, how to confirm receipt, how to handle errors, how to end.**

Two programs written by different people, running on different computers, made by different companies in different countries, cannot successfully exchange data unless they agree in advance on these rules. Someone writes the rules down in a document (on the internet, these are called **RFCs** — Requests for Comments, published since 1969). Anyone building software that "speaks" that protocol implements those exact rules. That's why my Mac can talk to a server in California running Linux, even though nobody coordinated the two builds.

Hold that definition. Everything else flows from it.

## 2. The world before TCP/IP — and why it was broken

In the 1960s and early 70s, computer networks existed — but they were **proprietary and incompatible**. IBM had its own networking protocol (SNA). DEC had its own (DECnet). Each computer company built a walled garden. An IBM computer could talk to another IBM computer fine, but it could not talk to a DEC computer at all. Not because the wires were different, but because nobody had agreed on rules for how they should talk.

Imagine if every building in Pune used its own private postal system that couldn't exchange mail with other buildings' systems. That's what networking was. Useful inside one vendor's world. Useless between worlds.

The US military funded a research agency called **ARPA** (Advanced Research Projects Agency) that wanted something better. They wanted a network that could connect:

- *Any* kind of computer, including ones that didn't exist yet
- Built by *any* vendor, with no licensing fees
- Robust enough to survive partial failures (Cold War — if a node got nuked, the network had to keep routing around it)

Two researchers — **Vint Cerf** and **Bob Kahn** — sat down in the early 1970s and designed a protocol to meet those goals. They published it as **RFC 675** in December 1974. They called it **TCP/IP**. By 1983, the entire ARPANET switched over to it, and that switch is the literal birth of what we now call "the internet."

The winning design principles — these echo through everything that came after:

1. **Open** — anyone can implement it without asking permission or paying fees
2. **Vendor-neutral** — not tied to any company
3. **Layered** — each layer does one job, layers can be swapped independently
4. **Dumb core, smart edges** — the network itself is simple; intelligence lives in the programs at each end

This is why the internet grew into what it is. Any new company could plug in without begging permission from IBM or DEC. Anyone could invent a new application on top without touching the core. That openness is the single reason I can today run a Python hedge fund on a Mac and have it talk to a weather API on AWS without either side knowing the other exists.

## 3. The unreliability problem — why IP alone isn't enough

In the ports explanation, IP was "the thing that delivers packets from one computer to another." True, but this glosses over a crucial detail: **IP is unreliable on purpose.**

IP's guarantee is essentially: *"I'll do my best to deliver this packet. No promises."*

Specifically, IP does **not** guarantee:

- **That the packet arrives at all.** If a router is congested, it drops packets to save itself.
- **That packets arrive in order.** Two packets sent back-to-back can take different paths and arrive out of sequence.
- **That packets arrive only once.** Re-sends and network hiccups can produce duplicates.
- **That packets are uncorrupted.** Radio interference can flip bits.

Why was IP designed this way? Because making the network itself simple and "dumb" was a principle. A dumb network is cheap, scales forever, and can't fail in complicated ways. The intelligence — reliability, ordering, error correction — is pushed out to the programs at each end. *"Smart edges, dumb core."*

The analogy: imagine mailing a 50-page novel to a friend by **writing each page on a separate postcard** and dropping them into random mailboxes across India. Eventually most will reach your friend — but some will get lost, some will arrive out of order, and occasionally a page will arrive twice. That's IP.

For some applications, this is totally fine. Live video calls, multiplayer games — if one packet is lost, you don't want to stop the whole stream and wait for a re-send. You just want the next frame. That's what **UDP** (User Datagram Protocol) is for — raw IP-style delivery with ports added, no reliability. Fast but lossy.

But for **most** things — sending an email, loading a web page, downloading a file, running a hedge fund — you need every byte to arrive in exactly the right order with zero corruption. If you download a ZIP file and one byte is wrong, the whole archive is garbage.

So someone had to invent a protocol that took IP's unreliable postcard delivery and built **reliability** on top of it. That protocol is **TCP** — Transmission Control Protocol.

## 4. What TCP actually does (and why each feature exists)

TCP is one of the cleverest protocols ever designed because each feature directly addresses one of IP's failures:

**a. Three-way handshake (connection setup)**
Before sending any data, TCP confirms both sides are alive and listening:
- Client: "SYN" ("Hi, can you hear me?")
- Server: "SYN-ACK" ("Yes, I hear you. Can you hear me?")
- Client: "ACK" ("Yes, I hear you. Let's start.")

Only after all three messages succeed is the "connection" open. Like two diplomats confirming they're both in the room before negotiations.

**b. Breaking big data into segments**
TCP slices your data (say, a 2 MB file) into small numbered pieces called **segments** (usually ~1500 bytes each) and sends them through IP one at a time. Each segment carries its segment number so the receiver can reassemble them.

**c. Acknowledgments + retransmission (handling loss)**
For every segment received, the receiver sends back an ACK: "Got segment 5." If the sender doesn't hear an ACK within a timeout, it assumes the segment was lost and re-sends it.

**d. Reordering buffer**
Because segments can arrive out of order, TCP buffers them and only hands them to the application *in the correct order*. Segment 7 arrives before segment 6? TCP holds segment 7 until segment 6 shows up, then delivers both in sequence.

**e. Checksums (handling corruption)**
Each segment carries a checksum — a small math fingerprint of its contents. The receiver recomputes it and compares. If they don't match, the segment is corrupted, and TCP treats it as lost.

**f. Flow control**
The receiver tells the sender "I can only handle 50 segments at a time — don't flood me." This is the **sliding window**. It prevents fast senders from overwhelming slow receivers.

**g. Congestion control**
If the network itself is congested, TCP backs off sending so it doesn't make things worse. This is genuinely profound — TCP's congestion-control algorithm is one of the main reasons the internet doesn't collapse under load. Every TCP connection in the world, at every moment, is politely backing off when it senses congestion. The cumulative effect is a self-regulating system. Nobody *forces* this cooperation — it's baked into the protocol, and because everyone speaks TCP, everyone cooperates.

**h. Connection teardown**
When done, both sides formally close with FIN/ACK messages.

**The point to feel in your gut:** TCP takes a network that loses packets, reorders them, duplicates them, and corrupts them — and hands your application a *perfect, ordered, gap-free stream of bytes*. Your application never has to worry about the underlying mess. You just open a TCP connection, write bytes in, read bytes out. The reliability is hidden.

This is one of the most important ideas in all of computer science: **a protocol built on top of an unreliable foundation can give you reliability, if it's clever enough.** TCP is the canonical example.

## 5. The "/IP" part

"TCP/IP" = TCP running on top of IP.

- **IP** delivers individual packets from machine to machine, addressed by IP address. Unreliable.
- **TCP** sits above IP and uses IP's raw packet delivery to build a reliable ordered byte stream between two programs, addressed by port.

Together: TCP/IP. The slash just means "the family of protocols these two represent." In practice, the family includes IP, TCP, UDP, ICMP, and others — but TCP/IP became the shorthand name for the whole thing because those two are the most important.

## 6. The layered stack — the key idea

This is the single most important mental model in networking. Once you see it, everything clicks.

Imagine mailing a handwritten letter from Pune to Boston:

1. You write the letter on a piece of paper
2. You put it in an envelope and address it
3. The post office puts your envelope (plus many others headed to the US) into a larger canvas bag
4. The canvas bag goes on a truck to Mumbai airport
5. The truck bags get loaded onto a plane
6. The plane flies to Boston
7. At Boston, the whole process unwinds: plane → truck → bag → envelope → letter

Each layer **wraps the previous one in its own wrapping, without caring what's inside.** The truck driver doesn't read your letter. The airline doesn't open the canvas bag. Each layer does one job and hands off.

The internet works exactly the same way. When Chrome requests `google.com/search`:

| Layer | What it adds | Analogy |
|-------|--------------|---------|
| **Application (HTTP)** | Chrome writes `GET /search?q=pune HTTP/1.1` | Your handwritten letter |
| **Transport (TCP)** | TCP wraps it in a segment, adds port numbers and reliability metadata | Envelope with sender/receiver apartment numbers |
| **Network (IP)** | IP wraps the TCP segment in a packet, adds source and destination IP addresses | Canvas bag with street addresses |
| **Data Link (Ethernet/Wi-Fi)** | The packet is wrapped in a frame with MAC addresses | Truck with route labels |
| **Physical** | The frame becomes electrical signals or radio waves | The actual plane/truck in motion |

At Google's end, everything unwinds in reverse. Radio waves → frames → packets → segments → the HTTP request. Google's web server reads it, computes the result, and sends a response back through the same layering in reverse.

**Why is layering so powerful?** Because each layer can be **swapped independently** without breaking the others:

- You can run the same HTTP over Wi-Fi, Ethernet, fiber, 5G, or satellite. Upper layers don't care what the physical medium is.
- You can run totally new application protocols (MCP, gRPC, WebSockets) on top of the same TCP/IP.
- When IPv4 ran out of addresses, engineers designed IPv6 — and most applications didn't need to change at all, because the change happened only at the IP layer.

Separate concerns, define clean interfaces between them, and each piece can evolve independently. Layering gave us a system that has survived and grown for 50 years without ever needing to be redesigned.

## 7. The application-layer zoo

On top of TCP/IP lives a whole ecosystem of **application-layer protocols**. Each solves one specific problem:

| Protocol | What it does | Example |
|----------|--------------|---------|
| **HTTP / HTTPS** | Request and return documents (web pages, APIs) | Your browser loading a page |
| **DNS** | Translate human names (google.com) → IP addresses | Before Chrome can connect, it asks DNS "where is google.com?" |
| **SMTP / IMAP** | Send and receive email | Your email client |
| **SSH** | Encrypted remote terminal | SSH'ing into a server |
| **FTP** | File transfer | Uploading files to a server (older) |
| **WebSocket** | Persistent two-way connection for real-time apps | Chat apps, live dashboards |
| **gRPC** | High-performance structured RPC between services | Modern microservices |
| **MCP** | **How AI models talk to external tools ← the new one** | Claude Code talking to workspace-mcp |

All of these run on top of TCP/IP. They differ in *what* they let you do, not in *how* bytes get from A to B.

## 8. MCP — the newest member of the family

**MCP = Model Context Protocol.** Anthropic published it in late 2024. It is, literally, a protocol — the exact same category of thing as HTTP and SMTP and SSH. It just solves a new problem that didn't exist until AI agents became useful.

**The problem MCP solves:**
Before MCP, if you wanted Claude to read your Gmail, someone had to write custom glue code connecting Claude to Gmail's API. If you also wanted Claude to query your PostgreSQL database, another custom glue piece. Browse the web, another one. Every tool integration was a bespoke, handwritten bridge. Thousands of engineers were re-solving the same problem in slightly different ways.

Anthropic looked at this and made the same argument Vint Cerf made in 1974, applied to AI agents:

> *"What if we defined an open, vendor-neutral protocol for AI agents to discover and use tools? Then you write a 'Gmail tool server' once, and every MCP-capable AI can use it."*

Notice the echo: **open, vendor-neutral, layered.** Same principles, new layer.

**MCP architecture** has two roles:

- **MCP Server** — a program that exposes some capability. "I can read Gmail." "I can query this database." "I can control a browser." Each server is written once and works for every MCP client.
- **MCP Client** — a program that wants to *use* those capabilities on behalf of an AI model. Claude Code is one example. Claude Desktop is another.

**The protocol itself** defines:
- How a client discovers what a server offers ("list your tools")
- How it invokes them ("call the tool named `read_email` with arg `inbox`")
- How results come back (structured JSON)
- How errors are communicated
- How the connection is set up and torn down

Same categories as any other protocol — handshake, messages, responses, error handling. Nothing new *in concept*. New only in what it enables.

## 9. What `workspace-mcp` actually is, in full layered view

The process that caused the port 8000 conflict — PID 54665, `workspace-mcp` — is an **MCP server**. It was started by Claude Code at the beginning of the session. It exposes capabilities like "read Gmail messages," "search Drive files," "edit a Google Doc."

When I ask Claude to look something up in Gmail, here's what actually flows across layers:

1. **Tool use layer**: Claude decides it needs `search_gmail_messages`. It formats an MCP tool call.
2. **MCP layer**: The tool call becomes a JSON-RPC message like `{"method": "tools/call", "params": {"name": "search_gmail_messages", ...}}`
3. **HTTP layer**: That JSON-RPC message gets wrapped in an HTTP POST request to `http://localhost:8000/...`
4. **TCP layer**: HTTP gets chopped into TCP segments, each with port 8000 as destination
5. **IP layer**: TCP segments get wrapped in IP packets addressed to `127.0.0.1` (localhost)
6. **Loopback**: Because it's localhost, the OS short-circuits — no Wi-Fi, no network cable. The packet goes straight to workspace-mcp.
7. **Back up the stack** at the receiving end: IP unwraps → TCP unwraps → HTTP unwraps → MCP unwraps → workspace-mcp reads the tool call and decides to reach out to Google's Gmail API.
8. **Another full stack trip** — workspace-mcp now makes its *own* HTTPS request to Google's servers in California, going through all the layers again, this time actually leaving the Mac over Wi-Fi → router → ISP → submarine cable → Google data center.
9. Google returns the emails, the response unwinds through all the layers, eventually workspace-mcp hands Claude a structured result.

**Every single hop is a protocol.** And every protocol is an agreement someone wrote down so that two independently-built programs could successfully exchange data. Without that stack of agreements, none of this works.

The incredible thing: when I write code to use an MCP tool, I don't think about any of the layers below MCP. TCP/IP just... works. That's the whole value of layering — the lower layers disappear from your mental workspace.

## 10. How to actually build intuition for all this

Three principles that work for understanding any protocol you'll ever encounter:

### Principle 1: "Every protocol exists because of a specific problem."

When you encounter any protocol — HTTP, SSH, DNS, MCP, anything — the first question is always: *what problem was the world trying to solve when someone invented this?* Once you see the problem, every feature becomes obvious. TCP's acknowledgments exist because IP drops packets. DNS exists because humans can't memorize IP numbers. MCP exists because writing custom glue for every AI tool doesn't scale. Features are never arbitrary — they are answers to real problems.

### Principle 2: "Stay at one layer at a time."

When writing application code, you don't think about TCP segments. When debugging a TCP problem, you don't think about Ethernet frames. When writing an MCP tool, you don't think about HTTP. The whole reason the stack was designed this way is so you can focus on *one layer* and trust the layers below.

Corollary: when something breaks, figure out *which layer* is broken. "The MCP tool isn't working" could be an issue at the tool-use layer, the MCP layer, the HTTP layer, the TCP layer, the IP layer, or the physical layer (did Wi-Fi drop?). Debugging is a vertical walk through the stack, checking each layer in turn.

### Principle 3: "Open protocols eat proprietary ones."

Historical pattern, over and over:
- TCP/IP ate IBM's SNA and DEC's DECnet
- HTTP ate Gopher and proprietary document formats
- Open-source databases ate Oracle
- **MCP is now in the process of eating proprietary AI tool integrations**

If you're trying to predict which technologies will win in a new space, bet on the open, layered, vendor-neutral one. It may start weaker, but over years it accumulates an ecosystem that closed competitors can't match.

This is directly relevant to my own work. **MegaFuse should be built on open standards wherever possible.** Every time I consider a proprietary lock-in, ask: "is this the TCP/IP of its space, or the SNA?"

## 11. Where this sits in the CS curriculum

This is the content of **Year 2–3: Computer Networks.** Canonical textbooks:

- **Kurose and Ross — Computer Networking: A Top-Down Approach** — starts at HTTP and works downward. Matches first-principles learning style.
- **Tanenbaum — Computer Networks** — the classic heavyweight.
- **Stanford CS144** — free online course where you actually build a working TCP implementation from scratch in C++, segment by segment. The "nanoGPT of networking."

A full networking course typically covers:

1. The layered model
2. Application layer: HTTP, DNS, SMTP, P2P
3. Transport layer: TCP in depth (flow/congestion control), UDP, sockets
4. Network layer: IP addressing, routing algorithms, BGP, IPv4 vs IPv6, NAT
5. Data link layer: Ethernet, Wi-Fi, switches, MAC addresses
6. Physical layer: signal encoding (brief)
7. Wireless & mobile networks
8. Network security: TLS/HTTPS, firewalls, VPNs, attacks
9. Software-defined networking

## 12. One-paragraph summary

> **A protocol is a pre-agreed set of rules that lets two programs, possibly built by strangers, reliably exchange data. TCP/IP is the foundational pair of protocols for the internet: IP delivers raw packets between machines by IP address (unreliably), and TCP runs on top of IP to build reliable, ordered, error-checked byte streams between specific programs (using ports). The whole internet is layered: physical → data link → IP → TCP → application. Application-layer protocols like HTTP, DNS, SSH, and now MCP all ride on top of TCP/IP — they differ in what they let you do, not in how bytes move. MCP is the newest example: an open, vendor-neutral protocol for AI agents to use external tools, born from the same engineering philosophy (open, layered, vendor-neutral) that made TCP/IP win 50 years ago. That same philosophy will almost certainly make MCP the dominant standard for AI tool integration, and it is a useful pattern to recognize when evaluating any technology.**

---

**Natural next topics** (pick whichever is most interesting):
- *How does a packet actually find its way across the internet — routing, BGP, submarine cables?*
- *What is HTTPS and how does encryption actually protect data in flight?*
- *Sockets — the programming interface that applications use to talk to TCP/IP.*
