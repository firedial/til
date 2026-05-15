pub mod basic;
use std::collections::HashMap;

fn unique(number: usize, map: &mut HashMap<String, usize>) {
    let mut suit = basic::suit::first_suit(number);

    loop {
        suit = suit.next_suit();

        if !suit.is_valid_suit() {
            if suit.is_first_suit() {
                break;
            };
            continue;
        }

        if !suit.waiting().is_tempai() {
            let key = if suit.is_iishanten() {"A1"} else {"A2"};
            *map.entry(key.to_string()).or_insert(0) += suit.combinations_number();
        } else {
            let v = suit.irreducible_suit();
            let mut result: Vec<_> = v.iter().map(|x| x.basic_form()).collect();
            result.sort();
            result.dedup();
            let key = result.iter().map(|x| x.basic_form().to_string()).collect::<Vec<_>>().join("|");

            *map.entry(key.clone()).or_insert(0) += suit.combinations_number();
        }

        if suit.is_first_suit() {
            break;
        };
    }
}

fn is_irreducible(number: usize) -> Vec<String> {
    let mut suit = basic::suit::first_suit(number);
    let mut results: Vec<String> = Vec::new();

    loop {
        suit = suit.next_suit();

        if suit.is_valid_suit() && suit.is_basic() && suit.waiting().is_tempai() {
            if suit.length() == 9 {
                if suit.is_irreducible() {
                    results.push(suit.to_string());
                }
            } else if suit.length() == 8 {
                if suit.is_irreducible() || suit.one_right_slide().is_irreducible() {
                    results.push(suit.to_string());
                }
            } else {
                if suit.one_right_slide().is_irreducible() {
                    results.push(suit.to_string());
                }
            }
        }

        if suit.is_first_suit() {
            break;
        };
    }

    results
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

    let mut map: HashMap<String, usize> = HashMap::new();
    let mut t_map: HashMap<String, String> = HashMap::new();
    let mut counter = 1;
    for n in [1, 2, 4, 5, 7, 8, 10, 11, 13] {
        let mut results = is_irreducible(n);
        results.sort();
        for s in &results {
            let t = format!("T{:03}", counter);
            // println!("{}: {}", t, s);
            t_map.insert(s.clone(), t);
            counter += 1;
        }
    }

    unique(13, &mut map);

    let mut c = 0;
    let mut entries: Vec<(Vec<String>, usize)> = map.iter().map(|(key, &value)| {
        let mut t_parts: Vec<String> = key.split('|')
            .map(|k| t_map.get(k).cloned().unwrap_or_else(|| k.to_string()))
            .collect();
        t_parts.sort();
        (t_parts, value)
    }).collect();

    entries.sort_by_key(|(parts, _)| {
        let mut sorted = parts.clone();
        sorted.sort();
        (parts.len(), sorted)
    });

    for (parts, value) in &entries {
        c += value;
        println!("|{}|{:?}|", parts.join(","), value);
    }

    println!("{}", c);
}
