# OAuth, Scopes, and How an API Knows Who You Are

**Context:** I wanted a command-line tool to read my own mail, and what should have been a five-minute setup turned into a sequence of errors I didn't understand — `invalid_scope`, then `access_denied`, then a warning that the app hadn't completed verification. Fixing them one at a time taught me more about how API authorization actually works than any explanation would have, because each error corresponded to a distinct concept I'd been treating as one thing called "logging in."

---

## 1. There is no single API — the layering

The first correction, before any auth. I'd assumed there was one big "Workspace API." There isn't:

```
Layer 3:  a CLI / a script / raw curl
              ↓ uses
Layer 2:  the Gmail API, the Drive API, the Calendar API — separate APIs
              ↓ talks to
Layer 1:  the actual services
```

**Each service has its own API**, and the CLI is a wrapper that translates terminal commands into HTTP requests against those endpoints. A script, a browser extension, and a `curl` command are all peers — different interfaces to the same kitchen.

That matters for auth because **you don't authorize "the account," you authorize an application to reach specific APIs on your behalf.** Every piece of the model below follows from that sentence.

---

## 2. The pieces, and what each is for

Six concepts hide behind the phrase "log in," and I needed all six before anything worked:

| piece | what it actually is |
|---|---|
| **project** | a container the provider uses to track API usage. Every call must belong to one. |
| **enabling an API** | APIs are **off by default** and must be explicitly switched on per project |
| **OAuth credentials** (`client_id` + `client_secret`) | identifies *the application* — not you |
| **consent screen** | the "this app wants access to your mail" dialog |
| **scopes** | precisely what the app may do — read mail, edit files, and so on |
| **test user** | while the app is unverified, only explicitly listed accounts may authorize it |

The distinction that unlocked it: **credentials identify the application; the login identifies you; scopes define what the combination may do.** Three separate things, and I'd been collapsing them into "credentials."

That's also why the client secret isn't a password to your account. It says *this is that application*. Your account access still requires you to click through consent, and the app still only gets what the scopes allow.

---

## 3. Scopes — the mistakes were the lesson

Scopes are permissions, in the sense a phone app asks for camera access. They're offered in bundles: a recommended set for ordinary use, a read-only set, and a full set including administrative permissions.

**Mistake 1 — I selected every scope.** Reasoning that more permissions meant fewer problems later. Result: `Error 400: invalid_scope`.

The cause is a genuine constraint: some scopes are **organization-only** — device and identity management permissions that don't exist for a personal account. Requesting a permission that cannot apply to you isn't ignored, it's rejected outright.

That inverted my model. I'd assumed scopes were a superset you narrow for politeness. They're **assertions about what the app will do, validated against what your account type can grant.** Asking for everything is not the safe default; it's a request that can be structurally invalid.

**Mistake 2 — I hadn't added myself as a test user.** Result: `Error 403: access_denied`, with a message that the app hadn't completed verification.

The cause: an application that hasn't been through the provider's review is in testing mode, and in testing mode **only explicitly listed accounts may authorize it** — including your own. Being the person who created it grants you nothing automatically.

**The fix** was both together: list myself as a test user, and request only the recommended scopes.

---

## 4. Why the friction exists, and why it's the right design

My instinct while fighting it was that this was gratuitous. Working through it, the opposite is true, and the reasons are worth stating because they're the argument for the whole model:

**Scopes exist so a compromised app is a bounded loss.** A tool that reads mail should not be able to delete files. Without scopes, authorizing anything authorizes everything, and the blast radius of any single bad tool is your entire account.

**The verification gate exists because consent screens are the attack surface.** A convincing dialog asking for access to your mail is exactly what a phishing app shows you. Unverified apps being limited to a list of accounts the developer explicitly named is what stops an unreviewed app from soliciting consent at scale.

**APIs being off by default is the same principle at the project level** — the reachable surface starts empty and you switch on only what you need.

So the errors weren't obstacles to route around. Each one was **the system correctly refusing an over-broad request**, and the fix in every case was to ask for less.

---

## 5. What I'd tell someone starting

**Request the narrowest scope set that does the job, first.** Not because it's tidy — because over-broad requests fail outright, and because narrowing later means going back through consent anyway.

**Read the error code as a diagnosis.** `invalid_scope` means *you asked for something that cannot apply to this account*. `access_denied` at the consent step means *this app isn't permitted to ask you yet*. They look similar in a terminal and they're completely different problems.

**And remember which identity each piece asserts.** When something fails, ask: is the *application* not recognized (credentials), is the *user* not permitted to consent (test user / verification), or is the *permission* not grantable (scopes)? Three questions, three fixes, and guessing between them is what turned five minutes into an afternoon.

---

## 6. What I took away

**"Log in" was hiding six concepts.** Project, enabled APIs, application credentials, consent, scopes, and user eligibility are separate mechanisms with separate failure modes, and no progress was possible until I stopped treating them as one.

**Asking for more permission is not the safe default.** It's the failing default — sometimes rejected outright, always increasing what a compromise costs.

**The friction is the feature.** Every step that annoyed me is a bound on what a badly-behaved application can do with an account that isn't its own. That's a design I'd want on the other side of it too — and the fastest way to internalize it was to hit each guard rail in turn and work out what it was protecting.
