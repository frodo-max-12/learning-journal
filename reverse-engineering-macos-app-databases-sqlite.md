# Reverse-Engineering a macOS App's Database

## What I learned today

### 1. Apps store data in hidden places
- macOS apps store their data in `~/Library/Application Support/`
- The `~` symbol means your home folder (`/Users/you`)
- `Library` is a hidden folder — you need `Cmd + Shift + G` in Finder to navigate there
- Wispr Flow stores everything at: `~/Library/Application Support/Wispr Flow/`

### 2. The `find` command — searching for files
- `find ~/Library -iname "*wispr*"` searches for files with "wispr" in the name
- `-iname` = case-insensitive name search
- `*` = wildcard (matches anything before/after)
- `| head -30` = pipe the output and show only first 30 lines

### 3. The `ls` command — listing files
- `ls -la` shows all files in a folder with details
- `-l` = long format (size, dates, permissions)
- `-a` = include hidden files (files starting with `.`)
- `\` before spaces = "escape" the space (tells terminal it's part of the name)

### 4. SQLite — the world's most common database
- **SQLite** is a database stored in a single file (`.sqlite`)
- Used everywhere: iMessage, Safari, Photos, Chrome, Wispr Flow
- `sqlite3` is a tool built into every Mac to read these databases
- Wispr Flow's database: `flow.sqlite` (~400MB)

### 5. SQL — talking to databases
- **SQL** (Structured Query Language) is the universal language for databases
- Think of a database table like an Excel spreadsheet

| SQL Command | What it does |
|---|---|
| `.tables` | List all tables (like sheets in Excel) |
| `.schema History` | Show column names of a table |
| `SELECT * FROM History LIMIT 3` | Get first 3 rows |
| `SELECT COUNT(*) FROM History` | Count total rows |
| `MIN(timestamp)`, `MAX(timestamp)` | Earliest and latest entries |
| `SUM(numWords)` | Add up all word counts |
| `COALESCE(a, b, '')` | Use `a` if available, else `b`, else empty |
| `ORDER BY timestamp ASC` | Sort oldest to newest |

### 6. Piping and text processing
- `|` (pipe) takes output of one command and feeds it into the next
- `awk` is a text processing tool — reformats data
- `>` writes output to a file instead of showing on screen
- `wc -w file.txt` counts words in a file

### 7. The developer's thinking pattern
```
find → inspect → understand → extract
```
1. **Find** — where's the data? (`find`)
2. **Inspect** — what files exist? (`ls`)
3. **Understand** — what's the structure? (`.tables`, `.schema`, `SELECT LIMIT 3`)
4. **Extract** — get what you need (`SELECT ... > file.txt`)

This is essentially what every "Export Data" button in any app does — an ETL (Extract, Transform, Load) pipeline.

## Commands I ran today

```bash
# Step 1: Find where Wispr Flow stores data
find ~/Library -iname "*wispr*" | head -30

# Step 2: List files in that folder
ls -la ~/Library/Application\ Support/Wispr\ Flow/

# Step 3: See database tables
sqlite3 ~/Library/Application\ Support/Wispr\ Flow/flow.sqlite ".tables"

# Step 4: See History table structure
sqlite3 ~/Library/Application\ Support/Wispr\ Flow/flow.sqlite ".schema History"

# Step 5: Peek at 3 rows
sqlite3 ~/Library/Application\ Support/Wispr\ Flow/flow.sqlite "SELECT timestamp, formattedText FROM History LIMIT 3"

# Step 6: Check stats
sqlite3 ~/Library/Application\ Support/Wispr\ Flow/flow.sqlite "SELECT COUNT(*) as total_transcripts, MIN(timestamp) as earliest, MAX(timestamp) as latest, SUM(numWords) as total_words FROM History"

# Step 7: Export all transcripts to a text file
sqlite3 -separator '|||' ~/Library/Application\ Support/Wispr\ Flow/flow.sqlite "SELECT timestamp, COALESCE(formattedText, asrText, '') FROM History ORDER BY timestamp ASC" | awk -F'\\|\\|\\|' '{ ts = $1; text = $2; if (text != "") { printf "\n[%s]\n%s\n", ts, text } }' > ~/Desktop/wispr_flow_export.txt

# Step 8: Verify word count
wc -w ~/Desktop/wispr_flow_export.txt
```

## Key takeaways
- Every app on your computer has a database you can explore
- The terminal gives you superpowers that no GUI can match
- SQL is one of the most valuable skills to learn — it works on any database, anywhere
- The `find → inspect → understand → extract` pattern works for any data problem
