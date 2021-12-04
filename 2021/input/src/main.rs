extern crate fern;
extern crate ureq;
extern crate anyhow;

use anyhow::Result;
#[allow(unused_imports)]
use log::{debug, error, info, warn, trace};


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
        .arg(clap::Arg::with_name("outfile")
            .help("Output filename")
            .short("f")
            .takes_value(true)
            .default_value("input")
        )
        .arg(clap::Arg::with_name("sessfile")
            .help("Session ID filename")
            .short("s")
            .takes_value(true)
            .default_value("session.txt")
        )
        .arg(clap::Arg::with_name("verbose")
            .help("Detailed output")
            .short("v")
            .multiple(true)
        )
        .arg(clap::Arg::with_name("year")
            .help("Event year")
            .short("y")
            .takes_value(true)
            .default_value("2021")
        )
        .arg(clap::Arg::with_name("day")
            .help("Event day")
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

    let session_id: String = std::fs::read_to_string(args.value_of("sessfile").unwrap())?;

    let url = format!("https://adventofcode.com/{}/day/{}/input",
        args.value_of("year").unwrap(),
        args.value_of("day").unwrap()
    );

    info!("Requesting input from {}", url);

    let cookie = ureq::Cookie::build("session", session_id)
        .domain("adventofcode.com")
        .path("/")
        .finish();

    debug!("Cookie: {}", cookie);

    let agent = ureq::agent();
    agent.set_cookie(cookie);
    debug!("Agent: {:?}", agent);

    let response = agent.get(&url).call();

    anyhow::ensure!(response.ok(), "Invalid response: {} {}", response.status(), response.status_text());

    let data = response.into_string()?;

    info!("Data: {:?}", data);

    std::fs::write(args.value_of("outfile").unwrap(), data.into_bytes())?;

    Ok(())
}
