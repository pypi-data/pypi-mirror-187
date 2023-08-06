use pyo3::{prelude::*, types::PyDict,wrap_pymodule};
use rayon::prelude::*;
mod submodule;


/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}
#[pyfunction]
fn search(contents: &str, needle: &str) -> usize {
    contents
        .par_lines()
        .map(|line| count_line(line, needle))
        .sum()
}

fn count_line(line: &str, needle: &str) -> usize {
    let mut total = 0;
    for word in line.split(' ') {
        if word == needle {
            total += 1;
        }
    }
    total
}

#[pyclass]
struct ExampleClass {
    #[pyo3(get, set)]
    value: i32,
}
#[pymethods]
impl ExampleClass {
    #[new]
    pub fn new(value: i32) -> Self {
        ExampleClass { value }
    }
}





/// A Python module implemented in Rust.
#[pymodule]
fn tackage(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(search, m)?)?;
    m.add_class::<ExampleClass>()?;
    let sys = PyModule::import(_py, "sys")?;
    let sys_modules: &PyDict = sys.getattr("modules")?.downcast()?;
    sys_modules.set_item("setuptools_rust_starter.submodule", m.getattr("submodule")?)?;
    Ok(())
}