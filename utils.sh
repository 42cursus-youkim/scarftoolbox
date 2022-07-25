#!/bin/bash

python3 $SCARFTOOL/vscode/install_vscode.py
export PATH="$PATH:$HOME/goinfre/vscode/Visual Studio Code.app/Contents/Resources/app/bin"

# python
py_dep () {
  echo installing py deps
  local PY=$(which python3)
  local REQ=~/.pyreq.txt
  [[ -f $REQ ]] && $PY -m pip install -r $REQ
  mv $REQ $REQ.old
  $PY -m pip freeze > $REQ
}

# brew
brew_dep() {
  echo installing brew deps
  local REQ=~/.Brewfile
  [[ -f $REQ ]] && brew bundle --file=$REQ
  mv $REQ $REQ.old
  brew bundle dump --file=$REQ --force
}

brew_dep
py_dep
