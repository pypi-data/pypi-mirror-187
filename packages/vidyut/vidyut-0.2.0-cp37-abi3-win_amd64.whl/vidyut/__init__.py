"""Python bindings for Vidyut.

This library defines Python bindings to Vidyut, a Rust project that provides
reliable infrastructure for Sanskrit software. These bindings are thin wrappers
over the underlying Rust code, but we have done what we can to make these
bindings Pythonic.

This library's main modules are:

- `vidyut.cheda`, which segments Sanskrit expressions
- `vidyut.kosha`, which compactly stores Sanskrit words
- `vidyut.prakriya`, which generates Sanskrit words

In general, all Vidyut code expects that Sanskrit text uses the SLP1
transliteration format. For details on how this form is defined, see:
https://en.wikipedia.org/wiki/SLP1
"""
