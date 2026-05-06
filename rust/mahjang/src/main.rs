pub mod basic;
use std::collections::HashMap;

fn is_irreducible(number: usize) {
    let mut suit = basic::suit::first_suit(number);

    let mut map: HashMap<String, usize> = HashMap::new();

    loop {
        suit = suit.next_suit();

        if suit.is_valid_suit() && suit.is_basic() && suit.waiting().is_tempai() {
            // println!("{}", suit.irreducible_suit().iter().map(|x| x.basic_form().to_string()).collect::<Vec<_>>().join(", "));

            // let v = suit.irreducible_suit();
            // let mut result: Vec<_> = v.iter().map(|x| x.basic_form()).collect();
            // result.sort();
            // result.dedup();
            // let key = result.iter().map(|x| x.basic_form().to_string()).collect::<Vec<_>>().join("|");

            // *map.entry(key.clone()).or_insert(0) += 1;
            // println!("{}: {}", suit, key);

            // continue;

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

    // println!("{:?}", map);
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
