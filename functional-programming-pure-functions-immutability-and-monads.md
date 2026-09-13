# Functional programming — pure functions, immutability, and monads

*Learned on March 1, 2026. I picked up "Functional Programming in Scala" (the Red Book by Chiusano and Bjarnason) because I wanted to understand the paradigm that keeps coming up in conversations about reliable software. This is what I took away from working through it.*

---

## Two ways to think about programming

Most programming I had encountered before this was **imperative** — you write a sequence of instructions that change things. Create a variable, modify it, loop through a list and update a counter, write to a file, change the state of an object. The program is a series of commands: do this, then do that, then change this.

Functional programming starts from a completely different premise. Instead of telling the computer *what to do step by step*, you describe *what things are*. A program is not a sequence of mutations — it is a composition of functions, each one transforming inputs into outputs without changing anything in the world around it.

The difference sounds philosophical until you see the practical consequences.

## Pure functions — the foundation of everything

A **pure function** has two properties:

1. **Same input always produces the same output.** If I call `add(3, 5)`, I get 8. Every time. Regardless of the time of day, the state of the database, or what other code ran before it.
2. **No side effects.** The function does not modify anything outside itself — no changing global variables, no writing to files, no printing to the screen, no updating a database.

This is called **referential transparency**: any call to a pure function can be replaced with its return value without changing the behavior of the program. If `add(3, 5)` is always 8, then anywhere I see `add(3, 5)` in my code, I can substitute 8, and nothing breaks.

Why does this matter? Consider this imperative code:

```scala
var total = 0
def addToTotal(x: Int): Int = {
  total += x    // side effect: modifying external state
  total
}
```

Calling `addToTotal(5)` the first time gives 5. Calling it again gives 10. The same input produces different outputs because the function depends on — and modifies — external state. I cannot reason about this function in isolation. I need to know the entire history of calls to understand what it will return.

Now contrast with the pure version:

```scala
def add(a: Int, b: Int): Int = a + b
```

I can understand this function completely by reading its definition. I can test it without setting up any state. I can call it from multiple threads without locks. I can rearrange the order of calls without fear. The function is a self-contained unit of logic.

> Pure functions are honest. Their type signature tells you everything they might do. An impure function's type signature lies — it says "I take an Int and return an Int" but secretly modifies a database.

## Immutability — the companion principle

If functions cannot have side effects, then data cannot be mutable. These two ideas are inseparable. In functional programming, once you create a value, it never changes. You do not update a list — you create a new list with the modifications. You do not change a variable — you bind a new name to a new value.

This sounds wasteful. If I have a list of a million elements and I want to add one, do I really copy the entire list? In practice, functional data structures use **structural sharing** — the new list shares almost all of its memory with the old one, only creating new nodes where things differ. Think of it like a wiki edit history: each version looks like a complete document, but under the hood it's storing only the diffs.

The payoff is enormous. If data never changes, an entire category of bugs disappears:

- No race conditions (two threads modifying the same data)
- No temporal coupling (function A must run before function B because B depends on A's side effect)
- No defensive copying (passing data to a function and worrying it might modify your copy)
- No "what changed this?" debugging sessions

I realized this connects to something I already understood from business: a ledger. In accounting, you don't erase entries — you add new entries that adjust the balance. The entire history is preserved. Immutability is the same principle applied to data in a program.

## Handling the real world: Option and Either

An immediate objection: if functions can't fail, can't throw exceptions, can't return null — how do you handle errors? Functional programming's answer is to make failure **explicit in the type system**.

Instead of a function that might return a value or might throw an exception:

```scala
def findUser(id: Int): User  // might throw NotFoundException!
```

You return a type that honestly represents the possibility of failure:

```scala
def findUser(id: Int): Option[User]  // returns Some(user) or None
```

`Option[User]` is an **algebraic data type** — it is either `Some(user)` (containing a value) or `None` (empty). The caller is forced to handle both cases. No null pointer exceptions. No forgotten try-catch blocks. The type system itself prevents you from ignoring the error case.

For richer error information, there is `Either[Error, User]`:

```scala
def findUser(id: Int): Either[String, User]  // returns Left("not found") or Right(user)
```

`Left` carries the error, `Right` carries the success. The naming convention is a bit odd, but the principle is powerful: errors are values, not exceptions. They flow through your program like any other data, composed and transformed using normal functions.

| Approach | How failure works | Caller must handle it? | Composable? |
|----------|------------------|----------------------|-------------|
| Exceptions | Thrown at runtime, interrupts flow | No (can forget try-catch) | Poorly |
| Null returns | Returns null, caller may not check | No (null propagates silently) | No |
| Option/Either | Returns a value encoding success or failure | Yes (compiler enforces it) | Yes |

## Strictness versus laziness

Scala (and most languages) are **strict** by default: expressions are evaluated the moment they are bound. If I write `val x = expensiveComputation()`, the computation runs immediately.

**Lazy** evaluation defers computation until the value is actually needed. The Red Book introduces this through `Stream` — a lazy list where elements are computed only when requested. This enables something that seems impossible: working with infinite data structures.

```scala
val naturals: Stream[Int] = Stream.from(1)  // 1, 2, 3, 4, ... forever
val firstTenEvens = naturals.filter(_ % 2 == 0).take(10).toList
// [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
```

This works because `filter` and `take` don't process the entire infinite stream — they produce a new description of a stream that will compute elements on demand. Only the 10 elements I asked for are ever materialized.

Laziness also enables **fusion** — chaining multiple operations (map, filter, take) that get executed in a single pass through the data, rather than creating intermediate collections at each step.

## The big abstraction: monads

This is the concept that everyone warns you about. "You'll read 50 monad tutorials and not understand monads, and then one day it clicks." I think the difficulty is that people explain monads in terms of category theory when the practical intuition is actually simple.

A **monad** is a design pattern for chaining operations that have some extra context.

Take `Option`. I have a chain of computations where each one might fail:

```scala
def getUser(id: Int): Option[User]
def getAddress(user: User): Option[Address]
def getCity(address: Address): Option[String]
```

I want to chain these: get the user, then get their address, then get the city. But each step might return `None`. Without monads, I'd write:

```scala
getUser(42) match {
  case Some(user) => getAddress(user) match {
    case Some(address) => getCity(address)
    case None => None
  }
  case None => None
}
```

Nested, repetitive, ugly. The monad pattern — specifically `flatMap` — lets me write:

```scala
getUser(42).flatMap(user => 
  getAddress(user).flatMap(address => 
    getCity(address)))
```

Or even more cleanly with Scala's for-comprehension:

```scala
for {
  user    <- getUser(42)
  address <- getAddress(user)
  city    <- getCity(address)
} yield city
```

This reads like straight-line code, but the `Option` monad is silently handling the failure case at every step. If `getUser` returns `None`, the whole chain short-circuits to `None`. No explicit error checking.

The key insight the Red Book drills home is that `List`, `Option`, `Either`, `State`, `IO` — they all support `flatMap`, and they all represent the same abstract pattern: **sequential computation where each step depends on the result of the previous one, with some extra context being managed automatically.** For `Option`, the context is "this might be empty." For `List`, it's "there might be multiple results." For `State`, it's "there's some state being threaded through." For `IO`, it's "this interacts with the outside world."

> A monad is not a burrito, not a box, not a space suit. It is the pattern of sequencing dependent computations where each step can produce a context (emptiness, multiplicity, state, effects) that gets handled uniformly by `flatMap`.

## Programs as descriptions

The deepest idea in the Red Book is one that took me a while to absorb. In pure functional programming, you do not *perform* effects — you *describe* them. An `IO[String]` value is not a string that was read from the console. It is a description of a program that, *when executed*, will read from the console and produce a string.

This separation of description from execution is what makes functional programs testable. You can inspect, compose, and transform descriptions without actually running them. You can swap out the interpreter — run the same description against a real database in production and a mock in testing. The program becomes a value, and values are things you can reason about.

This is the same principle I already understood from a completely different domain: a recipe is not a cake. A recipe is a description that, when executed by a baker with ingredients, produces a cake. You can analyze, modify, and share the recipe without ever turning on the oven. Functional programming treats all programs this way.

## What stayed with me

The Red Book's approach — building every abstraction from scratch, proving it works through exercises, then revealing that disparate things share the same algebraic structure — changed how I think about software design. The methodology is transferable: define a small set of operations, state the laws they must satisfy, then find implementations. This is algebra-driven design, and it works whether you're writing Scala, TypeScript, or Python.

I don't think functional programming is the only way to write software. But understanding it gave me a vocabulary for expressing ideas about correctness, composition, and effects that I didn't have before.

---

*What I studied next: algebraic data types and pattern matching in more depth, and how Haskell's type system enforces purity at the language level rather than by convention.*
