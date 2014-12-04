LSF
===

A simple abstraction built on top of existing LSF SWIG bindings.


Usage
-----

Basic job submission:

::

    import lsf

    job = lsf.submit('ls -lh', options={'queue': 'testing'})


Installation
------------

For installation, make sure you set the following environment variables:

::

    export LSF_INCLUDEDIR=/usr/local/lsf/8.0/include
    export LSF_LIBDIR=/usr/local/lsf/8.0/linux2.6-glibc2.3-x86_64/lib

Then, simply install with pip:

::

    pip install lsf


Testing
-------

To run tests, make sure that the environment variables specified in
`Installation`_ are set.  Then run tox:

::

    pip install tox
    tox
