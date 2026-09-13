# Bayesian reasoning — why "99% accurate" doesn't mean what you think

*Learned on March 7, 2026. I kept running into phrases like "update your priors" and "you're ignoring the base rate" in essays, podcasts, and work conversations. I could nod along, but the moment someone walked through the math — especially the classic medical test problem — I'd lose the thread. I decided to sit down and actually work through it.*

---

## The question that broke my intuition

Here is the setup. There is a disease that affects 1% of the population. There is a test for this disease that is 99% accurate — meaning if you have the disease, the test will correctly say "positive" 99% of the time, and if you don't have the disease, the test will correctly say "negative" 99% of the time.

You take the test. It comes back positive.

What is the probability that you actually have the disease?

Most people — including me, the first time I saw this — say "99%." The test is 99% accurate, I tested positive, so I'm 99% likely to be sick. That feels completely logical.

The actual answer is about 50%.

When I first saw that, I thought it was a trick question. It is not. It is a direct consequence of how conditional probability works, and understanding why is the gateway to Bayesian reasoning.

## Two different questions that sound the same

The confusion comes from mixing up two questions that sound identical but are mathematically very different:

1. **If I have the disease, what's the chance the test catches it?** This is 99%. It's what "99% accurate" means.
2. **If the test says positive, what's the chance I actually have the disease?** This is what I care about when I'm holding my test results.

These are both conditional probabilities, but they condition on different things. In notation:

- Question 1: P(positive | disease) = 0.99
- Question 2: P(disease | positive) = ???

The vertical bar means "given that." Flipping what comes before and after that bar changes everything. This is the heart of Bayes' theorem — it gives you the machinery to compute one direction when you know the other.

## Working through it with actual numbers

Abstract formulas never helped me learn anything. Let me use concrete numbers instead.

Imagine 10,000 people get tested. Given that 1% of the population has the disease:

- **100 people** actually have the disease
- **9,900 people** are healthy

Now apply the 99% accurate test to both groups:

| Group | Number of people | Test result | Count |
|-------|-----------------|-------------|-------|
| Sick | 100 | True positive (correctly detected) | 99 |
| Sick | 100 | False negative (missed) | 1 |
| Healthy | 9,900 | True negative (correctly cleared) | 9,801 |
| Healthy | 9,900 | False positive (wrongly flagged) | 99 |

Now look at everyone who tested positive: 99 true positives + 99 false positives = **198 positive results**.

Of those 198 people with positive results, only 99 actually have the disease.

P(disease | positive) = 99 / 198 = **50%**

Not 99%. Fifty percent. A coin flip.

## Why the base rate matters so much

The reason the answer is so far from 99% is the **base rate** — how common the disease is in the population. Only 1% of people are sick, which means 99% are healthy. Even a very accurate test, when applied to a massive pool of healthy people, will generate a large absolute number of false positives.

Think of it this way. The test makes two kinds of mistakes:

- It misses 1% of sick people (false negatives)
- It wrongly flags 1% of healthy people (false positives)

The same error rate — 1% — applied to 100 sick people gives you 1 mistake. Applied to 9,900 healthy people, it gives you 99 mistakes. The healthy group is so much larger that its mistakes swamp the signal from the sick group.

> The rarer the condition you're testing for, the more your positive results will be false alarms — even with an excellent test. This is the **false positive paradox**.

I find it helpful to think of an analogy. Suppose you're a security guard at a building with 10,000 employees, and you know exactly 100 of them are smuggling something. You have a scanner that's 99% accurate. It correctly beeps for 99 of the 100 smugglers. But it also falsely beeps for 99 of the 9,900 innocent employees. When the scanner beeps, you can't tell which group the person belongs to — roughly half the beeps are false alarms.

## The formal machinery: Bayes' theorem

Once the intuition is in place, the formula is just bookkeeping:

```
P(A|B) = P(B|A) × P(A) / P(B)
```

In the medical test case:

```
P(disease|positive) = P(positive|disease) × P(disease) / P(positive)
```

Let me plug in the numbers:

- P(positive|disease) = 0.99 (test sensitivity)
- P(disease) = 0.01 (base rate — this is the **prior**)
- P(positive) = P(positive|disease) × P(disease) + P(positive|no disease) × P(no disease)
  = 0.99 × 0.01 + 0.01 × 0.99
  = 0.0099 + 0.0099
  = 0.0198

So:

```
P(disease|positive) = 0.99 × 0.01 / 0.0198 = 0.0099 / 0.0198 = 0.5
```

Fifty percent, exactly as the counting method showed.

## What changes the answer dramatically

The interesting part is seeing what happens when you adjust the inputs. This is where the reasoning becomes genuinely useful rather than just a textbook exercise.

**What if the disease is more common?** Say 10% of the population has it instead of 1%.

| Group | Count | True positives/negatives | False positives/negatives |
|-------|-------|-------------------------|--------------------------|
| Sick (1,000) | 1,000 | 990 true positives | 10 false negatives |
| Healthy (9,000) | 9,000 | 8,910 true negatives | 90 false positives |

Now: P(disease | positive) = 990 / (990 + 90) = 990 / 1080 = **91.7%**

Much better! When the base rate goes up, the positive result becomes far more meaningful.

**What if you take the test twice?** This is the real power of Bayesian updating. After your first positive test, your probability of having the disease is 50%. That 50% now becomes your **new prior**. If you take a second independent test and it also comes back positive, you run the calculation again with P(disease) = 0.50 instead of 0.01:

```
P(disease|second positive) = 0.99 × 0.50 / (0.99 × 0.50 + 0.01 × 0.50)
                            = 0.495 / 0.5 
                            = 0.99
```

After two positive tests, you're at 99%. Each piece of evidence updates your belief. This is what people mean by "updating your priors."

## The vocabulary, demystified

Now the jargon that used to wash over me makes sense:

- **Prior probability**: What you believed before seeing the evidence. In the medical example, it's the 1% base rate. In everyday reasoning, it's your starting estimate of how likely something is.
- **Likelihood**: How probable the evidence is, assuming your hypothesis is true. The 99% sensitivity of the test.
- **Posterior probability**: Your updated belief after seeing the evidence. The 50% we calculated.
- **Base rate**: The prior probability of the thing you're testing for in the overall population.
- **Base rate fallacy**: The mistake of ignoring the prior and assuming the test accuracy directly translates to the probability of the hypothesis. This is exactly the mistake of saying "99% accurate test, therefore 99% chance I'm sick."

> Bayesian reasoning is fundamentally about this: you don't get to interpret evidence in isolation. The meaning of evidence depends on what you believed before you saw it.

## Why this matters beyond medical tests

Once I understood the structure, I started seeing it everywhere.

**Hiring.** If you're screening resumes and only 2% of applicants are truly great fits, even a "good" screening process with a 90% accuracy rate will flag mostly false positives. This is why structured interviews with multiple rounds exist — each round is another "test" that updates the probability, just like taking the medical test twice.

**Spam filters.** Only a small fraction of emails might be spam (say 5%). A filter that's 99% accurate at catching spam and 99% accurate at passing legitimate email will still flag some real emails as spam. The base rate of spam relative to legitimate email determines how aggressive the filter can be.

**Criminal justice.** If a forensic technique is "99.9% accurate" but the prior probability that any random person committed a specific crime is one in a million, a match is far less conclusive than it sounds.

The pattern is always the same: when the thing you're looking for is rare, even highly accurate detection methods produce more noise than signal, and you need multiple independent pieces of evidence to reach high confidence.

## The deeper insight I took away

What changed for me was realizing that Bayesian reasoning is not just a formula — it's a way of thinking about how beliefs should change in response to evidence. The formula is just the disciplined version of something we do intuitively (but badly): weighing new information against what we already know.

The reason we do it badly by default is that our brains anchor on the most vivid, recent piece of evidence — the positive test result — and forget the broader context — how rare the disease is. Bayes' theorem is a corrective for that anchoring bias. It forces you to ask: "Yes, but how likely was this *before* I saw the evidence?"

That single question — "what was the prior?" — has made me a better thinker about uncertainty, and I haven't even gotten to the deeper waters of Bayesian statistics yet.

---

*What I studied next: conditional probability and independence more formally, leading into information theory and how surprise relates to probability.*
