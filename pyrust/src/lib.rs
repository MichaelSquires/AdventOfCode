use pyo3::prelude::*;

use std::collections::HashMap;
use priority_queue::DoublePriorityQueue;

const INFINITY: i32 = 2147483647;
const INVALID: (i32, i32) = (-1, -1);

fn adjacent(height: i32, width: i32, xy: (i32, i32)) -> Vec<(i32, i32)> {
    let mut ret = Vec::<(i32, i32)>::new();
    let x = xy.0;
    let y = xy.1;

    let up = (x, y - 1);
    let down = (x, y + 1);
    let left = (x - 1, y);
    let right = (x + 1, y);

    for xy in [up, down, left, right].iter() {
        if xy.0 < 0 || xy.0 > width - 1 {
            continue;
        }

        if xy.1 < 0 || xy.1 > height - 1 {
            continue;
        }

        ret.push(*xy);
    }

    ret
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn dijkstra(graph: Vec<i32>, height: i32, width: i32) -> PyResult<Vec<(i32, i32)>> {
    let mut ret = Vec::new();

    let source = (0, 0);
    let target = (height - 1, width - 1);

    //let mut q = Vec::<(i32, i32)>::new();
    let mut q = DoublePriorityQueue::new();
    let mut dist = HashMap::<(i32, i32), i32>::new();
    let mut prev = HashMap::<(i32, i32), (i32, i32)>::new();

    dist.insert(source, 0);

    q.push(source, 0);

    while !q.is_empty() {
        let (u, _d) = q.pop_min().unwrap();

        for v in adjacent(height, width, u).iter() {
            let (x, y) = v;

            let alt = *dist.entry(u).or_insert(INFINITY) + graph[(x + width * y) as usize];
            let distv = dist.entry(*v).or_insert(INFINITY);
            let prevv = prev.entry(*v).or_insert(INVALID);

            if alt < *distv {
                *distv = alt;
                *prevv = u;
                q.push(*v, alt);
            }
        }
    }

    let mut u = target;
    while u != INVALID {
        ret.insert(0, u);
        u = *prev.get(&u).unwrap();
    }

    Ok(ret)
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn pyrust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(dijkstra, m)?)?;

    Ok(())
}