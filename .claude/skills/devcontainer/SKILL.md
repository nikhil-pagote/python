---
name: devcontainer
description: Set up a devcontainer using Podman for use with Zed editor. Use when the user asks to "set up devcontainer", "add devcontainer", "create devcontainer", "configure devcontainer with podman", or wants a reproducible container dev environment.
argument-hint: [project-path]
allowed-tools: [Read, Write, Edit, Bash]
version: 1.0.0
author: Nikhil Pagote
date: 2026-06-22
tags: [devcontainer, podman, zed, linux, containers, python]
status: active
reference: /home/nikhil/Documents/python/devcontainer-podman-zed.md
---

# Devcontainer Setup with Podman and Zed

Set up a `.devcontainer/` directory with Podman-compatible configuration for Zed's native devcontainer support.

## Arguments

Target project path (optional): $ARGUMENTS
If no path provided, use the current working directory.

## Instructions

### Step 1 — Check what already exists

Before creating files, check if `.devcontainer/` already exists:
```bash
ls <project-path>/.devcontainer/ 2>/dev/null
```
If files exist, read them first and edit rather than overwrite.

### Step 2 — Create `.devcontainer/Dockerfile`

Use the official Python image. Default to `python:3.13-slim` unless the user specifies another base image:

```dockerfile
FROM python:3.13-slim

RUN pip install uv
```

### Step 3 — Create `.devcontainer/docker-compose.yml`

```yaml
services:
  devcontainer:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ..:/workspace:cached
      - devcontainer-bashhistory:/commandhistory
      - /run/user/1000/podman/podman.sock:/var/run/docker-host.sock
      - ${HOME}/.gitconfig:/home/vscode/.gitconfig:ro
    working_dir: /workspace
    command: sleep infinity
    userns_mode: keep-id

volumes:
  devcontainer-bashhistory:
```

Key Podman-specific settings:
- `userns_mode: keep-id` — maps container user to host UID; required for rootless Podman to avoid file ownership issues
- Podman socket mount — enables container operations from inside the devcontainer

### Step 4 — Create `.devcontainer/devcontainer.json`

```json
{
  "name": "<project-name>",
  "dockerComposeFile": "docker-compose.yml",
  "service": "devcontainer",
  "workspaceFolder": "/workspace",
  "postCreateCommand": "git config --system --add safe.directory /workspace",
  "customizations": {
    "zed": {
      "extensions": ["python", "toml"]
    }
  }
}
```

Replace `<project-name>` with the actual project name. Adjust `customizations.zed.extensions` to match the project's languages.

### Step 5 — Verify Zed settings

Check if `use_podman` is set in Zed's settings. The Zed settings file is typically at `~/.config/zed/settings.json`. Read it and add the setting if missing:

```json
{
  "use_podman": true
}
```

### Step 6 — Verify Podman socket

```bash
# Check the socket exists
ls /run/user/1000/podman/podman.sock

# If missing, start and enable it
systemctl --user start podman.socket
systemctl --user enable podman.socket
```

### Step 7 — Check podman-compose is available

```bash
which podman-compose
```

If not found, tell the user to install it:
- Fedora/RHEL: `sudo dnf install podman-compose`
- Ubuntu/Debian: `sudo apt install podman-compose`
- pip: `pip install podman-compose`

### Step 8 — Report

Summarize what was created or modified, and tell the user to:
1. Reopen the project in Zed
2. Select **"Open in Container"** when prompted

## Reference

Full tutorial: `/home/nikhil/Documents/python/devcontainer-podman-zed.md`
