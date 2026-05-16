pub mod basic;
use std::collections::HashMap;

fn unique(number: usize, map: &mut HashMap<String, usize>, t_map: &HashMap<String, String>) {
    let mut suit = basic::suit::first_suit(number);

    loop {
        suit = suit.next_suit();

        if !suit.is_valid_suit() {
            if suit.is_first_suit() {
                break;
            };
            continue;
        }

        if !suit.waiting().is_tempai() && !suit.is_chiitoi_tempai() {
            // イーシャンテン以下
            let key = if suit.is_iishanten() || suit.is_chiitoi_iishanten() {"A1"} else {"A2"};
            *map.entry(key.to_string()).or_insert(0) += suit.combinations_number();
        } else if !suit.waiting().is_tempai() && suit.is_chiitoi_tempai() {
            // 七対子形だけで聴牌になる場合、単騎待ちとしてカウント
            *map.entry("100000000".to_string()).or_insert(0) += suit.combinations_number();
        }
        else {
            let v = suit.irreducible_suit();
            let mut result: Vec<String> = v.iter().map(|x| x.basic_form().to_string()).collect();

            // 七対子なら単騎待ちを追加
            if suit.is_chiitoi_tempai() {
                result.push("100000000".to_string());
            } else {
                if suit.agari_tile_count() == 0 {
                    // println!("no: {}", suit);
                }
            }

            result.sort();
            result.dedup();
            let key = result.join("|");

            if result.len() >= 14 {
                let mut t_parts: Vec<String> = result.iter()
                    .map(|k| t_map.get(k).cloned().unwrap_or_else(|| k.clone()))
                    .collect();
                t_parts.sort();
                let t_key = t_parts.join(",");
                // println!("{}: {}", t_key, suit);
            }
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

    unique(13, &mut map, &t_map);

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

    let total: usize = entries.iter().map(|(_, v)| v).sum();
    for (parts, value) in &entries {
        c += value;
        println!("|{}|{:?}|{:.10}|", parts.join(","), value, *value as f64 / total as f64 * 100.0);
    }

    println!("{}", c);
}
