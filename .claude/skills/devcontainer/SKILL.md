---
name: devcontainer
description: Set up or rebuild a devcontainer using rootless Podman for Zed editor. Use this skill whenever the user says "set up devcontainer", "add devcontainer", "create devcontainer", "containerize my project", "reproducible dev environment", "configure devcontainer with podman", "rebuild the container", "devcontainer not working", "open in container", or wants to isolate their project in a container with Zed. Trigger even if the user only mentions one of these keywords.
argument-hint: [project-path]
allowed-tools: [Read, Write, Edit, Bash]
version: 1.1.0
author: Nikhil Pagote
date: 2026-06-22
tags: [devcontainer, podman, zed, linux, containers, python]
status: active
reference: /home/nikhil/Documents/python/devcontainer-podman-zed.md
---

# Devcontainer Setup with Podman and Zed

Set up `.devcontainer/` config for Zed's native devcontainer support using rootless Podman.

## Arguments

Target project path (optional): `$ARGUMENTS`  
If no path provided, use the current working directory.

---

## Step 1 — Check prerequisites first

Before creating any files, verify the environment is ready. This saves the user from a broken setup.

**Check Podman socket:**
```bash
ls ${XDG_RUNTIME_DIR}/podman/podman.sock 2>/dev/null || echo "Socket missing"
```
If missing:
```bash
systemctl --user start podman.socket
systemctl --user enable podman.socket
```

**Check podman-compose:**
```bash
which podman-compose || echo "Not found"
```
If missing, tell the user to install it:
- Ubuntu/Debian: `sudo apt install podman-compose`
- Fedora/RHEL: `sudo dnf install podman-compose`
- pip: `pip install podman-compose`

**Check Zed `use_podman` setting:**
```bash
cat ~/.config/zed/settings.json 2>/dev/null
```
If `"use_podman": true` is absent, add it.

---

## Step 2 — Check what already exists

```bash
ls <project-path>/.devcontainer/ 2>/dev/null
```
If files exist, read them first and edit rather than overwrite.

---

## Step 3 — Create `.devcontainer/Dockerfile`

Default to `python:3.13-slim` unless the user specifies a different language or base image:

```dockerfile
FROM python:3.13-slim

RUN pip install uv
```

For non-Python projects, swap the base image (e.g. `node:20-slim`, `golang:1.22-bookworm`) and adjust the install command accordingly.

---

## Step 4 — Create `.devcontainer/docker-compose.yml`

```yaml
services:
  devcontainer:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ..:/workspace:cached
      - devcontainer-bashhistory:/commandhistory
      - ${XDG_RUNTIME_DIR}/podman/podman.sock:/var/run/docker-host.sock
      - ${HOME}/.gitconfig:/home/vscode/.gitconfig:ro
    working_dir: /workspace
    command: sleep infinity
    userns_mode: keep-id

volumes:
  devcontainer-bashhistory:
```

Key Podman-specific settings:
- `userns_mode: keep-id` — maps container user to host UID, preventing file ownership issues with rootless Podman
- `${XDG_RUNTIME_DIR}` — resolves to `/run/user/<UID>` at runtime, so the socket path works for any user (not just UID 1000)
- Podman socket mount — allows container operations from inside the devcontainer if needed

---

## Step 5 — Create `.devcontainer/devcontainer.json`

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

---

## Step 6 — Report

Summarize what was created or modified, then tell the user:

1. Reopen the project in Zed
2. Select **"Open in Container"** when prompted
3. If no prompt appears: `Alt+Ctrl+Shift+O` → Remote Projects → Connect Dev Container

---

## Rebuild (after config changes)

Zed does not auto-rebuild when `Dockerfile` or `devcontainer.json` changes. When the user asks to rebuild:

```bash
# Find the running container
podman ps

# Kill it
podman kill <container-name>
```

Then tell the user to reopen the project in Zed — it will rebuild from the updated config.

For a full clean rebuild (clears image cache):
```bash
podman rm -f <container-name>
podman rmi <image-name>
```

---

## Reference

Full guide including troubleshooting: `/home/nikhil/Documents/python/devcontainer-podman-zed.md`
