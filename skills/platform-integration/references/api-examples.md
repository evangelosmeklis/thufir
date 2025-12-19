# GitHub and GitLab API Examples for RCA

Complete API call examples for common root cause analysis scenarios.

## GitHub API Examples

### Authentication

All GitHub API calls require authentication:

```bash
curl -H "Authorization: Bearer ghp_your_token_here" \
     https://api.github.com/user
```

**Headers for all requests**:
```
Authorization: Bearer ghp_your_token_here
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
```

### Fetching Issue Details

**Get single issue**:
```bash
curl -H "Authorization: Bearer ghp_token" \
     https://api.github.com/repos/owner/repo/issues/456
```

**Response structure**:
```json
{
  "number": 456,
  "title": "Production: Users unable to login",
  "body": "Users are getting 500 errors when trying to log in.\n\nError: ConnectionPoolExhausted\nTime: 2025-12-19 14:32 UTC\n\nAffected: ~15,000 users",
  "labels": [
    {"name": "production"},
    {"name": "incident"},
    {"name": "p0"}
  ],
  "state": "open",
  "created_at": "2025-12-19T14:35:00Z",
  "updated_at": "2025-12-19T14:50:00Z",
  "assignees": [
    {"login": "oncall-engineer"}
  ]
}
```

**Extract RCA info from response**:
- Error: Look for error strings in `body`
- Time: Parse timestamps from `body` or `created_at`
- Impact: Look for "users affected" in `body`
- Labels: Check for "production", "incident" in `labels`

### Listing Issues with Filters

**Get open production issues**:
```bash
curl -H "Authorization: Bearer ghp_token" \
     "https://api.github.com/repos/owner/repo/issues?labels=production,incident&state=open"
```

**Get issues created in last 24 hours**:
```bash
curl -H "Authorization: Bearer ghp_token" \
     "https://api.github.com/repos/owner/repo/issues?since=2025-12-19T00:00:00Z"
```

**Parameters**:
- `labels`: Comma-separated list (AND logic)
- `state`: `open`, `closed`, or `all`
- `since`: ISO 8601 timestamp
- `sort`: `created`, `updated`, `comments`
- `direction`: `asc` or `desc`

### Fetching Commits

**List recent commits**:
```bash
curl -H "Authorization: Bearer ghp_token" \
     "https://api.github.com/repos/owner/repo/commits?since=2025-12-19T00:00:00Z"
```

**Response structure**:
```json
{
  "commits": [
    {
      "sha": "abc123def456",
      "commit": {
        "message": "Refactor database configuration",
        "author": {
          "name": "Developer Name",
          "email": "dev@example.com",
          "date": "2025-12-19T10:15:00Z"
        }
      },
      "files": [
        {
          "filename": "src/config/database.js",
          "status": "modified",
          "additions": 1,
          "deletions": 1,
          "changes": 2,
          "patch": "@@ -45,7 +45,7 @@\n- max: 100,\n+ max: 10,"
        }
      ]
    }
  ]
}
```

**Get commits for specific file**:
```bash
curl -H "Authorization: Bearer ghp_token" \
     "https://api.github.com/repos/owner/repo/commits?path=src/config/database.js&since=2025-12-19T00:00:00Z"
```

**Parameters**:
- `since`: ISO 8601 timestamp
- `until`: ISO 8601 timestamp
- `path`: Filter to specific file/directory
- `author`: Filter by commit author

### Getting File Blame

**Get blame for file**:
```bash
curl -H "Authorization: Bearer ghp_token" \
     "https://api.github.com/repos/owner/repo/blame/main/src/config/database.js"
```

**Response structure**:
```json
{
  "ranges": [
    {
      "age": 5,
      "start_line": 45,
      "end_line": 45,
      "commit": {
        "sha": "abc123def456",
        "author": {
          "name": "Developer Name",
          "email": "dev@example.com",
          "date": "2025-12-19T10:15:00Z"
        },
        "message": "Refactor database configuration"
      }
    }
  ]
}
```

**Use for RCA**:
- Find `start_line` matching stack trace line number
- Extract `commit.sha` for that line
- Get full commit details with sha

### Searching Code

**Search for error string**:
```bash
curl -H "Authorization: Bearer ghp_token" \
     "https://api.github.com/search/code?q=ConnectionPoolExhausted+repo:owner/repo"
```

**Response structure**:
```json
{
  "total_count": 3,
  "items": [
    {
      "name": "database.js",
      "path": "src/config/database.js",
      "html_url": "https://github.com/owner/repo/blob/main/src/config/database.js",
      "repository": {
        "full_name": "owner/repo"
      }
    }
  ]
}
```

**Advanced search queries**:
- `ConnectionPoolExhausted repo:owner/repo` - Search in specific repo
- `ConnectionPoolExhausted language:javascript` - Filter by language
- `ConnectionPoolExhausted path:src/config` - Search in specific path
- `"Could not acquire connection" repo:owner/repo` - Exact phrase

### Getting Pull Request Details

**Get PR details**:
```bash
curl -H "Authorization: Bearer ghp_token" \
     https://api.github.com/repos/owner/repo/pulls/123
```

**Response includes**:
- `title`, `body`: Description
- `merged_at`: When merged
- `merge_commit_sha`: Resulting commit
- `head.ref`: Source branch
- `base.ref`: Target branch
- `user`: PR author

**List PRs merged in timeframe**:
```bash
curl -H "Authorization: Bearer ghp_token" \
     "https://api.github.com/repos/owner/repo/pulls?state=closed&sort=updated&direction=desc"
```

Filter by `merged_at` in response to find PRs merged around incident time.

## GitLab API Examples

### Authentication

All GitLab API calls require authentication:

```bash
curl -H "PRIVATE-TOKEN: glpat_your_token_here" \
     https://gitlab.com/api/v4/user
```

**Alternative authorization header**:
```
Authorization: Bearer glpat_your_token_here
```

### Project ID

GitLab uses project ID instead of owner/repo:

**Get project ID from path**:
```bash
curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/group%2Fproject"
```

Use URL-encoded path: `group/project` → `group%2Fproject`

Response includes `id` field.

### Fetching Issue Details

**Get single issue**:
```bash
curl -H "PRIVATE-TOKEN: glpat_token" \
     https://gitlab.com/api/v4/projects/12345/issues/456
```

**Response structure**:
```json
{
  "iid": 456,
  "title": "Production: Users unable to login",
  "description": "Users are getting 500 errors...",
  "labels": ["production", "incident", "p0"],
  "state": "opened",
  "created_at": "2025-12-19T14:35:00.000Z",
  "updated_at": "2025-12-19T14:50:00.000Z",
  "assignees": [
    {"username": "oncall-engineer"}
  ]
}
```

**Note**: GitLab uses `iid` (internal ID) for issues, not `number`.

### Listing Issues with Filters

**Get open production issues**:
```bash
curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/12345/issues?labels=production,incident&state=opened"
```

**Parameters**:
- `labels`: Comma-separated list
- `state`: `opened`, `closed`, or `all`
- `created_after`: ISO 8601 timestamp
- `updated_after`: ISO 8601 timestamp
- `sort`: `created_at`, `updated_at`
- `order_by`: `asc` or `desc`

### Fetching Commits

**List recent commits**:
```bash
curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/12345/repository/commits?since=2025-12-19T00:00:00Z"
```

**Response structure**:
```json
[
  {
    "id": "abc123def456",
    "short_id": "abc123d",
    "title": "Refactor database configuration",
    "message": "Refactor database configuration\n\nAlign pool size with staging",
    "author_name": "Developer Name",
    "author_email": "dev@example.com",
    "authored_date": "2025-12-19T10:15:00.000Z",
    "committer_name": "Developer Name",
    "committer_email": "dev@example.com",
    "committed_date": "2025-12-19T10:15:00.000Z"
  }
]
```

**Get commits for specific file**:
```bash
curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/12345/repository/commits?path=src/config/database.js&since=2025-12-19T00:00:00Z"
```

**Parameters**:
- `since`: ISO 8601 timestamp
- `until`: ISO 8601 timestamp
- `path`: Filter to specific file
- `ref_name`: Branch name (default: default branch)

### Getting File Blame

**Get blame for file**:
```bash
curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/12345/repository/files/src%2Fconfig%2Fdatabase.js/blame?ref=main"
```

**Note**: Path must be URL-encoded: `src/config/database.js` → `src%2Fconfig%2Fdatabase.js`

**Response structure**:
```json
[
  {
    "commit": {
      "id": "abc123def456",
      "author_name": "Developer Name",
      "author_email": "dev@example.com",
      "authored_date": "2025-12-19T10:15:00.000Z",
      "message": "Refactor database configuration"
    },
    "lines": [
      "  max: 10,  // Changed from 100"
    ]
  }
]
```

### Searching Code

**Search in project**:
```bash
curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/12345/search?scope=blobs&search=ConnectionPoolExhausted"
```

**Response structure**:
```json
[
  {
    "basename": "database.js",
    "data": "...ConnectionPoolExhausted...",
    "path": "src/config/database.js",
    "filename": "src/config/database.js",
    "id": null,
    "ref": "main",
    "startline": 45,
    "project_id": 12345
  }
]
```

**Scopes**:
- `blobs`: Search file contents
- `commits`: Search commit messages
- `issues`: Search issues
- `merge_requests`: Search MRs

### Getting Merge Request Details

**Get MR details**:
```bash
curl -H "PRIVATE-TOKEN: glpat_token" \
     https://gitlab.com/api/v4/projects/12345/merge_requests/123
```

**Response includes**:
- `title`, `description`: Description
- `merged_at`: When merged
- `merge_commit_sha`: Resulting commit
- `source_branch`: Source branch
- `target_branch`: Target branch
- `author`: MR author

**List MRs merged in timeframe**:
```bash
curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/12345/merge_requests?state=merged&order_by=updated_at&sort=desc"
```

## Complete RCA Workflow Examples

### Scenario 1: GitHub Issue Reports Error

**Step 1: Fetch issue**:
```bash
issue_number=456
curl -H "Authorization: Bearer ghp_token" \
     "https://api.github.com/repos/owner/repo/issues/${issue_number}" \
     | jq '{title, body, created_at, labels: [.labels[].name]}'
```

**Step 2: Extract error from body**:
```bash
# Parse body to find error
error="ConnectionPoolExhausted"
```

**Step 3: Search code for error**:
```bash
curl -H "Authorization: Bearer ghp_token" \
     "https://api.github.com/search/code?q=${error}+repo:owner/repo" \
     | jq '.items[] | {path, name}'
```

**Step 4: Get blame for file**:
```bash
file_path="src/config/database.js"
curl -H "Authorization: Bearer ghp_token" \
     "https://api.github.com/repos/owner/repo/blame/main/${file_path}" \
     | jq '.ranges[] | select(.start_line == 45) | .commit | {sha, author, date, message}'
```

**Step 5: Get commit details**:
```bash
commit_sha="abc123def456"
curl -H "Authorization: Bearer ghp_token" \
     "https://api.github.com/repos/owner/repo/commits/${commit_sha}" \
     | jq '{sha, message, author: .commit.author, files: [.files[] | {filename, patch}]}'
```

### Scenario 2: GitLab Issue Analysis

**Step 1: Get project ID**:
```bash
project_path="group%2Fproject"
project_id=$(curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/${project_path}" \
     | jq -r '.id')
```

**Step 2: Fetch issue**:
```bash
issue_iid=456
curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/${project_id}/issues/${issue_iid}" \
     | jq '{title, description, created_at, labels}'
```

**Step 3: Search for error**:
```bash
error="ConnectionPoolExhausted"
curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/${project_id}/search?scope=blobs&search=${error}" \
     | jq '.[] | {path, startline, data}'
```

**Step 4: Get file blame**:
```bash
file_path="src%2Fconfig%2Fdatabase.js"
curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/${project_id}/repository/files/${file_path}/blame?ref=main" \
     | jq '.[] | {commit: .commit | {id, author_name, authored_date, message}, lines}'
```

**Step 5: List recent commits to file**:
```bash
curl -H "PRIVATE-TOKEN: glpat_token" \
     "https://gitlab.com/api/v4/projects/${project_id}/repository/commits?path=src/config/database.js&since=2025-12-19T00:00:00Z" \
     | jq '.[] | {id, title, author_name, authored_date}'
```

## Error Handling

### Rate Limiting

**GitHub**: 5,000 requests/hour for authenticated users
- Check headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

**GitLab**: 10 requests/second per IP
- Response: `429 Too Many Requests`

### Common Errors

**404 Not Found**:
- Repository/project doesn't exist
- Issue/commit not found
- Insufficient permissions

**401 Unauthorized**:
- Invalid token
- Token expired
- Token lacks required scopes

**403 Forbidden**:
- Rate limit exceeded
- Access denied to private repo

## Tips for Efficient API Usage

1. **Use filtering parameters** to reduce response size
2. **Cache responses** when appropriate (commits, blame)
3. **Batch requests** when possible
4. **Check rate limits** before making many requests
5. **Use webhooks** for real-time incident detection (advanced)
6. **Parse JSON with jq** for easier data extraction

## Integration with Thufir MCP

Instead of making raw API calls, use Thufir's MCP tools:

```
# Instead of curl commands, use MCP:
Use tool: github_get_issue
Parameters: {issue_number: 456}

Use tool: github_search_code
Parameters: {query: "ConnectionPoolExhausted"}

Use tool: github_get_blame
Parameters: {path: "src/config/database.js"}
```

MCP handles authentication, parsing, and error handling automatically.

---

These examples provide copy-paste templates for common RCA API interactions. Adapt repo names, project IDs, and tokens for your environment.
