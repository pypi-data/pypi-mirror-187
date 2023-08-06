use ordered_float::OrderedFloat;
use rand::Rng;

#[derive(Clone, Debug)]
pub struct Tournament {
    pub num_chosen: usize,
    pub size_tournament: usize,
}

impl Tournament {
    pub fn new(num_chosen: usize, size_tournament: usize) -> Self {
        Tournament {
            num_chosen,
            size_tournament,
        }
    }

    fn random_index<R>(rng: &mut R, length: usize) -> usize
    where
        R: Rng + Sized,
    {
        rng.gen_range(0..length)
    }

    pub fn select<R>(
        &self,
        fitness_values: &Vec<OrderedFloat<f64>>,
        rng: &mut R,
    ) -> Vec<Option<usize>>
    where
        R: Rng + Sized,
    {
        let length = fitness_values.len();
        (0..self.num_chosen)
            .map(|_| {
                (0..self.size_tournament)
                    .map(|_| Self::random_index(rng, length))
                    .max_by(|a, b| fitness_values[*a].cmp(&fitness_values[*b]))
            })
            .collect()
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_tournament() {
        use super::*;
        let selector = Tournament::new(2, 3);
        let individuals = vec![OrderedFloat(1.0), OrderedFloat(2.0), OrderedFloat(3.0)];
        let mut rng = rand::thread_rng();
        let chosen = selector.select(&individuals, &mut rng);
        assert_eq!(chosen.len(), selector.num_chosen)
    }
}
