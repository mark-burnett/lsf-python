# LSF
A simple abstraction built on top of existing LSF SWIG bindings.

To run tests, first make sure you set the proper environment variables:

```bash
export LSF_INCLUDEDIR=/usr/local/lsf/8.0/include
export LSF_LIBDIR=/usr/local/lsf/8.0/linux2.6-glibc2.3-x86_64/lib
```

Then run tox:

```bash
pip install tox
tox
```
