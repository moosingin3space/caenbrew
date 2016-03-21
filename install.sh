#!/bin/sh
set -euo pipefail

readonly CAENBREW_DIR="$HOME/.local"
readonly PIP="$HOME/.local/bin/pip"

# Assume that the user is using bash.
readonly PROFILE="$HOME/.bash_profile"
readonly PROFILE_MARKER='# Added by Caenbrew.'

main() {
    install_pip
    install_caenbrew
    add_local_dir_to_path
    echo "$(tput setaf 2)✓$(tput sgr0) Caenbrew successfully installed."
    echo '  You may have to restart your terminal.'
}

install_pip() {
    # CAEN loses packages a lot, so we can't rely on them having Pip installed.
    # In any case, it's very out-of-date.
    easy_install --prefix="$CAENBREW_DIR" pip
}

install_caenbrew() {
    # Note -- `pip install --user` functions assuming that the user has the
    # directory `~/.local`. We would have to add `~/.local` to our PATH to use
    # Caenbrew. But we need to do that anyways because Caenbrew installs all of
    # its packages to `~/.local` as well.
    mkdir -p "$CAENBREW_DIR"
    "$PIP" install --user caenbrew
}

add_local_dir_to_path() {
    touch "$PROFILE"
    if ! grep -q "$PROFILE_MARKER" "$PROFILE"; then
	# Note: we need to put ~/.local/bin *before* the rest of our PATH,
	# because there may be old CAEN executables of the same name in our
	# PATH. We need to make sure our newer ones take precedence.
        echo '' >>"$PROFILE"
        echo "$PROFILE_MARKER" >>"$PROFILE"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >>"$PROFILE"
    fi
}

main
