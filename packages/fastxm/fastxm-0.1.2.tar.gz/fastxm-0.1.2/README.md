# fastxm

For cross-matching astronomical catalogs. Like `np.intersect1d` but faster. 

### Installation

```bash
pip install fastxm
```

### Example usage

```python
from fastxm import intersect_1d

catalog_1 = ...
catalog_2 = ...

match_ix_1, match_ix_2 = intersect_1d(catalog_1['common_id'], catalog_2['common_id'], parallel=True)
```

### Tests/Benchmarks

This requires `pytest` and `pytest-benchmark`.

```bash
git clone https://github.com/al-jshen/fastxm
cd fastxm
pytest
```
