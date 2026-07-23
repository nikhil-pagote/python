//! Embedding CPython inside a Rust binary.
//!
//! Run with `cargo run` — there is no maturin step and no .so produced.

use pyo3::prelude::*;
use pyo3::types::PyDict;

fn main() -> PyResult<()> {
    // Every interaction with Python happens inside `attach`, which acquires the
    // GIL and hands back the `py` token proving we hold it.
    Python::attach(|py| {
        // 1. Import a stdlib module and read an attribute off it.
        let sys = py.import("sys")?;
        let version: String = sys.getattr("version")?.extract()?;
        println!("interpreter: {}", version.replace('\n', " "));

        // 2. Call a function and extract the result back into a Rust type.
        let math = py.import("math")?;
        let sqrt: f64 = math.call_method1("sqrt", (256.0,))?.extract()?;
        println!("math.sqrt(256) -> {sqrt}");

        // 3. Run an arbitrary snippet, passing values in and pulling them out
        //    via a globals dict.
        let globals = PyDict::new(py);
        globals.set_item("numbers", vec![3, 1, 4, 1, 5, 9, 2, 6])?;
        py.run(
            c"result = sorted(set(numbers), reverse=True)",
            Some(&globals),
            None,
        )?;
        let result: Vec<i64> = globals.get_item("result").unwrap().unwrap().extract()?;
        println!("sorted(set(numbers)) -> {result:?}");

        // 4. Define a Python function, then call it from Rust.
        py.run(c"def shout(s): return s.upper() + '!'", Some(&globals), None)?;
        let shout = globals.get_item("shout").unwrap().unwrap();
        let shouted: String = shout.call1(("hello from rust",))?.extract()?;
        println!("shout(...) -> {shouted}");

        Ok(())
    })
}
