use std::vec;

use ordered_float::OrderedFloat;

/// Struct for optimization iteration.
/// Iterate through the following strategies.
/// * This iterator has a main counter and a sub counter.
/// * When the main counter reaches `max_generation_num`, the iteration is terminated.
/// * When the main counter reaches `min_generation_num` and the sub counter reaches `extended_generation_num`,
///   the iteration is terminated.
/// * Start counting the sub counter from the point when violations reaches 0.
///
/// # Arguments
/// * min_generation_num - Minimum number of iterations.
/// * max_generation_num - Maximum number of iterations.
/// * extended_generation_num - Extended number of iterations.
#[derive(Clone)]
pub struct GenerationIterator {
    current_index: usize,
    extend_index: usize,
    current_scores: Option<Vec<OrderedFloat<f64>>>,
    min_generation_num: usize,
    max_generation_num: usize,
    extended_generation_num: usize,
}

impl GenerationIterator {
    pub fn new(
        min_generation_num: usize,
        max_generation_num: usize,
        extended_generation_num: usize,
    ) -> Self {
        GenerationIterator {
            current_index: 0,
            extend_index: 0,
            current_scores: None,
            min_generation_num: min_generation_num,
            max_generation_num: max_generation_num,
            extended_generation_num: extended_generation_num,
        }
    }
    pub fn set_scores(&mut self, scores: &Vec<OrderedFloat<f64>>) {
        self.current_scores = Some(scores.clone());
    }
    pub fn index(&self) -> usize {
        self.current_index
    }
    pub fn extend_index(&self) -> usize {
        self.extend_index
    }
}

impl Iterator for GenerationIterator {
    type Item = usize;

    fn next(&mut self) -> Option<Self::Item> {
        if self.current_index >= self.max_generation_num {
            return None;
        }
        if self.current_index >= self.min_generation_num
            && self.extend_index >= self.extended_generation_num
        {
            return None;
        }
        let result = self.current_index;
        let scores = self.current_scores.clone().unwrap_or(vec![]);
        if (self.current_scores.is_some()
            && scores.iter().min().unwrap_or(&OrderedFloat(0.0)) >= &OrderedFloat(0.0)
            && self.extend_index == 0)
            || self.extend_index >= 1
        {
            self.extend_index += 1;
        }
        self.current_index += 1;
        Some(result)
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_generation_iterator() {
        use super::*;
        let min_generation_num = 200;
        let max_generation_num = 300;
        let extended_generation_num = 200;
        // If the score is non-negative, the iteration terminates with min_generation_num.
        let mut gen = GenerationIterator::new(
            min_generation_num,
            max_generation_num,
            extended_generation_num,
        );
        gen.set_scores(&vec![OrderedFloat(0.0)]);
        while let Some(_i) = gen.next() {}
        assert_eq!(gen.index(), min_generation_num);

        // If a non-negative score is set during the process,
        // the iteration terminates with extended_generation_num from that point on.
        let mut gen = GenerationIterator::new(
            min_generation_num,
            max_generation_num,
            extended_generation_num,
        );
        let num_extend = 50;
        gen.set_scores(&vec![OrderedFloat(-1.0)]);
        while let Some(i) = gen.next() {
            if i == num_extend - 1 {
                gen.set_scores(&vec![OrderedFloat(1.0)]);
            }
        }
        assert_eq!(gen.index(), min_generation_num + num_extend);

        // If no score is set, the iteration terminates with max_generation_num.
        let mut gen = GenerationIterator::new(
            min_generation_num,
            max_generation_num,
            extended_generation_num,
        );
        while let Some(_i) = gen.next() {}
        assert_eq!(gen.index(), max_generation_num);
    }
}
