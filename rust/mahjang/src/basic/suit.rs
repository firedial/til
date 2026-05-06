use super::agari;
use std::fmt;
use crate::basic::agari::Waiting;
use std::ops::{Sub};
use super::remove;
use super::irreducible;

pub const SUIT_LENGTH: usize = 9;
pub const TILE_COUNT: usize = 4;

#[derive(Debug, Copy, Clone)]
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

    pub fn is_valid_suit(&self) -> bool {
        self.suit.iter().all( |x| *x <= TILE_COUNT )
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

    pub fn sendable_waiting_form_remove(&self) -> Vec<Self> {
        remove::sendable_waiting_form_remove(self)
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

    fn reverse(&self) -> Suit {
        Suit { suit: std::array::from_fn(|i| self.suit[SUIT_LENGTH - 1 - i])}
    }

    fn left_index(&self) -> usize {
        for i in 0 .. SUIT_LENGTH {
            if self.suit[i] != 0 {
                return i;
            }
        }

        unreachable!();
    }

    fn right_index(&self) -> usize {
        SUIT_LENGTH - self.reverse().left_index() - 1
    }

    pub fn length(&self) -> usize {
        self.right_index() - self.left_index() + 1
    }

    pub fn one_right_slide(&self) -> Suit {
        let mut new_suit = self.suit;
        new_suit[0] = 0;

        for index in 1 .. SUIT_LENGTH {
            new_suit[index] = self.suit[index - 1];
        }

        Suit { suit: new_suit }
    }

    pub fn right_slide(&self) -> Suit {
        let mut new_suit = self.suit;
        let length = self.length();

        for index in 0 .. SUIT_LENGTH {
            new_suit[index] = if index < SUIT_LENGTH - length { 0 } else {self.suit[index - (SUIT_LENGTH - length)]}
        }

        Suit { suit: new_suit }
    }

    fn gravity(&self) -> isize {
        let mut diff = 0;
        let left_index = self.left_index();
        let right_index = self.right_index();

        loop {
            // 左右対称形
            if left_index + diff >= right_index - diff {
                return 0;
            }

            // 左重心
            if self.suit[left_index + diff] > self.suit[right_index - diff] {
                return 1;
            }

            // 右重心
            if self.suit[left_index + diff] < self.suit[right_index - diff] {
                return -1;
            }

            diff += 1;
        }
    }

    pub fn is_basic(&self) -> bool {
        // 左接地で左重心であれば基本形
        self.left_index() == 0 && self.gravity() >= 0
    }

    pub fn is_mentsu_irreducible(&self) -> bool {
        irreducible::is_mentsu_irreducible(self)
    }

    pub fn is_sendable_waiting_form_irreducible(&self) -> bool {
        irreducible::is_sendable_waiting_form_irreducible(self)
    }

    pub fn is_irreducible(&self) -> bool {
        irreducible::is_irreducible(self)
    }
}

impl Sub for Suit {
    type Output = Suit;

    fn sub(self, other: Suit) -> Suit {
        Suit {
            suit: std::array::from_fn(|i| self.suit[i] - other.suit[i])
        }
    }
}

impl fmt::Display for Suit {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self.suit.iter().map( |x| x.to_string() ).collect::<String>())
    }
}

pub fn first_suit(count: usize) -> Suit {
    let mut suit = [0; SUIT_LENGTH];
    suit[SUIT_LENGTH - 1] = count;
    Suit { suit: suit }
}
