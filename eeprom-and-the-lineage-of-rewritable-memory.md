# EEPROM and the Lineage of Rewritable Memory

**Context:** I came across an EEPROM part while looking at a circuit and asked what I actually wanted to know: where is it used, why does it exist, and what's the history? The answer is a clean four-step lineage where **each step exists because the previous one had one specific, painful limitation** — and it ends with the surprise that flash memory, the thing in every phone and SSD, is a variant of EEPROM rather than a separate invention.

---

## 1. The name is a contradiction, and the contradiction is historical

**EEPROM** — Electrically Erasable Programmable Read-Only Memory.

"Read-only memory that you can write to" is a contradiction on its face. The label stuck because of what it *evolved from*: it's a ROM that gained the ability to be rewritten, and the family name never got updated.

Which is a small instance of something I keep meeting — a technical term that was precise when coined and now needs its history to make sense, the same way "static" RAM means a retention property rather than a power property.

---

## 2. What it is mechanically

Each bit is stored in a single transistor with an extra layer: a **floating gate** — a sliver of conductor completely surrounded by insulating oxide. Because it's electrically isolated, any charge placed on it just sits there, in principle for decades.

- **To write:** apply a high voltage that forces electrons to tunnel *through* the insulator onto the floating gate — a quantum-mechanical effect called Fowler–Nordheim tunneling.
- **To erase:** reverse the voltage and tunnel the electrons back off.
- **To read:** the presence or absence of trapped charge shifts the transistor's threshold voltage, which the read circuitry interprets as a 1 or a 0.

**That tunneling step explains everything else about the technology:**

| property | because |
|---|---|
| non-volatile | the charge has nowhere to go |
| wears out (~10⁴–10⁶ cycles) | every tunneling event slightly damages the oxide |
| writes are slow (ms) vs reads (ns) | the high-voltage charge pumping takes time |

One mechanism, three consequences. That's the kind of explanation I look for — you don't memorize the three properties, you remember the mechanism and derive them.

---

## 3. The lineage — each step fixing one specific pain

**Mask ROM (1960s).** The bit pattern was etched into the silicon at the factory using a custom photomask. Cheap at scale, **impossible to change**. Find a firmware bug after the wafer run and you throw out the chips.

**PROM (1956).** Field-programmable via tiny fuses you'd blow with a high-voltage pulse. **One-time write** — once blown, permanent. Better for prototyping, still wasteful.

**EPROM (1971).** The breakthrough: a floating gate in a MOS transistor, with electrons injected by high voltage and removed by **exposing the chip to ultraviolet light** through a quartz window in the package.

Suddenly you could reprogram a chip — but only by pulling it out of its socket, putting it in a UV eraser for twenty minutes, and reprogramming it on a dedicated machine. This is why chips from that era have a little quartz window on top, usually covered with a sticker.

I love this detail because it makes the constraint physical and visible. The window *is* the erase mechanism. You can look at a chip and see what generation of memory technology it belongs to.

**EEPROM (1977).** Solved the UV problem by making the tunneling oxide thin enough — around 100 ångströms — that the floating gate could be erased **electrically** rather than with light.

No UV erasers. No pulling chips out of sockets. **You could rewrite memory while the system was running, byte by byte.** That's a profound change in what an embedded system can do: a device can now update its own configuration, keep a counter across power cycles, or store calibration data it learns about itself.

**Flash (1984).** And here's the part I didn't know: flash is **a variant of EEPROM optimized for cost and density.** It erases in large blocks rather than individual bytes, which lets the cells be packed much more tightly.

Everything in an SSD, a USB stick, or phone storage descends from that 1977 work. **EEPROM is the parent technology; flash is the wildly successful child.**

---

## 4. Why block erasure was the trade that mattered

That last step is worth dwelling on, because it explains a behaviour I'd previously found arbitrary.

EEPROM erases a byte at a time. Flash erases a whole block. Giving up byte-level erasure is what buys the density — fewer control structures per cell — and density is what made mass storage affordable.

But it's why flash storage needs a **translation layer**: writing one logical byte may require reading a whole block, modifying it, erasing it, and rewriting it. The layer that hides this is doing real work, and it's the source of write amplification, wear levelling, and most of what makes SSD firmware complicated.

So a single 1984 design decision — *erase in blocks to get density* — propagates all the way up into why your SSD has a controller with its own processor on it.

---

## 5. Where EEPROM still is

It didn't get displaced by flash; it occupies the niche flash gave up. Small amounts of data that change occasionally and must survive power loss, written a byte at a time:

- device configuration and calibration constants
- serial numbers and identity data
- counters that must persist across power cycles
- small parameter stores in automotive and industrial controllers

That's why the parts are physically tiny and, per byte, expensive — you're not buying capacity, you're buying **byte-level rewritability with decades of retention** in a package that costs cents to place on a board.

Which finally explained a pricing question I'd wondered about: a small EEPROM can cost meaningfully more than a vastly larger flash chip. You're paying for the *access granularity* and the qualification, not the megabytes.

---

## 6. What I took away

**The lineage is a chain of single fixes.** Can't change it → can change it once → can change it with UV and a socket puller → can change it electrically, in circuit, byte by byte → can change it in blocks, densely, cheaply. Each step is one limitation removed, and the last step trades a capability back for density.

**Flash isn't a separate invention.** It's EEPROM with a different erase granularity, and knowing that connects consumer storage directly to a 1977 idea about oxide thickness.

**Physical artefacts encode their constraints.** A quartz window on a chip package is an erase mechanism you can see. That's rarer than it should be — most constraints are invisible — and it's worth noticing when a design makes its own limitation legible.
