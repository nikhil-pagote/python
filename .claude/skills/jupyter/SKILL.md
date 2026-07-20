---
name: jupyter
description: Manage the Jupyter notebook server — start, stop, or restart it. Use this skill whenever the user says "start jupyter", "stop jupyter", "restart jupyter", "open notebook", "launch notebook", "kill jupyter", or any variation of wanting to run, open, or manage a Jupyter notebook server in this project.
argument-hint: [start|stop|restart] [notebook-path]
allowed-tools: [Bash]
version: 1.0.0
author: Nikhil Pagote
tags: [jupyter, notebook, uv, python]
---

# Jupyter Notebook Server Management

Manage the Jupyter notebook server for this project. This project uses `uv` — never use `python` or `pip` directly.

**Project root:** `/home/nikhil/Documents/python`
**Notebooks directory:** `AgenticAI/notebooks/`

## Arguments

`$ARGUMENTS` may contain:
- An action: `start`, `stop`, or `restart`
- An optional notebook path (relative or filename only)

If no action is given, infer from the user's message (e.g. "launch" → start, "kill" → stop).

---

## Start

```bash
cd /home/nikhil/Documents/python
uv run jupyter notebook [notebook-path] --no-browser &
```

- If a notebook filename is given without a path, prepend `AgenticAI/notebooks/`
- Use `--no-browser` to avoid auto-opening a browser tab (the user controls when to open it)
- After starting, wait ~2 seconds then run:

```bash
uv run jupyter notebook list
```

This shows the running server URL and token. Print the URL clearly so the user can open it.

**Check if already running first:**
```bash
pgrep -af "jupyter" 2>/dev/null
```
If a server is already running, report the existing URL instead of starting a second one.

---

## Stop

Find and kill the Jupyter process:

```bash
pkill -f "jupyter" && echo "Jupyter stopped"
```

If nothing was running, say so — don't show an error.

Verify it stopped:
```bash
pgrep -af "jupyter" 2>/dev/null || echo "Confirmed: no jupyter process running"
```

---

## Restart

Stop first, then start:

1. Run the Stop steps above
2. Wait 1 second
3. Run the Start steps above

---

## Report

Always end with a clear one-line status:
- Start: `Jupyter running at http://localhost:8888/?token=...`
- Stop: `Jupyter stopped`
- Restart: `Jupyter restarted at http://localhost:8888/?token=...`
