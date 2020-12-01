extern crate fern;
extern crate anyhow;

use anyhow::Result;
use log::{debug, error, info, warn, trace};


fn setup_logger(level: log::LevelFilter) -> Result<(), fern::InitError> {
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
            0 => { log::LevelFilter::Info }
            1 => { log::LevelFilter::Debug }
            _ => { log::LevelFilter::Trace }
        }
    )?;

    Ok(matches)
}

fn main() -> Result<()> {

    let args = init()?;

    let data: String = std::string::String::from_utf8(std::fs::read(args.value_of("infile").unwrap())?)?;

    let values: Vec<u32> = data.lines().map(|line| line.parse::<u32>().unwrap()).collect();

    let mut found = false;

    // PART 1
    for ii in values.iter() {
        for kk in values.iter() {
            if ii + kk != 2020 {
                continue;
            }

            println!("PART 1: ii {}, kk {}, result {}", ii, kk, ii * kk);
            found = true;
            break;
        }

        if found {
            break;
        }
    }

    found = false;

    // PART 2
    for ii in values.iter() {
        for kk in values.iter() {
            for jj in values.iter() {
                if ii + kk + jj != 2020 {
                    continue;
                }

                println!("PART 2: ii {}, kk {}, jj {}, result {}", ii, kk, jj, ii * kk * jj);
                found = true;
                break;
            }

            if found {
                break;
            }
        }

        if found {
            break;
        }
    }

    Ok(())
}
