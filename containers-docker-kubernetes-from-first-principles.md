# Containers, Docker, and Kubernetes — from first principles

*Got curious about ECS and EKS — two AWS services I kept seeing referenced — and discovered they were the wrong place to start. Container orchestration is a chain of four ideas, each one solving a problem the previous one created. Working through that chain backwards finally made the whole modern cloud-native stack make sense.*

---

## Why this needed to be a separate entry

I had been seeing terms like "Docker," "Kubernetes," "ECS," "EKS," and "containerised" for months without a clear mental model. Every explanation I had read assumed I already knew what came before, so I would chase a definition and end up with five new undefined terms. Eventually I realised the only way to understand it is to start with the *problem* each tool was invented to solve and walk forward through the chain. Each layer is the solution to the previous layer's failure mode.

## The original problem — "it works on my machine"

Before containers, software deployment had a chronic, infuriating problem.

A developer would build an application on their laptop. The application depended on a precise environment: a specific version of Python, a specific version of PostgreSQL, a specific Linux distribution, specific libraries at specific versions, specific system tools.

They would hand it to operations to deploy on production servers. Production had different versions of all of those. The application would crash, behave subtly differently, or refuse to start at all. The conversation that followed always sounded the same:

"It works on my machine."

This was THE problem of software deployment for thirty years. Every server was slightly different. Every application needed a precise environment. Mismatches caused failures. Engineers spent half of their lives debugging why something worked locally but broke in production.

**Containers solved this problem.**

## A container, defined

A **container** is a packaged bundle that includes:

- Your application code.
- Every library it depends on.
- Every system tool it needs.
- The exact versions of everything.
- A minimal stripped-down operating system.

All zipped into a single file that can run identically anywhere — your laptop, AWS, Google Cloud, a Raspberry Pi — because everything it depends on travels with it.

The analogy that made this stick for me is **the shipping container**. Before standardised shipping containers in the 1950s, every cargo ship was loaded differently — barrels, crates, sacks, all different shapes. Loading and unloading took weeks. Then someone invented the standard shipping container: same dimensions worldwide. Now any container fits any ship, any truck, any train, any crane. Loading time dropped from weeks to hours. Global trade exploded.

Software containers do the same for code. Standardised package, runs anywhere, no more "works on my machine."

## Container vs. virtual machine

Before containers, the way to get this kind of isolation was to use a virtual machine. So why are containers a separate thing?

| | Virtual Machine | Container |
|---|---|---|
| What is included | Full operating system + apps | Just apps + dependencies |
| Size | 5–50 GB | 50–500 MB |
| Boot time | 30–60 seconds | Under 1 second |
| Isolation | Full (separate OS kernel) | Process-level (share host kernel) |
| How many per server | 10–50 | 1,000–10,000 |
| Use case | Heavy workloads, full isolation | Microservices, modern apps |

Containers share the host operating system's kernel, so they are dramatically lighter than VMs. You can run thousands of containers on one server. You can only run dozens of VMs on the same server.

Mental model: **a container is to a VM what a townhouse is to a standalone house** — shares walls (the kernel), still has its own front door (process isolation), much more efficient use of land (server resources).

## Docker — the tool that made containers mainstream

The concept of containers existed in Linux for years before Docker — kernel features called cgroups and namespaces dating to 2008 made them theoretically possible. But they were extremely hard to use. You had to manually configure low-level kernel features. Almost nobody did.

In 2013, a company called Docker Inc. released a tool also called Docker, and that tool made containers easy. Docker provided four things:

1. **A simple format for defining what is in a container** — a file called a Dockerfile. It looks like this:

```dockerfile
FROM python:3.11
COPY app.py /app/
RUN pip install flask
CMD python /app/app.py
```

This says: "Start with a base of Python 3.11, copy my app.py into the container, install Flask, and when the container runs, execute the app."

2. **A command to build it.** `docker build` packages the Dockerfile plus your code into a portable bundle called an **image**.

3. **A command to run it.** `docker run` takes that image and starts a container from it.

4. **A registry called Docker Hub** — a public repository where you can upload your images and download other people's. Like GitHub but for container images. NGINX, PostgreSQL, Python, Node.js — all available as pre-built images.

Docker exploded in popularity. By 2015 the word "Docker" was synonymous with "container" in most engineering conversations.

The vocabulary that comes with Docker:

- **Image** — the static, packaged bundle. The recipe.
- **Container** — a running instance of an image. The cooked meal from the recipe.
- **Dockerfile** — the recipe definition.
- **Docker Hub** — the public registry of images.
- **Docker Engine** — the software that builds, runs, and manages containers on a machine.

## The next problem — "how do I run 10,000 containers?"

Running one Docker container is easy. Running ten is fine. The problem starts when you need to run thousands.

A modern internet company runs **tens or hundreds of thousands of containers** across its infrastructure. Some serve web traffic. Some run databases. Some process payments. Some run AI inference. Suddenly the problems multiply:

1. Where should each container run? You have a thousand servers and ten thousand containers. Which container goes on which server?
2. What if a container crashes? You want it restarted automatically. On the same server? A different one?
3. What if a server dies? All its containers need to move somewhere else, fast.
4. What if traffic spikes? You want to spin up more copies of certain containers automatically.
5. How do containers find each other? The "user service" container needs to talk to the "database" container. How do they discover each other?
6. How do you update without downtime? You want to deploy a new version. Replace containers one at a time so users do not notice.
7. Where do passwords and API keys live?
8. How do you wire up networking, load balancing, persistent storage, monitoring, logging?

Doing all of this manually for thousands of containers is impossible. **You need orchestration software.**

## Kubernetes — the orchestrator that won

In 2014, Google released an open-source tool called **Kubernetes** (often shortened to **k8s** — k, then 8 letters, then s). Kubernetes is software that runs across a fleet of servers and manages containers automatically.

The pitch is essentially: tell Kubernetes what you want, not how to do it. You write a configuration that says "I want 50 copies of this container running, exposed on this port, with this much memory each." Kubernetes figures out how to make that true and keeps it true.

What Kubernetes does for you:

- Decides which physical server each container runs on.
- Restarts containers if they crash.
- Moves containers to other servers if a server dies.
- Scales up or down based on configuration.
- Handles networking — containers can find each other by name.
- Handles rolling updates so deploys do not cause downtime.
- Manages secrets, persistent storage, load balancing, monitoring.

The vocabulary:

- **Cluster** — a fleet of servers running Kubernetes together.
- **Node** — one server in the cluster.
- **Pod** — the smallest unit Kubernetes manages. Usually one container per pod.
- **Deployment** — a definition like "I want 50 copies of this container running, always."
- **Service** — a stable network endpoint for talking to a deployment.
- **Ingress** — routes external traffic into the cluster.
- **ConfigMap / Secret** — config files / passwords for containers.
- **kubectl** — the command-line tool for talking to Kubernetes (pronounced "cube-control" or "cube-cuttle").

Kubernetes is now the operating system of the modern internet. Almost every modern cloud-native application runs on it somewhere.

## Where Kubernetes came from

This is one of my favourite stories in tech, and it explains why Kubernetes won so decisively.

Google had built an internal system called **Borg** since 2003 to manage containers across their data centres. Every Google service — Gmail, Search, YouTube — ran on Borg. They had been doing container orchestration internally for over a decade before the rest of the industry even had the problem.

In 2014, Google open-sourced a cleaner reimplementation called Kubernetes. Within three years it became the industry standard. **This is one of the most strategically important open-source releases in tech history** — it commoditised Google's core infrastructure advantage so that the rest of the industry could catch up to AWS. Google was a distant third in cloud at the time and could not catch AWS through pricing alone, so they instead handed the world the same orchestration playbook Google had been refining for a decade. It worked: Kubernetes is universal, and it is portable across clouds, which directly hurts AWS's lock-in advantage.

## ECS and EKS — finally, the AWS services I started with

Now I can finally explain what ECS and EKS are.

Once containers and Kubernetes became standard, AWS realised that customers wanted to run containers on AWS, but they did not want to manage Kubernetes themselves (Kubernetes is famously complex to operate). So AWS built two managed container services.

### ECS — Elastic Container Service

This is **AWS's own container orchestrator**, built before Kubernetes won.

- Simpler than Kubernetes.
- Tightly integrated with AWS — works seamlessly with S3, RDS, Lambda, IAM.
- AWS-proprietary — you cannot easily move to another cloud.
- Good for teams that want simplicity and do not need Kubernetes' full power.

Use ECS if you are all-in on AWS and do not want to deal with Kubernetes complexity.

### EKS — Elastic Kubernetes Service

This is **a managed version of Kubernetes** that AWS runs for you.

- Real Kubernetes, the open-source standard.
- AWS handles the complex parts (control plane, upgrades).
- Portable — your workloads can move to Google's GKE or Azure's AKS with minimal changes.
- Industry standard. Most modern engineers know Kubernetes.

Use EKS if you want Kubernetes (industry standard) but do not want to manage it yourself, or if you want portability across clouds.

| | ECS | EKS |
|---|---|---|
| What it is | AWS's own orchestrator | Managed Kubernetes |
| Complexity | Lower | Higher |
| AWS lock-in | High | Low (Kubernetes is portable) |
| Industry adoption | AWS-only | Universal |
| Cost | Lower (no control plane fee) | $0.10/hour for control plane |

The other clouds have direct equivalents:

| | AWS | Google Cloud | Azure |
|---|---|---|---|
| Managed Kubernetes | EKS | GKE | AKS |
| Proprietary container service | ECS | Cloud Run | Container Instances |

GKE (Google Kubernetes Engine) is generally considered the best managed Kubernetes — Google invented Kubernetes, after all. Hyperscalers and AI labs often pick GKE over EKS for serious workloads.

## The full stack, top to bottom

This is the picture I now have when I look at a modern cloud architecture diagram.

```
[A web request from a user's browser]
        ▼
[Software: app code running in a Docker container]
        ▼
[Software: container runtime + Linux kernel]
        ▼
[Software: Kubernetes orchestrating thousands of containers]
        ▼
[Service: EKS (or GKE / AKS) managing the Kubernetes cluster]
        ▼
[Service: EC2 instances forming the Kubernetes nodes]
        ▼
[Hypervisor: virtualisation layer slicing physical hardware]
        ▼
[Physical server: CPUs, RAM, storage, networking in a data centre]
```

When a user hits a modern cloud application:

1. DNS routes the request to a load balancer.
2. The load balancer sends the request to one of many pods running the application's container.
3. The pod sits on a Kubernetes node, which is an EC2 instance.
4. The EC2 instance is a virtual machine on a physical server.
5. The physical server is one of millions in the cloud provider's fleet.

Six layers of abstraction. Each one solves a different problem. **Modern cloud engineering is essentially "managing all these layers correctly."**

## The chain in summary

The whole story compressed into one paragraph:

Software broke when moved between machines because of environment differences. Containers solved this by packaging the environment with the code. Docker made containers easy enough that everyone adopted them. Running containers at scale created new problems (scheduling, healing, networking). Kubernetes solved those by orchestrating thousands of containers across servers. Cloud providers wrapped Kubernetes in managed services (EKS, GKE, AKS) so that customers could use it without operating it. Today, almost every modern cloud-native application runs in containers, on Kubernetes, on virtual machines, on physical servers in a data centre. Each layer was a response to the previous layer's limit.

> The container revolution was not really about containers. It was about *standardisation*. Once code became portable across machines, the entire industry could be rewritten in terms of "what runs," not "where it runs." Kubernetes is what happens when standardised code meets infinite scale.

---

*This sits on top of [the four foundational AWS services — EC2, S3, Lambda, RDS](the-four-foundational-aws-services-ec2-s3-lambda-rds.md), which explains the underlying primitives that Kubernetes nodes are built on. The layer below that is [what compute actually means — from physical servers to EC2](what-compute-actually-means-from-physical-servers-to-ec2.md).*
