use pyo3::prelude::*;

use std::collections::HashMap;

const INFINITY: i32 = 2147483647;
const INVALID: (i32, i32) = (-1, -1);

fn foreach(height: i32, width: i32) -> Vec<(i32, i32)> {
    let mut ret = Vec::new();

    for x in 0..width {
        for y in 0..height {
            ret.push((x,y))
        }
    }

    ret
}

fn adjacent(height: i32, width: i32, xy: (i32, i32)) -> Vec<(i32, i32)> {
    let mut ret = Vec::<(i32, i32)>::new();
    let x = xy.0;
    let y = xy.1;

    let up = (x, y - 1);
    let down = (x, y + 1);
    let left = (x - 1, y);
    let right = (x + 1, y);

    for xy in [up, down, left, right].iter() {
        if xy.0 < 0 || xy.0 > width {
            continue;
        }

        if xy.1 < 0 || xy.1 > height {
            continue;
        }

        ret.push(*xy);
    }

    ret
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn dijkstra(graph: Vec<i32>, height: i32, width: i32) -> PyResult<Vec<(i32, i32)>> {
    let ret = Vec::new();

    let source = (0, 0);
    let target = (height - 1, width - 1);

    let mut q = Vec::<(i32, i32)>::new();
    let mut dist = HashMap::<(i32, i32), i32>::new();
    let mut prev = HashMap::<(i32, i32), (i32, i32)>::new();

    for xy in foreach(height, width).iter() {
        dist.insert(*xy, INFINITY);
        prev.insert(*xy, INVALID);
        q.push(*xy);
    }

    *dist.get_mut(&source).unwrap() = 0;

    while q.len() != 0 {
        if q.len() % 1000 == 0 {
            println!("QLEN: {}", q.len());
        }
        let mut mindist = INFINITY;
        let mut u = INVALID;
        for xy in q.iter() {
            let d = *dist.get(xy).unwrap();
            if d < mindist {
                mindist = d;
                u = *xy;
            }
        }

        if u == INVALID {
            return Ok(ret);
        }

        q.retain(|x| *x != u);

        if u == target {
            let mut s = Vec::<(i32, i32)>::new();
            if *prev.get(&u).unwrap() != INVALID || u == source {
                while u != INVALID {
                    s.insert(0, u);
                    u = *prev.get(&u).unwrap();
                }
            }

            return Ok(s);
        }

        for v in adjacent(height, width, u).iter() {
            if !q.contains(v) {
                continue;
            }

            let (x, y) = v;

            let d = *dist.get(&u).unwrap();
            let alt = d + graph[(x + width * y) as usize];
            if alt < *dist.get(&v).unwrap() {
                *dist.get_mut(&v).unwrap() = alt;
                *prev.get_mut(&v).unwrap() = u;
            }
        }
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