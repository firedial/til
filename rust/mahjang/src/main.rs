pub mod basic;

fn main() {
    let suit = basic::suit::Suit {
        suit: [1, 1, 0, 0, 2, 0, 0, 0, 0],
    };
    println!("is agari {}", suit.is_agari());
    println!("is tempai {}", suit.waiting().is_tempai());
    println!("waiting {:?}", suit.waiting());
}
