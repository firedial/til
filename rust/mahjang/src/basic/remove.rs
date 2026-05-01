use super::suit::*;

pub fn shuntsu_remove(suit: &Suit) -> Vec<Suit> {
    let mut v = Vec::with_capacity(SUIT_LENGTH);

    for i in 0 .. SUIT_LENGTH - 2 {
        if suit.suit[i] >= 1 && suit.suit[i + 1] >= 1 && suit.suit[i + 2] >= 1 {
            let mut removed_suit = suit.suit;
            removed_suit[i] -= 1;
            removed_suit[i + 1] -= 1;
            removed_suit[i + 2] -= 1;
            v.push(Suit { suit: removed_suit } );
        }
    }
    v
}

pub fn kotsu_remove(suit: &Suit) -> Vec<Suit> {
    let mut v = Vec::with_capacity(SUIT_LENGTH);

    for i in 0 .. SUIT_LENGTH {
        if suit.suit[i] >= 3 {
            let mut removed_suit = suit.suit;
            removed_suit[i] -= 3;
            v.push(Suit { suit: removed_suit } );
        }
    }
    v
}

pub fn mentsu_remove(suit: &Suit) -> Vec<Suit> {
    let mut result = shuntsu_remove(suit);
    result.extend(kotsu_remove(suit));
    result
}

pub fn atama_remove(suit: &Suit) -> Vec<Suit> {
    let mut v = Vec::with_capacity(SUIT_LENGTH);

    for i in 0 .. SUIT_LENGTH {
        if suit.suit[i] >= 2 {
            let mut removed_suit = suit.suit;
            removed_suit[i] -= 2;
            v.push(Suit { suit: removed_suit } );
        }
    }
    v
}
