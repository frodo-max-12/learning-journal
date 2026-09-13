# Web Development Fundamentals & Frontend Frameworks

**Context:** Learned by reading through a real-world single-page dashboard built with vanilla HTML, CSS, and JavaScript — a mind map visualization with tabbed panels, data-driven cards, and responsive design.

---

## 1. The Three Core Languages of the Web

Every website is built with three languages that each handle a different job:

| Language | Role | Analogy |
|----------|------|---------|
| **HTML** | Structure — what's on the page | The skeleton of a building |
| **CSS** | Styling — how it looks | The paint, furniture, and decoration |
| **JavaScript** | Behavior — what it does | The electricity and plumbing |

In a single `.html` file, all three coexist:
- CSS lives inside `<style>...</style>` tags
- JavaScript lives inside `<script>...</script>` tags
- Everything else (the tags, the content) is HTML

---

## 2. How to Visually Identify Each Language

### HTML — angle brackets everywhere
```html
<div class="card">
  <h3>Title</h3>
  <p>Some text</p>
</div>
```
- Opening tags: `<div>`, `<p>`, `<h3>`
- Closing tags: `</div>`, `</p>`
- Attributes inside tags: `class="..."`, `id="..."`, `onclick="..."`

### CSS — selectors with curly braces, colons, and semicolons
```css
.card {
  background: #ffffff;
  border-radius: 12px;
  padding: 16px;
}
```
- Selectors start with `.` (class), `#` (id), or tag names like `body`
- Pattern is always: `selector { property: value; }`
- Uses units like `px`, `rem`, `%`, `vh`

### JavaScript — variables, functions, and logic
```js
const items = data.filter(item => item.count > 10);
document.getElementById('grid').innerHTML = html;
```
- Variable declarations: `const`, `let`, `var`
- `=` for assignment on standalone lines
- Arrow functions: `(a, b) => ...`
- Dot chaining: `object.method().anotherMethod()`
- Keywords: `function`, `if`, `for`, `return`

---

## 3. Key HTML Concepts Learned

- **Semantic elements** like `<header>` tell browsers and screen readers the purpose of a section
- **`<meta viewport>`** makes pages responsive on mobile devices
- **`<link>`** loads external resources like Google Fonts
- **Nesting** — tags inside tags, like Russian dolls, defines the page hierarchy
- **Empty placeholder divs** (e.g., `<div id="grid"></div>`) can be filled later by JavaScript
- **Inline event handlers** like `onclick="doSomething()"` connect HTML to JS functions
- **`<br>`** creates line breaks; `<strong>` makes text bold

---

## 4. Key CSS Concepts Learned

### CSS Custom Properties (Variables)
```css
:root {
  --accent: #4f46e5;
  --bg: #f7f7fa;
}
body { background: var(--bg); }
```
Define colors/values once, reuse everywhere. Change one line to update the whole theme.

### The Universal Reset
```css
* { margin: 0; padding: 0; box-sizing: border-box; }
```
Removes browser default spacing and makes `border-box` the sizing model (width/height includes padding and border).

### Flexbox Layout
```css
.row { display: flex; gap: 16px; flex-wrap: wrap; }
```
Arranges children in a row (or column) with gaps. `flex-wrap` lets items wrap to the next line.

### CSS Grid
```css
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
```
Creates a responsive grid that automatically adjusts column count based on available space.

### Gradient Text Effect
```css
h1 {
  background: linear-gradient(135deg, #1a1a2e, #4f46e5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```
Clips a gradient to the shape of the text — a popular design technique.

### Hover Micro-interactions
```css
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(79, 70, 229, 0.08);
}
```
Lifts an element and adds a shadow on hover for a polished feel.

### Responsive Design with Media Queries
```css
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; }
}
```
Changes layout rules based on screen size (e.g., single column on phones).

### Other Useful Patterns
- `margin: 0 auto` — centers a block element horizontally
- `position: absolute` — positions an element relative to its nearest positioned ancestor
- `overflow: hidden` — clips content that extends beyond an element's bounds
- `pointer-events: none` — makes an element invisible to clicks (pass-through)
- `transition: all 0.3s` — smoothly animates property changes over 0.3 seconds

---

## 5. Key JavaScript Concepts Learned

### DOM Manipulation
```js
document.getElementById('grid')         // Find an element by ID
document.querySelectorAll('.panel')      // Find all elements matching a CSS selector
element.classList.add('active')          // Add a CSS class
element.classList.remove('active')       // Remove a CSS class
element.innerHTML = '<p>New content</p>' // Replace an element's HTML content
```
The DOM (Document Object Model) is the browser's representation of the page as a tree of objects that JS can read and modify.

### Array Methods
```js
Object.entries(data)                    // Convert object to [key, value] pairs
  .filter(([k]) => k !== 'Other')      // Remove unwanted items
  .sort((a, b) => b[1] - a[1])         // Sort by value descending
  .map(([name, count]) => `...`)        // Transform each item into HTML
  .join('')                             // Combine all strings into one
  .reduce((sum, [, v]) => sum + v, 0)   // Sum up all values
```

### Template Literals
```js
const html = `<div class="card">
  <div class="name">${name}</div>
  <div class="count">${count}</div>
</div>`;
```
Backtick strings that allow multi-line text and embedded variables via `${...}`.

### Appending Hex Opacity
```js
style="background:${color}22"  // 22 in hex ≈ 13% opacity
style="border:1px solid ${color}44"  // 44 in hex ≈ 27% opacity
```
A trick to create tinted backgrounds by appending an alpha value to a hex color.

### Pattern: Data → HTML Rendering
The general pattern used throughout:
1. Define data as JavaScript objects/arrays
2. Loop through the data with `.map()` or `for...of`
3. Generate HTML strings with template literals
4. Inject into the page with `.innerHTML`

---

## 6. Frontend Frameworks & Libraries

### Why Do Frameworks Exist?
Vanilla JS works for small pages, but for complex apps (Gmail, Instagram, Notion) with thousands of interactive elements, manually managing the DOM becomes unmanageable. Frameworks provide:
- **Components** — reusable, self-contained building blocks
- **Reactive data** — the screen auto-updates when data changes (like a spreadsheet)
- **Structure** — organized patterns for large codebases

### The Big Three

| | React | Vue | Angular |
|---|---|---|---|
| **Created by** | Facebook (2013) | Evan You (2014) | Google (2016) |
| **Type** | Library | Progressive framework | Full framework |
| **Language** | JavaScript + JSX | JavaScript + templates | TypeScript |
| **Learning curve** | Medium | Gentle | Steep |
| **Analogy** | An engine (you pick the rest) | A well-designed car | An entire factory |
| **Used by** | Instagram, Airbnb, Netflix | Alibaba, GitLab, Nintendo | Google, Microsoft, Forbes |

### React — Key Ideas
- **JSX**: Write HTML-like syntax inside JavaScript
- **State**: Data that changes over time; when state updates, the component re-renders automatically
- **Hooks**: Functions like `useState` and `useEffect` that add features to components
- **Philosophy**: Minimal and flexible — choose your own tools for everything else

### Vue — Key Ideas
- **Single File Components**: `<template>`, `<script>`, and `<style>` in one file
- **Double curly braces**: `{{ variable }}` for inserting data into HTML
- **Scoped styles**: CSS that only affects its own component
- **Philosophy**: Approachable, well-organized, gentle learning curve

### Angular — Key Ideas
- **TypeScript required**: JavaScript with type annotations (e.g., `name: string`)
- **Decorators**: `@Component`, `@Input()` — metadata annotations on classes
- **Batteries included**: Built-in routing, forms, HTTP, testing
- **Philosophy**: Opinionated and comprehensive — suited for large enterprise teams

### The Broader Ecosystem

| Tool | What It Is |
|------|-----------|
| **Svelte** | A compiler — converts components to vanilla JS at build time, no runtime framework in the browser |
| **Next.js** | React + server-side rendering + routing + APIs (a "meta-framework") |
| **Nuxt.js** | Same concept as Next.js but for Vue |
| **Tailwind CSS** | Utility-first CSS — use pre-built classes like `text-red-500 font-bold p-4` instead of writing custom CSS |
| **jQuery** | The dominant JS tool from 2006–2015; simplified DOM manipulation before frameworks took over |

### The Evolution of Web Development
1. **HTML/CSS/JS** — simple pages with basic interactivity
2. **jQuery** — simplified verbose vanilla JS syntax
3. **Frameworks (React/Vue/Angular)** — structured component-based architecture for complex apps
4. **Meta-frameworks (Next.js/Nuxt.js)** — added server rendering, routing, and more on top
5. **Compiler-first (Svelte/Solid)** — pushing for simpler, faster approaches

Each layer exists because the previous one wasn't sufficient for growing complexity.

---

## 7. Terminology Glossary

| Term | Meaning |
|------|---------|
| **Vanilla JS** | Plain JavaScript with no frameworks or libraries |
| **DOM** | Document Object Model — the browser's tree of page elements that JS can manipulate |
| **Component** | A reusable, self-contained UI building block (used in React/Vue/Angular) |
| **State** | Data in a component that can change over time and triggers re-rendering |
| **Reactive** | The UI automatically updates when underlying data changes |
| **JSX** | React's syntax for writing HTML-like code inside JavaScript |
| **TypeScript** | JavaScript with added type checking (used by Angular) |
| **Compiler** | A tool that transforms code from one form to another before it runs |
| **Runtime** | Framework code that runs in the browser alongside your code |
| **Server-side rendering (SSR)** | Generating HTML on the server before sending to the browser |
| **Responsive design** | Making a page adapt its layout to different screen sizes |
| **Semantic HTML** | Using tags that describe meaning (e.g., `<header>`, `<nav>`) not just appearance |
| **Flexbox** | CSS layout mode for arranging items in a row or column |
| **CSS Grid** | CSS layout mode for two-dimensional grid layouts |
| **Media query** | CSS rule that applies styles only at certain screen sizes |

---

*Learned by reverse-engineering a real dashboard project — the best way to learn code is to read code.*
