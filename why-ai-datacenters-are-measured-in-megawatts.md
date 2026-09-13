# Why AI Datacenters Are Measured in Megawatts

**Context:** Every announcement about AI infrastructure is denominated in power — a 1 GW campus, a 250 MW cluster. That struck me as odd. A datacenter is full of computers, so why is the headline number an electricity figure rather than a compute figure? The answer is that **power is the thing actually being rationed**, and following that led into grid interconnection queues, a set of very strange corporate deals, and a genuinely different picture of the constraint in India.

---

## 1. Why power, and not FLOPS or GPU count

Three reasons, and the third is the one that convinced me.

**Because it's what's scarce.** Chips, racks, land, and fibre are procurable or scalable. Megawatts at the meter are not. Grid interconnections in the US take four to seven years to approve. GPUs ship in months; a new 500 MW substation does not.

**Because power converts cleanly into compute.** Current accelerators draw roughly 0.7–1 kW each, and a dense rack lands around 120 kW. After cooling overhead, a gigawatt of facility load works out to somewhere around a million high-end GPU-equivalents. So "5 GW" is shorthand for "about five million GPUs' worth of capacity" — an honest translation, not marketing.

**Because a watt survives generational churn, and nothing else does.** This is the good reason:

- **FLOPS depend on precision.** A number quoted at FP4 isn't comparable to one at FP8 or FP16, and vendors quote whichever flatters them.
- **GPU counts go stale every 18 months.** "100,000 GPUs" means something completely different across two generations.
- **A watt is a watt.** It's the only unit that lets you compare a 2024 facility with a 2028 one on equal footing.

That's the part I'd underrated. The industry didn't pick megawatts for drama. It picked the one unit that doesn't need a footnote about which hardware generation and which numeric precision you meant.

**And the economics are denominated in power too.** Electricity is 30–50% of five-year total cost of ownership. AI-grade construction runs tens of millions of dollars per megawatt, several times traditional datacenter cost. Power purchase agreements are negotiated in MW. When the capital plan, the operating cost, and the physical constraint are all in the same unit, that unit wins.

The framing flipped around 2023. Before, people said "100,000 GPUs." After, they say "1 GW" — because the moment power became the binding constraint, that's what everyone started planning, financing, and bragging in.

---

## 2. What a "grid interconnect" actually is

I'd assumed this meant buying electricity. It doesn't.

**You're buying the right to extract a specific load at a specific point on the grid, plus the upgrades needed to make that safe.** The package has four parts:

1. **Physical infrastructure** — a dedicated substation, high-voltage transformers, protective relays, metering, switchgear, and a transmission line tap.
2. **Studies** — system impact, facilities, and affected-systems studies, where engineers model whether the grid can absorb the load without voltage collapse or thermal violations.
3. **Legal agreements** — a multi-hundred-page interconnection agreement specifying who pays for which upgrades.
4. **Permits** — federal environmental review, state siting approval, local zoning and easements.

The reframe that stuck: a large new load is not a customer, it's a **modification to the grid.** The grid was planned around a demand forecast, and dropping a gigawatt onto one node invalidates that plan locally. The four-year process is the cost of re-planning.

---

## 3. Why it takes 4–7 years in the US

Five bottlenecks that compound:

**Queue backlog.** The major grid operators have hundreds to thousands of gigawatts sitting in interconnection queues — more than the systems they'd connect to. Studies are done in clustered batches, and each cluster cycle is roughly two years.

**Transmission build-out.** New high-voltage lines take 8–12 years. Right-of-way acquisition and eminent-domain litigation eat years, and essentially no new ultra-high-voltage capacity has been built in the US in the last decade.

**Equipment lead times.** Large power transformers run 2–4 years, from only a handful of qualified manufacturers worldwide. Switchgear is 18–30 months. This one surprised me most — the constraint isn't only regulatory, it's that **the world's ability to manufacture large transformers is finite** and was sized for a slower-growing grid.

**Regulatory layering.** Federal, state, grid-operator, environmental, and local jurisdictions overlap with no single decision-maker. Environmental review alone can be 2–4 years.

**Litigation.** Transmission lines get sued at every jurisdiction they cross.

For a large facility, the binding step is usually transmission upgrades or queue position — **not** the substation itself. The thing you're paying for isn't the thing making you wait.

---

## 4. The strange deals, explained

There's a category of headline that had never made sense to me: a technology company buying the output of a specific nuclear plant, or restarting a shut-down reactor, or co-locating gas turbines with a datacenter.

Read against the interconnection queue, they're all the same move: **behind-the-meter generation, to bypass the queue entirely.**

If you connect to the public grid, you join a multi-year queue and pay for shared upgrades. If you site your load *next to* an existing generator and take power directly, you're not making the same demand on the transmission system, so much of that process doesn't apply. Buying an existing plant's output means the generation and its interconnection **already exist** — you're moving the load to the power instead of moving power to the load.

Which explains why the deals cluster around *existing* nuclear plants rather than new build: the value is the interconnection that's already there and already approved.

The honest framing is that these are **workarounds, not solutions.** They relocate demand rather than adding supply, and there's a finite stock of underused existing generation to attach yourself to. It buys years, not a permanent answer.

---

## 5. India — a different shape of constraint

I wondered whether India would hit the same wall as datacenters scale here. The answer is yes, but the bottleneck has a different geometry: **less a binding wall, more a series of specific pressure points.**

Comparable projects take roughly 1.5–3 years rather than 4–7. The reasons are structural:

- **State governments compete for the investment** rather than merely permitting it, offering fast-track approvals and tariff support.
- **The captive power route** — building your own dedicated generation — bypasses the distribution utility entirely and can be done in 18–24 months.
- **There's genuine headroom.** Substantial underutilized thermal capacity means the existing grid often has room, which is precisely what the US grid lacks.
- **Less federal-state friction** in the approval chain.

The offsetting problems are real but different in kind: the financial weakness of state distribution companies creates payment-security disputes, land acquisition is genuinely hard, and new inter-state transmission corridors still take 3–5 years.

So the comparison isn't "India is faster." It's that **the US constraint is transmission and queue position, while India's is counterparty risk and land** — and the second set is more tractable with money and negotiation than the first is.

---

## 6. What I took away

**The unit an industry measures itself in tells you what's scarce.** Nobody chose megawatts as a marketing device; the accounting migrated to the constraint. That's a general tell worth watching — when the headline metric changes, something about the binding resource changed first.

**"Approval takes four years" is usually five separate problems.** Queue, transmission, equipment manufacturing, jurisdictional overlap, litigation. They compound, and only some are regulatory — the transformer lead time is a manufacturing fact that no amount of permitting reform touches.

**Odd-looking deals are usually rational responses to an invisible constraint.** A software company restarting a nuclear reactor reads as strange until you see the interconnection queue, at which point it's the obvious move. When a decision looks irrational, the usual problem is that I can't see the constraint it's optimizing against.
