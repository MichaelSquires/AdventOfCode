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

const TREE: char = '#';

#[derive(Clone, Debug)]
struct Grid {
    grid: Vec<Vec<char>>,
}

impl Grid {
    fn new(grid: Vec<Vec<char>>) -> Self {
        Self { grid: grid }
    }

    fn rows(&self) -> usize {
        self.grid.len()
    }

    fn cols(&self) -> usize {
        self.grid[0].len()
    }

    fn tree(&self, x: usize, y: usize) -> bool {
        self.grid[y][x] == TREE
    }
}

fn check(grid: &Grid, right: usize, down: usize) -> u32 {
    let mut x: usize = 0;
    let mut y: usize = 0;

    let mut trees = 0;

    let cols = grid.cols();
    let rows = grid.rows();

    loop {
        x += right;
        y += down;

        if x >= cols {
            x -= cols;
        }

        if y >= rows {
            break;
        }

        if grid.tree(x, y) {
            trees += 1;
        }
    }

    trees
}

fn main() -> Result<()> {
    let args = init()?;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;

    let grid = Grid::new(data.lines().map(|line| line.chars().collect()).collect());

    trace!("GRID: {:?}", grid);
    debug!("ROWS {}, COLS {}", grid.rows(), grid.cols());

    let part1 = check(&grid, 3, 1);
    let part2 = check(&grid, 1, 1)
        * check(&grid, 3, 1)
        * check(&grid, 5, 1)
        * check(&grid, 7, 1)
        * check(&grid, 1, 2);

    println!("PART 1: {}", part1);
    println!("PART 2: {}", part2);

    Ok(())
}
