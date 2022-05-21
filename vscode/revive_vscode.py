#!/usr/bin/env python3

from pathlib import Path
from os import system

paths = [
    Path("/Users/youkim/.vscode/extensions"),
    Path("/Users/youkim/Library/Application Support/Code/CachedData"),
]


def should_be_dir(path: Path):
    if path.is_dir():
        return
    system(f"rm '{path}' && mkdir '{path}'")


for path in paths:
    should_be_dir(path)

system("code -s")
