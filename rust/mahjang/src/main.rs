pub mod basic;

fn main() {
    let suit = basic::suit::Suit {
        suit: [1, 1, 0, 0, 2, 0, 0, 0, 0],
    };
    println!("is agari {}", suit.is_agari());
    println!("is tempai {}", suit.waiting().is_tempai());
    println!("waiting {:?}", suit.waiting());

    let mut suit2 = basic::suit::first_suit(13);
    let mut count = 0;
    let mut tempai_count = 0;
    loop {
        suit2 = suit2.next_suit();
        if suit2.is_valid_suit() {
            count += 1;
            if suit2.waiting().is_tempai() {
                tempai_count += 1;
            }
        }

        if suit2.is_first_suit() {
            break;
        };
    }
    println!("count {}", count);
    println!("tempai count {}", tempai_count);
}
