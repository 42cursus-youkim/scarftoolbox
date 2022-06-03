#!/usr/bin/env python3

from os import environ

HOME = environ["HOME"]

from os import system
from pathlib import Path

paths = [
    Path(f"{HOME}/.vscode/extensions"),
    Path(f"{HOME}/Library/Application Support/Code/CachedData"),
]


def should_be_dir(path: Path):
    if path.is_dir():
        return
    system(f"rm '{path}' && mkdir '{path}'")


for path in paths:
    should_be_dir(path)

system("code -s")
