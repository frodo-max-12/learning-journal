# Hyperscalers explained — the pyramid of cloud computing

---

## The word, properly defined

A **hyperscaler** is a company that operates data centres at such massive scale that it designs and builds its own infrastructure end to end — servers, networking, cooling, software, and increasingly chips — instead of buying anything off the shelf.

The word is literal. It refers to companies whose computing scale is so large that it operates at *hyper* (extreme) scale: millions of servers, dozens of data centres, hundreds of megawatts to gigawatts of power.

Once I understood this, every news story about AI infrastructure suddenly made more sense. The reason terms like "frontier lab" and "AI capex" feel like they belong to a different conversation than "small business cloud" is because they literally do — they sit at completely different layers of the pyramid.

## The threshold to qualify

There is no committee that certifies hyperscalers. But the rough criteria look like this:

- One million or more servers under management.
- Ten billion or more dollars per year in capital expenditure on infrastructure.
- Multiple regions, each with multiple data centres.
- A custom software stack — your own operating system, networking, storage layers.
- Direct relationships with TSMC, ASML, and energy utilities at the executive level.

Maybe 8 companies on Earth meet this bar. That is the entire club.

## The full list

| Hyperscaler | What they run | Estimated server count |
|---|---|---|
| AWS (Amazon) | EC2, S3, the dominant public cloud | 5M+ |
| Microsoft Azure | #2 public cloud + Office 365 + OpenAI infrastructure | 4M+ |
| Google Cloud + internal | GCP + Search + YouTube + Gemini | 3M+ |
| Meta | Facebook, Instagram, WhatsApp, Reels | 2M+ |
| Apple | iCloud, App Store, services | 1M+ |
| Alibaba Cloud | China's #1 cloud | 2M+ |
| Tencent | WeChat infrastructure | 1M+ |
| ByteDance | TikTok | 1M+ |

That is essentially all of them. Every other company that has cloud infrastructure is, by this definition, a tier below.

## The tier below — large, but not hyperscalers

This second tier is sometimes called "tier-2 cloud" or just "large cloud providers." They are big businesses, but a different category from the eight above.

- **Oracle Cloud, IBM Cloud, Salesforce, SAP** — large public clouds with serious enterprise customers, but at one to two orders of magnitude smaller scale than AWS or Azure.
- **Neoclouds** — a recent category. CoreWeave, Lambda, Crusoe, Voltage Park, Nebius. These are GPU-rental specialists. They have hundreds of thousands of GPUs each, but not the millions-of-servers-across-everything diversification of a true hyperscaler. They are essentially "vertical hyperscalers for AI."
- **DigitalOcean, Linode, Vultr, OVHCloud** — mid-tier clouds focused on developer simplicity or European geography.

## The tier below that — enterprise data centres

This is where most companies actually live.

- Fortune 500 companies running their own data centres (banks, insurance, telcos).
- Universities, governments, defence contractors.
- Anyone running a "private cloud" or on-premises infrastructure.

These customers spend a lot of money on infrastructure but at completely different scales — hundreds of servers per company rather than millions.

## The pyramid as a mental model

I started drawing this pyramid in my head and it explained nearly every weird asymmetry in how the AI infrastructure market behaves:

```
       [Hyperscalers — 8 companies, $300B/yr]
              ▲
       [Neoclouds — ~20 companies, $30B/yr]
              ▲
       [Tier-2 clouds — ~50 companies, $20B/yr]
              ▲
       [AI labs + enterprise AI — ~500 cos, $30B/yr]
              ▲
       [EMS / ODMs — ~50 companies, $20B/yr]
              ▲
       [System integrators — ~thousands, $10B/yr]
```

Total spend in the top ring is **larger than every layer below it combined**. The eight hyperscalers spend roughly $300-400 billion per year on infrastructure. That is the bulk of what the AI capex headlines are pointing at.

But concentration goes the other way. Those eight companies buy from maybe 5-10 vendors directly. The thousands of companies in the bottom layers buy from a fragmented ecosystem.

## Why hyperscalers behave so differently from everyone else

Once you see the pyramid, several things click into place.

**Hyperscalers buy direct from chip designers.** They have the volume and the cash to negotiate billion-dollar contracts with NVIDIA, AMD, Intel, Broadcom, and TSMC directly. They get allocation priority. NVIDIA ships them new GPUs before anyone else.

**Hyperscalers design their own silicon.** Once you cross roughly $10 billion per year in compute spend, the return on investment of designing your own chip flips positive. Below that, you buy merchant silicon. Above that, every dollar saved by going custom multiplies across millions of servers. Every hyperscaler has crossed that threshold and is now actively designing its own chips.

**Hyperscalers operate physical infrastructure at a scale nobody else can.** Thomas Kurian talked about Google "manufacturing data centres instead of constructing them" — they pre-assemble entire racks or rows in factories and deploy them as units. They invest behind the meter for energy generation. They lock in real estate years in advance. None of this is feasible at smaller scale.

**Hyperscalers are not capacity-constrained the way their customers are.** This was the part I found most interesting in the Kurian interview. He explicitly described why Google has TPU capacity to spare while frontier AI labs report being compute-constrained: Google planned for the AI moment many years in advance, owns its own silicon, and operates the physical layer end-to-end. The AI labs are renting from someone else's stack, and that stack costs them more per unit because they cannot capture the silicon margin.

## Why the pyramid matters even if you do not work at a hyperscaler

The single biggest insight from understanding this pyramid: **hyperscaler economics drive almost every other layer's economics, but in inverse ways**.

When hyperscalers design their own ARM CPU, that is one less Intel Xeon they buy. Intel's revenue shifts to other parts of the pyramid. When hyperscalers commit to TSMC for years of leading-edge wafer capacity, that crowds out everyone below them and forces tier-2 clouds and enterprise to use older process nodes.

When hyperscalers consume the lion's share of NVIDIA's H100 and B200 production, the merchant market — neoclouds, AI startups, enterprise AI — is left with whatever allocation remains. This is why "supply" in the AI infrastructure market is not really about how many chips TSMC fabricates. It is about how many chips remain *after the hyperscalers take their share*.

## A different lens — who is and is not a hyperscaler customer

The pyramid also flips standard customer-segmentation thinking.

If you are selling enterprise AI software, the **hyperscalers are your competitors, not your customers**. Their cloud businesses sell the same kind of services you do, often at lower prices.

If you are selling components or hardware, the **hyperscalers are mostly out of reach as customers** — they buy direct, in volume, from designers and fabs. Your real customers are the layers below them.

If you are running an AI lab, you are a **customer of hyperscalers** at the infrastructure layer — you rent their compute. But you are also a competitor at the model layer if you build foundation models.

If you are running a neocloud or a tier-2 cloud, you are stuck in a strange position — you compete with hyperscalers for the same workloads but cannot match their cost structure. You survive by specialising (GPU-only, AI-optimised, lower egress fees, geographic focus).

## The Thomas Kurian interview mapped onto the pyramid

Once I had the pyramid, the interview became readable in a different way.

When Kurian said Google does not have a TPU shortage while other labs are compute-constrained — that is hyperscaler vertical integration showing up. When he said Google can serve TPU demand from Anthropic, OpenAI competitors, capital markets firms, and the Department of Energy at the same time — that is hyperscaler scale. When he described placing TPUs *inside customer data centres* near stock exchanges — that is hyperscaler operational reach. When he said "every CEO makes their own decisions" about hiring versus layoffs — he was implicitly contrasting hyperscaler demand-rich Google against software companies further down the pyramid that face different capacity-versus-demand dynamics.

Almost every weird asymmetry in the AI infrastructure market today traces back to which layer of the pyramid you are talking about. The eight companies at the top operate by completely different rules than everyone below them, because they have completely different scale.

> A hyperscaler is not just a big cloud company. It is a company that, by virtue of scale, can vertically integrate the entire computing stack — chips, servers, data centres, energy, software — and capture the margin at every layer. There are about eight of them. The pyramid below them is everyone else.

---

*This sits underneath [why hyperscalers build their own chips and why Intel lost](why-hyperscalers-build-their-own-chips-and-why-intel-lost.md), which goes deeper on the chip-design side of the pyramid. For the layer below — the actual compute infrastructure being sold — see [what compute actually means](what-compute-actually-means-from-physical-servers-to-ec2.md).*
