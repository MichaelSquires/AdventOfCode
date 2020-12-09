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

    let mut part1 = 0;
    let mut part2 = 0;

    let numbers: Vec<u64> = data
        .lines()
        .map(|line| line.parse::<u64>().unwrap())
        .collect();

    let prelen = match args.value_of("infile") {
        Some("sample") => 5,
        Some("input") | _ => 25,
    };

    for ii in 0..numbers.len() - prelen {
        let mut preamble = numbers[ii..prelen + ii].to_vec();
        preamble.sort();

        let curr = numbers[prelen + ii];

        debug!("preamble: {:?}", preamble);
        debug!("curr: {:?}", curr);

        if preamble[0] + preamble[1] > curr {
            part1 = curr;
            break;
        }
    }

    println!("PART 1: {}", part1);

    'outer: for ii in 0..numbers.len() {
        for kk in ii..numbers.len() {
            if numbers[ii..kk].iter().sum::<u64>() == part1 {
                let mut range = numbers[ii..kk].to_vec();
                range.sort();

                part2 = range[0] + range.last().unwrap();
                break 'outer;
            }
        }
    }

    println!("PART 2: {}", part2);

    Ok(())
}
