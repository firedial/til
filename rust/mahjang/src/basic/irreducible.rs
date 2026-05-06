use super::suit::*;

pub fn is_mentsu_irreducible(suit: &Suit) -> bool {
    let removed_suit = suit.mentsu_remove();
    let original_waiting = suit.waiting();
    for s in removed_suit {
        let waiting = s.waiting();
        if original_waiting == waiting {
            return false;
        }
    }

    true
}

pub fn is_sendable_waiting_form_irreducible(suit: &Suit) -> bool {
    let removed_suit = suit.sendable_waiting_form_remove();
    let original_waiting = suit.waiting();
    for s in removed_suit {
        // 除去した後が待ち送り形であれば、除去したところに待ちがあるので追加する
        let waiting = if s.is_agari() {
            (*suit - s).waiting() + s.waiting()
        } else {
            s.waiting()
        };

        if original_waiting == waiting {
            return false;
        }
    }

    true
}

pub fn is_irreducible(suit: &Suit) -> bool {
    // 正規形であれば待ち送り形の既約を見る
    if suit.is_regular() && !suit.is_sendable_waiting_form_irreducible() {
        return false;
    }

    suit.is_mentsu_irreducible()
}

pub fn irreducible_suit(suit: &Suit) -> Vec<Suit> {
    let mut v = Vec::new();

    if !suit.waiting().is_tempai() {
        return v;
    }

    if suit.is_irreducible() {
        v.push(*suit);
        return v;
    }

    if suit.is_regular() {
        let removed_suit = suit.sendable_waiting_form_remove();
        for s in removed_suit {
            v.extend(irreducible_suit(&s));
        }
    }

    let removed_suit = suit.mentsu_remove();
    for s in removed_suit {
        v.extend(irreducible_suit(&s));
    }

    v
}
