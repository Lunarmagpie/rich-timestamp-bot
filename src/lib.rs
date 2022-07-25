use pyo3::prelude::*;
use rust_fuzzy_search;

#[pyclass]
struct StringSearcher {
    words: Vec<String>,
}

#[pymethods]
impl StringSearcher {
    #[new]
    fn new(words: Vec<String>) -> Self {
        Self { words }
    }

    fn fuzzy_search(&self, s: &str, n: usize) -> Vec<String> {
        let words = self.words.iter().map(String::as_str).collect::<Vec<&str>>();
        let results = rust_fuzzy_search::fuzzy_search_best_n(s, words.as_slice(), n);
        results.iter().map(|x| x.0.to_owned()).collect()
    }
}

#[pymodule]
fn rusty(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<StringSearcher>().unwrap();
    Ok(())
}
