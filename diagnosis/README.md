# `diagnosis` API

The `diagnosis` API consist several packages & modules to work with  logging, file, cache, downloader, data
transformation, and many more. The `diagnosis.core` package is built with [Cython](https://cython.org) - meaning it has
to be built before usage. To build it simply run the Cython build script in the project root:

```sh
chmod +x scripts/*
./scripts/cython.sh
```

## `diagnosis` API packages

- `diagnosis.core` - Core functionality including utilities & base classes.

  - `diagnosis.core.base` - Consist of base classes for `Mode` and `Base` class for other objects.

  - `diagnosis.core.utils` - Consist of utility classes e.g `File`, `Log`, `Downloader`, and `Cache`.

  - `diagnosis.core.data` - Consists of data processing pipelines.

- `diagnosis.tests` - Core functionality includes testing Python & C++ files.

  - `diagnosis.tests.cpp` - Consists of test for C++ files.

  - `diagnosis.tests.python` - Consists of unittests for Python files.
