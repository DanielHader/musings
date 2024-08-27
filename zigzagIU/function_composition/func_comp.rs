use std::env;

// there are n^n functions from a set of n elements to itself (set endomorphisms)
// this function enumerates all set endomorphisms
//   n is the size of the set
//   m is the index of the function (mod n^n)
//   x is the input (mod n)
fn endomorphism(n: u32, m: u32, x: u32) -> u32 {
    (m / n.pow(x % n)) % n
}

// determines the index of the composition of the n-set endomorphisms indexed by m1 and m2
// the composition performs m1 first then m2
fn composition(n: u32, m1: u32, m2: u32) -> u32 {

    let mut m3: u32 = 0;
    
    for y in 1..(n+1) {
	let res: u32 = endomorphism(n, m2, endomorphism(n, m1, n-y));
	m3 = m3 * n + res
    }

    return m3;
}

fn main() {

    let n: u32;
    
    let arg = env::args().nth(1);
    match arg {
	None => { println!("please provide a positive integer argument"); return; },
	Some(arg) => {
	    n = match arg.parse::<u32>() {
		Err(_) => 0,
		Ok(n) => n,
	    };
	}
    }

    if n == 0 {	println!("please provide a positive integer argument"); return; }
    
    let npn = n.pow(n);

    let width = {
	let mut d = 0;
	while 10_u32.pow(d) <= npn { d += 1; }
	d+1
    };

    print!("{:>width$} ", "", width=(width as usize));
    for m in 0..n.pow(n) {
	print!("{:>width$}", m, width=(width as usize));
    }
    println!("");
    
    for m2 in 0..n.pow(n) {
	print!("{:>width$}|", m2, width=(width as usize));
	for m1 in 0..n.pow(n) {
	    print!("{:>width$}", composition(n, m1, m2), width=(width as usize));
	}
	println!("");
    }
}
