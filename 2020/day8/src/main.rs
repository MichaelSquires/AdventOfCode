extern crate anyhow;

#[allow(unused_imports)]
use anyhow::{anyhow, bail, ensure, Result};
#[allow(unused_imports)]
use log::{debug, error, info, trace, warn};

#[derive(Debug)]
enum Instruction {
    Acc(i32),
    Jmp(i32),
    Nop,
}

impl Instruction {
    fn new(line: &str) -> Self {
        let re = regex::Regex::new(r"(\w+) ([+-]\d+)").unwrap();
        let caps = re.captures(line).unwrap();
        match &caps[1] {
            "acc" => Instruction::Acc(caps[2].parse::<i32>().unwrap()),
            "jmp" => Instruction::Jmp(caps[2].parse::<i32>().unwrap()),
            "nop" => Instruction::Nop,
            _ => {
                panic!("Invalid instruction: {}", &caps[1])
            }
        }
    }
}

#[derive(Debug)]
struct VirtualMachine {
    pc: i32,
    seen: std::collections::HashSet<i32>,
    acc: i32,
}

impl VirtualMachine {
    fn new() -> Self {
        Self {
            pc: 0,
            seen: std::collections::HashSet::new(),
            acc: 0,
        }
    }

    fn execute(&mut self, lines: &Vec<&str>) -> Result<i32> {
        loop {
            if self.seen.contains(&self.pc) {
                break;
            }

            debug!("PC: {}", self.pc);

            self.seen.insert(self.pc);

            let ins = Instruction::new(&lines[self.pc as usize]);
            match ins {
                Instruction::Acc(v) => {
                    debug!("ACC: {}", v);
                    self.acc += v;
                    self.pc += 1
                }

                Instruction::Jmp(v) => {
                    debug!("JMP: {}", v);
                    self.pc += v
                }

                Instruction::Nop => {
                    debug!("NOP");
                    self.pc += 1
                }
            }

            if self.pc > lines.len() as i32 {
                bail!("PC out of bounds: {} >= {}", self.pc, lines.len());
            }

            if self.pc == lines.len() as i32 {
                break;
            }
        }

        Ok(self.acc)
    }
}

fn main() -> Result<()> {
    let opts = vec![clap::Arg::with_name("infile")
        .help("Input filename")
        .required(true)];

    let args = utils::init(Some(opts))?;

    let data = std::fs::read_to_string(args.value_of("infile").unwrap())?;
    let lines: Vec<&str> = data.lines().collect();

    let mut part1 = 0;
    let mut part2 = 0;

    // PART 1
    let mut vm = VirtualMachine::new();
    part1 = vm.execute(&lines)?;
    println!("PART 1: {}", part1);

    let last = data.lines().count();

    for ii in 0..last {
        let mut modified: Vec<&str> = data.lines().collect();
        let line = modified[ii];

        if !line.contains("nop") && !line.contains("jmp") {
            continue;
        }

        info!("curr: {}", ii);

        let nop = modified[ii].replace("jmp", "nop");
        let jmp = modified[ii].replace("nop", "jmp");

        if line.contains("nop") {
            debug!("nop -> jmp {}", ii);
            modified[ii] = jmp.as_str();
        }

        if line.contains("jmp") {
            debug!("jmp -> nop {}", ii);
            modified[ii] = nop.as_str();
        }

        let mut vm = VirtualMachine::new();
        match vm.execute(&modified) {
            Ok(v) => {
                part2 = v;
            }
            Err(v) => {
                error!("{}", v);
                continue;
            }
        }

        if vm.pc == last as i32 {
            break;
        }
    }

    println!("PART 2: {}", part2);

    Ok(())
}
