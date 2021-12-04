extern crate anyhow;

#[allow(unused_imports)]
use anyhow::{anyhow, bail, ensure, Result};
#[allow(unused_imports)]
use log::{debug, error, info, trace, warn};

fn main() -> Result<()> {
    let opts = vec![clap::Arg::with_name("infile")
        .help("Input filename")
        .required(true)];

    let args = utils::init(Some(opts))?;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;

    let mut adapters: Vec<u32> = data
        .lines()
        .map(|line| line.parse::<u32>().unwrap())
        .collect();
    adapters.sort();

    trace!("adapters: {:?}", adapters);

    // PART 1
    let mut ones = 0;
    let mut threes = 1;

    let mut curr = 0;
    for ii in 0..adapters.len() {
        match adapters[ii] - curr {
            1 => {
                ones += 1;
            }
            3 => {
                threes += 1;
            }
            _ => {
                panic!("Invalid difference");
            }
        }

        curr = adapters[ii];
    }

    debug!("ones {}, threes {}", ones, threes);
    println!("PART 1: {}", ones * threes);

    // PART 2
    // Algorithm shamelessly stolen and modified from here:
    // https://github.com/lu-reit/AdventOfCode_2020_Rust/blob/master/aoc_10/src/main.rs
    // https://www.reddit.com/r/adventofcode/comments/ka8z8x/2020_day_10_solutions/gf9qirg/

    // Insert outlet at beginning
    adapters.insert(0, 0);

    // Insert device at end
    adapters.push(adapters.last().unwrap() + 3);

    let len = adapters.len();

    // Holds the number of possible paths that still can be taken
    let mut paths: Vec<u64> = vec![1; len];

    // Deal with the edgecase adapters.len() - 3
    if adapters[len - 1] - adapters[len - 3] <= 3 {
        paths[len - 3] = 2;
    }

    // Iterate through adapters/paths in reverse and sum over the paths
    // for the previous adapters which are in range
    for ii in (0..len - 3).rev() {
        let mut path_sum = paths[ii + 1];

        if adapters[ii + 2] - adapters[ii] <= 3 {
            path_sum += paths[ii + 2]
        }

        if adapters[ii + 3] - adapters[ii] <= 3 {
            path_sum += paths[ii + 3]
        }

        paths[ii] = path_sum;
    }

    println!("PART 2: {}", paths[0]);

    Ok(())
}
