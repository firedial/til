use super::suit::*;

#[derive(Debug)]
struct WaitingStructure {
    is_tanki: bool,
    is_shampon: bool,
    is_kanchan: bool,
    // 34 で 5 待ちの時
    is_ryanmen_left: bool,
    // 67 で 5 待ちの時
    is_ryanmen_right: bool,
}

impl WaitingStructure {
    pub fn is_wating(&self) -> bool {
        self.is_tanki || self.is_shampon || self.is_kanchan || self.is_ryanmen_left || self.is_ryanmen_right
    }
}

#[derive(Debug)]
pub struct Waiting {
    waiting: [WaitingStructure; SUIT_LENGTH],
    is_sendable: bool,
}

impl Waiting {
    pub fn is_tempai(&self) -> bool {
        self.is_sendable || self.waiting.iter().any( |x| x.is_wating() )
    }
}

pub fn is_agari(suit: &Suit) -> bool {

    // 手牌の合計が 0 なら和了形
    if suit.sum() == 0 {
        return true;
    }

    match suit.sum() % 3 {
        1 => false, // 手牌の合計が 3n + 1 なら和了形にならない
        2 => { // 手牌の合計が 3n + 2 なら雀頭を除去する
            let removed_suit = suit.atama_remove();
            for s in removed_suit {
                return is_agari(&s);
            }
            return false;
        }
        0 => { // 手牌の合計が 3n なら面子を除去する
            let removed_suit = suit.mentsu_remove();
            for s in removed_suit {
                return is_agari(&s);
            }
            return false;
        }
        _ => unreachable!(),
    }
}

pub fn waiting(suit: &Suit) -> Waiting {
    let waiting = std::array::from_fn(|i| {
        WaitingStructure {
            is_tanki: {
                // 正規形の手牌が条件に必要
                suit.is_regular() && suit.suit[i] >= 1 && {
                    let mut removed_suit = suit.suit;
                    removed_suit[i] -= 1;
                    Suit { suit: removed_suit }.is_agari()
                }
            },
            is_shampon: {
                suit.suit[i] >= 2 && {
                    let mut removed_suit = suit.suit;
                    removed_suit[i] -= 2;
                    Suit { suit: removed_suit }.is_agari()
                }
            },
            is_kanchan: {
                i > 0 && i < SUIT_LENGTH - 1 && suit.suit[i - 1] >= 1 && suit.suit[i + 1] >= 1 && {
                    let mut removed_suit = suit.suit;
                    removed_suit[i - 1] -= 1;
                    removed_suit[i + 1] -= 1;
                    Suit { suit: removed_suit }.is_agari()
                }
            },
            is_ryanmen_left: {
                i > 1 && suit.suit[i - 1] >= 1 && suit.suit[i - 2] >= 1 && {
                    let mut removed_suit = suit.suit;
                    removed_suit[i - 1] -= 1;
                    removed_suit[i - 2] -= 1;
                    Suit { suit: removed_suit }.is_agari()
                }
            },
            is_ryanmen_right: {
                i < SUIT_LENGTH - 2 && suit.suit[i + 1] >= 1 && suit.suit[i + 2] >= 1 && {
                    let mut removed_suit = suit.suit;
                    removed_suit[i + 1] -= 1;
                    removed_suit[i + 2] -= 1;
                    Suit { suit: removed_suit }.is_agari()
                }
            },
        } }
    );

    Waiting {
        waiting: waiting,
        is_sendable: suit.is_agari(),
    }
}
