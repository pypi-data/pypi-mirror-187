# curvenote

The Curvenote helper library for working in Jupyter Notebooks with Python kernels

## Installation

```bash
    ~$ python -m pip install curvenote
```

## Function Summary

- `stash` save a dict or pandas dataframe in a cell output without diaplying the data

  ```python
       from curvenote import stash

       stash('myvars', myvars)
  ```
