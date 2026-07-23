use pyo3::prelude::*;

/// A simple counter you can increment from Python.
#[pyclass]
struct Counter {
    count: i64,
}

#[pymethods]
impl Counter {
    #[new]
    fn new() -> Self {
        Counter { count: 0 }
    }

    /// Increase the counter by `by` and return the new value.
    fn increment(&mut self, by: i64) -> i64 {
        self.count += by;
        self.count
    }

    #[getter]
    fn count(&self) -> i64 {
        self.count
    }
}

#[pymodule]
fn hello_pyclass(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Counter>()?;
    Ok(())
}
