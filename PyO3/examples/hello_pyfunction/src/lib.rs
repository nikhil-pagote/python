use pyo3::prelude::*;

/// Add two integers.
#[pyfunction]
fn add(a: i64, b: i64) -> PyResult<i64> {
    Ok(a + b)
}

/// Greet a name.
#[pyfunction]
fn greet(name: String) -> PyResult<String> {
    Ok(format!("Hello, {name} from Rust!"))
}

#[pymodule]
fn hello_pyfunction(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_function(wrap_pyfunction!(greet, m)?)?;
    Ok(())
}
