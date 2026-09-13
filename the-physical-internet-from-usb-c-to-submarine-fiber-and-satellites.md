# The physical internet — from USB-C to submarine fiber and satellites

**Context:** This sits one layer below [TCP/IP](tcp-ip-protocols-and-how-mcp-fits-in.md) and [ports/IP](ports-ip-addresses-and-localhost-from-first-principles.md). Those entries are about how computers *agree* to talk; this one is about the *physical medium* the data actually travels through — copper, glass, or radio. The sections below follow the questions in the order they came up, so the arc reads the way the curiosity unfolded: starting from "why does my laptop have an RJ45 port at all" and ending at "why doesn't satellite internet just work like satellite TV."

---

## 1. Why use LAN cables at all? Why not just USB-C everywhere?

USB-C can hit 40 Gbps on USB4, faster than most home Ethernet. So speed isn't why my laptop has a separate RJ45 port — USB and Ethernet were designed for completely different problems.

- **Distance.** Standard USB-C maxes out around 1 m for full-speed signalling; active cables stretch to maybe 4–5 m before signal integrity collapses. Ethernet (Cat 5e/6) runs cleanly to 100 m on cheap copper, and fiber variants run kilometers. The ISP-to-router-to-wall wiring in a building is dozens or hundreds of meters of cable — USB physically cannot do that without expensive repeaters every few meters.
- **Topology.** USB is host-device. There's a "master" (the laptop) and "slaves" (mouse, drive). Plugging two USB hosts together to talk as peers requires special bridge chips. Ethernet was designed from day one as **peer-to-peer**: any node can talk to any other, with built-in MAC addressing, collision handling, and switching. That's the entire foundation of how the internet works. Reinventing that on USB would mean rebuilding Ethernet on top of it.
- **Electrical isolation.** Ethernet uses differential signalling on twisted pairs, with small transformers (magnetics) that **galvanically isolate** each end. A lightning surge on the cable doesn't fry the router because the isolation contains it. USB has a direct electrical connection — fine for a desk, dangerous between buildings or even between rooms with different ground potentials.
- **Infrastructure inertia.** 40+ years of standardisation on RJ45 jacks, Cat-whatever cabling, switches, and Ethernet framing. Every data center, ISP backbone, and office wiring closet is built on it. USB-C connectors are also far more fragile than RJ45 — not rated for the plug cycles or vibration that fixed infrastructure demands.

In a sense the laptop *does* use USB-like signalling for networking — across centimeters of PCB between the Ethernet/Wi-Fi chip and the CPU. The moment data has to leave the laptop and cross a room, building, or city, the protocol has to change.

---

## 2. So why does the USB signal drop at one meter while Ethernet runs 100?

The reason came down to physics, and it's surprisingly clean.

**Copper is a low-pass filter.** Any copper cable attenuates higher frequencies more than lower ones, mainly due to two effects:

- **Skin effect** — at high frequency, current crowds onto the surface of the wire, raising the effective resistance.
- **Dielectric loss** — the plastic insulation absorbs more energy at higher frequencies.

The higher the signalling frequency, the more dB lost per meter. So the question really is: at what frequency does each protocol actually send its bits?

- **USB 3.0** sends at a **5 GHz baud rate** over a single differential pair. USB 3.2 doubles that. USB4 pushes to 20 GHz.
- **Gigabit Ethernet** runs at only **125 MHz** per pair — about **40× lower frequency than USB 3.0**.

How does Ethernet still move 1 Gbps at 125 MHz? Two tricks:

- **Four twisted pairs in parallel**, all transmitting simultaneously in both directions, with echo cancellation to separate transmit from receive. USB high-speed lanes typically use one pair per direction.
- **PAM-5 encoding** — instead of "high or low" per clock tick, each symbol carries one of five voltage levels. More bits per Hz, so it can run at a much lower frequency for the same throughput. 10 Gigabit Ethernet pushes further with PAM-16 and DSP-heavy equalisation, still topping out around 400 MHz on the wire.

**Cable construction matters too.** Cat 6 uses solid 23 AWG copper with each pair twisted at a *specific, different* rate to cancel crosstalk and reject EMI, engineered to controlled 100-ohm impedance along the whole length. USB-C cables are 28–32 AWG on the data lines, much thinner, shorter by design, built for flexibility.

Ethernet receivers also do heavy **adaptive equalisation** — a DSP that learns the cable's frequency response and inverts it, essentially undoing the attenuation. This recovery is much harder at USB's frequencies because the noise floor has already swamped the signal.

The trade-off is one design dial: USB optimised for **maximum bandwidth on a short, flexible, cheap cable**; Ethernet for **long reach over modest-cost cable with sophisticated signal recovery**. Same physics, opposite choices.

---

## 3. What runs across the oceans — optical or Ethernet?

Submarine cables are **fiber optic**, and have been since the late 1980s. The first transatlantic fiber cable, TAT-8, entered service in 1988 and replaced the copper coaxial cables that had carried telephone traffic since the 1950s.

The "Ethernet vs optical" framing is itself a category error: Ethernet is a *protocol* (how data is framed and addressed), while what's in the cable is the *physical medium*. You can run Ethernet framing over fiber, and most of the internet's backbone does. But the physical layer under the ocean is glass, not copper.

**Why fiber and not copper?** The same physics from section 2, pushed to extremes. Copper attenuates badly over distance, and an ocean crossing is 5,000–13,000 km. The old coaxial cables needed signal repeaters every few kilometers and topped out around 4,000 simultaneous phone calls. Fiber loses only about **0.2 dB per kilometer** at 1550 nm wavelength — hundreds of times better than copper at high frequency.

**Anatomy of a submarine cable** (inside out):

- A few dozen optical fibers, total cross-section roughly the diameter of a pencil.
- A copper or aluminum tube carrying high-voltage DC (often 10,000+ V).
- Steel wires for tensile strength.
- Polyethylene insulation.
- A tar-soaked outer layer.
- Armor wire on shallow-water sections exposed to anchors and trawls.

The high-voltage DC powers **optical amplifiers** spaced every ~50–100 km along the cable. These are usually Erbium-Doped Fiber Amplifiers (EDFAs) — clever devices that pump energy directly into the existing photons rather than converting back to electrical and re-transmitting. They need power, and the only practical way to deliver it across 10,000 km of seabed is to push DC down the cable itself from landing stations on each end.

**Capacity per cable.** Google's Dunant (transatlantic, 2021) carries ~250 Tbps. Microsoft and Meta's MAREA carries ~200 Tbps. They achieve this with **wavelength-division multiplexing (DWDM)** — sending many different colors of light down the same fiber simultaneously, each carrying its own data stream, separated at the other end. Each fiber pair carries 100+ wavelengths.

About **550+ active submarine cables** worldwide, carrying roughly **99% of international internet traffic**. Satellites handle the remaining sliver.

---

## 4. Sharks, anchors, length, ocean-floor pressure — what actually threatens these cables?

This was the question where my intuition was most wrong, and the answers were the most satisfying.

**Length.** Not millions of km. The longest, SEA-ME-WE-3, is ~39,000 km — close to one Earth-circumference. Most transoceanic cables are 6,000–13,000 km. The *total* length of all submarine cables on Earth combined is around 1.4 million km, but no single cable is anywhere near that.

**Sharks — not a myth, but overstated.** Sharks really did bite cables, especially in the 1980s, possibly attracted by EM fields from the power conductors. Vulnerable sections were re-wrapped in Kevlar-like sheathing. Statistically today, sharks are a minor cause of damage. The real culprits are humans: **fishing trawlers dragging nets** and **ships dropping anchors** account for roughly two-thirds of all cable faults. Underwater landslides, earthquakes, and abrasion against rocks make up most of the rest. About 100–150 cable faults globally per year.

**The internet doesn't break on a single cut.** With 550+ cables and traffic between any two regions running over many of them, a single cut auto-reroutes within milliseconds. There's a specialised fleet of **~60 cable-repair ships** stationed around the world. They grapple the broken cable up from the seabed, splice in a new section, and lay it back down. A typical repair takes days to weeks. The exception is places with few cables — Tonga lost most of its internet for over a month when its single submarine cable was severed by a volcanic eruption.

**Where the cables sit.** Depends on depth:

- **Shallow water (≤1,500 m)** — cables are *buried* 1–3 m deep in trenches dug by ploughs towed behind cable-laying ships, specifically to protect them from anchors and fishing gear.
- **Deep ocean (>1,500 m)** — they lie on the seabed under their own weight, draped over underwater mountains and across abyssal plains. Burying is impractical and unnecessary; almost nothing down there can damage them. Cable-laying ships use detailed bathymetric maps to plan routes that avoid undersea volcanoes, steep slopes, and known seismic zones.

They don't float — they're considerably denser than water.

**Pressure — this is the cool part.** At an average ocean depth of ~3,700 m, water pressure is about 370 atmospheres (~5,400 psi). The Mariana Trench exceeds 1,000 atmospheres. That sounds catastrophic, but: **pressure is only a problem if there's a pressure differential**. A submarine has air inside at 1 atm and seawater pushing in at hundreds — that's why submarine hulls have to be massively reinforced. A submarine cable, by contrast, is **solid all the way through**. There is no air pocket inside. Glass, copper, steel, and polyethylene are all incompressible solids packed tightly. The water pushes uniformly on every side and the cable just sits there. The cable doesn't care about absolute pressure — only about pressure *gradients across a void*, which don't exist inside a solid cable.

The repeaters and optical amplifiers *are* sealed pressure vessels, since they contain electronics that need to be protected from seawater. Those housings are machined from solid beryllium-copper or titanium and rated for 25+ years at full ocean depth.

---

## 5. If fiber is so good, why isn't it everywhere? Why use Ethernet cables at all?

We *are* moving in that direction — fiber is steadily replacing copper everywhere it makes economic sense. But there are real reasons copper Ethernet still dominates the last few meters, and one of them is a feature fiber simply cannot match.

- **Cost at the endpoints.** A fiber port needs a *transceiver* — a laser, photodiode, and driver electronics — at each end. A basic 10 Gbps fiber transceiver costs $30–100. A copper Ethernet PHY chip is a few dollars; the RJ45 jack is stamped metal. Across hundreds of ports in a building, or in a $400 laptop, the difference matters.
- **Termination and repair.** Cut a copper Ethernet cable and a $20 crimping tool puts a new RJ45 on in three minutes. Field-terminating fiber needs either a *fusion splicer* ($3,000–10,000 to align and melt glass cores with sub-micron precision) or pre-polished connectors with mechanical splices that are finicky and lossy.
- **Fragility.** Fiber is glass. It has a minimum bend radius — bend too tight and the light leaks out or the fiber cracks. Copper twisted-pair tolerates being yanked, stepped on, stapled, and threaded through tight conduits in ways that destroy fiber.
- **Power over Ethernet — the killer feature.** PoE delivers up to **90 W** down the same Ethernet cable that's carrying data. This powers VoIP phones, ceiling-mounted Wi-Fi access points, security cameras, door access controllers, even some LED lighting. One cable, no separate power supply, no electrician needed at the device end. **Fiber carries light, not electrons — it cannot deliver power.** A separate power cable would defeat most of the convenience. This single feature keeps copper Ethernet in office buildings indefinitely.
- **Devices don't have fiber ports.** Laptops, phones, printers, smart TVs, game consoles, IoT — all Wi-Fi or RJ45. Adding fiber means adding a transceiver to every device, raising BoM and complicating industrial design.

**Where fiber has won:** undersea cables, intercity backbones, between data center buildings, between rooms in large data centers, ISP central office to the neighborhood, and increasingly fiber-to-the-home (FTTH). Within data centers, fiber has displaced copper for almost any link longer than a rack.

**The trend.** Twenty years ago fiber stopped at the ISP's central office and DSL/coax carried the last few km. Today fiber often runs straight to a box on the house. Inside the house, copper or Wi-Fi takes over. Within another decade or two, fiber may go all the way to a small media converter near the router, and the wired drop to devices may disappear into Wi-Fi 7/8 and beyond.

We use both, each where it makes sense. Fiber for distance, bandwidth, and immunity to interference. Copper for the last short hop, where its low cost, ruggedness, easy termination, and PoE give it advantages fiber can't match.

---

## 6. Detour — is the average ocean depth really only 3.7 km?

When the pressure discussion mentioned 3,700 m average depth, my intuition pushed back hard — I thought oceans were tens or hundreds of km deep. Turns out 3.7 km is correct, and "hundreds of km" is geologically impossible.

- **Average ocean depth: ~3,700 m (3.7 km).** Well-established from sonar mapping of the seafloor.
- **Deepest known point — Challenger Deep, Mariana Trench: ~10,935 m (~10.9 km).** The absolute deepest spot anywhere in Earth's oceans.

**Why hundreds of km can't be right.** Earth's crust is only about **5–10 km thick under the oceans** (30–50 km under continents). Below that is the mantle — solid hot rock. If the ocean were "hundreds of km" deep, it would punch straight through the crust into the mantle. Even the Mariana Trench at 11 km is just barely deeper than the oceanic crust is thick in most places; it exists because of subduction, where one tectonic plate is being pushed under another.

**A few scale references that make 11 km feel right:**

- Driving 11 km on a highway takes ~6–7 minutes. The depth of the Mariana Trench is shorter than the morning commute.
- **Mount Everest is 8.85 km tall.** Drop Everest into the Challenger Deep and its peak is still **~2 km underwater** — the tallest mountain on Earth would disappear into the deepest trench.
- Commercial airliners cruise at 10–12 km altitude. The deepest ocean is roughly the same distance below sea level as a passenger jet is above it.
- Earth's radius is **6,371 km**. Average ocean depth is **0.06% of that**. If Earth were shrunk to a basketball, the oceans would be a layer thinner than a sheet of paper on the surface.

**Specific depth numbers worth knowing:**

| Feature | Depth |
| --- | --- |
| Continental shelves (near coastlines) | 0–200 m |
| Average ocean depth | 3,700 m |
| Mid-ocean ridges | ~2,500 m below sea level |
| Abyssal plains | 4,000–6,000 m |
| Ocean trenches (subduction zones) | 6,000–11,000 m |
| Challenger Deep (deepest point) | 10,935 m |

Only about **1% of the ocean is deeper than 6,000 m**. The trenches are exceptional features, not the norm. The misconception likely comes from confusing ocean depth with the depth we've drilled into Earth (the Kola Superdeep borehole reached 12 km) or from sci-fi visualisations of bottomless trenches. The ocean is vast horizontally — 71% of Earth's surface — but vertically it's a thin film.

---

## 7. Then why lay so many cables at all — why not just use satellites or radio? Mobile towers use radio, right?

Mobile towers *do* use radio — but only for the **last hop**. Even a mobile call rides on fiber for almost its entire journey. The radio part is just from phone to nearest tower (1–5 km); the tower has fiber backhaul to the rest of the network. Wireless is unbeatable for the last few kilometers and terrible for the whole internet. Six constraints, each decisive on its own:

**Bandwidth gap.** A single modern submarine cable carries ~250 Tbps. A Starlink satellite carries about 20 Gbps total, shared across hundreds or thousands of users in its coverage footprint. So one undersea cable ≈ **10,000+ Starlink satellites of capacity**. There are 550+ cables. Aggregate international internet traffic is around 1 petabit/sec; satellites carry well under 1%.

**Radio spectrum is a finite shared resource.** Wireless uses chunks of the electromagnetic spectrum, and there's only so much usable spectrum to go around. Lower frequencies (good for range and obstacle penetration) are crowded with TV, radio, military, aviation, and cellular allocations. Higher frequencies have more bandwidth but don't travel as far or penetrate obstacles. **Every wireless system on Earth shares this same finite spectrum.** Fiber doesn't have this problem — each cable has its own private "spectrum" inside the glass. Want more capacity? Lay another cable. You can't lay more spectrum — there's only one electromagnetic spectrum and everyone shares it.

**Latency depends on which satellite.** Geostationary satellites at 36,000 km altitude give ~240 ms minimum round-trip — before any processing. Makes video calls miserable, gaming unplayable. LEO satellites like Starlink at ~550 km bring latency to 20–40 ms, competitive with fiber. So LEO has solved latency, but at the cost of needing *thousands* of satellites. Fiber across the Atlantic is ~60 ms each way — still latency-competitive with LEO for most routes.

**Weather and atmosphere.** High-frequency radio (necessary for high bandwidth) gets attenuated by rain, snow, fog, even humidity. Heavy rain can knock out satellite links — "rain fade." Solar storms disrupt them. Fiber sealed inside a cable on the ocean floor doesn't care.

**Cost per bit.** A submarine cable costs $100–500M to lay but operates for 25 years carrying hundreds of Tbps continuously. Per gigabyte transferred, fiber is **orders of magnitude cheaper** than any wireless option. Satellites are expensive to build, expensive to launch, have 5–7 year LEO lifespans, and deliver much lower capacity per dollar.

**Earth's curvature blocks terrestrial radio.** Radio waves mostly travel in straight lines and don't bend around the planet. To cover a continent with cell towers you need thousands of them, each connected by fiber backhaul. To cover an ocean — there's nothing to put a tower on. Satellites solve the line-of-sight problem by getting high enough to see a wide area, but then you're back to bandwidth, latency, and spectrum constraints.

**Why mobile networks work the way they do.** The phone connects wirelessly to a tower 1–5 km away. The tower has a fiber connection back to the carrier's network, which connects to the broader internet through more fiber. The wireless part is only the very last segment, because that's the only part where running a cable to each user is impractical. As soon as you can use fiber, you use fiber.

---

## 8. What about the future? Won't Starlink eventually replace cables and Jio/Airtel?

Honest answer: no, not even close, and probably not ever. The math is striking.

**Capacity at full Starlink build-out.** ~7,000 satellites today; SpaceX's target is ~40,000. Each satellite carries roughly 20 Gbps. Full constellation:

```
40,000 satellites × 20 Gbps = ~800 Tbps total global capacity
```

A single new submarine cable like Bifrost or Topaz carries 250+ Tbps. The full submarine cable network carries on the order of **1,000,000 Tbps (≈ 1 exabit/sec)**. Starlink at full build is **less than 0.1%** of that.

Worse: Starlink's capacity is shared globally and constrained by spectrum, while submarine cables can be added indefinitely. If more capacity is needed, lay more cables. You cannot just "add more spectrum" — it's a fixed natural resource.

**Two hard ceilings on scaling satellites up:**

- **Spectrum.** Satellite-to-ground uses Ku, Ka, and V bands, heavily regulated and shared with other services worldwide. Packing more satellites doesn't help if they interfere on the same frequencies. The total information moveable from space to Earth is bounded by `available spectrum × ground area`, not by satellite count.
- **Orbital congestion (Kessler syndrome).** 40,000 satellites in LEO is already raising serious collision and debris concerns. 400,000 is unthinkable. There is a hard ceiling on how big these constellations can get.

**Why Jio/Airtel won't be replaced either.** Three reasons:

- **Phones can't talk to satellites well.** Phone antennas and batteries are tiny. Existing direct-to-cell services (Starlink + T-Mobile, AST SpaceMobile) currently deliver kilobits/sec — enough for emergency texts, not for video calls. The signal has to travel hundreds of km to a satellite versus 1–5 km to a cell tower, with limited transmitter power.
- **Indoor coverage is dismal.** LEO satellite signals struggle to penetrate buildings. Phones work inside offices because nearby towers blast strong signals at relatively low frequencies. Satellites cannot replicate that without enormous ground antennas.
- **Density math.** Mumbai has ~21 million people in a relatively small area. If they all tried to stream video through satellites overhead, a few satellites would have to deliver hundreds of Tbps to one city. They cannot. Cell towers work because each serves a few hundred meters to a few km, and there are millions of them. You cannot replicate that density from space.

**Economics are inverted for dense areas.** Starlink works because rural Alaska has so few people that nobody wanted to lay fiber. In Mumbai or Bangalore, terrestrial infrastructure serves millions of users per km² at a fraction of the per-user cost of satellites. Jio's 5G rollout reaches hundreds of millions; Starlink in India will likely serve at most a few hundred thousand.

**What Starlink will change.** Genuinely transformative for specific use cases:

- Rural and remote areas fiber and cell towers haven't reached economically (large parts of rural India, Africa, Latin America, mountainous regions).
- Ships, aircraft, trains — anything moving across regions.
- Disaster recovery when terrestrial networks fail (as in Tonga's volcanic eruption).
- Backup connectivity for businesses that can't tolerate outages.
- Direct-to-cell as an emergency fallback — phones won't lose all connectivity in remote areas.

**Cell carriers are often Starlink's customers, not its competitors.** Jio and Airtel both need ways to extend coverage to remote villages economically. Running fiber and building towers in remote Rajasthan or the Northeast is expensive; buying satellite backhaul is cheaper. Jio is already partnered with SES, Airtel with OneWeb. The future is hybrid: cell towers in cities, fiber backbones across continents, satellites filling gaps and serving mobile users.

**On submarine cables specifically — even more decisively no.** The capacity ratio is so lopsided that there's no realistic path. The opposite is happening: as satellite constellations grow, they need *more* ground-side fiber to connect their ground stations to the rest of the internet. Starlink itself depends on submarine cables.

Submarine cable construction is actually accelerating. Google, Meta, Microsoft, and Amazon are all building their own cables right now.

---

## 9. But satellite TV (Tata Sky, Dish TV) delivers HD video to millions of homes — so why doesn't satellite internet just work the same way?

This was the question that felt cleverest to ask, and the answer turned out to be the most fundamental in the whole conversation. The single key distinction is **broadcast vs unicast**, and once you see it, everything else clicks.

**Satellite TV is broadcast.** When Tata Sky transmits channel 555 showing a cricket match, it sends out **one** signal — and every dish in the satellite's footprint receives the same signal at the same time. Whether 1 person or 100 million people are watching, **the satellite uses exactly the same bandwidth**. 500 TV channels at ~5 Mbps each = ~2.5 Gbps of total downlink, serving an entire country at once. Very tractable.

**Internet is unicast.** Every user requests unique data. My YouTube stream is different from my neighbor's. My aunt is on a video call; my kid is downloading a game. The network has to deliver a **separate** stream to each user. To serve 1 million internet users at a modest 25 Mbps each, the satellite needs **25,000,000 Mbps = 25 Tbps** simultaneously — roughly **10,000× more bandwidth** than broadcasting 500 TV channels. Physics can't support it.

That one difference — *1 stream serving N viewers* vs *N streams for N users* — explains why one medium scales beautifully from space and the other doesn't.

**Two further differences:**

- **TV is one-way; internet is two-way.** A Tata Sky dish only *receives*. The internet fundamentally needs an uplink for every web request, every Zoom frame, every search query. Transmitting up to a satellite is much harder than receiving from one — the satellite is far away and ground equipment has limited power and antenna size. That's why old satellite "internet" used a satellite downlink plus a regular phone line uplink. And it's why Starlink terminals cost $500–600 versus a ~$30 TV dish — they need a phased-array transmitter.
- **Modern internet is fundamentally personalised.** Netflix, YouTube, Hotstar — nobody tunes in at 8 pm to watch what's showing. People watch what they want, when they want. Even TV became unicast. The moment communication is personal, broadcast economics break down.

**Could you do broadcast-style internet?** In principle yes, and CDNs already do an analogous thing on the ground by caching popular content close to users. For live sports, breaking news, or really popular content, broadcast satellites could in theory deliver to millions of receivers efficiently. But the everyday internet is on-demand and personalised. Once communication is personal, broadcast economics break.

So Tata Sky works precisely because of what TV *isn't*: it isn't personal. The internet is, and that's why we need cables.

---

## 10. The architecture that emerged

Tracing the questions in order builds a picture the original "USB vs LAN" question never hinted at. The physical internet is layered:

- **Wired fiber backbone** — submarine cables across oceans, terrestrial fiber across continents and into neighborhoods. The high-capacity arteries.
- **Cell towers and copper Ethernet** — the local access layer. Cell towers reach a few km wirelessly; copper Ethernet runs the last 100 m and delivers PoE. Every cell tower has fiber backhaul.
- **Satellites** — the gap-filler. Genuinely valuable for rural areas, ships, aircraft, disaster recovery, military use, and broadcast applications. *Complement* terrestrial networks; don't replace them.

Each layer exists because of constraints the others can't satisfy. USB-C is great at the desk and useless across a building. Copper Ethernet is great inside a building and useless across an ocean. Fiber is great across an ocean and impractical to terminate at every device. Wireless is essential for the last mile and incapable of handling the backbone. Satellites are essential for the gaps and incapable of replacing the cables.

If submarine cables were replaced with satellites, we'd need millions of them, the spectrum couldn't physically support it, and the modern internet — streaming video, cloud computing, real-time everything — would collapse back to dial-up speeds. The architecture isn't accidental.
