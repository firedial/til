pub mod basic;

fn is_irreducible(number: usize) {
    let mut suit = basic::suit::first_suit(number);

    loop {
        suit = suit.next_suit();

        if suit.is_valid_suit() && suit.is_basic() && suit.waiting().is_tempai() {
            if suit.length() == 9 {
                if suit.is_irreducible() {
                    println!("{}b", suit);
                }
            } else if suit.length() == 8 {
                if suit.is_irreducible() {
                    println!("{}l", suit);
                }
                if suit.one_right_slide().is_irreducible() {
                    println!("{}r", suit);
                }
            } else {
                if suit.is_irreducible() {
                    println!("{}l", suit);
                }
                if suit.one_right_slide().is_irreducible() {
                    println!("{}c", suit);
                }
                if suit.right_slide().is_irreducible() {
                    println!("{}r", suit);
                }
            }
        }

        if suit.is_first_suit() {
            break;
        };
    }
}


fn main() {
    // let suit = basic::suit::Suit {
    //     suit: [0, 1, 4, 2, 1, 1, 0, 0, 0],
    // };
    // println!("right {:?}", suit.right_slide());

    // let r = suit.is_irreducible();
    // println!("irreducible {:?}", r);
    // println!("is agari {}", suit.is_agari());
    // println!("is tempai {}", suit.waiting().is_tempai());
    // println!("waiting {:?}", suit.waiting());

    for n in [1, 2, 4, 5, 7, 8, 10, 11, 13] {
        is_irreducible(n);
    }
}
