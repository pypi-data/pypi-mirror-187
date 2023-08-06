# Module Hygiene
_Simple tools to help with Python namespace hygiene!_


## Description

This is an opinionated project! I prefer Python modules to only 
include what's necessary for users. If I'm in an IDE and type
`from module import <TAB>`, I want only API-level elements to 
be available! Many Python projects use a leading underscore to
specify _private_-like objects and modules. Still, it's sometimes
nice to keep things simple without multiple `_module` definitions
in a package.

This package is my solution! It currently provides a single function,
`cleanup`, which returns code to delete all `locals` which are not 
in a provided "export list".

## Usage

See the example usage below. Note that we need to import `T` to add
a proper typed signature for the function `square`. Unfortunately,
this means that `T` is also available to anyone who imports 
this module. 

By default, `cleanup` assumes 
the name of the module's export list is `'__export__'`. If you 
want to choose a different export list name, pass that name as a 
`str` to cleanup!

```python
"""module.py

A python module which exports a single function, `square`.
"""

from hygiene import cleanup
from typing  import T 

__export__ = [
    "square",
]

def square(x: T) -> T:
    """Returns the square of x!"""
    return x ** 2

if __name__ != "__main__":
    cleanup()
```

This `cleanup` approach will likely change how you write Python modules.
If you need a Python package throughout your module, like `numpy`, 
you likely `import numpy as np` at the top of your module, and use `np`
in various functions throughout the module. If you `cleanup` at the end of 
the module, your code will break on execution because `np` will no longer 
exist! 

If you choose to use `cleanup`, then you will need to `import` modules 
**at the function level**. Personally, I like this better anyways! Every 
dependency is right next to where it's used. One major downside of this 
approach is you need to parse your source code for `import` statements 
to track all dependencies. 

```python
"""another.py

Another module which exports a single function, `abssqrt`!
"""

from hygiene import cleanup
from typing  import T

# Don't do this!
# from numpy import abs, sqrt

__export_list__ = [
    "abssqrt",
]

def abssqrt(x: T) -> T:
    """Returns the square root of the absolute value of `x`!"""
    from numpy import abs, sqrt
    return sqrt(abs(x))

if __name__ != "__main__":
    cleanup(export = __export_list__)
```
