use primes::{Sieve, TrialDivision, PrimeSet};
use std::rc::Rc;

type Z = i32;

#[derive(Clone)]
struct ZP {
    func: Rc<dyn Fn(Z) -> Z>,
}

impl ZP {
    fn from_z(n: Z) -> ZP {
        ZP { func: Rc::new(move |p:Z| n.rem_euclid(p)) }
    }

    fn at(&self, p:Z) -> Z { (self.func)(p) }
}

impl std::ops::Add for ZP {
    type Output = Self;

    fn add(self, other: Self) -> Self {
        Self {
            func: Rc::new(move |p:Z| (self.clone().at(p) + other.clone().at(p)).rem_euclid(p))
        }
    }
}

fn tiny_text(num: u32) -> String {
    const TINY_DIGITS: [char; 10] = ['\u{2080}','\u{2081}','\u{2082}','\u{2083}','\u{2084}',
                                     '\u{2085}','\u{2086}','\u{2087}','\u{2088}','\u{2089}',];
    let mut result = String::new();
    let mut digits = Vec::with_capacity(32);

    let mut num_copy = num;
    while num_copy > 0 {
        let digit;
        (digit, num_copy) = (num_copy % 10, num_copy / 10);
        digits.push(digit);
        
    }

    for digit in digits.iter().rev() {
        result.push(TINY_DIGITS[*digit as usize])
    }
    result
}

impl std::fmt::Debug for ZP {
    
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "[ ")?;
        for p in TrialDivision::new().iter().take(10) {
            write!(f, "{}{}, ", self.at(p as Z), tiny_text(p as u32))?;
        }
        write!(f, "... ]")
    }
}

fn main() {

    let mut _sieve = Sieve::new();
    
    let zp_15 = ZP::from_z(15);
    let zp_26 = ZP::from_z(26);

    println!("{:?}", zp_15);
    println!("{:?}", zp_26);
    
    let zp_sum = zp_15 + zp_26;

    println!("{:?}", zp_sum);
}
