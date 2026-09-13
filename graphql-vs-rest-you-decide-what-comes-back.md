# GraphQL vs REST — Who Decides What Comes Back

**Context:** I'd spent a while learning REST APIs, felt like I understood "how APIs work," and then hit one that used **GraphQL** instead. That forced me to realize I'd learned *one* way an API can work, not the general case. The difference between the two comes down to a single question — *who decides what data you get back?* — and almost everything else follows from the answer.

---

## 1. The one-sentence difference

**REST: the server decides what you get.**

```
GET /v1/catalog/products/XC7A200T-2FBG484I

→ returns everything the endpoint returns — specs, images, marketing copy,
  documents, attributes — even if you only wanted the stock quantity.
```

**GraphQL: you decide what you get.**

```graphql
{
  supSearchMpn(q: "XC7A200T-2FBG484I") {
    results {
      part {
        mpn
        manufacturer { name }
        sellers {
          company { name }
          offers { inventoryLevel prices { price currency } }
        }
      }
    }
  }
}

→ returns only the fields listed. Nothing else.
```

The analogy that made it stick: REST is a **fixed menu** — order the chicken and you get the plate as the kitchen composes it, sides and garnish included. GraphQL is a **build-your-own bowl** — you name the ingredients.

---

## 2. One endpoint instead of many

This is the difference you notice first in practice, and it's a direct consequence of the first one.

**REST has many endpoints**, because the URL is how you say what you want:

```
GET /v1/catalog/products/{mpn}    ← product details
GET /v1/catalog/categories        ← categories
GET /v1/catalog/manufacturers     ← manufacturers
GET /v1/search?q=FPGA             ← search
```

**GraphQL has one:**

```
POST https://api.example.com/graphql    ← everything goes here
```

Every request goes to the same URL, and the **query in the body** says what you want. One door that leads everywhere, instead of many separate doors.

Which relocates something rather than removing it. In REST, the API's structure is expressed in its **URL space** — you learn the API by learning its endpoints. In GraphQL, the structure is expressed in its **schema** — you learn it by learning the type graph. Same complexity, different place to look for it.

---

## 3. Reading a GraphQL query

The syntax looked alien until I saw the one property that organizes it:

```graphql
query Search($mpn: String!) {     ← name the query; $mpn is a String; ! means required
  supSearchMpn(q: $mpn, limit: 2) {
    results {
      part {
        mpn
        manufacturer { name }      ← the manufacturer object, but ONLY its name
        specs {
          attribute { shortname }
          value
        }
      }
    }
  }
}
```

> **The structure of the query mirrors the structure of the response.**

What you write is the shape of what comes back. Omit a field and it won't be there. Nest a selection and you get a nested object. That's why it's readable once you stop looking for REST's verbs and paths — the query *is* the response with the values removed.

**Variables** keep queries reusable — declare `$mpn` in the query, pass `{"mpn": "..."}` alongside it, and the same query text serves every lookup. That separation is what makes queries cacheable and safely parameterized, the same reason prepared statements exist in SQL.

---

## 4. Why GraphQL exists at all

Two failure modes of REST, which the design targets directly:

**Over-fetching.** You wanted a stock number and got a page of marketing copy. On a mobile connection that's real bandwidth, and it's the problem the format was originally built to solve.

**Under-fetching — the "N+1" round trip.** You need parts, and for each part its sellers, and for each seller their offers. In REST that's one request for the list plus N requests for the details. In GraphQL it's one query, because the nesting is expressed in the request.

And the reason it originated at a company building mobile clients is exactly that: many different screens each needing a different slice of the same graph, over connections where a round trip is expensive. Rather than building a bespoke endpoint per screen, let the client describe its slice.

---

## 5. What GraphQL gives up

The honest other half, because "you decide what you get" isn't free:

**HTTP caching stops working the easy way.** REST's `GET /products/123` is a cacheable URL — proxies, browsers, and CDNs all understand it. Every GraphQL request is a `POST` to the same URL with a different body, so none of that infrastructure helps and caching moves into the application.

**The server can't predict its own load.** A client can compose a legal query that's enormously expensive — deep nesting, wide fan-out. REST endpoints have bounded, known cost; GraphQL needs query-depth limits and cost analysis to avoid a single request doing damage.

**Errors get subtler.** A REST call fails with a status code. A GraphQL request can return HTTP 200 with a `data` field that's partially filled and an `errors` array beside it. "Did it work?" stops being a one-line check.

So it isn't strictly better — it's a different distribution of who bears the complexity. **REST puts the burden on the API designer to anticipate what clients need. GraphQL puts it on the client to ask well, and on the server to defend itself.**

---

## 6. Two APIs, two shapes, and why

The pair I was comparing made the design logic legible:

| | the REST one | the GraphQL one |
|---|---|---|
| what it is | one supplier's own catalog | an **aggregator** across thousands of suppliers |
| API style | REST | GraphQL |
| analogy | one restaurant's menu | a delivery app carrying every restaurant's menu |
| auth | public endpoints | always authenticated |

That difference isn't fashion. A single catalog has a small, stable set of things you'd want and a natural URL per thing. **An aggregator is a graph** — parts have sellers, sellers have offers, offers have prices, and every client wants a different depth through it. The data shape argues for the API style.

Which is the takeaway I'd keep: **when you meet an API, the style tells you something about the data behind it.**

---

## 7. What I took away

**"I understand APIs" meant "I understand REST."** One example is not the category, and I wouldn't have found that out without hitting a second one that broke my expectations.

**Ask who decides the response shape.** That single question separates the two designs and predicts nearly every downstream difference — endpoint count, caching story, over-fetching, error handling.

**Flexibility relocates cost, it doesn't remove it.** Letting clients specify the response solved over-fetching and created a load-prediction problem, a caching problem, and a subtler error model. That's the same trade I keep meeting — the cost moves to a different party or a different phase, and whether that's an improvement depends on who's better placed to bear it.
