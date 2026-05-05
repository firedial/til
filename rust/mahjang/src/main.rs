pub mod basic;

fn is_irreducible(number: usize) -> usize {
    let mut suit = basic::suit::first_suit(number);
    let mut count = 0;

    loop {
        suit = suit.next_suit();

        if suit.is_valid_suit() && suit.is_basic() && suit.waiting().is_tempai() {
            if suit.length() == 9 {
                if suit.is_irreducible() {
                    count += 1
                }
            } else if suit.length() == 8 {
                if suit.is_irreducible() || suit.one_right_slide().is_irreducible() {
                    count += 1
                }
            } else {
                if suit.one_right_slide().is_irreducible() {
                    count += 1
                }
            }
        }

        if suit.is_first_suit() {
            break;
        };
    }

    count
}


fn main() {
    // let suit = basic::suit::Suit {
    //     suit: [0, 1, 4, 2, 1, 1, 3, 1, 0],
    // };
    // let r = suit.is_irreducible();
    // println!("irreducible {:?}", r);
    // println!("is agari {}", suit.is_agari());
    // println!("is tempai {}", suit.waiting().is_tempai());
    // println!("waiting {:?}", suit.waiting());

    for n in [1, 2, 4, 5, 7, 8, 10, 11, 13] {
        let c = is_irreducible(n);
        println!("count {}", c);
    }
}
