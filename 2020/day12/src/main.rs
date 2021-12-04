extern crate anyhow;
extern crate regex;

#[allow(unused_imports)]
use anyhow::{anyhow, bail, ensure, Result};
#[allow(unused_imports)]
use log::{debug, error, info, trace, warn};


#[derive(Debug)]
enum Direction {
    North,
    East,
    South,
    West,
}

impl Direction {
    fn turn(&self, degrees: i32) -> Direction {
        let turn = degrees / 90;

        let direction = match (self, turn) {
            (Self::North, 2) | (Self::East, 1) | (Self::West, 3) => Self::South,
            (Self::North, 3) | (Self::East, 2) | (Self::South, 1) => Self::West,
            (Self::East, 3) | (Self::South, 2) | (Self::West, 1) => Self::North,
            (Self::North, 1) | (Self::South, 3) | (Self::West, 2) => Self::East,

            (Self::North, -2) | (Self::East, -3) | (Self::West, -1) => Self::South,
            (Self::North, -1) | (Self::East, -2) | (Self::South, -3) => Self::West,
            (Self::East, -1) | (Self::South, -2) | (Self::West, -3) => Self::North,
            (Self::North, -3) | (Self::South, -1) | (Self::West, -2) => Self::East,

            _ => { panic!("Invalid values: {:?} {}", self, degrees); }
        };

        debug!("{:?} + {} ({}) = {:?}", self, degrees, turn, direction);

        direction
    }
}

#[derive(Debug)]
enum Action {
    North,
    South,
    East,
    West,
    Left,
    Right,
    Forward,
}


#[derive(Debug)]
struct Navigation {
    direction: Direction,

    x: i32,
    y: i32,
}

impl Navigation {
    fn new() -> Self {
        Self { direction: Direction::East, x: 0, y: 0 }
    }

    fn step(&mut self, action: Action, value: i32) {

        match action {
            Action::Left => { self.direction = self.direction.turn(-value); }
            Action::Right => { self.direction = self.direction.turn(value); }

            Action::North => { self.y += value; }
            Action::South => { self.y -= value; }
            Action::East => { self.x += value; }
            Action::West => { self.x -= value; }

            Action::Forward => {
                match self.direction {
                    Direction::North => { self.y += value; }
                    Direction::South => { self.y -= value; }
                    Direction::East => { self.x += value; }
                    Direction::West => { self.x -= value; }
                }
            }
        };

        debug!("Action {:?}, value {}, x {}, y {}", action, value, self.x, self.y);
    }

    fn distance(&self) -> i32 {
        self.x.abs() + self.y.abs()
    }
}

fn main() -> Result<()> {
    let opts = vec![clap::Arg::with_name("infile")
        .help("Input filename")
        .required(true)];

    let args = utils::init(Some(opts))?;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;

    let mut nav = Navigation::new();

    let re = regex::Regex::new(r"([NSEWLRF])(\d+)").unwrap();
    for cap in re.captures_iter(&data) {
        let value = cap[2].parse::<i32>()?;

        let action = match &cap[1] {
            "N" => Action::North,
            "S" => Action::South,
            "E" => Action::East,
            "W" => Action::West,
            "L" => Action::Left,
            "R" => Action::Right,
            "F" => Action::Forward,
            _ => { panic!("Invalid direction: {}", &cap[1]); }
        };

        nav.step(action, value);
    }

    // PART 1
    let mut part1 = nav.distance();
    println!("PART 1: {}", part1);

    // PART 2
    let mut part2 = 0;
    println!("PART 2: {}", part2);

    Ok(())
}
