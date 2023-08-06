Introduction
============

This package defines Python bindings for `Vidyut`_, a high-performance Sanskrit
toolkit written in Rust. It includes modules for segmentation, word generation,
word lookup, and sandhi.

Our Python API is lightweight and mirrors the underlying Rust API, with minor
change to be more Pythonic.

.. _Vidyut: https://github.com/ambuda-org/vidyut


System requirements
-------------------

This package requires Python 3.7 or newer. You can check your Python
installation by running the following command:

.. code-block:: text

    $ python3 --version


Installation
------------

This package has two parts: its *code* and its *data*.


Code
~~~~

Our Python bindings are published under the `vidyut` package on PyPI and do not
require a Rust installation. You can install the `vidyut` package like so:

.. code-block:: text

    $ pip install vidyut

You can also experiment with our latest bindings by installing directly from
our repo. To use this method, you must have Rust installed on your computer:

.. code-block:: text

    $ pip install git+https://github.com/ambuda-org/vidyut-py.git


Data
~~~~

*(Requires Rust's `cargo` command)*

Vidyut is more interesting when it is used with our rich linguistic data. In
the future, we will provide pre-built versions of this data. But for now, you
must build this data manually.

You can build Vidyut's linguistic data by using our Rust repo:

.. code-block:: text

    $ git clone https://github.com/ambuda-org/vidyut.git
    $ cd vidyut/vidyut-cheda
    $ make install

The output data will be in `data/vidyut-x.y.z`, where `x.y.z` is the Vidyut
version. Once the `data` folder has been created, you can move it wherever you
like.


Getting help
------------

To ask for help and file bugs, we encourage you to `create an issue`_ on our
repo on GitHub. For more casual questions, you can also join the `#nlp` channel
on our `Discord`_ server.

.. _`create an issue`: https://github.com/ambuda-org/vidyut-py/issues
.. _Discord: https://discord.gg/7rGdTyWY7Z
