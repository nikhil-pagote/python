# Claude Code — Slash Command Cheatsheet

> A reference for the `/` commands available inside the Claude Code CLI.
> Type `/` at the prompt to see the live list in your version, since available
> commands depend on your Claude Code release, plugins, and configured skills.

**How slash commands work**
- Type `/` followed by the command name at the Claude Code prompt.
- Some commands open an interactive dialog (e.g. `/model`, `/config`).
- Some take arguments (e.g. `/loop 5m /review`).
- Commands fall into two groups: **built-in commands** (part of the CLI) and
  **skills** (modular capabilities, also invoked with `/`).

---

## 1. Getting Help & Info

| Command | Description |
|---|---|
| `/help` | Show help and the list of available commands. |
| `/release-notes` | View the release notes / changelog for your installed version. |
| `/bug` | Report a bug or issue with Claude Code to Anthropic. |
| `/doctor` | Run diagnostics to check your Claude Code installation health. |
| `/status` | Show current session status (model, account, working directory, etc.). |
| `/cost` | Show token usage and estimated cost for the current session. |
| `/usage` | View your plan's usage limits and current consumption. |

---

## 2. Session & Conversation Control

| Command | Description |
|---|---|
| `/clear` | Clear the conversation history and start fresh (frees up context). |
| `/compact` | Summarize and compress the conversation to reclaim context space while keeping key info. |
| `/resume` | Resume a previous conversation/session. |
| `/export` | Export the current conversation (e.g. to a file) for sharing or records. |
| `/btw <text>` | Add a side note / "by the way" context to the conversation without derailing the main task. |

---

## 3. Model & Account

| Command | Description |
|---|---|
| `/model` | Choose which Claude model to use for the session (e.g. Opus, Sonnet, Haiku). |
| `/fast` | Toggle Fast mode (faster Opus output). Available on Opus 4.6 / 4.7. |
| `/login` | Log in to your Anthropic / Claude account. |
| `/logout` | Log out of the current account. |
| `/privacy-settings` | View and adjust data / privacy preferences. |
| `/upgrade` | Upgrade your plan or the Claude Code CLI. |

---

## 4. Configuration & Customization

| Command | Description |
|---|---|
| `/config` | Open the settings dialog (theme, model, editor behavior, etc.). |
| `/update-config` | Configure the harness via `settings.json` — permissions, env vars, hooks, and automated behaviors ("whenever X, do Y"). |
| `/permissions` | View and manage tool/command permissions (what Claude can run without asking). |
| `/fewer-permission-prompts` | Scan transcripts and auto-build an allowlist of safe commands to reduce permission prompts. |
| `/hooks` | Configure hooks — shell commands that run automatically on events (e.g. before/after a tool call). |
| `/keybindings-help` | Customize keyboard shortcuts / rebind keys (`~/.claude/keybindings.json`). |
| `/terminal-setup` | Configure terminal integration for the best Claude Code experience. |
| `/vim` | Toggle Vim editing mode for the input prompt. |
| `/statusline` | Configure a custom status line for the CLI. |

---

## 5. Project Setup & Context

| Command | Description |
|---|---|
| `/init` | Generate a `CLAUDE.md` file documenting the codebase so Claude has project context. |
| `/memory` | View and edit Claude's persistent memory / `CLAUDE.md` context files. |
| `/add-dir <path>` | Add another directory to the workspace so Claude can read/edit files there. |
| `/mcp` | Manage MCP (Model Context Protocol) servers — connect external tools and data sources. |
| `/agents` | View and manage subagents available for delegating tasks. |

---

## 6. Code Review & Quality

| Command | Description |
|---|---|
| `/review` | Review a pull request. |
| `/code-review` | Review the current diff for correctness bugs at a chosen effort level; `--comment` posts findings inline on a PR. |
| `/security-review` | Run a security review of pending changes on the current branch. |
| `/pr-comments` | Fetch and view comments on a GitHub pull request. |
| `/verify` | Run the app and observe behavior to confirm a change/fix actually works. |

---

## 7. Running & Automating Work

| Command | Description |
|---|---|
| `/run` | Launch and drive the project's app to see a change working (CLI, server, browser, etc.). |
| `/loop [interval] <command>` | Run a prompt or slash command repeatedly. With an interval (`/loop 5m /review`) it polls; without one, Claude self-paces. |
| `/schedule` | Create, list, update, or run scheduled remote agents (cron-style routines), including one-off timed runs. |

---

## 8. Building with the Claude API

| Command | Description |
|---|---|
| `/claude-api` | Build, debug, and optimize Claude API / Anthropic SDK apps; also migrates code between Claude model versions. Includes prompt-caching guidance. |

---

## Quick Tips

- **Discover commands live:** Type `/` to see everything available in *your*
  install — this list evolves between releases.
- **Skills vs. built-ins:** Skills (like `/verify`, `/code-review`, `/run`) are
  modular and may differ per project/plugin setup; built-ins (`/help`, `/clear`,
  `/model`) are always present.
- **Arguments:** Many commands accept arguments after the name, e.g.
  `/btw remember to update the README` or `/loop 10m /security-review`.
- **Context hygiene:** Use `/compact` when a long session slows down, and
  `/clear` when starting an unrelated task — both free up the context window.
- **Run shell commands inline:** Prefix with `!` (e.g. `! git status`) to run a
  shell command directly in the session.

---

*Cheatsheet generated for personal learning and training-material use.*
*Verify command availability against your installed Claude Code version, as*
*commands are added and changed over time.*
