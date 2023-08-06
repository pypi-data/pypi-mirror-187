# avrdude_windows

This package installs the avrdude (x32 and x64-only) binaries for Windows via pypi/pip. There is a single python function in this library which allows you to get the path of the avrdude executable:

```python
from avrdude_windows import get_avrdude_path

print(get_avrdude_path())
```

The MIT license in this repository only applies to the single python function mentioned above - avrdude is licensed separately. Source code and binary releases for avrdude can be found in the [project repository](https://github.com/avrdudes/avrdude/releases). 

If you are using Mac, you should use Homebrew instead:

```
brew install avrdude
```

Or on Linux, you should use the package manager of your distribution, for example:

```
sudo apt install avrdude
```