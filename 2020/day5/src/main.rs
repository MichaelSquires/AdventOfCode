extern crate anyhow;

#[allow(unused_imports)]
use anyhow::{anyhow, bail, ensure, Result};
#[allow(unused_imports)]
use log::{debug, error, info, trace, warn};

#[derive(Debug)]
struct Seat {
    row: u32,
    col: u32,
    id: u32,
}

impl Seat {
    fn new(id: &str) -> Self {
        let mut row: u32 = 0;
        let mut col: u32 = 0;

        let mut rshift = 6;
        let mut cshift = 2;

        debug!("SEAT: {}", id);

        for ii in id.chars() {
            match ii {
                'B' => {
                    row |= 1 << rshift;
                    rshift -= 1;
                }
                'F' => {
                    rshift -= 1;
                }
                'R' => {
                    col |= 1 << cshift;
                    cshift -= 1;
                }
                'L' => {
                    cshift -= 1;
                }
                _ => {}
            }
        }

        Self {
            row,
            col,
            id: row * 8 + col,
        }
    }
}

fn main() -> Result<()> {
    let opts = vec![clap::Arg::with_name("infile")
        .help("Input filename")
        .required(true)];

    let args = utils::init(Some(opts))?;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;

    let mut seats: Vec<Seat> = data
        .split("\n")
        .filter(|line| !line.is_empty())
        .map(|line| Seat::new(&line))
        .collect();

    let mut part1 = 0;
    let mut part2 = 0;

    // PART 1
    for seat in seats.iter() {
        // Search for highest seat id
        if seat.id > part1 {
            part1 = seat.id;
        }
    }

    // PART 2
    // Sort seats by id
    seats.sort_by(|a, b| a.id.cmp(&b.id));

    // Find the lowest seat id
    let lowest: usize = seats[0].id as usize;

    // Iterate over all the seats
    for ii in lowest..lowest + seats.len() {
        let curr = &seats[ii - lowest];
        let next = &seats[ii + 1 - lowest];

        trace!("ii: {}, {:?} {:?}", ii, curr, next);

        // Next seat id - current seat id should be 1. If not, we found our seat
        if next.id - curr.id != 1 {
            part2 = next.id - 1;
            break;
        }
    }

    println!("PART 1: {}", part1);
    println!("PART 2: {}", part2);

    Ok(())
}
