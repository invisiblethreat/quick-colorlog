# `quick-colorlog`

Inspired by `coloredlogs` but without the subprocesses.

### Quickstart

```python
from quick_colorlog import init_colors

init_colors()
```

### Defaults

By default, the log level is set to `logging.INFO` and the output stream is
attached to `sys.stderr`. To change these, pass arguments to `init_colors()`

```python
from quick_colorlog import init_colors

init_colors(level=logging.DEBUG, output=sys.stdout)
```

