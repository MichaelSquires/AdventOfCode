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

    let earliest = data.lines().next().unwrap().parse::<u32>().unwrap();
    let schedule = data.lines().skip(1).next().unwrap();
    let busses: Vec<u32> = schedule.split(",").filter(|&e| e != "x").map(|bus| bus.parse::<u32>().unwrap()).collect();

    debug!("EARLIEST: {}", earliest);
    debug!("SCHEDULE: {}", schedule);
    debug!("BUSES: {:?}", busses);

    let mut min = earliest * 2;
    let mut bus = 0;

    for bb in busses.iter() {
        let mut counter = 1;

        loop {
            let arrival = bb * counter;
            if arrival > earliest && arrival < min {
                debug!("ARRIVAL: {} ({}, {})", arrival, bb, counter);
                bus = *bb;
                min = arrival;
                break;
            }

            if arrival > earliest && arrival > min {
                break;
            }

            counter += 1
        }
    }

    // PART 1
    let mut part1 = (min - earliest) * bus;
    println!("PART 1: {}", part1);

    // PART 2
    let mut part2 = 0;
    println!("PART 2: {}", part2);

    Ok(())
}
