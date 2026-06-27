---
title: Devcontainer with Podman and Zed
description: Guide for setting up and using devcontainers with rootless Podman and Zed editor on Linux, using Zed's native devcontainer support
version: 1.0.0
author: Nikhil Pagote
date: 2026-06-22
tags: [devcontainer, podman, zed, linux, docker-compose, python, containers]
status: active
audience: developers using Zed on Linux with rootless Podman
---

# Devcontainer with Podman and Zed

Zed has native devcontainer support — no extension required. This guide covers setup with rootless Podman on Linux.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [One-Time Setup](#one-time-setup)
3. [Project Structure](#project-structure)
4. [Opening in Zed](#opening-in-zed)
5. [Daily Workflow](#daily-workflow)
6. [Container Management](#container-management)
7. [Quick Reference](#quick-reference)
8. [Tips and Troubleshooting](#tips-and-troubleshooting)

---

## Prerequisites

- Podman installed and available on `PATH`
- Rootless Podman socket running
- A project with `.devcontainer/devcontainer.json`

---

## One-Time Setup

### Enable Podman in Zed settings

Open Zed settings (`Ctrl+,`) and add:

```json
{
  "use_podman": true
}
```

### Ensure the Podman socket is running

```bash
# Start the socket
systemctl --user start podman.socket

# Enable on boot
systemctl --user enable podman.socket

# Verify
ls /run/user/1000/podman/podman.sock
```

### Install podman-compose (if using docker-compose.yml)

```bash
# Fedora/RHEL
sudo dnf install podman-compose

# Ubuntu/Debian
sudo apt install podman-compose

# pip
pip install podman-compose
```

---

## Project Structure

```
project/
├── .devcontainer/
│   ├── devcontainer.json
│   ├── docker-compose.yml  # optional, if using compose
│   └── Dockerfile
└── src/
```

### devcontainer.json

```json
{
  "name": "My Project",
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

> Zed extensions listed under `customizations.zed.extensions` are loaded automatically when you open the container.

### docker-compose.yml

```yaml
services:
  devcontainer:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ..:/workspace:cached
      - devcontainer-bashhistory:/commandhistory
      # Podman socket for container operations inside devcontainer
      - /run/user/1000/podman/podman.sock:/var/run/docker-host.sock
      # Share host git identity
      - ${HOME}/.gitconfig:/home/vscode/.gitconfig:ro
    working_dir: /workspace
    command: sleep infinity
    # Required for rootless Podman — maps container user to host UID
    userns_mode: keep-id

volumes:
  devcontainer-bashhistory:
```

### Dockerfile

```dockerfile
FROM python:3.13-slim

RUN pip install uv
```

> Use `python:3-slim` to always track the latest stable Python minor version, or pin to `python:3.13-slim` for reproducibility.

---

## Opening in Zed

### Automatic prompt

When you open a project that contains `.devcontainer/devcontainer.json`, Zed displays a prompt. Select **"Open in Container"** — Zed builds the image, starts the container, and reconnects the project inside it.

### Manual via command palette

```
Alt+Ctrl+Shift+O  →  Remote Projects  →  Connect Dev Container
```

Or search the command palette for: `Project: Open Remote`

Once connected, Zed runs all terminals, tasks, and language servers **inside the container**. Files are linked via the workspace mount, so you edit them normally in Zed.

---

## Daily Workflow

```
1. Open project in Zed
2. Select "Open in Container" when prompted (or via command palette)
3. Edit files in Zed as normal
4. Open a terminal in Zed (Ctrl+`) — it runs inside the container
5. Run your code from that terminal
```

The workspace is bind-mounted, so files saved in Zed are immediately visible inside the container.

---

## Container Management

### Rebuild after config changes

Zed does **not** auto-rebuild when `devcontainer.json` or `Dockerfile` changes. Kill and reopen:

```bash
# Find the container
podman ps

# Kill it
podman kill <container-name>
```

Then reopen the project in Zed — it will rebuild.

### Other useful commands

```bash
# List running containers
podman ps

# Stop a container
podman stop <container-name>

# Remove a container (keeps the image)
podman rm <container-name>

# Full rebuild (removes image cache)
podman rm -f <container-name>
podman rmi <image-name>
# Then reopen in Zed to rebuild from scratch
```

---

## Quick Reference

| Action | How |
|--------|-----|
| Open project in container | Open project in Zed → "Open in Container" prompt |
| Manual open in container | `Alt+Ctrl+Shift+O` → Remote Projects → Connect Dev Container |
| Terminal inside container | `Ctrl+`` in Zed (after opening in container) |
| Rebuild container | `podman kill <name>` → reopen project in Zed |
| Enable Podman in Zed | `"use_podman": true` in Zed settings.json |
| Start Podman socket | `systemctl --user start podman.socket` |

---

## Tips and Troubleshooting

### Zed doesn't detect the devcontainer
Make sure `.devcontainer/devcontainer.json` exists at the project root. Zed looks for this file when opening a project.

### Permission errors on mounted files
Add `userns_mode: keep-id` to your service in `docker-compose.yml`. This maps the container user to your host UID so file ownership stays consistent with rootless Podman.

### Changes to Dockerfile not picked up
Zed caches the image. Kill the container with `podman kill <name>`, then reopen the project in Zed to force a rebuild.

### podman-compose errors with docker-compose.yml
If Zed fails to start the container via compose, check that `podman-compose` is on your `PATH`:
```bash
which podman-compose
```
If it's missing or named differently, symlink it:
```bash
sudo ln -s $(which podman-compose) /usr/local/bin/docker-compose
```

### Podman socket not found
```bash
systemctl --user start podman.socket
ls /run/user/1000/podman/podman.sock  # confirm it exists
```
