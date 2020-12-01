extern crate fern;
extern crate anyhow;

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
        .arg(clap::Arg::with_name("verbose")
            .help("Detailed output")
            .short("v")
            .multiple(true)
        )
        .arg(clap::Arg::with_name("infile")
            .help("Input filename")
            .required(true)
        )
        .get_matches();

    setup_logger(
        match matches.occurrences_of("verbose") {
            0 => { log::LevelFilter::Warn }
            1 => { log::LevelFilter::Info }
            2 => { log::LevelFilter::Debug }
            _ => { log::LevelFilter::Trace }
        }
    )?;

    Ok(matches)
}

const VALUE: u32 = 2020;

fn main() -> Result<()> {

    let args = init()?;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;

    let values: Vec<u32> = data.lines().map(|line| line.parse::<u32>().unwrap()).collect();

    let mut part1 = 0;
    let mut part2 = 0;

    // PART 1
    for ii in values.iter() {
        for kk in values.iter() {
            if part1 == 0 && ii + kk == VALUE {
                part1 = ii * kk;
            }

            if part2 == 0 {
                for jj in values.iter() {
                    if ii + kk + jj != VALUE  {
                        continue;
                    }

                    part2 = ii * kk * jj;
                    break;
                }
            }
        }

        if part1 != 0 && part2 != 0 {
            break;
        }
    }

    println!("PART 1: {}", part1);
    println!("PART 2: {}", part2);

    Ok(())
}
