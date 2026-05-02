use super::agari;
use crate::basic::agari::Waiting;
use super::remove;

pub const SUIT_LENGTH: usize = 9;

#[derive(Debug)]
pub struct Suit {
    pub suit: [usize; SUIT_LENGTH],
}

impl Suit {
    pub fn sum(&self) -> usize {
        let mut sum = 0;
        for s in self.suit{
            sum += s;
        }
        return sum;
    }

    pub fn is_regular(&self) -> bool {
        self.sum() % 3 == 1
    }

    pub fn is_agari(&self) -> bool {
        agari::is_agari(self)
    }

    pub fn waiting(&self) -> Waiting {
        agari::waiting(self)
    }

    pub fn mentsu_remove(&self) -> Vec<Self> {
        remove::mentsu_remove(self)
    }

    pub fn atama_remove(&self) -> Vec<Self> {
        remove::atama_remove(self)
    }

    pub fn next_suit(&self) -> Suit {
        // 先頭以降に0でないものを見つける
        for index in 1..SUIT_LENGTH {
            if self.suit[index] != 0 {
                let mut new_suit = self.suit;
                new_suit[0] = 0;
                new_suit[index - 1] = self.suit[0] + 1;
                new_suit[index] -= 1;
                return Suit { suit: new_suit };
            }
        }

        // 見つけられなかった場合は最初の手牌を返す
        return first_suit(self.sum());
    }

    pub fn is_first_suit(&self) -> bool {
        first_suit(self.sum()).suit == self.suit
    }
}

pub fn first_suit(count: usize) -> Suit {
    let mut suit = [0; SUIT_LENGTH];
    suit[SUIT_LENGTH - 1] = count;
    Suit { suit: suit }
}
