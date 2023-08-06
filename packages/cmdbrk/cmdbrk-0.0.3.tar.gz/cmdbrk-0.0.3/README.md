# cmdbrk.py
Quickly and easily handle command line arguments.

## Usage

Basic Example:

```python
from cmdbrk import handle
from sys    import argv

print(handle(argv))
```

### 0.0.3
Patch bug in 0.0.2: If prefix length is over 1, the flag still includes part of the prefix

### 0.0.2
Made flags not include the prefix.

### 0.0.1
Added option to change prefix.
