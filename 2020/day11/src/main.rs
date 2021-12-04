extern crate anyhow;

#[allow(unused_imports)]
use anyhow::{anyhow, bail, ensure, Result};
#[allow(unused_imports)]
use log::{debug, error, info, trace, warn};

use std::char::CharTryFromError;
use std::convert::TryFrom;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Seat {
    Empty,
    Occup,
    Floor,
}

impl std::fmt::Display for Seat {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Empty => write!(f, "L"),
            Self::Occup => write!(f, "#"),
            Self::Floor => write!(f, "."),
        }
    }
}

impl TryFrom<char> for Seat {
    type Error = CharTryFromError;

    fn try_from(c: char) -> Result<Self, Self::Error> {
        match c {
            'L' => Ok(Seat::Empty),
            '#' => Ok(Seat::Occup),
            '.' => Ok(Seat::Floor),
            _ => { panic!("Invalid char: {}", c); }
        }
    }
}

#[derive(Debug, Eq, PartialEq)]
struct Grid {
    grid: Vec<Vec<Seat>>,
    prev: Vec<Vec<Seat>>,
}

impl std::fmt::Display for Grid {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let rows = self.grid.len();
        let cols = self.grid[0].len();

        for row in 1 .. rows - 1 {
            for col in 1 .. cols - 1 {
                write!(f, "{}", self.grid[row][col])?;
            }
            write!(f, "\n")?;
        }
        Ok(())
    }
}

impl Grid {
    fn new(data: &str) -> Self {
        // Create a grid out of the input data
        let grid: Vec<Vec<Seat>> = data.lines().map(|line| line.chars().map(|c| Seat::try_from(c).unwrap()).collect()).collect();

        let rows = grid.len();
        let cols = grid[0].len();

        // Create two empty grids that are slightly larger than the input grid. The extra rows/cols
        // are so we can have a buffer space around the input grid and not have to worry about
        // border collisions.
        let mut curr: Vec<Vec<Seat>> = vec![vec![Seat::Floor; cols + 2]; rows + 2];

        for row in 0 .. rows {
            for col in 0 .. cols {
                curr[row+1][col+1] = grid[row][col];
            }
        }

        Self { grid: curr, prev: grid.clone() }
    }

    fn get(&self, x: usize, y: usize) -> Seat {
        self.grid[x][y]
    }

    fn adjacent1(&self, row: usize, col: usize) -> u32 {
        let mut neighbors = 0;

        // Check all adjacent positions
        for xx in 0..=2 {
            for yy in 0..=2 {
                if xx == 1 && yy == 1 {
                    continue;
                }
                if self.prev[row + xx - 1][col + yy - 1] == Seat::Occup {
                    neighbors += 1;
                }
            }
        }
        neighbors
    }

    fn step1(&mut self) -> bool {

        let rows = self.grid.len();
        let cols = self.grid[0].len();

        self.prev = self.grid.clone();

        let mut changed = false;

        debug!("rows {}, cols {}", rows, cols);

        for row in 1 .. rows {
            for col in 1 .. cols {
                let seat = self.prev[row][col];

                // No seat here, go around
                if seat == Seat::Floor {
                    continue;
                }

                let neighbors = self.adjacent1(row, col);

                if neighbors == 0 && seat == Seat::Empty {
                    debug!("{}x{} {:?} -> {:?}", row, col, self.grid[row][col], Seat::Occup);
                    self.grid[row][col] = Seat::Occup;
                    changed = true;
                }

                if neighbors >= 4 && seat == Seat::Occup {
                    debug!("{}x{} {:?} -> {:?}", row, col, self.grid[row][col], Seat::Empty);
                    self.grid[row][col] = Seat::Empty;
                    changed = true;
                }
            }
        }

        debug!("changed: {}", changed);
        changed
    }

    fn adjacent2(&self, row: usize, col: usize) -> u32 {
        let rows = self.grid.len();
        let cols = self.grid[0].len();

        let mut neighbors = 0;

        // Check all adjacent positions
        for xx in 0..=2 {
            for yy in 0..=2 {
                if xx == 1 && yy == 1 {
                    continue;
                }
                if self.prev[row + xx - 1][col + yy - 1] == Seat::Occup {
                    neighbors += 1;
                }
            }
        }


        neighbors
    }

    fn step2(&mut self) -> bool {

        let rows = self.grid.len();
        let cols = self.grid[0].len();

        self.prev = self.grid.clone();

        let mut changed = false;

        debug!("rows {}, cols {}", rows, cols);

        for row in 1 .. rows {
            for col in 1 .. cols {
                let seat = self.prev[row][col];

                // No seat here, go around
                if seat == Seat::Floor {
                    continue;
                }

                let neighbors = self.adjacent2(row, col);

                if neighbors == 0 && seat == Seat::Empty {
                    debug!("{}x{} {:?} -> {:?}", row, col, self.grid[row][col], Seat::Occup);
                    self.grid[row][col] = Seat::Occup;
                    changed = true;
                }

                if neighbors >= 5 && seat == Seat::Occup {
                    debug!("{}x{} {:?} -> {:?}", row, col, self.grid[row][col], Seat::Empty);
                    self.grid[row][col] = Seat::Empty;
                    changed = true;
                }
            }
        }

        debug!("changed: {}", changed);
        changed
    }

    fn occupied(&self) -> u32 {
        let mut occupied = 0;

        let rows = self.grid.len();
        let cols = self.grid[0].len();

        for row in 1 .. rows {
            for col in 1 .. cols {
                let seat = self.grid[row][col];

                if seat == Seat::Occup {
                    occupied += 1;
                }
            }
        }

        occupied
    }
}

fn main() -> Result<()> {
    let opts = vec![clap::Arg::with_name("infile")
        .help("Input filename")
        .required(true)];

    let args = utils::init(Some(opts))?;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;

    // PART 1
    let mut grid = Grid::new(&data);
    while grid.step1() {}
    println!("PART 1: {}", grid.occupied());

    // PART 2
    let mut grid = Grid::new(&data);
    while grid.step2() {}
    println!("PART 2: {}", grid.occupied());

    Ok(())
}
