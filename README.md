# Caenbrew [![Build Status](https://travis-ci.org/arxanas/caenbrew.svg?branch=master)](https://travis-ci.org/arxanas/caenbrew) [![PyPI version](https://img.shields.io/pypi/v/caenbrew.svg)](https://pypi.python.org/pypi/caenbrew)

Caenbrew lets you easily install packages on CAEN.

# Installation

Run this in your terminal on CAEN:

```
$ curl -fsSL https://raw.githubusercontent.com/arxanas/caenbrew/master/install.sh | sh
```

Then restart your terminal and brew away!

# Usage

To install a package, use `caenbrew install`:

```
$ caenbrew install fish
==> Downloading fish... (curl https://fishshell.com/files/2.2.0/fish-2.2.0.tar.gz --output fish-2.2.0.tar.gz)
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 2161k  100 2161k    0     0   490k      0  0:00:04  0:00:04 --:--:--  490k
==> Extracting package... (tar -xf fish-2.2.0.tar.gz -C package_contents --strip-components 1)
==> Configuring package... (./configure --prefix /home/wkhan/.local)
configure: WARNING: doxygen version 1.8.5 found, but 1.8.7 required
==> Building package... (make)
FISH_BUILD_VERSION = 2.2.0
complete.cpp: In member function ‘void completer_t::complete_cmd(const wcstring&, bool, bool, bool, bool)’:
complete.cpp:1153:123: warning: ignoring return value of ‘int expand_string(const wcstring&, std::vector<completion_t>&, expand_flags_t, parse_error_list_t*)’, declared with attribute warn_unused_result [-Wunused-result]
         (void)expand_string(str_cmd, this->completions, ACCEPT_INCOMPLETE | DIRECTORIES_ONLY | this->expand_flags(), NULL);
                                                                                                                           ^
==> Installing package... (make install)
/usr/bin/install: omitting directory ‘share/tools/web_config/js’
/usr/bin/install: omitting directory ‘share/tools/web_config/partials’
/usr/bin/install: omitting directory ‘share/tools/web_config/sample_prompts’
✓ Package fish installed.
```
