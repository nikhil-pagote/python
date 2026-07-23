---
title: Maturin Workflow
description: How to build and import the PyO3 examples using maturin inside the devcontainer
version: 1.0
author: Nikhil Pagote
date: 2026-07-23
tags: [pyo3, rust, maturin, devcontainer, learning]
status: draft
---

# Maturin Workflow

Each example under `PyO3/examples/` is a standalone maturin project
(`Cargo.toml` + `pyproject.toml` + `src/lib.rs`) — no workspace, so they build
independently.

## Prerequisites

Run this inside the devcontainer (`python_devcontainer-devcontainer-1`), not on
the host. The container's `Dockerfile` installs the Rust toolchain (`rustup`)
and `maturin` (via `pip`). If the container was built before this was added,
rebuild it:

```bash
podman kill python_devcontainer-devcontainer-1
# then reopen the project in Zed to rebuild
```

## Build and import an example

From inside an example directory, with a Python venv active:

```bash
cd PyO3/examples/hello_pyfunction
maturin develop
```

`maturin develop` compiles the Rust crate and installs it into the active
Python environment, importable by its `[lib] name`:

```bash
python -c "import hello_pyfunction; print(hello_pyfunction.add(2, 3))"
```

Same pattern for `hello_pyclass`:

```bash
cd PyO3/examples/hello_pyclass
maturin develop
python -c "from hello_pyclass import Counter; c = Counter(); print(c.increment(5)); print(c.count)"
```

## Notes

- `maturin develop` is for local iteration (debug build, fast). Use
  `maturin build --release` to produce an installable wheel.
- `target/` (Rust build artifacts) is gitignored at the repo root — no need to
  clean it manually.
