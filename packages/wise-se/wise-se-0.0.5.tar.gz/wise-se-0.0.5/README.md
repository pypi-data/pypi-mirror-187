# PyWiSE: A Python Twin of the Verified Symbolic Bug Finder WiSE

PyWiSE is a re-implementation of the (verified) Coq version of WiSE in Python. It
features a command-line interface and parser to symbolically execute IMP programs. All
code, with the exception of the parser and CLI code, closely mirror the Coq
implementation. To demonstrate this, the original Coq code is provided as
inline-comments close to the code mirroring it.

The relevant files are:

- `streams.py`, mirroring `streams.v`&mdash;a small library for infinite streams.
- `imp.py`, mirroring `imp.v`&mdash;the IMP programming language.
- `symex.py`, mirroring `symex.v`&mdash;symbolic evaluation of expressions.
- `bugfinder.py`, mirroring `bugfinder.v`&mdash;the implementation of the bug finder.

## Installation

PyWiSE project requires Python 3.10 or higher. It is on PyPi; a simple
`pip install wise-se` suffices to install the symbolic executor in the current Python
environment.

If you want to build the project locally, we recommend using a virtual environment:

```shell
cd /path/to/PyWiSE
python3.10 -m venv venv
source venv/bin/activate
pip install .[dev,test]
```

Either way, the `wise` command should now be available on your command line. You can
test it as follows:

```shell
$ echo "if x <= 0 then
    x = 17;
    fail
  else
    skip
  fi" > test.imp
$ wise test.imp
Analyzing file test.imp

BUG FOUND
  Path:  x <= 0
  Store: {}{x -> 17}
```

Enter `wise -h` for a short help text.

## Copyright, Authors and License

Copyright © 2023 Arthur Correnson and Dominic Steinhöfel.

PyWiSE is released under the GNU General Public License v3.0 (see [COPYING](COPYING)).
