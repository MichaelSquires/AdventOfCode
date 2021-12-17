use pyo3::prelude::*;

use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};

const INFINITY: i32 = 2147483647;
const INVALID: (i32, i32) = (-1, -1);

#[derive(Copy, Clone, Eq, PartialEq)]
struct Node {
    u: (i32, i32),
    d: i32
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        other.d.cmp(&self.d)
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

#[pyfunction]
fn dijkstra(graph: Vec<i32>, height: i32, width: i32) -> PyResult<Vec<(i32, i32)>> {
    let mut ret = Vec::new();

    let source = (0, 0);
    let target = (height - 1, width - 1);

    let mut q = BinaryHeap::new();
    let mut dist = HashMap::<(i32, i32), i32>::new();
    let mut prev = HashMap::<(i32, i32), (i32, i32)>::new();

    dist.insert(source, 0);

    q.push(Node { u: source, d: 0 });

    while let Some(Node { u, d: _d }) = q.pop() {

        for v in [(u.0, u.1+1), (u.0, u.1-1), (u.0-1, u.1), (u.0+1, u.1)].iter() {
            let (x, y) = *v;

            // Make sure we're still within the bounds of the grid
            if x < 0 || x > width - 1 || y < 0 || y > height - 1 {
                continue;
            }

            let alt = *dist.entry(u).or_insert(INFINITY) + graph[(x + width * y) as usize];
            let distv = dist.entry(*v).or_insert(INFINITY);
            let prevv = prev.entry(*v).or_insert(INVALID);

            if alt < *distv {
                *distv = alt;
                *prevv = u;
                q.push(Node { u: *v, d: alt });
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