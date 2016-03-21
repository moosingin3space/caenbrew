# Caenbrew [![Build Status](https://travis-ci.org/arxanas/caenbrew.svg?branch=master)](https://travis-ci.org/arxanas/caenbrew) [![PyPI version](https://img.shields.io/pypi/v/caenbrew.svg)](https://pypi.python.org/pypi/caenbrew)

Caenbrew lets you easily install packages on CAEN.

# Installation

Run this in your terminal on CAEN:

```
curl -fsSL https://raw.githubusercontent.com/arxanas/caenbrew/master/install.sh | sh
```

Then restart your terminal and brew away!

# Usage

Commands:

  * `caenbrew list`: List all packages.
  * `caenbrew list -s '<term>'`: List all packages matching a search term.
  * `caenbrew install <package>`: Install a package.
  * `caenbrew install -f <package>`: Force-install or reinstall a package. (Use
    `caenbrew install -f caenbrew` if you want to update Caenbrew.)
  * `caenbrew uninstall <package>`: Uninstall a package.

Caenbrew has knowledge of CAEN-specific build quirks. For example, the `ncurses`
library has two separate bugs which may manifest when trying to compile it on
CAEN. This is all taken care of for you by the package author.

Caenbrew will automatically resolve and install dependencies for you. For
example, the `tmux` package will automatically install `libevent` and `ncurses`.
