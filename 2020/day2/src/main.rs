extern crate anyhow;
extern crate fern;
extern crate regex;

use anyhow::Result;
#[allow(unused_imports)]
use log::{debug, error, info, trace, warn};

fn setup_logger(level: log::LevelFilter) -> Result<()> {
    let colors = fern::colors::ColoredLevelConfig::new()
        .error(fern::colors::Color::BrightRed)
        .warn(fern::colors::Color::BrightYellow)
        .info(fern::colors::Color::BrightWhite)
        .debug(fern::colors::Color::BrightBlack)
        .trace(fern::colors::Color::Cyan);

    fern::Dispatch::new()
        .format(move |out, message, record| {
            out.finish(format_args!(
                "[{}][{}] {}",
                record.target(),
                colors.color(record.level()),
                message
            ))
        })
        .level(level)
        .chain(std::io::stderr())
        .apply()?;

    Ok(())
}

fn init() -> Result<clap::ArgMatches<'static>> {
    let argv: Vec<String> = std::env::args().collect();

    let matches = clap::App::new(&argv[0])
        .arg(
            clap::Arg::with_name("verbose")
                .help("Detailed output")
                .short("v")
                .multiple(true),
        )
        .arg(
            clap::Arg::with_name("infile")
                .help("Input filename")
                .required(true),
        )
        .get_matches();

    setup_logger(match matches.occurrences_of("verbose") {
        0 => log::LevelFilter::Warn,
        1 => log::LevelFilter::Info,
        2 => log::LevelFilter::Debug,
        _ => log::LevelFilter::Trace,
    })?;

    Ok(matches)
}

fn main() -> Result<()> {
    let args = init()?;

    let mut part1 = 0;
    let mut part2 = 0;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;

    let re = regex::Regex::new(r"(\d+)-(\d+)\s+([a-z]):\s+([a-z]+)").unwrap();
    for cap in re.captures_iter(&data) {
        let min = cap[1].parse::<usize>()?;
        let max = cap[2].parse::<usize>()?;
        let letter = &cap[3];
        let passwd = &cap[4];

        debug!("min {}, max {}, ltr {}, pwd {}", min, max, letter, passwd);

        // PART 1
        let matches: Vec<&str> = passwd.matches(letter).collect();

        debug!("matches: {:?}", matches);

        let count = matches.len();

        if count >= min && count <= max {
            part1 += 1;
        }

        // PART 2
        let bytes = passwd.as_bytes();
        let first = (bytes[min - 1] as char).to_string();
        let second = (bytes[max - 1] as char).to_string();

        debug!(
            "first {}, second {}, letter {}, passwd {}",
            first, second, letter, passwd
        );

        if (first == letter || second == letter) && !(first == letter && second == letter) {
            part2 += 1;
        }
    }

    println!("PART 1: {}", part1);
    println!("PART 2: {}", part2);

    Ok(())
}
