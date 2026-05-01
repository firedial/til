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
}
