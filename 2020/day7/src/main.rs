extern crate anyhow;

#[allow(unused_imports)]
use anyhow::{anyhow, bail, ensure, Result};
#[allow(unused_imports)]
use log::{debug, error, info, trace, warn};

#[derive(Debug)]
struct Bags {
    map: std::collections::HashMap<String, Vec<String>>,
}

impl Bags {
    fn new() -> Self {
        Self {
            map: std::collections::HashMap::new(),
        }
    }

    fn create(&mut self, key: &str) {
        let key = key.to_string();
        self.map.entry(key).or_insert(Vec::new());
    }

    fn insert(&mut self, key: &str, val: &str) {
        let key = key.to_string();
        let val = val.to_string();
        self.map.entry(key).and_modify(|l| l.push(val));
    }

    fn contains_bag(&self, outer: &str, inner: &str) -> bool {
        let inner = &inner.to_string();

        if !self.map.contains_key(outer) {
            panic!("Invalid key: {}", outer);
        }

        let bag: &Vec<String> = &self.map[outer];
        bag.contains(inner) || bag.iter().any(|b| self.contains_bag(b, inner))
    }

    fn count(&self, outer: &str) -> u32 {
        let bag: &Vec<String> = &self.map[outer];

        bag.iter()
            .fold(bag.len() as u32, |acc, x| acc + self.count(x))
    }
}

fn main() -> Result<()> {
    let opts = vec![clap::Arg::with_name("infile")
        .help("Input filename")
        .required(true)];

    let args = utils::init(Some(opts))?;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;

    let mut part1 = Bags::new();
    let mut part2 = Bags::new();

    // PART 1
    let outer_re = regex::Regex::new(r"(\w+ \w+) bags contain (.*)").unwrap();
    let inner_re = regex::Regex::new(r"(?:(\d+) (\w+ \w+) bag)").unwrap();

    for outer in outer_re.captures_iter(&data) {
        let outer_bag: &str = &outer[1];
        let inner_bags: &str = &outer[2];

        part1.create(outer_bag);
        part2.create(outer_bag);

        for inner in inner_re.captures_iter(inner_bags) {
            let count = inner[1].parse::<u32>()?;
            let color = &inner[2];
            part1.insert(outer_bag, color);

            for _ii in 0..count {
                part2.insert(outer_bag, color);
            }
        }
    }

    let mut total = 0;
    for outer in outer_re.captures_iter(&data) {
        let outer_bag: &str = &outer[1];

        if part1.contains_bag(outer_bag, "shiny gold") {
            total += 1;
        }
    }

    println!("PART 1: {}", total);
    println!("PART 2: {}", part2.count("shiny gold"));

    Ok(())
}
