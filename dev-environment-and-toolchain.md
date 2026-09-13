# Setting Up My Dev Environment

## What I learned today

### 1. The Terminal
- The terminal is a text-based way to talk to your computer
- Commands are typed, not clicked
- Silence (no output) usually means success

### 2. Node.js and npm
- **Node.js** lets your computer run JavaScript code
- **npm** (Node Package Manager) is like an app store for code
- `npm install -g <package>` installs a package globally (available everywhere)
- The `-g` flag means "global"

### 3. Git basics
- **Git** is a version control tool — it tracks changes to your files over time
- `git init` starts tracking a folder
- `git config --global` sets settings for all projects on your computer
- Every commit needs a name and email attached to it

### 4. GitHub and the GitHub CLI
- **GitHub** is a website that stores your git repositories online
- **gh** is GitHub's command-line tool
- `gh auth login` connects your terminal to your GitHub account
- Tokens are like temporary passwords that let your terminal access GitHub

### 5. Homebrew
- **Homebrew** is a package manager for macOS
- `brew install <tool>` installs tools on your Mac

### 6. Key commands I used today
| Command | What it does |
|---------|-------------|
| `node --version` | Check Node.js version |
| `npm --version` | Check npm version |
| `npm install -g openclaw` | Install OpenClaw globally |
| `git config --global user.name "Name"` | Set git username |
| `git config --global user.email "email"` | Set git email |
| `brew install gh` | Install GitHub CLI |
| `gh auth login` | Log into GitHub |
| `git init` | Start tracking a folder with git |

## What I set up
- [x] Node.js and npm (already installed)
- [x] OpenClaw (installed via npm)
- [x] Git (configured name and email)
- [x] GitHub CLI (installed and logged in)
- [ ] OpenClaw onboarding (next step!)
