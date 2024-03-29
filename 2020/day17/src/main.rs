extern crate anyhow;
extern crate fern;

use anyhow::Result;

#[allow(unused_imports)]
use log::{debug, error, info, trace, warn};

pub fn setup_logger(level: log::LevelFilter) -> Result<()> {
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

pub fn init(opts: Option<Vec<clap::Arg<'static, '_>>>) -> Result<clap::ArgMatches<'static>> {
    let argv: Vec<String> = std::env::args().collect();

    // Always add the "verbose" option
    let mut options = vec![clap::Arg::with_name("verbose")
        .help("Detailed output")
        .short("v")
        .multiple(true)];

    // Extend options with passed in arguments
    if let Some(v) = opts {
        options.extend_from_slice(&v);
    }

    // Create the parser and parse the command line
    let matches = clap::App::new(&argv[0]).args(&options).get_matches();

    // Setup the logger
    setup_logger(match matches.occurrences_of("verbose") {
        0 => log::LevelFilter::Warn,
        1 => log::LevelFilter::Info,
        2 => log::LevelFilter::Debug,
        _ => log::LevelFilter::Trace,
    })?;

    Ok(matches)
}

fn main() -> Result<()> {
    let opts = vec![clap::Arg::with_name("infile")
        .help("Input filename")
        .required(true)];

    let args = utils::init(Some(opts))?;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;

    let lines: Vec<&str> = data.lines().collect();

    let mut cubes = std::collections::HashSet::new();

    for xx in 0..lines.len() {
        let line: &str = lines[xx];

        for yy in 0..line.len() {
            if &line[yy..yy+1] == "#" {
                cubes.insert((xx, yy, 0));
            }
        }
    }

    for ii in 0..6 {

    }


    // PART 1
    let mut part1 = 0;
    println!("PART 1: {}", part1);

    // PART 2
    let mut part2 = 0;
    println!("PART 2: {}", part2);

    Ok(())
}
