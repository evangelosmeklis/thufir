# Useful Git Aliases for Root Cause Analysis

Git aliases streamline common RCA investigation commands. Add these to your `~/.gitconfig` file under the `[alias]` section.

## Installation

Edit your `~/.gitconfig`:

```bash
vim ~/.gitconfig
```

Add aliases under `[alias]` section:

```ini
[alias]
  # Your aliases here
```

Or use `git config` command:

```bash
git config --global alias.today 'log --since="1 day ago" --oneline'
```

## Essential RCA Aliases

### Log Aliases

**Recent commits (today)**:
```ini
today = log --since="1 day ago" --oneline --decorate
```

Usage: `git today`

**Recent commits (this week)**:
```ini
week = log --since="1 week ago" --oneline --decorate
```

Usage: `git week`

**Pretty log with graph**:
```ini
lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --date=relative
```

Usage: `git lg`

**File history with diffs**:
```ini
flog = log -p --follow
```

Usage: `git flog -- path/to/file.js`

**Search commit messages**:
```ini
search = log --all --grep
```

Usage: `git search "database"`

**Show commits by author**:
```ini
who = log --author
```

Usage: `git who "Developer Name"`

**Timeline (commits with date)**:
```ini
timeline = log --pretty=format:'%C(yellow)%h%Creset %C(cyan)%ad%Creset | %s %C(green)(%an)%Creset' --date=short
```

Usage: `git timeline --since="2025-12-19"`

### Diff Aliases

**Show changes in last commit**:
```ini
last = diff HEAD~1 HEAD
```

Usage: `git last`

**Word-level diff**:
```ini
wdiff = diff --word-diff
```

Usage: `git wdiff commit1 commit2`

**Diff with stats**:
```ini
ds = diff --stat
```

Usage: `git ds commit1 commit2`

### Blame Aliases

**Blame with line numbers**:
```ini
bl = blame -w -C -C -C
```

Usage: `git bl path/to/file.js`

**Blame specific line range**:
```ini
blr = blame -L
```

Usage: `git blr 40,50 path/to/file.js`

### Show Aliases

**Show commit with stat**:
```ini
ss = show --stat
```

Usage: `git ss commit_sha`

**Show files changed in commit**:
```ini
files = show --name-only
```

Usage: `git files commit_sha`

**Show commit summary**:
```ini
summary = show --oneline --stat
```

Usage: `git summary commit_sha`

## Investigation Workflow Aliases

### Find Recent Changes

**All changes in last 24 hours**:
```ini
recent = log --since='1 day ago' --all --stat --oneline
```

Usage: `git recent`

**Changes to specific directory**:
```ini
dirlog = log --oneline --
```

Usage: `git dirlog src/config/`

### Track Specific Code

**Find when code was added or removed**:
```ini
find-code = log -S
```

Usage: `git find-code "max: 100"`

**Find when code pattern changed**:
```ini
find-pattern = log -G
```

Usage: `git find-pattern "pool.*max"`

### Commit Details

**Full commit details**:
```ini
details = show --format=full
```

Usage: `git details commit_sha`

**Commit with patch**:
```ini
patch = format-patch -1
```

Usage: `git patch commit_sha`

## Advanced RCA Aliases

### Time-Based Investigation

**Commits in time range**:
```ini
range = log --since --until --oneline
```

Usage: `git range --since="2025-12-19 00:00" --until="2025-12-19 23:59"`

**Commits before incident**:
```ini
before = log --until
```

Usage: `git before --until="2025-12-19 14:30"`

**Commits during incident window**:
```ini
during = log --since --until --pretty=format:'%h %ad | %s (%an)' --date=iso
```

Usage: `git during --since="2025-12-19 14:00" --until="2025-12-19 15:00"`

### Author Investigation

**Commits by author in timeframe**:
```ini
author-recent = log --author --since="1 week ago" --oneline
```

Usage: `git author-recent "Developer Name"`

**Author stats**:
```ini
author-stats = shortlog -sn --since="1 week ago"
```

Usage: `git author-stats`

### File-Specific

**All commits touching file**:
```ini
file-commits = log --follow --oneline --
```

Usage: `git file-commits path/to/file.js`

**File changes with diffs**:
```ini
file-changes = log -p --follow --
```

Usage: `git file-changes path/to/file.js`

**File history (condensed)**:
```ini
file-history = log --pretty=format:'%C(yellow)%h%Creset %C(cyan)%ad%Creset | %s %C(green)(%an)%Creset' --date=short --follow --
```

Usage: `git file-history path/to/file.js`

### Comparison Aliases

**Compare branches**:
```ini
compare = diff --stat
```

Usage: `git compare main develop`

**Changes not yet merged**:
```ini
not-merged = log --oneline --no-merges origin/main..HEAD
```

Usage: `git not-merged`

**Deployment diff**:
```ini
deployment-diff = diff --stat
```

Usage: `git deployment-diff deployed_commit HEAD`

## Complete Investigation Aliases

### RCA Workflow

**Full investigation log**:
```ini
rca = log --all --graph --decorate --pretty=format:'%C(yellow)%h%C(reset) %C(cyan)%ad%C(reset) %C(green)%an%C(reset)%n  %s%n  %C(red)%d%C(reset)%n' --date=iso
```

Usage: `git rca --since="2025-12-19"`

**Incident timeline**:
```ini
incident = log --all --pretty=format:'%C(red)%h%C(reset) | %C(cyan)%ad%C(reset) | %C(green)%an%C(reset) | %s' --date=iso-strict
```

Usage: `git incident --since="2025-12-19 14:00" --until="2025-12-19 15:00"`

**Configuration changes**:
```ini
config-changes = log --oneline -- "*.config.js" "*.json" "*.yaml" "*.yml" ".env*"
```

Usage: `git config-changes --since="1 week ago"`

### Quick Checks

**Latest commit**:
```ini
latest = log -1 HEAD --stat
```

Usage: `git latest`

**Who changed this line**:
```ini
who-line = blame -L
```

Usage: `git who-line 45,45 file.js`

**What changed here**:
```ini
what-changed = log -p -S
```

Usage: `git what-changed "problematic code"`

## Customization

### Create Custom RCA Aliases

Add project-specific aliases:

**For microservices**:
```ini
service-changes = log --oneline -- services/
api-changes = log --oneline -- src/api/
db-changes = log --oneline -- migrations/ src/database/
```

**For specific incident types**:
```ini
db-incidents = log --grep="database" --grep="connection" --grep="query" --all-match
perf-incidents = log --grep="performance" --grep="slow" --grep="timeout" --all-match
```

### Chain Aliases

Combine aliases with git commands:

```bash
# Recent changes to config files
git timeline --since="1 week ago" -- config/

# Author's recent work on API
git author-recent "Developer Name" -- src/api/

# Incident window for specific service
git incident --since="2025-12-19 14:00" --until="2025-12-19 15:00" -- services/api/
```

## Complete .gitconfig Example

```ini
[alias]
  # Logs
  today = log --since='1 day ago' --oneline --decorate
  week = log --since='1 week ago' --oneline --decorate
  lg = log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
  timeline = log --pretty=format:'%C(yellow)%h%Creset %C(cyan)%ad%Creset | %s %C(green)(%an)%Creset' --date=short

  # Search
  search = log --all --grep
  find-code = log -S

  # Blame
  bl = blame -w -C -C -C
  blr = blame -L

  # Show
  ss = show --stat
  files = show --name-only
  last = diff HEAD~1 HEAD

  # RCA specific
  rca = log --all --graph --decorate --pretty=format:'%C(yellow)%h%C(reset) %C(cyan)%ad%C(reset) %C(green)%an%C(reset)%n  %s%n' --date=iso
  incident = log --all --pretty=format:'%C(red)%h%C(reset) | %C(cyan)%ad%C(reset) | %C(green)%an%C(reset) | %s' --date=iso-strict
  recent = log --since='1 day ago' --all --stat --oneline

  # File tracking
  file-commits = log --follow --oneline --
  file-changes = log -p --follow --

  # Comparisons
  compare = diff --stat
  wdiff = diff --word-diff
```

## Usage Tips

1. **Start broad**: `git recent` to see all recent activity
2. **Narrow down**: `git timeline --since="incident-time" -- affected/path/`
3. **Find specifics**: `git bl file.js` to identify line authors
4. **Investigate**: `git show commit_sha` for full details

Save time by using aliases instead of typing full git commands repeatedly during investigations.
