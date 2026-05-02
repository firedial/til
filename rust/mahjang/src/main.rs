pub mod basic;

fn main() {
    let suit = basic::suit::Suit {
        suit: [1, 1, 0, 0, 2, 0, 0, 0, 0],
    };
    println!("is agari {}", suit.is_agari());
    println!("is tempai {}", suit.waiting().is_tempai());
    println!("waiting {:?}", suit.waiting());

    let mut suit2 = basic::suit::first_suit(4);
    while true {
        suit2 = suit2.next_suit();
        println!("suit {:?}", suit2.suit);
        if suit2.is_first_suit() {
            break;
        };
    }
}
