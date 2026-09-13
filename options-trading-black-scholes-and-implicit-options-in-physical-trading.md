# Options, Black-Scholes, and the hidden options inside every trade — from first principles

*Learned on April 7, 2026. SEBI's ban on Jane Street came up in the news, and I realized I never actually understood options properly. The conversation turned into one of the most useful bridges I've found between finance theory and the physical semiconductor trading I do every day.*

---

## The starting point: SEBI vs Jane Street

SEBI had just hit Jane Street with the largest disgorgement order in Indian securities history -- roughly 4,843 crore rupees. The accusation was that Jane Street had been manipulating the Bank Nifty index on derivative expiry days: pumping component stocks in the morning session while building short option positions, then dumping the stocks in the afternoon so those option positions would print money at expiry.

I read the headlines and realized something embarrassing. I had been hearing words like "calls," "puts," "short positions," and "expiry" for years -- in newspapers, on Twitter, in conversations with friends in finance -- and I still did not actually understand what any of it meant at a mechanical level. Not the vibes, the mechanics. What exactly was Jane Street doing, and why did it work?

That question led me somewhere I did not expect: straight back to my own business.

## What an option actually is

The core idea is deceptively simple. An option is the right to do something, without the obligation. You pay a small fee upfront -- the premium -- to lock in that right for a fixed period of time. If things go your way, you exercise the right. If they do not, you walk away. You only lose the premium.

There are two flavors:

- A **call option** gives you the right to *buy* at a fixed price (the strike price)
- A **put option** gives you the right to *sell* at a fixed price

The analogy that made it click for me was from my own world. Imagine I am trading MCUs through a components distributor. A customer needs 10,000 units of STM32F103 in three weeks. I do not have stock yet, but I know a supplier in Shenzhen who might sell at 80 rupees per unit. The customer will pay 120.

Now imagine the supplier says: "Pay me 5 rupees per unit today, and I guarantee you can buy at 80 per unit anytime in the next 30 days. But you do not have to." That 5 rupees is the option premium. I just bought a call option with a strike price of 80 and a 30-day expiry.

**If the market price jumps to 150**, I exercise the option, buy at 80, sell at 120 to my customer. My all-in cost is 85 per unit (80 + the 5 premium), so I clear 35 per unit in profit. Without the option, I would have had to buy at 150 and lose money on the deal.

**If the market floods and the price drops to 50**, I walk away. I lose 5 per unit -- the premium -- and nothing more. I am not forced to buy at 80 when the open market price is 50.

That asymmetry -- limited downside, large upside -- is the entire architecture of options. It is insurance with leverage built in.

A put is the mirror image. If I am holding 50 lakh rupees of DRAM inventory and I am worried prices will crash, a put lets me sell at today's price regardless of what happens. If prices crash, I exercise the put. If prices rise, I let it expire worthless and sell at the higher market price. The premium is just the cost of sleeping well at night.

## The four basic positions

Once you understand calls and puts, there are four things you can do, and each represents a different bet about the future:

| Position | You think... | Risk profile |
|---|---|---|
| **Buy a call** | Price goes UP | Limited loss (premium), unlimited upside |
| **Buy a put** | Price goes DOWN | Limited loss (premium), large upside |
| **Sell a call** | Price stays flat or drops | Collect premium, but unlimited risk if price rockets |
| **Sell a put** | Price stays flat or rises | Collect premium, but large risk if price crashes |

Buying options is like buying insurance. Selling options is like being the insurance company. Most of the time, nothing dramatic happens and the seller pockets the premium. But when something dramatic does happen, the seller gets crushed. This is why selling options is profitable on average but catastrophic at the tails.

And this is exactly what Jane Street was doing. They were selling call options and buying put options on Bank Nifty -- both bets that profit when the index falls. Then they artificially pumped the index in the morning (making those options look worthless so they could sell at fat premiums) and dumped it in the afternoon so their short positions would pay off at expiry. They were engineering the very outcome they had bet on.

## How do you price an option? The Black-Scholes intuition

So the natural next question: if I pay a premium for an option, what should that premium actually be? Why 5 rupees and not 2 or 15?

Fischer Black and Myron Scholes answered this in 1973, and the intuition behind their formula is more useful than the math itself. An option's price is essentially the probability-weighted average of all possible payoffs at expiry, discounted back to today. Five inputs determine it:

| Input | What it means | Effect on option price |
|---|---|---|
| **Current price (S)** | Where the asset trades right now | Higher S makes calls more valuable, puts less |
| **Strike price (K)** | The price you are locking in | Lower K makes calls more valuable |
| **Time to expiry (T)** | How long the option lasts | More time = more expensive (more can happen) |
| **Volatility (sigma)** | How wildly the price swings | Higher volatility = option worth more |
| **Risk-free rate (r)** | Cost of tying up money | Minor factor, but it is there |

Here is what I found remarkable: four of these five inputs are directly observable. You can look up the current price, the strike price, the time remaining, and the interest rate. The one thing you are actually debating when you trade options is **volatility** -- how much will the price move between now and expiry?

This leads to a concept called **implied volatility**. Instead of plugging volatility into Black-Scholes to get a price, traders work backwards. They take the market price of an option and reverse-engineer what level of volatility the market is implicitly assuming. When financial news says "the VIX is at 25," they are saying the options market implies 25% annualized volatility in the S&P 500. The VIX is not a measurement of actual volatility -- it is a measurement of the market's *fear*.

## Time decay and the Greeks

Every option has a ticking clock. Each day that passes, the option loses some of its time value -- a phenomenon called **theta decay**. This accelerates as expiry approaches. On day 1 of a 30-day option, you might lose 0.20 per day. On day 28, you might lose 1.50 per day. The last few days before expiry are where things get intense, because small price moves translate into enormous swings in option value.

This is precisely why Jane Street operated on expiry days. Near expiry, a concept called **gamma** -- the rate at which an option's sensitivity to price changes is itself changing -- goes through the roof. A small push on the index in the right direction at the right time can flip the value of billions of rupees in option positions. The timing was not incidental. It was the entire strategy.

The Greeks -- delta, gamma, theta, vega -- are really just sensitivity dials. Delta tells you how much your option moves per rupee move in the stock. Gamma tells you how fast delta itself is changing. Theta is the daily time decay. Vega measures sensitivity to volatility shifts. You do not need to memorize the formulas. The mental model is: options are not static bets; they are living instruments whose characteristics change every day, every hour, as the inputs shift.

## The bridge to physical trading: implicit options everywhere

This is where the conversation took a turn that genuinely changed how I think about my own work. Every deal I do in semiconductor spot trading has an options structure embedded in it, even though no formal option contract exists.

**When I find demand but have not locked in supply**, I am holding a real call option. A customer says they need 10,000 MCUs and will pay 120 per unit. I think I can source at 80-90. The strike price is my best sourcing price. The expiry is however long the customer will wait. The premium is my time and effort. If sourcing volatility is low (I have three reliable suppliers), this is a deep in-the-money call -- just execute it. If sourcing is uncertain and the part is constrained, this is an at-the-money call with high time value. Worth pursuing, but also worth hedging by locking in a supplier quote with a small deposit before confirming the customer order.

**When I am holding inventory without a confirmed buyer**, I am long the underlying asset and my risk is that prices drop. The implicit put question becomes: at what price would I cut my losses and sell? If I bought NAND flash at 200 per unit, expect to sell at 280, but would dump at 180 -- I have mentally set a strike price of 180 with an implicit premium of 20 per unit. The discipline is that I need to actually execute at 180, not hold and hope. In formal options, the structure forces you -- the contract expires. In physical trading, I have to be the enforcement mechanism.

**When a customer asks me to hold a price for two weeks**, I have effectively sold them a call option. They can walk away; I cannot. The question is: what should I charge for this? Black-Scholes logic says it depends on the volatility of that component's price, the length of the commitment window, and my sourcing certainty. The practical takeaway is that I should never hold price for free on volatile parts. A non-refundable booking deposit is literally an option premium the customer pays me.

> The deepest insight from this conversation: options theory is not just a financial markets thing. It is a framework for thinking about any situation where you are managing uncertainty over time. The five Black-Scholes inputs -- current price, target price, time, volatility, and the cost of capital -- apply just as much to a semiconductor deal as they do to a Nifty derivative.

## What made this click

I think the reason options never made sense to me before is that every explanation I encountered started with the jargon -- calls, puts, strike, expiry -- as if these were abstract financial concepts you had to memorize. What made it click this time was starting from a situation I already understood (trading chips, locking in supplier prices, managing inventory risk) and recognizing that the option structure was already there, hiding in plain sight. The finance vocabulary was just naming patterns that physical traders have dealt with forever.

Jane Street was not doing anything conceptually exotic. They were doing what every trader does -- managing the relationship between information, timing, and price -- but at a scale and speed that crossed the line from arbitrage into manipulation. Understanding options helped me see both what they did and why SEBI was right to call it out.

---

*What I studied next: [MCP vs CLI -- how AI tools connect to the world](mcp-vs-cli-how-ai-tools-connect-to-the-world.md), where I explored how the tools I use every day actually communicate under the hood.*
