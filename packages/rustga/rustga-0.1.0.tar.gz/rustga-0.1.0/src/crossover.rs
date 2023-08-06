use crate::search_range::*;
use rand::Rng;
use std::cmp;

/// Two pointers crossover algorithms for children DNA sequences.
#[derive(Clone, Copy)]
pub struct TwoPointCrossOver {
    pub crossover_pb: f64,
}

impl TwoPointCrossOver {
    pub fn new(crossover_pb: f64) -> Self {
        TwoPointCrossOver { crossover_pb }
    }

    pub fn crossover<R>(
        self,
        child1: &IndividualType,
        child2: &IndividualType,
        rng: &mut R,
    ) -> (IndividualType, IndividualType)
    where
        R: Rng + Sized,
    {
        if rng.gen_range(0.0..1.0) < self.crossover_pb {
            let size: usize = cmp::min(child1.len(), child2.len());
            let mut cxp1 = rng.gen_range(0..size);
            let mut cxp2 = rng.gen_range(0..size - 1);
            if cxp2 >= cxp1 {
                cxp2 = cxp2 + 1;
            } else {
                (cxp1, cxp2) = (cxp2, cxp1);
            }
            let mut crossed_1: IndividualType = child1.clone();
            let mut crossed_2: IndividualType = child2.clone();
            crossed_1[cxp1..cxp2].clone_from_slice(&child2[cxp1..cxp2]);
            crossed_2[cxp1..cxp2].clone_from_slice(&child1[cxp1..cxp2]);
            (crossed_1, crossed_2)
        } else {
            (child1.clone(), child2.clone())
        }
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_crossover() {
        use super::*;
        let crossover_operator = TwoPointCrossOver::new(1.0);
        let child1 = vec![
            IndividualElement::Float(1.0),
            IndividualElement::Float(2.0),
            IndividualElement::Float(3.0),
        ];
        let child2 = vec![
            IndividualElement::Float(10.0),
            IndividualElement::Float(20.0),
            IndividualElement::Float(30.0),
            IndividualElement::Float(40.0),
        ];
        let mut rng = rand::thread_rng();
        let (crossed_1, crossed_2) = crossover_operator.crossover(&child1, &child2, &mut rng);
        assert_eq!(crossed_1.len(), child1.len());
        assert_eq!(crossed_2.len(), child2.len());
        assert_ne!(crossed_1, child1);
        assert_ne!(crossed_2, child2);
    }
    #[test]
    fn test_no_crossover() {
        use super::*;
        let crossover_operator = TwoPointCrossOver::new(0.0);
        let child1 = vec![
            IndividualElement::Float(1.0),
            IndividualElement::Float(2.0),
            IndividualElement::Float(3.0),
        ];
        let child2 = vec![
            IndividualElement::Float(10.0),
            IndividualElement::Float(20.0),
            IndividualElement::Float(30.0),
            IndividualElement::Float(40.0),
        ];
        let mut rng = rand::thread_rng();
        let (crossed_1, crossed_2) = crossover_operator.crossover(&child1, &child2, &mut rng);
        assert_eq!(crossed_1.len(), child1.len());
        assert_eq!(crossed_2.len(), child2.len());
        assert_eq!(crossed_1, child1);
        assert_eq!(crossed_2, child2);
    }
}
