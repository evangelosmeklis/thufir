# Contributing to Thufir

Thank you for your interest in contributing to Thufir! This document provides guidelines for contributing to the project.

## 🎯 Ways to Contribute

### 1. Report Bugs
- Use GitHub Issues to report bugs
- Include reproduction steps
- Provide error messages and logs
- Mention your environment (OS, Claude Code version)

### 2. Suggest Features
- Open a GitHub Issue with the "enhancement" label
- Describe the use case
- Explain how it would help incident investigation
- Consider if it fits Thufir's RCA focus

### 3. Improve Documentation
- Fix typos and clarify instructions
- Add examples and use cases
- Improve setup guides
- Expand troubleshooting sections

### 4. Add Skills/Commands
- Contribute new investigation skills
- Add commands for other incident sources
- Expand reference materials
- Add real-world RCA patterns

### 5. Enhance MCP Integrations
- Improve existing MCP servers
- Add new integrations (AWS, K8s, etc.)
- Optimize API calls
- Add error handling

## 🚀 Getting Started

### Setup Development Environment

1. **Fork and clone the repository**:
```bash
git clone https://github.com/YOUR-USERNAME/thufir.git
cd thufir
```

2. **Install dependencies**:
```bash
# For Prometheus MCP
cd mcp-servers/prometheus
pip install -r requirements.txt

# For GitLab MCP
cd ../gitlab
pip install -r requirements.txt

# For GitHub MCP (official server)
npm install -g @modelcontextprotocol/server-github
```

3. **Configure test environment**:
```bash
cp .claude/thufir.local.md.example .claude/thufir.local.md
# Edit with your test credentials
```

4. **Test the plugin**:
```bash
cc --plugin-dir .
```

## 📝 Contribution Guidelines

### Code Style

**Skills:**
- Use imperative/infinitive form (not second person)
- Third-person descriptions with specific trigger phrases
- Keep SKILL.md lean (1,500-2,000 words)
- Move detailed content to references/
- Include working examples in examples/

**Commands:**
- Write instructions FOR Claude (not to user)
- Use clear YAML frontmatter
- Specify minimal necessary allowed-tools
- Provide usage examples

**Agents:**
- Include concrete `<example>` blocks in description
- Write comprehensive system prompts
- Specify appropriate model and tools
- Document triggering conditions

### File Organization

```
thufir/
├── .claude-plugin/       # Plugin manifest
├── skills/              # Knowledge skills
│   └── skill-name/
│       ├── SKILL.md
│       ├── references/
│       └── examples/
├── commands/            # User commands
├── agents/             # Autonomous agents
├── mcp-servers/        # MCP integrations
└── .claude/            # Configuration
```

### Naming Conventions

- **Files**: kebab-case (e.g., `analyze-prometheus.md`)
- **Directories**: kebab-case (e.g., `root-cause-analysis`)
- **Variables**: Follow language conventions
- **Commits**: Imperative mood (e.g., "Add feature" not "Added feature")

### Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md following Keep a Changelog format
- Add inline comments for complex logic
- Include usage examples

## 🧪 Testing

### Manual Testing

1. **Test skills load correctly**:
```bash
# Ask question matching skill trigger
"How do I perform root cause analysis?"
```

2. **Test commands execute**:
```bash
/rca:investigate
```

3. **Test agent triggers**:
```bash
# Mention production issue
"We have high error rates in production"
```

4. **Test MCP servers**:
```bash
# Verify servers show up
/mcp
```

### Validation

Run validation before submitting:
```bash
# Check JSON syntax
jq empty .claude-plugin/plugin.json
jq empty .mcp.json

# Check for common issues
grep -r "password\|secret" . --exclude-dir=.git
```

## 📋 Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

- Follow code style guidelines
- Add tests if applicable
- Update documentation
- Keep commits atomic and focused

### 3. Commit Messages

Use conventional commits format:

```
type(scope): Short description

Longer description if needed

- Bullet points for details
- Reference issues: Fixes #123
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Examples**:
```
feat(skills): Add Kubernetes diagnostics skill
fix(prometheus): Handle timeout errors gracefully
docs(readme): Improve installation instructions
```

### 4. Update CHANGELOG

Add entry under `[Unreleased]`:

```markdown
### Added
- New feature description

### Changed
- Changed behavior description

### Fixed
- Bug fix description
```

### 5. Submit Pull Request

- Push your branch to GitHub
- Open a PR against `main` branch
- Fill out the PR template
- Link related issues
- Request review

### 6. Code Review

- Address reviewer feedback
- Update PR with changes
- Keep discussion focused and professional
- Resolve conversations when addressed

### 7. Merge

- PRs require approval from maintainer
- Ensure CI passes (when available)
- Squash commits if needed
- Maintainer will merge when ready

## 🎨 Contribution Ideas

### High Priority
- [ ] Additional MCP servers (AWS CloudWatch, Datadog, etc.)
- [ ] Slack/PagerDuty integration for notifications
- [ ] Kubernetes diagnostics skill
- [ ] Automated timeline visualization
- [ ] Historical RCA database

### Medium Priority
- [ ] More PromQL query patterns
- [ ] Additional investigation workflows
- [ ] Performance optimization for large repos
- [ ] Multi-language support for code search
- [ ] Custom report templates

### Documentation
- [ ] Video tutorials
- [ ] More real-world examples
- [ ] Troubleshooting cookbook
- [ ] Integration guides for specific tools
- [ ] Best practices guide

## 🐛 Bug Reports

### Good Bug Report Includes:

1. **Summary**: Clear, concise description
2. **Steps to Reproduce**: Exact steps to trigger bug
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**:
   - OS and version
   - Claude Code version
   - Plugin version
   - Relevant configuration
6. **Logs**: Error messages and stack traces
7. **Screenshots**: If UI-related

### Template:

```markdown
**Summary**
Brief description of the bug

**Steps to Reproduce**
1. Step one
2. Step two
3. Step three

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: macOS 14.0
- Claude Code: v1.0.0
- Thufir: v1.0.0

**Logs**
```
Error messages here
```

**Additional Context**
Any other relevant information
```

## 💬 Questions?

- Open a GitHub Discussion
- Check existing issues and docs first
- Be specific and provide context
- Share relevant code/config snippets

## 📜 Code of Conduct

- Be respectful and professional
- Welcome newcomers
- Focus on constructive feedback
- Assume good intentions
- Report unacceptable behavior

## 🙏 Recognition

Contributors will be:
- Listed in README acknowledgments
- Credited in CHANGELOG
- Mentioned in release notes

Thank you for contributing to Thufir! Your help makes incident investigation better for everyone. 🚀
