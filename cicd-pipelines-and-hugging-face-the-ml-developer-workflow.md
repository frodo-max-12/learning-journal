# CI/CD pipelines and Hugging Face -- the ML developer workflow

*Learned on March 25, 2026. I kept seeing "Hugging Face" everywhere in AI discussions and had no idea what it actually was. The conversation started with a simple "what is this thing?" and ended up covering why GitHub cannot host ML models, how developers automate their testing and deployment, and a surprising connection to David Deutsch's philosophy of error correction.*

---

## What is Hugging Face and why does it exist?

I had been seeing the name Hugging Face for months. Every time a new open-source AI model dropped -- Llama, Mistral, Stable Diffusion -- people would link to Hugging Face. I assumed it was some kind of AI company, but I could not figure out what it actually *did*. Was it a model? A platform? A library?

The answer: Hugging Face is GitHub for machine learning. It is a platform where people share, discover, and collaborate on AI models, datasets, and demo applications. Instead of training a model from scratch (which costs millions of dollars and months of compute), you can grab a pre-trained model off Hugging Face and fine-tune it or use it directly. They host tens of thousands of models covering everything from text generation to image recognition to speech-to-text.

They also built an open-source Python library called Transformers that gives you a unified interface to load and run any model with just a few lines of code. This dramatically lowered the barrier to entry for AI development. Before Hugging Face, working with ML models was fragmented and painful -- every model had its own loading procedure, its own data format, its own quirks. Transformers said: here is one consistent interface for all of them.

But the question that immediately followed was obvious.

## Why not just use GitHub?

GitHub already lets you store code, collaborate with others, and version-control your work. Why do ML developers need a separate platform?

The answer comes down to what ML models actually are and what Git was designed to handle.

**The file size problem is the big one.** A single AI model can be anywhere from a few hundred megabytes to hundreds of gigabytes. GPT-3's weights are roughly 350 GB. GitHub has a hard limit of 100 MB per file. Even with Git LFS (Large File Storage), which lets you store pointers to large files, it gets clunky and expensive fast. Hugging Face was designed from the ground up to handle massive files efficiently -- downloading, versioning, and streaming them.

**Git was built for text diffs, not binary blobs.** When you change a line of code on GitHub, Git stores just the difference -- the old line and the new line. This is elegant and efficient for source code. But a trained model is a giant blob of numerical weights -- billions of floating-point numbers packed into a binary file. When you retrain a model and the weights change, Git cannot compute a meaningful diff. It just stores the entire new file alongside the old one. Version history balloons in size and becomes useless for understanding what changed.

**Discovery and standardization matter.** On Hugging Face, every model has a standardized "model card" -- a structured description of what it does, how it was trained, its performance benchmarks, its limitations, and its license. You can filter models by task (text generation, image classification), framework (PyTorch, TensorFlow), language, model size, and more. GitHub repos are freeform -- there is no structured way to search "show me all French language translation models sorted by accuracy."

**Inference in the browser.** Hugging Face provides APIs where you can test a model directly on their website without downloading anything. Type a sentence, get a translation. Upload an image, get a classification. GitHub has nothing like this because GitHub was never designed to *run* what it hosts.

| | GitHub | Hugging Face |
|---|---|---|
| **Designed for** | Source code (text files) | ML models (large binary blobs) |
| **File size limit** | 100 MB per file | Handles multi-GB files natively |
| **Version control** | Line-by-line diffs (efficient for code) | Full model versioning (handles binary weights) |
| **Discovery** | Freeform repos, star counts | Structured model cards, task/framework filters |
| **Try before download** | No (it hosts code, not running apps) | Yes (inference API in browser) |
| **Collaboration** | Pull requests, code review | Model discussions, community model cards |

## How developers use both together

In practice, ML developers do not choose between GitHub and Hugging Face. They use both, and the division of labor is clean.

**GitHub holds the code.** The training scripts, data preprocessing pipelines, API server code, evaluation scripts, and configuration files -- everything that is human-written logic. This is text, it diffs well, and Git handles it beautifully.

**Hugging Face holds the model.** The actual trained weights -- the heavy binary files that are the output of the training process. These get versioned on Hugging Face with commit hashes, so you can always roll back to a previous model version.

**The code references the model by name.** Somewhere in the GitHub repo, there is a line like:

```python
model = AutoModel.from_pretrained("mistralai/Mistral-7B")
```

That string -- `"mistralai/Mistral-7B"` -- is a pointer to a specific model on Hugging Face. When the code runs, it downloads (and caches) the model automatically. The GitHub repo stays small and clean. The heavy lifting lives on Hugging Face.

For open-source AI projects, the pattern is remarkably consistent: the paper and model go on Hugging Face, the training and evaluation code go on GitHub, and the README on each links to the other. Check any major model release and you will see this two-platform dance.

## CI/CD: the automation layer connecting everything

This is where the conversation took a turn into something I had heard about for years but never understood: CI/CD. The term kept appearing in developer discussions, job descriptions, and technical blogs. I knew it stood for Continuous Integration / Continuous Deployment. I did not know what that meant in practice.

The analogy that made it click: imagine you are writing a book with ten co-authors. Everyone is working on different chapters simultaneously. CI/CD is the system that makes sure nobody's work breaks anyone else's, and that the latest version of the book is always available to readers.

### Continuous Integration (the CI part)

Continuous Integration means: every time a developer pushes their code changes, an automated system immediately runs a battery of tests. Does the application still start? Does the login still work? Did this new change break the payment system? Are there any security vulnerabilities in the new dependencies?

If something fails, the team gets alerted instantly. The person who pushed the change fixes it while the context is still fresh in their head.

Without CI, teams used to merge everyone's code together periodically -- sometimes monthly -- and it would be a nightmare of conflicts and broken interactions. Developers actually had a name for this: **integration hell**. CI eliminates integration hell by integrating continuously (hence the name) instead of in painful, infrequent batches.

The tools that run these automated checks are called CI servers. The most common one today is GitHub Actions, which is built right into GitHub. You write a configuration file that says "every time someone pushes code, run these test commands," and GitHub's servers execute it automatically.

```yaml
# A simple GitHub Actions CI config
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install
      - run: npm test
```

That is the whole thing. Every push triggers a fresh virtual machine that checks out the code, installs dependencies, and runs the test suite. If any test fails, the push gets flagged.

### Continuous Deployment (the CD part)

Continuous Deployment extends the automation past testing into shipping. Once the CI tests pass and the code is merged into the main branch, the system automatically deploys the new version to the live application. No human manually uploading files to a server. No "deployment day" where everyone holds their breath.

Some teams use a slightly softer version called **Continuous Delivery** -- the code is always *ready* to deploy, but a human still clicks the final "go" button. The distinction is about how much you trust your automated tests.

In plain English:

- **CI** = automatically check that nothing is broken every time someone makes a change
- **CD** = automatically send the working version to users

### CI/CD in the ML workflow

This is where the two threads -- Hugging Face and CI/CD -- come together.

For ML projects, CI/CD looks a bit different because you are not just testing code; you are also evaluating model performance. A typical setup:

1. Developer pushes new training code or a data preprocessing change to GitHub
2. GitHub Actions triggers automatically
3. The CI pipeline pulls the latest model from Hugging Face, runs it against a benchmark dataset, and checks whether accuracy regressed
4. If everything passes, the pipeline deploys the updated model to production

Some teams also wire it in the other direction: when a new model version is pushed to Hugging Face, it triggers a GitHub workflow that automatically redeploys the application. The two platforms talk to each other through CI/CD.

## The Deutsch connection: error correction as a universal principle

This is the part of the conversation that surprised me the most. I have been reading David Deutsch's work for over five years -- *The Beginning of Infinity* is one of the most important books I have ever encountered. And as I was learning about CI/CD, I realized it embodies one of Deutsch's deepest ideas: **the centrality of error correction to all knowledge creation**.

Deutsch argues that progress -- in science, in technology, in any domain -- is not about avoiding errors. It is about creating systems that *detect and correct* errors quickly. Good explanations are those that are hard to vary without destroying their explanatory power, and the way you discover whether an explanation is good is by testing it, finding where it breaks, and fixing it.

CI/CD is exactly this principle applied to software. The philosophy is not "write perfect code." The philosophy is "write code, test it immediately, catch errors fast, fix them while context is fresh, and keep iterating." The entire system is designed around the assumption that errors will happen and that the speed of error correction matters more than the prevention of errors.

> Every push is a conjecture. Every test suite is an attempted refutation. Every deployment is a provisional acceptance, always subject to revision.

This is Deutsch's epistemology, implemented as infrastructure.

And it extends to ML in a particularly interesting way. When you train a model, you are generating a conjecture about the structure of some data. When you evaluate it against a test set, you are attempting to refute that conjecture. When evaluation fails (accuracy dropped, bias increased, the model hallucinates more), you go back and revise. The CI/CD pipeline automates this cycle of conjecture and refutation so it happens on every single code change, not just when someone remembers to check.

The teams that ship the best software are not the ones that write the fewest bugs. They are the ones whose error-correction cycles are the fastest. That is a Deutschian insight wearing an engineering hat.

## What I actually learned

Two concepts that kept appearing in technical discussions finally clicked for me in this conversation. Hugging Face exists because ML artifacts have fundamentally different storage, versioning, and discovery needs than source code -- GitHub was not built for binary blobs measured in gigabytes. CI/CD exists because the most robust way to build anything complex is not to aim for perfection but to build rapid, automated error-correction into the process itself.

The two connect naturally: in a modern ML workflow, GitHub holds the logic, Hugging Face holds the models, and CI/CD is the automated feedback loop that keeps both in sync and catches regressions before they reach users. It is a division of labor that makes the whole system more resilient than any single platform could be.

---

*What I studied next: [Everything is text underneath -- file formats demystified](everything-is-text-underneath-file-formats-demystified.md), where I opened an Excel file with a zip tool and discovered that every complex file format is structured text in disguise.*
