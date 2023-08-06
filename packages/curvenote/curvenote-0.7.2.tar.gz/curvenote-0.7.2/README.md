# curvenote

The Curvenote helper library for working in Jupyter Notebooks with Python kernels

## Installation

```bash
    ~$ python -m pip install curvenote
```

## Summary

- `stash` save a dict or pandas dataframe in a cell output without diaplying the data

  ```python
       from curvenote import stash

       stash('myvars', myvars)
  ```

- `AppState` a traitlet based class to help manage state in ipywidgets ui's

  ```python
    from curvenote import AppState, with_state

    state = AppState()

    # register a widget in state
    wave_1_amp = FloatSlider(1.0, min=0.1, max=5.0, step=0.1, description="1 - Amp")
    state.register_stateful_widget(wave_1_amp, "wave_1_amp", Float(1.0))

    # register any trailet as a propery
    state.register_stateful_property("my_dict", Dict(dict(A="hello", B="world", C=1)))

    # observe the entire state
    def my_update_fn(state):
      some_calc_function(state.wave_1_amp, state.my_dict)
    state.observe(with_state(my_update_fn))

    # observe a single registered widget
    def wave_1_observer(evt):
      pass
    state.register_widget_observer("wave_1_amp", wave_1_observer)

    # observe a single trait
    def trait_observer(evt):
      pass
    state.register_widget_observer("my_dict", trait_observer)

    # display state changes for debugging
    from IPython.display import display
    display(state.outlet)

  ```
