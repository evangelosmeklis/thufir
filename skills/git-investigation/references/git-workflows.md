# Complete Git Investigation Workflows for RCA

Step-by-step workflows for common root cause analysis scenarios using git.

## Workflow 1: Stack Trace Leads to Specific File and Line

**Scenario**: Error stack trace points to `src/api/auth.js:127`

### Steps

**1. Blame the specific line**:
```bash
git blame -L 127,127 src/api/auth.js
```

Output:
```
abc123de (Developer X 2025-12-19 10:15:00 +0000 127)   if (!user) throw new AuthError();
```

**2. Extract commit SHA** (`abc123de`) and view full commit:
```bash
git show abc123de
```

**3. Analyze commit**:
- When was it made? Does it correlate with incident time?
- What other changes were in this commit?
- Was this a bug fix or new feature?
- Does commit message explain the change?

**4. Check if line existed before this commit**:
```bash
git show abc123de~1:src/api/auth.js | grep -n "AuthError"
```

**5. If issue might be from earlier change, check full file history**:
```bash
git log -p --follow -- src/api/auth.js | less
# Search for line 127 changes over time
```

### Expected Outcome

Identify exact commit that introduced or modified the problematic line, along with context of why the change was made.

---

## Workflow 2: Recent Deployment Broke Something

**Scenario**: Code worked before deployment at 14:30, broke after. Need to find what changed.

### Steps

**1. Find deployment commit SHA** (from CI/CD logs, git tags, or deployment records):
```bash
# If using tags
git tag --sort=-creatordate | head -5

# If you know approximate time
git log --since="2025-12-19 14:00" --until="2025-12-19 14:35" --oneline
```

Let's say deployed commit is `def456`.

**2. Find previous deployment commit**:
```bash
# Previous tag
git describe --tags def456~1

# Or previous commit to main
git log --oneline -1 def456~1
```

Let's say previous deployment was `abc123`.

**3. Compare the two deployments**:
```bash
git diff abc123 def456 --stat
```

Review files changed between deployments.

**4. Focus on suspicious files** (configuration, database, API endpoints):
```bash
git diff abc123 def456 -- src/config/ src/api/ src/database/
```

**5. Review each changed file in detail**:
```bash
git diff abc123 def456 -- src/config/database.js
```

**6. List all commits between deployments**:
```bash
git log --oneline abc123..def456
```

**7. Review each commit individually**:
```bash
git show <commit_sha>
```

### Expected Outcome

Identify specific commit(s) and file change(s) that introduced the bug between deployments.

---

## Workflow 3: Configuration Change Suspected

**Scenario**: Suspect recent configuration file change caused issue.

### Steps

**1. List configuration files** in repository:
```bash
find . -name "*.config.js" -o -name "*.json" -o -name "*.yaml" -o -name ".env*"
```

**2. Check recent commits to config files**:
```bash
git log --since="1 week ago" --oneline -- "*.config.js" "*.json" "config/"
```

**3. Review each config commit**:
```bash
git show <commit_sha>
```

Look for:
- Value changes (numbers, strings, booleans)
- Added or removed configuration keys
- Environment-specific settings

**4. For suspicious commit, check diff in detail**:
```bash
git diff <commit_sha>~1 <commit_sha> -- config/database.js
```

**5. Check when config was last known to work**:
```bash
# If you know working commit
git show <working_commit>:config/database.js

# Compare with current
git diff <working_commit> HEAD -- config/database.js
```

**6. Identify specific value change**:
```bash
# Find when specific value changed
git log -S "max: 100" -- config/database.js
```

### Expected Outcome

Pinpoint exact configuration value that changed and when, correlating with incident timeline.

---

## Workflow 4: Code Worked Last Week, Broken Now (Git Bisect)

**Scenario**: Feature worked in last week's release, broken in current version. Many commits in between.

### Steps

**1. Identify known-good commit**:
```bash
# Last week's release tag
good_commit=$(git rev-parse v1.2.0)

# Or commit from 1 week ago
git log --since="1 week ago" --until="1 week ago" --oneline | head -1
```

**2. Start bisect**:
```bash
git bisect start
git bisect bad HEAD  # Current version is broken
git bisect good $good_commit  # Last week's version worked
```

Git will checkout a commit halfway between good and bad.

**3. Test the code**:
```bash
# Option A: Manual test
npm install
npm test
# Or manually reproduce the bug

# Option B: Automated test script
./test-for-regression.sh
```

**4. Mark result**:
```bash
# If broken
git bisect bad

# If working
git bisect good
```

**5. Repeat** until git identifies first bad commit:
```
abc123de is the first bad commit
```

**6. Review the bad commit**:
```bash
git show abc123de
```

**7. End bisect**:
```bash
git bisect reset
```

### Automated Bisect

If you have a test that can detect the regression:

```bash
git bisect start HEAD v1.2.0
git bisect run ./test-regression.sh
```

Test script should exit 0 for good, non-zero for bad.

### Expected Outcome

Identify exact commit that introduced the regression.

---

## Workflow 5: Find Who Changed Specific Code Pattern

**Scenario**: Need to find when/who changed code matching a specific pattern (e.g., database connection logic).

### Steps

**1. Search for code pattern in current version**:
```bash
git grep "createConnectionPool"
```

**2. Find when this code was added**:
```bash
git log -S "createConnectionPool" --all
```

**3. Review each commit that mentions this pattern**:
```bash
git log -p -S "createConnectionPool"
```

**4. For more specific pattern matching (regex)**:
```bash
git log -G "pool.*max.*[0-9]+" --all
```

**5. Find recent changes to files containing pattern**:
```bash
# First find files
files=$(git grep -l "createConnectionPool")

# Then check their history
for file in $files; do
  echo "=== $file ==="
  git log --since="1 month ago" --oneline -- "$file"
done
```

**6. Blame lines matching pattern**:
```bash
# Find line number
git grep -n "createConnectionPool" src/config/database.js

# Blame that line
git blame -L <line_number>,<line_number> src/config/database.js
```

### Expected Outcome

Identify all commits that modified specific code pattern, with authors and timestamps.

---

## Workflow 6: Correlate Git History with Incident Timeline

**Scenario**: Incident occurred at specific time. Find what code changes happened around that time.

### Steps

**1. Define time window** (e.g., 2 hours before incident to incident start):
```bash
incident_time="2025-12-19 14:32:00"
window_start="2025-12-19 12:30:00"
window_end="2025-12-19 14:32:00"
```

**2. List all commits in window**:
```bash
git log --since="$window_start" --until="$window_end" --pretty=format:'%h %ai | %s (%an)' --all
```

**3. Focus on deployments (merges to main)**:
```bash
git log --since="$window_start" --until="$window_end" --first-parent main --oneline
```

**4. Check for configuration changes in window**:
```bash
git log --since="$window_start" --until="$window_end" --oneline -- config/ "*.config.js"
```

**5. Review each commit in detail**:
```bash
for commit in $(git log --since="$window_start" --until="$window_end" --format='%h'); do
  echo "=== Commit $commit ==="
  git show --stat $commit
  echo ""
done
```

**6. Create timeline visualization**:
```bash
git log --since="$window_start" --until="$window_end" --all --graph --pretty=format:'%C(yellow)%h%Creset %C(cyan)%ai%Creset | %s %C(green)(%an)%Creset'
```

**7. Check what was deployed at incident time**:
```bash
git log -1 --until="$incident_time" main --oneline
```

### Expected Outcome

Clear timeline of code changes with timestamps, allowing correlation with incident occurrence.

---

## Workflow 7: Multiple Files Changed, Find Common Commit

**Scenario**: Several files seem involved in the issue. Find if they were changed together.

### Steps

**1. List files involved**:
```bash
files=(
  "src/api/auth.js"
  "src/database/users.js"
  "src/config/database.js"
)
```

**2. Find commits touching any of these files**:
```bash
git log --oneline -- "${files[@]}"
```

**3. Find commits touching ALL files (intersection)**:
```bash
# Manual check: for each commit, check if it touched all files
for commit in $(git log --oneline -- "${files[@]}" | cut -d' ' -f1); do
  changed_files=$(git show --name-only --format='' $commit)
  all_present=true
  for file in "${files[@]}"; do
    if ! echo "$changed_files" | grep -q "$file"; then
      all_present=false
      break
    fi
  done
  if $all_present; then
    echo "Commit $commit changed all files:"
    git show --stat $commit
  fi
done
```

**4. Or check commits in time range affecting multiple areas**:
```bash
git log --since="1 week ago" --stat | grep -B 5 -A 10 "src/api/auth.js\|src/database/users.js"
```

**5. Review commits that changed multiple related files**:
```bash
git log --since="1 week ago" --stat -- src/api/ src/database/ src/config/
```

### Expected Outcome

Identify commits that modified multiple related files, potentially introducing cross-component bugs.

---

## Workflow 8: Find When Code Was Deleted

**Scenario**: Missing code that used to exist. Find when it was removed.

### Steps

**1. Search for deleted code pattern**:
```bash
git log -S "deleted code pattern" --all
```

**2. Review commits that changed this code**:
```bash
git log -p -S "deleted code pattern"
```

Look for commits where the code appears in `-` lines (deletions).

**3. If you know the file**:
```bash
git log -p -- path/to/file.js | grep -B 5 -A 5 "deleted code"
```

**4. Find last commit containing the code**:
```bash
git log -S "deleted code pattern" --all --format='%h' | head -1
```

**5. Find commit that deleted it** (next commit after last containing it):
```bash
last_with_code=$(git log -S "deleted code pattern" --all --format='%h' | head -1)
git log --oneline $last_with_code~1..HEAD -- path/to/file.js
```

**6. Review deletion commit**:
```bash
git show <commit_that_deleted_it>
```

### Expected Outcome

Identify when and why code was removed, with full commit context.

---

## Workflow 9: Find Changes by Specific Developer

**Scenario**: Suspect recent changes by specific developer might be related to issue.

### Steps

**1. List developer's recent commits**:
```bash
git log --author="Developer Name" --since="1 week ago" --oneline
```

**2. Review with diffs**:
```bash
git log --author="Developer Name" --since="1 week ago" -p
```

**3. Focus on specific area**:
```bash
git log --author="Developer Name" --since="1 week ago" --oneline -- src/api/
```

**4. Check developer's commits in incident window**:
```bash
git log --author="Developer Name" --since="2025-12-19 12:00" --until="2025-12-19 15:00" --pretty=format:'%h %ai | %s'
```

**5. Review each commit's full details**:
```bash
for commit in $(git log --author="Developer Name" --since="1 week ago" --format='%h'); do
  git show --stat $commit
done
```

### Expected Outcome

Comprehensive list of developer's recent changes for review.

---

## Workflow 10: Compare Production vs Staging Code

**Scenario**: Issue appears in production but not staging. Find code differences.

### Steps

**1. Identify production and staging branches/commits**:
```bash
prod_commit=$(git rev-parse origin/production)
staging_commit=$(git rev-parse origin/staging)
```

**2. Compare overall differences**:
```bash
git diff $staging_commit $prod_commit --stat
```

**3. Review differences in detail**:
```bash
git diff $staging_commit $prod_commit
```

**4. Focus on specific suspicious areas**:
```bash
git diff $staging_commit $prod_commit -- src/config/ src/api/
```

**5. List commits in production not in staging**:
```bash
git log --oneline $staging_commit..$prod_commit
```

**6. Or commits in staging not in production**:
```bash
git log --oneline $prod_commit..$staging_commit
```

**7. Check for configuration differences**:
```bash
git diff $staging_commit $prod_commit -- "*.config.js" ".env*" "config/"
```

### Expected Outcome

Identify code differences between environments that might explain behavior discrepancy.

---

## Quick Reference

| Workflow | Command Pattern |
|----------|----------------|
| Blame line | `git blame -L <line>,<line> <file>` |
| Recent commits | `git log --since="1 day ago" --oneline` |
| Config changes | `git log --oneline -- config/ "*.config.*"` |
| Find code | `git log -S "pattern"` |
| Bisect regression | `git bisect start HEAD <good_commit>` |
| Timeline | `git log --since="time" --until="time" --pretty=format:'%h %ai | %s'` |
| Author's work | `git log --author="name" --since="1 week ago"` |
| Compare commits | `git diff commit1 commit2` |
| Deleted code | `git log -S "deleted pattern" --all` |
| Multiple files | `git log --oneline -- file1 file2 file3` |

---

Use these workflows as templates. Adapt time ranges, file paths, and search patterns to your specific investigation needs.
