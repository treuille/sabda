fn main() {
    println!("Hello, world! (From rust compiled directly to MacOS!)");

    let sum_to: u64 = 1_000_000;
    let mut sum: u64 = 0;
    for i in 0..sum_to {
        sum += i;
    }

    println!("The sum to {} is {}", sum_to, sum);
}
