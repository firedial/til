pub mod basic;

fn is_irreducible(suit: &basic::suit::Suit) -> bool {
    if suit.is_valid_suit() && suit.is_basic() && suit.waiting().is_tempai() {
        if suit.length() == 9 {
            if suit.is_irreducible() {
                return true;
            }
        } else if suit.length() == 8 {
            if suit.is_irreducible() || suit.one_right_slide().is_irreducible() {
                return true;
            }
        } else {
            if suit.one_right_slide().is_irreducible() {
                return true;
            }
        }
    }

    false
}


fn main() {
    let suit = basic::suit::Suit {
        suit: [0, 1, 4, 2, 1, 1, 3, 1, 0],
    };
    // println!("is agari {}", suit.is_agari());
    // println!("is tempai {}", suit.waiting().is_tempai());
    // println!("waiting {:?}", suit.waiting());

    let r = is_irreducible(&suit);
    println!("irreducible {:?}", r);

    // let mut suit2 = basic::suit::first_suit(13);
    // let mut count = 0;
    // loop {
    //     suit2 = suit2.next_suit();

    //     if suit2.is_first_suit() {
    //         break;
    //     };
    // }
    // println!("count {}", count);
}
