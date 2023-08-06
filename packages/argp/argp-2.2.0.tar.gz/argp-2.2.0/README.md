# argp

Memorable api wrapper for argparse

## Installation

```
$ pip install argp
```
## Use case

Argparse is a good library, but the API is not the most memorable. This provides a succinct wrapper that
preserves all the power of argparse, but make the parser easier to initialize.

Usage:

```python
import argp

def do_foo(args):
    print("Subcommand foo", args)

def do_bar(args):
    print("Another subcommand",args)

argp.init()
argp.sub("foo", do_foo, help="Some help text")
bar = argp.sub("bar", do_bar)
bar.arg("--myarg", help="Extra arg for bar")
argp.parse()

```

Api [documentation](https://vivainio.github.io/argp/)

See [Demo app](demoapp.py) for some other use cases

## License

MIT


