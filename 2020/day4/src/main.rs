extern crate anyhow;
extern crate itertools;

use anyhow::{anyhow, bail, ensure, Result};
#[allow(unused_imports)]
use log::{debug, error, info, trace, warn};

#[derive(Debug)]
struct Passport {
    dict: std::collections::HashMap<String, String>,
}

impl Passport {
    fn from_string(data: String) -> Self {
        let mut dict = std::collections::HashMap::new();

        for item in data.split(" ") {
            if item.is_empty() {
                continue;
            }

            let mut kv = item.split(":");
            let key = kv.next().unwrap().to_string();
            let val = kv.next().unwrap().to_string();

            dict.insert(key, val);
        }

        Self { dict }
    }

    fn p1_is_valid(&self) -> bool {
        itertools::all(&["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"], |&key| {
            self.dict.contains_key(key)
        })
    }

    fn byr(&self) -> Result<u32> {
        ensure!(self.dict.contains_key("byr"), "BYR not found");

        let byr = self.dict.get("byr").unwrap();
        ensure!(byr.len() == 4, "Invalid BYR: {}", byr);

        let byrval = byr.parse::<u32>()?;
        ensure!(
            byrval >= 1920 && byrval <= 2002,
            "BYR out of range: {}",
            byrval
        );

        Ok(byrval)
    }

    fn iyr(&self) -> Result<u32> {
        ensure!(self.dict.contains_key("iyr"), "IYR not found");

        let iyr = self.dict.get("iyr").unwrap();
        ensure!(iyr.len() == 4, "Invalid IYR: {}", iyr);

        let iyrval = iyr.parse::<u32>()?;
        ensure!(
            iyrval >= 2010 && iyrval <= 2020,
            "IYR out of range: {}",
            iyrval
        );

        Ok(iyrval)
    }

    fn eyr(&self) -> Result<u32> {
        ensure!(self.dict.contains_key("eyr"), "EYR not found");

        let eyr = self.dict.get("eyr").unwrap();
        ensure!(eyr.len() == 4, "Invalid EYR: {}", eyr);

        let eyrval = eyr.parse::<u32>()?;
        ensure!(
            eyrval >= 2020 && eyrval <= 2030,
            "EYR out of range: {}",
            eyrval
        );

        Ok(eyrval)
    }

    fn hgt(&self) -> Result<&String> {
        ensure!(self.dict.contains_key("hgt"), "HGT not found");

        let hgt = self.dict.get("hgt").unwrap();

        let hgtval = hgt.get(..hgt.len() - 2).unwrap().parse::<u32>()?;
        let unit = hgt.get(hgt.len() - 2..).unwrap();

        ensure!(unit == "cm" || unit == "in", "Invalid HGT: {}", hgt);

        match unit {
            "cm" => {
                ensure!(hgtval >= 150 && hgtval <= 193, "HGT out of range: {}", hgt)
            }
            "in" => {
                ensure!(hgtval >= 59 && hgtval <= 76, "HGT out of range: {}", hgt)
            }
            &_ => {
                bail!("Invalid unit: {}", unit)
            }
        }

        Ok(hgt)
    }

    fn hcl(&self) -> Result<&String> {
        ensure!(self.dict.contains_key("hcl"), "HCL not found");

        let hcl = self.dict.get("hcl").unwrap();
        ensure!(hcl.starts_with("#"), "Invalid HCL: {}", hcl);
        ensure!(
            itertools::all(hcl[1..].chars(), |l| (l >= '0' && l <= '9')
                || (l >= 'a' && l <= 'f')),
            "Invalid HCL: {}",
            hcl
        );

        Ok(hcl)
    }

    fn ecl(&self) -> Result<&String> {
        ensure!(self.dict.contains_key("ecl"), "ECL not found");

        let ecl = self.dict.get("ecl").unwrap();

        match ecl.as_str() {
            "amb" | "blu" | "brn" | "gry" | "grn" | "hzl" | "oth" => Ok(ecl),
            _ => Err(anyhow!("Invalid ECL: {}", ecl)),
        }
    }

    fn pid(&self) -> Result<u32> {
        ensure!(self.dict.contains_key("pid"), "PID not found");

        let pid = self.dict.get("pid").unwrap();
        ensure!(pid.len() == 9, "Invalid PID: {}", pid);

        let pidval = pid.parse::<u32>()?;

        Ok(pidval)
    }

    fn p2_is_valid(&self) -> Result<bool> {
        self.byr()?;
        self.iyr()?;
        self.eyr()?;
        self.hgt()?;
        self.hcl()?;
        self.ecl()?;
        self.pid()?;

        Ok(true)
    }
}

fn main() -> Result<()> {
    let opts = vec![clap::Arg::with_name("infile")
        .help("Input filename")
        .required(true)];

    let args = utils::init(Some(opts))?;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;
    let records: Vec<String> = data.split("\n\n").map(|r| r.replace("\n", " ")).collect();
    let passports: Vec<Passport> = records
        .iter()
        .map(|r| Passport::from_string(r.to_string()))
        .collect();

    debug!("PASSPORTS: {:?}", passports);

    let mut part1 = 0;
    let mut part2 = 0;

    for passport in passports.iter() {
        if passport.p1_is_valid() {
            part1 += 1;
        }

        match passport.p2_is_valid() {
            Ok(true) => {
                part2 += 1;
            }
            Ok(false) => {}
            Err(m) => {
                debug!("{}", m);
            }
        }
    }

    println!("PART 1: {}", part1);
    println!("PART 2: {}", part2);

    Ok(())
}
