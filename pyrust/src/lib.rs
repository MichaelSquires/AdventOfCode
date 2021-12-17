use pyo3::prelude::*;

use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};

const INFINITY: i32 = 2147483647;
const INVALID: (i32, i32) = (-1, -1);
const SOURCE: (i32, i32) = (0, 0);

#[derive(Copy, Clone, Eq, PartialEq)]
struct Node {
    xy: (i32, i32),
    val: i32
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        other.xy.cmp(&self.xy)
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

#[pyfunction]
fn dijkstra(graph: &PyAny) -> PyResult<Vec<(i32, i32)>> {

    let height: i32 = graph.getattr("height")?.extract()?;
    let width: i32 = graph.getattr("width")?.extract()?;
    let grid: Vec<i32> = graph.getattr("_grid")?.extract()?;

    let mut ret = Vec::new();

    let target = (height - 1, width - 1);

    let mut q = BinaryHeap::new();
    let mut dist = HashMap::<(i32, i32), i32>::new();
    let mut prev = HashMap::<(i32, i32), (i32, i32)>::new();

    dist.insert(SOURCE, 0);

    q.push(Node { xy: SOURCE, val: 0 });

    while let Some(Node { xy: u, val: _d }) = q.pop() {

        for v in [(u.0, u.1+1), (u.0, u.1-1), (u.0-1, u.1), (u.0+1, u.1)].iter() {
            let (x, y) = *v;

            // Make sure we're still within the bounds of the grid
            if x < 0 || x > width - 1 || y < 0 || y > height - 1 {
                continue;
            }

            let val = grid[(x + width * y) as usize];
            let alt = *dist.entry(u).or_insert(INFINITY) + val;
            let distv = dist.entry(*v).or_insert(INFINITY);
            let prevv = prev.entry(*v).or_insert(INVALID);

            if alt < *distv {
                *distv = alt;
                *prevv = u;
                q.push(Node { xy: *v, val: alt });
            }
        }
    }

    // Construct shortest path from prev info
    let mut u = target;
    while u != INVALID {
        ret.insert(0, u);
        u = *prev.get(&u).unwrap();
    }

    Ok(ret)
}

#[pymodule]
fn pyrust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(dijkstra, m)?)?;

    Ok(())
}