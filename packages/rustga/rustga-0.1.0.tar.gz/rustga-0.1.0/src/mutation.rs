use crate::search_range::*;
use rand::Rng;

/// Two pointers crossover algorithms for children DNA sequences.
#[derive(Clone, Copy)]
pub struct RandomMutation {
    pub point_mutation_pb: f64,
}

impl RandomMutation {
    pub fn new(point_mutation_pb: f64) -> Self {
        RandomMutation { point_mutation_pb }
    }

    fn random_pick(search_range: &SearchRangeTypes) -> IndividualElement {
        match search_range {
            SearchRangeTypes::ContinuousRange(cr) => cr.random_pick(),
            SearchRangeTypes::SteppedRange(sr) => sr.random_pick(),
            SearchRangeTypes::NumberFiniteSet(nf) => nf.random_pick(),
            SearchRangeTypes::StringFiniteSet(sf) => sf.random_pick(),
            SearchRangeTypes::MultiContinuousRange(mcr) => mcr.random_pick(),
            SearchRangeTypes::MultiSteppedRange(msr) => msr.random_pick(),
        }
    }

    pub fn mutate<R>(
        self,
        individual: &IndividualType,
        search_range: &Vec<SearchRangeTypes>,
        rng: &mut R,
    ) -> IndividualType
    where
        R: Rng + Sized,
    {
        individual
            .iter()
            .zip(search_range.iter())
            .map(|(x, y)| {
                if rng.gen_range(0.0..1.0) <= self.point_mutation_pb {
                    Self::random_pick(y)
                } else {
                    x.clone()
                }
            })
            .collect::<Vec<_>>()
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_mutation() {
        use super::*;
        let mutation_operator = RandomMutation::new(1.0);
        let individual = vec![
            IndividualElement::Float(1.0),
            IndividualElement::String(String::from("a")),
            IndividualElement::Float(3.0),
        ];
        let search_range: Vec<SearchRangeTypes> = vec![
            SearchRangeTypes::ContinuousRange(ContinuousRange {
                lower: 0.0,
                upper: 10.0,
            }),
            SearchRangeTypes::StringFiniteSet(FiniteSet {
                values: vec![String::from("a"), String::from("b")],
            }),
            SearchRangeTypes::ContinuousRange(ContinuousRange {
                lower: 0.0,
                upper: 10.0,
            }),
        ];
        let mut rng = rand::thread_rng();
        let mutated = mutation_operator.mutate(&individual, &search_range, &mut rng);
        assert_eq!(mutated.len(), individual.len());
        assert_ne!(mutated, individual);
    }
    #[test]
    fn test_no_mutation() {
        use super::*;
        let mutation_operator = RandomMutation::new(0.0);
        let individual = vec![
            IndividualElement::Float(1.0),
            IndividualElement::String(String::from("a")),
            IndividualElement::Float(3.0),
        ];
        let search_range: Vec<SearchRangeTypes> = vec![
            SearchRangeTypes::ContinuousRange(ContinuousRange {
                lower: 0.0,
                upper: 10.0,
            }),
            SearchRangeTypes::StringFiniteSet(FiniteSet {
                values: vec![String::from("a"), String::from("b")],
            }),
            SearchRangeTypes::ContinuousRange(ContinuousRange {
                lower: 0.0,
                upper: 10.0,
            }),
        ];
        let mut rng = rand::thread_rng();
        let mutated = mutation_operator.mutate(&individual, &search_range, &mut rng);
        assert_eq!(mutated.len(), individual.len());
        assert_eq!(mutated, individual);
    }
}
