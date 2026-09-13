# What "compute" actually means — from a physical server to EC2

---

## The honest starting point

When I read industry conversations like "OpenAI is compute-constrained," "AWS sold $X billion of compute," or "we are buying 100,000 GPUs of compute," I had a fuzzy mental image. Servers somewhere. Chips. Numbers being crunched. But if you had asked me "what is physically happening in those servers," I could not have answered cleanly.

So I asked. And the answer turned out to be both simpler and stranger than I expected.

## My initial model — and why it was almost right

My intuition was: a server in an Amazon data centre is just a normal computer kept in a building somewhere else. CPU, RAM, storage, motherboard. No monitor, no keyboard. Accessed remotely. That is all.

**That is correct as the foundation.** A modern AWS server is genuinely a physical computer. It is roughly the size of a pizza box (1U or 2U so it fits in a server rack), has 1 or 2 CPU sockets each holding a Xeon or ARM chip with 64-128 cores, 256GB to 2TB of DDR5 RAM, NVMe SSDs for storage, fast networking cards, and a small management chip called a BMC that lets engineers manage the box remotely even when its main operating system is dead.

Forty-or-so of these boxes get racked into a cabinet. A data centre has thousands of cabinets. A region (like AWS's us-east-1) has multiple data centres distributed across what they call availability zones.

So my original model was right at the bottom layer. What I was missing were the **four abstractions stacked on top of those physical servers** that turn "computers in a building" into "the cloud."

## Layer 1 — virtualisation, and why it breaks the simple model

Here is the first thing that complicated my picture.

A physical server with 128 CPU cores and 1TB of RAM is much larger than what most workloads actually need. A typical web server needs maybe 4 cores and 16GB of RAM. So cloud providers do not sell whole physical servers. They slice them up.

The slicing is done by software called a **hypervisor**. The hypervisor runs on the physical server and creates many isolated virtual computers on top of it. Each virtual computer:

- Believes it has its own CPU, RAM, disk, and network card.
- Runs its own operating system.
- Is fully isolated from the other virtual computers sharing the same physical hardware.
- Can be created, destroyed, resized, or moved between physical servers in seconds.

These virtual computers are called **instances**. When AWS sells you "an EC2 instance," they are renting you one virtual slice of one of their physical servers. You do not know which physical server it lives on. You do not know who else is sharing the hardware. AWS picks.

This was the mental shift I needed. **The thing you "rent" from a cloud provider is not a server. It is a virtual computer running on a server.** The physical hardware is shared, the virtualisation makes it feel private.

## What EC2 actually is

EC2 stands for Elastic Compute Cloud. It is AWS's product name for these rented virtual computers.

An EC2 instance has:

- A type (like `t3.medium`, `m5.xlarge`, `c5.4xlarge`) defining its compute size — CPU cores, RAM, network speed.
- An OS image (called an AMI — Amazon Machine Image) that boots when the instance starts.
- A network configuration (which subnet, which IP address).
- Attached storage (called EBS volumes — virtual disks).
- A pricing rate per hour or per second of running time.

Some example sizes:

| Instance type | vCPUs | RAM | GPU | Use case |
|---|---|---|---|---|
| `t3.micro` | 2 | 1 GB | — | Tiny test server |
| `m5.xlarge` | 4 | 16 GB | — | Standard web server |
| `c5.24xlarge` | 96 | 192 GB | — | Heavy computation |
| `p4d.24xlarge` | 96 | 1,152 GB | 8× A100 | AI training |

The "elastic" word is the magic. You can launch 1,000 instances in 60 seconds and shut them all down 60 seconds later, paying only for the seconds they ran. Capacity feels infinite because behind the scenes, the cloud provider has millions of physical servers idling, ready to slice up on demand.

If you owned physical servers instead, you would have to buy hardware, wait weeks for delivery, install it in a rack, and then be stuck with it whether or not you needed it. The elasticity of cloud is what made cloud win.

## What "compute" actually means as industry shorthand

Now the term "compute" stopped being fuzzy.

In industry usage, "compute" means **CPU and GPU and TPU cycles available for executing programs**. When people say "we are compute-constrained," they mean their workloads need to run, those workloads need processor cycles to run, and they do not have enough cycles available — so the work runs too slowly or not at all.

Different work needs different kinds of compute:

- Web serving — light CPU, lots of network input/output.
- Database queries — moderate CPU, lots of memory and disk.
- Video encoding — heavy CPU, often specialised media chips.
- AI training — massive GPU or TPU cycles plus high memory bandwidth plus fast interconnect between chips.
- AI inference — moderate GPU or TPU cycles, but extremely latency-sensitive.

When a hyperscaler executive says "we are not capacity-constrained," they mean they have enough physical servers, chips, power, and network to satisfy the workload demand they are seeing. When an AI lab says they are "compute-constrained," they mean they want to train bigger models or serve more users than their available chip cycles allow.

## What is actually happening inside the physical server

This is where it got philosophically interesting.

A CPU does **one thing only**. It reads numbers from memory, performs arithmetic on them, and writes the results back to memory. Billions of times per second.

That is it.

Every single thing a computer does — running a browser, playing a video, training a neural network, ordering food — is decomposed into:

1. Load some numbers from memory into the CPU's registers.
2. Add, subtract, multiply, compare, or shift those numbers.
3. Store the result back in memory.
4. Repeat.

A modern Xeon does roughly 100 billion such operations per second per core, across 64 cores. So one server can do roughly **6.4 trillion arithmetic operations per second**.

A GPU like an NVIDIA H100 does about **2 quadrillion operations per second** in the FP8 number format used in AI inference — roughly 300 times more than a CPU. Not because GPU operations are individually faster, but because the GPU is designed to do many simple operations in parallel rather than fewer complex ones sequentially. A specialised inference chip like Google's TPU pushes this further by tuning the silicon specifically for the matrix multiplications that neural networks need.

That is what "compute" is at the most fundamental level: arithmetic on numbers, repeated trillions of times per second per machine.

Everything else — operating systems, programming languages, browsers, AI models — is a tower of abstractions built on top of that single primitive.

## Tracing one ChatGPT request through the whole stack

To anchor this, I traced what physically happens when I type a question into ChatGPT and hit enter.

1. My browser sends the text over the internet to OpenAI's servers.
2. The text arrives at a Microsoft Azure data centre (OpenAI runs on Azure).
3. Azure routes it to a physical server containing 8 NVIDIA H100 GPUs.
4. That physical server is running a hypervisor that has carved out a virtual machine dedicated to OpenAI's inference workload.
5. Inside that VM, an inference engine loads GPT-4's weights from local NVMe storage into the GPU's HBM memory.
6. My text gets converted into numbers (tokens).
7. Those numbers are multiplied against the model's weights — billions of arithmetic operations across 8 GPUs.
8. The output numbers are converted back into text.
9. The text is sent back to my browser.

Total time: maybe 500 milliseconds. Total operations: trillions of multiplications. Total physical hardware involved: one server, out of millions in Microsoft's fleet.

**Compute is step 7.** Everything else is plumbing.

## The summary I wish someone had given me at the start

A cloud server is a physical computer in a building, almost certainly in Northern Virginia, Oregon, Dublin, Mumbai, Singapore, or somewhere similar. It has a CPU, RAM, storage, networking. No monitor or keyboard. You access it remotely.

The two refinements to that simple picture:

**Virtualisation.** That physical computer is sliced into many virtual computers so dozens of customers can share it without seeing each other's data. When you "rent an EC2 instance," you are renting one virtual slice, not the whole physical machine.

**Scale plus automation.** AWS has roughly 5 million physical servers across more than 100 data centres in 30+ regions. The "elastic" feeling comes from software that can spin up a virtual machine in 30 seconds because there is always spare capacity sitting somewhere. You never see the seams.

Strip away every product name, every marketing term, every piece of cloud jargon, and a hyperscaler is: **many computers, in many buildings, with software that lets you rent slices of them by the second**.

> Compute, at the bottom of the stack, is just arithmetic on numbers — a CPU loading bits, adding them, and writing the result back, billions of times per second. Everything above that, from operating systems to AI models, is a tower of abstractions standing on that one primitive.

---

*This connects to [computer architecture — why CPU, RAM, and storage exist](computer-architecture-why-cpu-ram-and-storage-exist.md) which goes deeper on the speed hierarchy inside a single machine. The next layer up is [the four foundational AWS services — EC2, S3, Lambda, RDS](the-four-foundational-aws-services-ec2-s3-lambda-rds.md), which are the building blocks the cloud is sold as.*
