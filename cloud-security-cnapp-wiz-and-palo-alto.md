# Cloud Security, CNAPP, and the $32 Billion Wiz Acquisition — understanding a major CS industry segment

*Learned on March 15, 2026. I came across news about Google acquiring Wiz for $32 billion and wanted to understand what Wiz actually does, why it matters, and how the competitive landscape works. The deeper I dug, the more it revealed about how the entire cloud computing industry is structured.*

---

## Starting with the question: what is cloud security, and why is it a separate thing?

When companies move their computing to the cloud — running their applications on Amazon Web Services (AWS), Microsoft Azure, or Google Cloud Platform (GCP) instead of their own physical servers — a new category of security problems emerges.

In the old world, security was relatively straightforward to conceptualize. You had your servers in a room, you controlled who had physical access, you ran firewalls, and you monitored traffic. The perimeter was clear: inside the building was trusted, outside was untrusted.

In the cloud, there is no physical perimeter. Your applications are running on someone else's infrastructure, spread across multiple data centers, often across multiple cloud providers. The code is packaged in containers, deployed through automated pipelines, and scaled up and down dynamically. The attack surface — the number of places where something could go wrong — is vastly larger and constantly shifting.

This is why cloud security became its own category. The traditional tools were not designed for this world.

## CNAPP — the acronym you need to know

The specific market category that companies like Wiz and Palo Alto Networks compete in is called **CNAPP**: Cloud-Native Application Protection Platform. This is an analyst term (coined by Gartner, the research firm that names these categories), and it describes a comprehensive platform that secures cloud-native applications across their entire lifecycle.

What does "cloud-native" mean? It means applications that are designed from the ground up to run in the cloud — using containers (like Docker), orchestrators (like Kubernetes), serverless functions, and microservices. These are not old applications that got "lifted and shifted" to the cloud. They are built differently, and they need to be secured differently.

A CNAPP typically covers several areas that used to be separate products:

| Security Function | What It Does |
|---|---|
| Cloud Security Posture Management (CSPM) | Checks whether your cloud infrastructure is configured correctly — are your storage buckets accidentally public? Are your access permissions too broad? |
| Cloud Workload Protection (CWP) | Protects the actual workloads running in the cloud — containers, virtual machines, serverless functions |
| Cloud Infrastructure Entitlement Management (CIEM) | Manages who (and what) has access to what resources — identity and permissions |
| Infrastructure as Code Scanning | Checks the code that defines your infrastructure for security problems before it is deployed |
| Vulnerability Management | Scans for known vulnerabilities in the software components you are using |

The key insight behind CNAPP is that all of these functions need to be unified. When they are separate tools from separate vendors, you get fragmented visibility — you might know about a vulnerability in a container but not realize that the container has overly broad permissions that make the vulnerability exploitable. A good CNAPP connects these dots.

## Wiz — the startup that leapt to the front

Wiz, founded in 2020 by a team of Israeli cybersecurity veterans (several of whom had previously built and sold a company to Microsoft), took an approach that the industry found compelling: build everything from scratch, in-house, as a single unified platform. Instead of stitching together acquired products, they wrote a single codebase that could see across an organization's entire cloud environment and surface risks in context.

This matters because the alternative — which is what Palo Alto Networks did with its competing product, Prisma Cloud — is to acquire multiple companies and then try to integrate their products into a coherent platform. Acquisition-driven integration is hard. Each acquired product has its own architecture, its own data model, its own user interface. Making them feel like one product takes years, and sometimes never fully works.

Wiz's unified approach gave it a notable advantage. Customers could deploy it and get a single view of their cloud security posture, with risks prioritized by actual exploitability rather than just raw vulnerability counts. In an industry drowning in alerts, the ability to say "these are the three things that actually matter right now" was enormously valuable.

> Wiz's advantage came from building everything in-house as a single platform, while competitors stitched together acquired products. Integration is one of the hardest problems in enterprise software.

## Palo Alto Networks and Nikesh Arora

On the other side of this competition sits Palo Alto Networks, led by CEO Nikesh Arora. Arora has a fascinating career arc that I wanted to understand because it intersects with so many major companies.

Arora was Google's Senior Vice President and Chief Business Officer — described by analysts as effectively "the acting CEO" and one of the most critical leaders in Google's executive management team. He left Google in 2014, not because of a power struggle (as I initially speculated), but for a genuinely staggering offer: he became President and COO of SoftBank, where he received total compensation exceeding $200 million.

After leaving SoftBank, Arora became CEO of Palo Alto Networks, where he has been driving the company's transformation from a traditional firewall company into a comprehensive cybersecurity platform. This is relevant because Palo Alto's Prisma Cloud product is Wiz's most direct competitor.

An important timeline detail: when Arora left Google in mid-2014, Sundar Pichai was Google's Android chief, not yet CEO. Pichai became CEO in 2015 with the Alphabet restructuring. So the two were not really rivals at Google — they operated in different domains (Arora in business and revenue, Pichai in product and engineering). I initially imagined Google's acquisition of Wiz as some kind of revenge move against Arora, but the reality is far more strategic and far less personal.

## Why Google spent $32 billion on Wiz

Google Cloud is the third-place cloud provider, behind AWS and Azure. This is not a comfortable position. The acquisition of Wiz was, as Wedbush analysts put it, "a shot across the bow" at Microsoft and Amazon, both of whom have invested heavily in cloud security.

The strategic logic is clear:

1. **Competitive differentiation.** If Google Cloud can offer the best cloud security platform as a native part of its offering, that is a powerful reason for enterprises to choose GCP over AWS or Azure.

2. **Revenue diversification.** Google's core business is advertising. Cloud is the most promising path to reducing that dependency, and security is one of the highest-value, stickiest parts of the cloud business. Once a company trusts you with their security, they are unlikely to leave.

3. **Market timing.** Cloud security spending is growing faster than almost any other category in enterprise software. Acquiring the market leader at this stage locks in a dominant position.

The $32 billion price tag sounds enormous, but in context, it reflects how valuable the cloud security market is expected to become. Wiz was reportedly generating hundreds of millions in annual recurring revenue and growing rapidly.

## The vendor lock-in question

Here is where it gets interesting. One of Wiz's strengths as an independent company was that it was cloud-agnostic — it worked equally well across AWS, Azure, and GCP. This was essential because most large enterprises use multiple cloud providers.

Now that Wiz is part of Google, customers are asking the obvious question: will it stay truly neutral? Or will Google subtly (or not so subtly) make Wiz work best with GCP?

Nikesh Arora's response to the acquisition was revealing. Rather than sounding alarmed, he said it might actually *help* Palo Alto Networks: "We're happy they're now part of Google, it gives us more room to operate." His reasoning is that some customers who previously chose Wiz for its independence will now worry about Google ownership creating bias toward GCP. Those customers might look to Palo Alto's Prisma Cloud (or other independent vendors) instead.

> When a neutral platform gets acquired by a cloud provider, its neutrality becomes suspect. This is a recurring pattern in enterprise software — independence is a feature, and acquisitions can destroy it.

## What this taught me about the CS industry

This one story — Wiz, Palo Alto, Google, the $32 billion acquisition — is a lens into several important patterns in the technology industry.

First, **the build-vs-buy tension in enterprise software**. Wiz won by building a unified product from scratch. Palo Alto struggled by acquiring and integrating. This same dynamic plays out across the entire software industry. Building from scratch gives you architectural coherence but takes time. Acquiring gives you speed but creates integration debt.

Second, **the cloud providers are platforms competing for the entire stack**. AWS, Azure, and Google do not just sell infrastructure. They sell databases, AI services, developer tools, security, and increasingly everything a business needs. An acquisition like Wiz is about controlling another layer of that stack.

Third, **career paths in tech at the highest levels are remarkably fluid**. Arora moved from Google to SoftBank to Palo Alto Networks, across business leadership, investing, and cybersecurity. At the executive level, the domain expertise matters less than the ability to build organizations, execute strategy, and navigate markets.

Finally, I was struck by the sheer scale of the numbers. Thirty-two billion dollars for a company founded in 2020. This is possible because cloud security is not optional — every company running in the cloud needs it, the consequences of failure are catastrophic, and the market is growing with the cloud itself. When the stakes are existential and the market is expanding, valuations can become extraordinary.

---

*What I studied next: understanding how cloud infrastructure actually works — what happens when you "deploy to the cloud" and how containers, orchestration, and scaling work under the hood.*
