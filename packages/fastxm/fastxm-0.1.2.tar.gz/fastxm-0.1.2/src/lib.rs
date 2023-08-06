use numpy::{IntoPyArray, PyArray1, PyReadonlyArray1};
use pyo3::prelude::*;
use pyo3::{wrap_pyfunction, PyResult, Python};
use rayon::prelude::*;

pub fn argsort<T>(arr: &[T]) -> Vec<usize>
where
    T: Ord,
{
    let mut indices: Vec<usize> = (0..arr.len()).collect();
    indices.sort_unstable_by_key(|&index| &arr[index]);
    indices
}

#[pyfunction]
pub fn i1d<'py>(
    py: Python<'py>,
    a: PyReadonlyArray1<u64>,
    b: PyReadonlyArray1<u64>,
) -> PyResult<(&'py PyArray1<usize>, &'py PyArray1<usize>)> {
    let (a, b) = if a.len() < b.len() { (b, a) } else { (a, b) };
    let a = a.as_slice()?;
    let b = b.as_slice()?;
    let indices = argsort(a);
    let sorted_a = indices.iter().map(|&i| a[i]).collect::<Vec<_>>();
    let (a_ix, b_ix): (Vec<usize>, Vec<usize>) = b
        .iter()
        .enumerate()
        .filter_map(|(i, b_i)| {
            let index = sorted_a.binary_search(&b_i);
            if let Ok(index) = index {
                Some((indices[index], i))
            } else {
                None
            }
        })
        .unzip();

    Ok((a_ix.into_pyarray(py), b_ix.into_pyarray(py)))
}

macro_rules! make_i1d_implementation {
    ($($n:ident, $t:expr),+) => {
        $(
            #[pyfunction]
            pub fn $n<'py>(
                py: Python<'py>,
                a: PyReadonlyArray1<$t>,
                b: PyReadonlyArray1<$t>,
            ) -> PyResult<(&'py PyArray1<usize>, &'py PyArray1<usize>)> {
                let (a, b) = if a.len() < b.len() { (b, a) } else { (a, b) };
                let a = a.as_slice()?;
                let b = b.as_slice()?;
                let indices = argsort(a);
                let sorted_a = indices.iter().map(|&i| a[i]).collect::<Vec<_>>();
                let (a_ix, b_ix): (Vec<usize>, Vec<usize>) = b
                    .iter()
                    .enumerate()
                    .filter_map(|(i, b_i)| {
                        let index = sorted_a.binary_search(&b_i);
                        if let Ok(index) = index {
                            Some((indices[index], i))
                        } else {
                            None
                        }
                    })
                    .unzip();

                Ok((a_ix.into_pyarray(py), b_ix.into_pyarray(py)))
            }
        )+
    };
}

macro_rules! make_par_i1d_implementation {
    ($($n:ident, $t:expr),+) => {
        $(
            #[pyfunction]
            pub fn $n<'py>(
                py: Python<'py>,
                a: PyReadonlyArray1<$t>,
                b: PyReadonlyArray1<$t>,
            ) -> PyResult<(&'py PyArray1<usize>, &'py PyArray1<usize>)> {
                let (a, b) = if a.len() < b.len() { (b, a) } else { (a, b) };
                let a = a.as_slice()?;
                let b = b.as_slice()?;
                let indices = argsort(a);
                let sorted_a = indices.par_iter().map(|&i| a[i]).collect::<Vec<_>>();
                let (a_ix, b_ix): (Vec<usize>, Vec<usize>) = b
                    .par_iter()
                    .enumerate()
                    .filter_map(|(i, b_i)| {
                        let index = sorted_a.binary_search(&b_i);
                        if let Ok(index) = index {
                            Some((indices[index], i))
                        } else {
                            None
                        }
                    })
                    .unzip();

                Ok((a_ix.into_pyarray(py), b_ix.into_pyarray(py)))
            }
        )+
    };
}

make_i1d_implementation!(
    i1d_i8, i8, i1d_i16, i16, i1d_i32, i32, i1d_i64, i64, i1d_u8, u8, i1d_u16, u16, i1d_u32, u32,
    i1d_u64, u64, i1d_isize, isize, i1d_usize, usize
);
make_par_i1d_implementation!(
    par_i1d_i8,
    i8,
    par_i1d_i16,
    i16,
    par_i1d_i32,
    i32,
    par_i1d_i64,
    i64,
    par_i1d_u8,
    u8,
    par_i1d_u16,
    u16,
    par_i1d_u32,
    u32,
    par_i1d_u64,
    u64,
    par_i1d_isize,
    isize,
    par_i1d_usize,
    usize
);

#[pymodule]
fn fastxm(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(i1d_i8, m)?)?;
    m.add_function(wrap_pyfunction!(i1d_i16, m)?)?;
    m.add_function(wrap_pyfunction!(i1d_i32, m)?)?;
    m.add_function(wrap_pyfunction!(i1d_i64, m)?)?;
    m.add_function(wrap_pyfunction!(i1d_u8, m)?)?;
    m.add_function(wrap_pyfunction!(i1d_u16, m)?)?;
    m.add_function(wrap_pyfunction!(i1d_u32, m)?)?;
    m.add_function(wrap_pyfunction!(i1d_u64, m)?)?;
    m.add_function(wrap_pyfunction!(i1d_isize, m)?)?;
    m.add_function(wrap_pyfunction!(i1d_usize, m)?)?;
    m.add_function(wrap_pyfunction!(par_i1d_i8, m)?)?;
    m.add_function(wrap_pyfunction!(par_i1d_i16, m)?)?;
    m.add_function(wrap_pyfunction!(par_i1d_i32, m)?)?;
    m.add_function(wrap_pyfunction!(par_i1d_i64, m)?)?;
    m.add_function(wrap_pyfunction!(par_i1d_u8, m)?)?;
    m.add_function(wrap_pyfunction!(par_i1d_u16, m)?)?;
    m.add_function(wrap_pyfunction!(par_i1d_u32, m)?)?;
    m.add_function(wrap_pyfunction!(par_i1d_u64, m)?)?;
    m.add_function(wrap_pyfunction!(par_i1d_isize, m)?)?;
    m.add_function(wrap_pyfunction!(par_i1d_usize, m)?)?;
    Ok(())
}
