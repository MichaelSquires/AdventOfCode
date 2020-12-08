extern crate anyhow;

#[allow(unused_imports)]
use anyhow::{anyhow, bail, ensure, Result};
#[allow(unused_imports)]
use log::{debug, error, info, trace, warn};

use std::collections::HashSet;

fn main() -> Result<()> {
    let opts = vec![clap::Arg::with_name("infile")
        .help("Input filename")
        .required(true)];

    let args = utils::init(Some(opts))?;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;

    let groups: Vec<&str> = data.split("\n\n").collect();

    debug!("GROUPS {:?}", groups);

    let mut part1 = 0;
    let mut part2 = 0;

    // PART 1
    for group in groups.iter() {
        let mut set = HashSet::new();

        for cc in group.chars() {
            if cc == '\n' {
                continue;
            }

            set.insert(cc);
        }

        part1 += set.len();
    }

    // PART 2
    for group in groups.iter() {
        let answers: Vec<&str> = group.split('\n').filter(|l| !l.is_empty()).collect();

        let yes: Vec<char> = answers[0]
            .chars()
            .filter(|&c| answers.iter().skip(1).all(|a| a.contains(c)))
            .collect();

        part2 += yes.len();
    }

    println!("PART 1: {}", part1);
    println!("PART 2: {}", part2);

    Ok(())
}
