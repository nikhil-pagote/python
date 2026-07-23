---
title: PyO3 Learning Examples
description: Minimal PyO3 examples for learning Rust-Python bindings, built with maturin
version: 1.0
author: Nikhil Pagote
date: 2026-07-23
tags: [pyo3, rust, python, maturin, learning]
status: draft
---

# PyO3

Minimal, standalone PyO3 examples for learning — each one a separate maturin
project. Build inside the devcontainer (Rust + maturin are installed there;
see `docs/maturin-workflow.md`).

## Layout

```
PyO3/
├── docs/                     # concept notes
│   ├── pyo3-basics.md
│   └── maturin-workflow.md
└── examples/
    ├── hello_pyfunction/     # #[pyfunction] + #[pymodule] basics
    ├── hello_pyclass/        # #[pyclass] + #[pymethods] basics
    └── embed_python/         # the reverse: Rust binary running CPython
```

PyO3 goes both ways, and the examples are split accordingly:

| Direction | Crate type | Built with | Examples |
|---|---|---|---|
| Python imports Rust | `cdylib` + `extension-module` | `maturin develop` | `hello_pyfunction`, `hello_pyclass` |
| Rust runs Python | binary + `auto-initialize` | `cargo run` | `embed_python` |

The two pyo3 features are **mutually exclusive**. `extension-module` leaves
libpython unlinked because the importing interpreter supplies those symbols; an
embedding binary has no host interpreter and must link libpython itself.
Enabling both produces link errors that don't obviously point at the cause.

## Quickstart — Python imports Rust

`maturin develop` installs the built module into the **active virtualenv**, so
activate one first. The devcontainer's shells do not set `VIRTUAL_ENV`, and
maturin fails without it.

```bash
source /workspace/.venv/bin/activate

cd PyO3/examples/hello_pyfunction
maturin develop
python -c "import hello_pyfunction; print(hello_pyfunction.add(2, 3))"
```

Prefer not to activate? Pass the venv per-command instead:

```bash
VIRTUAL_ENV=/workspace/.venv maturin develop
```

The installed module is a compiled `.so`, so re-run `maturin develop` after
every Rust change — edits to `src/lib.rs` have no effect until you rebuild.

## Quickstart — Rust runs Python

No virtualenv and no maturin; this one is an ordinary binary crate.

```bash
cd PyO3/examples/embed_python
cargo run
```

See `docs/maturin-workflow.md` for the full workflow and `docs/pyo3-basics.md`
for what each macro does.
