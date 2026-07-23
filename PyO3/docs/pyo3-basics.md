---
title: PyO3 Basics
description: Core PyO3 building blocks used by the examples in this directory — pyfunction, pyclass, and pymodule
version: 1.0
author: Nikhil Pagote
date: 2026-07-23
tags: [pyo3, rust, python, ffi, learning]
status: draft
---

# PyO3 Basics

Notes to accompany `PyO3/examples/`. Not a PyO3 reference — just the pieces used here.

## `#[pyfunction]`

Exposes a plain Rust function to Python. Argument and return types are converted
automatically for common types (`i64`, `String`, `f64`, `Vec<T>`, etc.). Return
`PyResult<T>` so Rust errors can become Python exceptions.

See `examples/hello_pyfunction/src/lib.rs`.

## `#[pyclass]` / `#[pymethods]`

`#[pyclass]` marks a Rust struct as a Python type. `#[pymethods]` defines what's
callable on it from Python:
- `#[new]` — the `__init__` constructor.
- Plain methods — instance methods.
- `#[getter]` / `#[setter]` — computed properties (or use `#[pyo3(get, set)]` on a
  field directly for a plain attribute).

See `examples/hello_pyclass/src/lib.rs`.

## `#[pymodule]`

The entry point Python imports. Registers functions with `wrap_pyfunction!` and
classes with `m.add_class::<T>()`. The function name **must** match the library
name in `Cargo.toml` (`[lib] name = "..."`) — that's what Python imports.

## Doc comments become docstrings

`///` comments above a `#[pyfunction]` or `#[pyclass]` are exposed as the
Python `__doc__` string — `help(hello_pyfunction.add)` will show it.

## Newer alternative: declarative modules

Recent PyO3 also supports a declarative `#[pyo3::pymodule] mod name { ... }`
form with `#[pymodule_export]`, which skips the manual `wrap_pyfunction!` calls.
The examples here use the classic functional form instead because it makes the
registration step explicit — useful while still learning how PyO3 wires things
up.
