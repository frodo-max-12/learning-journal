# The four foundational AWS services — EC2, S3, Lambda, RDS

*After understanding what an EC2 instance actually is, I wanted to know how it relates to the other AWS service names I see thrown around constantly — S3, Lambda, RDS, and so on. Turns out four services give you 80% of cloud literacy. Each one solves a fundamentally different problem, and once you see the four problems they solve, the rest of AWS makes sense.*

---

## Why these four

AWS today has more than 200 services with marketing-friendly names. Most engineers I know cannot name half of them. But almost every modern cloud application is built on top of just four services. If you understand these four, you can read any cloud architecture diagram and roughly know what is going on.

The four are:

- **EC2** — virtual servers you rent.
- **S3** — file storage.
- **Lambda** — code that runs on demand without managing a server.
- **RDS** — managed databases.

Each solves a problem that comes up in nearly every application. They compose together so cleanly that the same four-piece pattern appears in almost every cloud architecture.

## EC2 — compute (a virtual computer you rent)

**Full name:** Elastic Compute Cloud.
**What it is:** A virtual computer running on AWS infrastructure. CPU, RAM, storage, network. You pick the size, you install whatever operating system and software you want, you pay per hour or per second.
**What it solves:** "I need a computer to run my code on, and I do not want to buy and maintain a physical machine."

Some example sizes:

| Instance type | vCPU | RAM | GPU | Hourly | Monthly (24/7) |
|---|---|---|---|---|---|
| t3.micro | 2 | 1 GB | — | $0.0104 | ~$8 |
| t3.medium | 2 | 4 GB | — | $0.042 | ~$30 |
| m5.xlarge | 4 | 16 GB | — | $0.192 | ~$140 |
| m5.4xlarge | 16 | 64 GB | — | $0.768 | ~$560 |
| c5.24xlarge | 96 | 192 GB | — | $4.08 | ~$2,975 |
| g5.xlarge | 4 | 16 GB | 1× A10G | $1.006 | ~$734 |
| p5.48xlarge | 192 | 2,048 GB | 8× H100 | $98.32 | ~$71,700 |

You can save 30-72% off these list prices by committing to one or three years (called Reserved Instances or Savings Plans), or by using spot instances (50-90% cheaper but AWS can reclaim them with two minutes notice).

The mental model that landed for me: **renting an EC2 instance is like renting a furnished apartment.** You have full control. You also have to take out the trash and fix things when they break. The cloud provider handles the building (physical hardware), but inside the apartment, the responsibility is yours.

You would use EC2 when you need a long-running server with full control — running a custom application, hosting a website, training an AI model, or anything else where you need a full computer that stays on.

## S3 — storage (a place to put files)

**Full name:** Simple Storage Service.
**What it is:** A massively scalable file store. You upload files (called "objects") into containers (called "buckets") and they sit there until you delete them, replicated across multiple data centres.
**What it solves:** "I need to store files cheaply, durably, and access them from anywhere on the internet."

Pricing is per GB stored per month, plus per-request fees, plus bandwidth out.

| Storage class | $/GB/month | When to use |
|---|---|---|
| S3 Standard | $0.023 | Frequently accessed data |
| S3 Standard-Infrequent Access | $0.0125 | Backups, less-frequent access |
| S3 Glacier Instant Retrieval | $0.004 | Archives with fast retrieval |
| S3 Glacier Deep Archive | $0.00099 | Cold archive (12-hour retrieval) |

S3 has one of the highest durability guarantees in the industry: **99.999999999%** (eleven nines). Statistically, if you stored 100 billion files for a year, you would expect to lose one. Files are replicated across multiple physically separated data centres automatically.

Crucially, **S3 has no CPU**. It does not run your code. It just stores and retrieves files. If you want code to do something to the files, you need to point another service at S3.

The mental model: **S3 is a warehouse**. You put boxes in, you get boxes out, but the warehouse does not process the contents of the boxes. The upside is you can store infinite quantity at low cost. The downside is that retrieving and acting on the data has to happen elsewhere.

You would use S3 for:

- User uploads (photos, videos, documents).
- Backups.
- Hosting static websites.
- Storing AI training datasets.
- Storing model weights — large foundation model weights live in S3 or its equivalents.
- Data lakes for analytics.

The trap with S3 is bandwidth. Storage is cheap (a few cents per GB per month), but **bandwidth out** to the internet is $0.09 per GB. If you store 1 TB at $23/month and your users download all of it once, the bandwidth bill is $90 — four times the storage cost. This egress pricing is how AWS makes huge margins on S3, and it is the single most common surprise on cloud bills.

## Lambda — serverless compute (run code without managing a server)

**Full name:** AWS Lambda. Named after the lambda functions in computer science.
**What it is:** You upload a function (a small piece of code), configure a trigger, and AWS runs the function whenever the trigger fires. You never see or manage a server.
**What it solves:** "I have small bits of code I want to run occasionally, and I do not want to pay for a server that sits idle most of the time."

Pricing is per invocation plus per millisecond of execution.

- $0.20 per 1 million requests.
- $0.0000166667 per GB-second of execution.
- Free tier: 1 million requests + 400,000 GB-seconds per month, forever.

| Workload | Cost per month |
|---|---|
| Tiny webhook (1M invocations, 128MB, 100ms each) | Free tier covers it — $0 |
| Image resizer (10M invocations, 512MB, 500ms each) | ~$2 |
| Medium API (100M invocations, 256MB, 200ms each) | ~$103 |
| Heavy data pipeline (1B invocations, 1GB, 1s each) | ~$16,800 |

For most personal projects and small businesses, Lambda is essentially free.

The mental model: **with EC2 you rent a server that runs continuously. With Lambda you rent the right to run code on demand.** When the trigger fires, AWS spins up a container, runs your function, and shuts it down. You never see any of this.

The key constraint is that each Lambda invocation is **stateless** — when the function ends, everything in its memory is forgotten. If you need to remember anything, persistent data has to live in S3 or a database. Lambda functions are also capped at 15 minutes of execution time. They are designed for short, bursty work.

Triggers can be HTTP requests, S3 uploads, database changes, scheduled times, queue messages, and many more.

You would use Lambda for:

- Resizing images when they upload to S3.
- Webhook handlers (someone POSTs to your URL, run this code).
- Scheduled jobs (every night at 2 AM, run this report).
- API backends (Lambda + API Gateway = a serverless API).
- Glue between AWS services.

The Thomas Kurian interview made me think about Lambda differently. He named "consumer agent VMs" as the next big infrastructure bottleneck — agents running for hours, holding state, calling tools, but only when needed. That is essentially "Lambda for AI agents." The infrastructure pattern Lambda invented for short stateless functions is exactly what agentic workloads need at a different scale.

## RDS — managed databases

**Full name:** Relational Database Service.
**What it is:** A database server (PostgreSQL, MySQL, MariaDB, Oracle, SQL Server, or Aurora) that AWS runs and manages for you.
**What it solves:** "I need a database, but I do not want to install, configure, patch, back up, or replicate the database software myself."

Roughly 2x the cost of an equivalent EC2 instance, because AWS handles the management overhead.

| Instance type | vCPU | RAM | Hourly | Monthly (24/7) |
|---|---|---|---|---|
| db.t3.micro | 2 | 1 GB | $0.018 | ~$13 |
| db.t3.medium | 2 | 4 GB | $0.072 | ~$53 |
| db.m5.xlarge | 4 | 16 GB | $0.342 | ~$250 |
| db.r5.4xlarge | 16 | 128 GB | $1.92 | ~$1,400 |
| db.r5.24xlarge | 96 | 768 GB | $11.52 | ~$8,400 |

Plus storage at $0.115/GB/month, and roughly 2x cost if you enable Multi-AZ replication for failover.

The mental model: **RDS is renting an apartment with a property manager who handles all maintenance**. You live there, you decorate, but you do not fix the plumbing yourself. You could run PostgreSQL yourself on EC2 and save money, but then you would have to install it, configure backups, set up replication, handle failovers when servers crash, manage version upgrades, secure it, and monitor performance. RDS does all that. You pay a premium, you get peace of mind.

RDS is for **structured data** — tables with rows, columns, schemas, foreign keys. User accounts, transactional data, anything that fits a relational model. S3 is for **unstructured files** — images, videos, blobs of text. Most applications use both at the same time.

## How they compose — a real example

Imagine building Instagram-for-pets, a photo-sharing app for pet owners. The four-service pattern looks like this:

| Need | AWS service used |
|---|---|
| Web servers running the application | **EC2** — 4 instances behind a load balancer |
| User accounts, follower relationships, comments | **RDS** — PostgreSQL database |
| Pet photos uploaded by users | **S3** — bucket storing all images |
| Image processing (generate thumbnails when uploaded) | **Lambda** — triggered by S3 uploads |
| Email notifications when someone comments | **Lambda** — triggered by RDS events |
| Static marketing website | **S3** — with static website hosting enabled |
| Scheduled cleanup of unused photos | **Lambda** — runs daily |

That is a complete application architecture using all four services. Each does what it is best at and they compose cleanly. Putting realistic numbers on it for a mid-sized app with 10,000 users:

| Service | Setup | Cost/month |
|---|---|---|
| EC2 | 4× m5.xlarge web servers (24/7) | ~$560 |
| RDS | db.m5.xlarge PostgreSQL + 500 GB storage + Multi-AZ | ~$650 |
| S3 | 2 TB user uploads (Standard) | ~$47 + bandwidth |
| Lambda | 50M function invocations | ~$50 |
| **Total** | | **~$1,300/month** |

Add CloudFront, load balancers, DNS, and you are at maybe $1,500-$2,000/month for a real production app.

## The pricing hierarchy

At small scale, ordered cheapest to most expensive:

1. **Lambda** — most workloads land in the free tier. $0-$50/month for typical usage.
2. **S3** — pennies per GB stored. Often under $50/month unless you are storing huge media.
3. **EC2** — $10-$100/month for small servers, scales linearly with size.
4. **RDS** — same compute as EC2 plus a 2x management premium.

At massive scale the order flips. Lambda gets expensive at billions of invocations per month, and most teams switch to EC2 or containers for that volume. EC2 becomes very economical at scale with reserved instances. S3 storage stays cheap but **bandwidth fees dominate**. RDS gets expensive enough at large scale that many companies move to self-managed databases on EC2 to save 30-50%.

## The compute / storage split

I noticed a pattern across these four services that is useful as a mental compression.

- **EC2 and Lambda are compute** — they are where code runs.
- **S3 and RDS are storage** — they are where data lives.

Compute is ephemeral. Turn it off and the work stops, but no data is lost (because data lives in S3 or RDS). Storage is persistent. Your data stays there until you explicitly delete it.

Almost every cloud application has at least one compute service and at least one storage service. Most have all four. The other 200 AWS services are either built on top of these (CloudFront, Route 53, Elastic Beanstalk) or are specialised variants (DynamoDB is a NoSQL alternative to RDS; ECS and EKS are container compute alternatives to plain EC2; SageMaker is a managed AI training environment).

## The other clouds use the same pattern

Once I had this four-service mental model for AWS, I realised Google Cloud and Azure use the exact same pattern with different names.

| Function | AWS | Google Cloud | Azure |
|---|---|---|---|
| Virtual servers | EC2 | Compute Engine (GCE) | Virtual Machines |
| Object storage | S3 | Cloud Storage (GCS) | Blob Storage |
| Serverless functions | Lambda | Cloud Functions | Azure Functions |
| Managed databases | RDS | Cloud SQL | SQL Database |

Same problems, same solutions, different vocabulary. If you have learned one cloud, the second cloud is mostly translation work.

> Cloud architecture, stripped of vendor jargon, is just the answer to four questions. Where does my code run continuously? Where do my files live? Where does my code run on demand? Where does my structured data live? AWS's answers are EC2, S3, Lambda, RDS. Every other cloud has equivalents.

---

*The layer below this is [what compute actually means — from physical servers to EC2](what-compute-actually-means-from-physical-servers-to-ec2.md), which explains what is actually behind the EC2 abstraction. The layer above is [containers, Docker, and Kubernetes from first principles](containers-docker-kubernetes-from-first-principles.md), which explains how modern apps are packaged and orchestrated on top of these primitives.*
