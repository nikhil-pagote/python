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
    └── hello_pyclass/        # #[pyclass] + #[pymethods] basics
```

## Quickstart

```bash
cd PyO3/examples/hello_pyfunction
maturin develop
python -c "import hello_pyfunction; print(hello_pyfunction.add(2, 3))"
```

See `docs/maturin-workflow.md` for the full workflow and `docs/pyo3-basics.md`
for what each macro does.
