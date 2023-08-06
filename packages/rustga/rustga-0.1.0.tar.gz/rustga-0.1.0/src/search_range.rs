use pyo3::prelude::*;
use rand::distributions::WeightedIndex;
use rand::prelude::*;
use rand::Rng;
use std::cmp;

pub type IndividualType = Vec<IndividualElement>;
/// Enum for the different types of elements that can be in an individual.
#[derive(Clone, Debug, PartialEq)]
pub enum IndividualElement {
    Float(f64),
    String(String),
}

impl PartialOrd for IndividualElement {
    fn partial_cmp(&self, other: &Self) -> Option<cmp::Ordering> {
        match (self, other) {
            (IndividualElement::Float(f1), IndividualElement::Float(f2)) => f1.partial_cmp(f2),
            (IndividualElement::String(s1), IndividualElement::String(s2)) => s1.partial_cmp(s2),
            _ => None,
        }
    }
}

impl ToPyObject for IndividualElement {
    fn to_object(&self, py: Python) -> PyObject {
        match self {
            IndividualElement::Float(f) => f.to_object(py),
            IndividualElement::String(s) => s.to_object(py),
        }
    }
}

/// Trait dealing with search range for optimization.
pub trait SearchRange: Clone {
    fn random_pick_from_rng<R: Rng + Sized>(&self, rng: &mut R) -> IndividualElement;
    fn random_pick(&self) -> IndividualElement {
        let mut rng = rand::thread_rng();
        self.random_pick_from_rng(&mut rng)
    }
}

#[derive(Clone)]
pub struct ContinuousRange {
    pub lower: f64,
    pub upper: f64,
}

impl ContinuousRange {
    pub fn range(&self) -> f64 {
        self.upper - self.lower
    }
}

impl SearchRange for ContinuousRange {
    fn random_pick_from_rng<R: Rng + Sized>(&self, rng: &mut R) -> IndividualElement {
        IndividualElement::Float(rng.gen_range(self.lower..=self.upper))
    }
}

impl FromPyObject<'_> for ContinuousRange {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let lower = ob.get_item(0).unwrap().extract::<f64>()?;
        let upper = ob.get_item(1).unwrap().extract::<f64>()?;
        Ok(ContinuousRange { lower, upper })
    }
}

#[derive(Clone)]
pub struct SteppedRange {
    pub lower: f64,
    pub upper: f64,
    pub step: f64,
}

impl SteppedRange {
    pub fn range_length(&self) -> usize {
        ((self.upper - self.lower) / self.step).round() as usize + 1
    }
}

impl SearchRange for SteppedRange {
    fn random_pick_from_rng<R: Rng + Sized>(&self, rng: &mut R) -> IndividualElement {
        let range = ((self.upper - self.lower) / self.step).round() as u32;
        let val = rng.gen_range(0..=range);
        IndividualElement::Float(self.lower + val as f64 * self.step)
    }
}

impl FromPyObject<'_> for SteppedRange {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let lower = ob.get_item(0).unwrap().extract::<f64>()?;
        let upper = ob.get_item(1).unwrap().extract::<f64>()?;
        let step = ob.get_item(2).unwrap().extract::<f64>()?;
        Ok(SteppedRange { lower, upper, step })
    }
}

#[derive(Clone)]
pub struct MultiContinuousRange {
    pub ranges: Vec<ContinuousRange>,
}

impl SearchRange for MultiContinuousRange {
    fn random_pick_from_rng<R: Rng + Sized>(&self, rng: &mut R) -> IndividualElement {
        let weights = self.ranges.iter().map(|r| r.range()).collect::<Vec<_>>();
        let dist = WeightedIndex::new(weights).unwrap();
        self.ranges[dist.sample(rng)].random_pick_from_rng(rng)
    }
}

impl FromPyObject<'_> for MultiContinuousRange {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let ranges = ob.extract::<Vec<ContinuousRange>>()?;
        Ok(MultiContinuousRange { ranges })
    }
}

#[derive(Clone)]
pub struct MultiSteppedRange {
    pub ranges: Vec<SteppedRange>,
}

impl SearchRange for MultiSteppedRange {
    fn random_pick_from_rng<R: Rng + Sized>(&self, rng: &mut R) -> IndividualElement {
        let weights = self
            .ranges
            .iter()
            .map(|r| r.range_length())
            .collect::<Vec<_>>();
        let dist = WeightedIndex::new(weights).unwrap();
        self.ranges[dist.sample(rng)].random_pick_from_rng(rng)
    }
}

impl FromPyObject<'_> for MultiSteppedRange {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let ranges = ob.extract::<Vec<SteppedRange>>()?;
        Ok(MultiSteppedRange { ranges })
    }
}

#[derive(Clone)]
pub struct FiniteSet<T> {
    pub values: Vec<T>,
}

impl SearchRange for FiniteSet<f64> {
    fn random_pick_from_rng<R: Rng + Sized>(&self, rng: &mut R) -> IndividualElement {
        let val = rng.gen_range(0..self.values.len());
        IndividualElement::Float(self.values[val])
    }
}

impl FromPyObject<'_> for FiniteSet<f64> {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let values = ob.extract::<Vec<f64>>()?;
        Ok(FiniteSet { values })
    }
}

impl SearchRange for FiniteSet<String> {
    fn random_pick_from_rng<R: Rng + Sized>(&self, rng: &mut R) -> IndividualElement {
        let val = rng.gen_range(0..self.values.len());
        IndividualElement::String(self.values[val].clone())
    }
}

impl FromPyObject<'_> for FiniteSet<String> {
    fn extract(ob: &PyAny) -> PyResult<Self> {
        let values = ob.extract::<Vec<String>>()?;
        Ok(FiniteSet { values })
    }
}

#[derive(Clone)]
pub enum SearchRangeTypes {
    ContinuousRange(ContinuousRange),
    SteppedRange(SteppedRange),
    NumberFiniteSet(FiniteSet<f64>),
    StringFiniteSet(FiniteSet<String>),
    MultiContinuousRange(MultiContinuousRange),
    MultiSteppedRange(MultiSteppedRange),
}
