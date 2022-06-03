#!/usr/bin/env python3

from pathlib import Path
from sys import argv

from ..config import *

CACHE_DIR = HOME / "goinfre" / "Cache"

if len(argv) != 2:
    print("need only one arg")
    exit(1)

name = Path(argv[1])
rel_path = name.relative_to(HOME)
cache_path = CACHE_DIR / rel_path

cache_path.mkdir(parents=True, exist_ok=True)


name.unlink()
name.symlink_to(cache_path)

print(f"{name} -> {cache_path}")
