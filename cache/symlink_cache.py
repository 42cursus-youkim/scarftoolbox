#!/usr/bin/env python3
"""
Copyright 2022 scarf

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


from __future__ import annotations

from os import environ, system
from pathlib import Path
from shutil import move
from typing import Dict, Generator, List

"""
Constants
"""
CacheDirs = Dict[Path, List[str]]  # Type alias
HOME = Path(environ["HOME"])
app_support = HOME / "Library" / "Application Support"
goinfre = HOME / "goinfre" / "Cache"

"""
Configurations
"""
NAMES: CacheDirs = {
    HOME / "Library": ["Mail"],  # Evaluates to /Users/<user>/Library/Mail
    HOME
    / "Library"
    / "Caches": [
        "com.google.SoftwareUpdate",
        "vscode-cpptools/ipch",
        "Google/Chrome/Profile 5",
        "Homebrew",
    ],
    # Evaluates to...
    # /Users/<user>/Library/Caches/com.google.SoftwareUpdate
    # /Users/<user>/Library/Caches/vscode-cpptools/ipch
    # and so on...
    app_support
    / "Code": [
        "Cache",
        "CachedData",
        "CachedExtensions",
        "CachedExtensionVSIXs",
        "Code Cache",
        "User/workspaceStorage",
        "User/globalStorage/ms-vsliveshare.vsliveshare",
    ],
    app_support
    / "Slack": [
        "Cache",
        "CachedData",
        "Service Worker/CacheStorage",
        "Service Worker/ScriptCache",
    ],
    app_support
    / "Google"
    / "Chrome"
    / "Profile 5": ["Service Worker/CacheStorage"],
    HOME / ".brew" / "Library" / "Taps" / "homebrew": ["homebrew-core/.git"],
    HOME / ".brew": [".git"],
    HOME / ".vscode": ["extensions"],
}

"""
Implementation
"""


def caches(names: CacheDirs) -> Generator[Path, None, None]:
    for directory, caches in names.items():
        yield from (directory / cache for cache in caches)


def to_goinfre(path: Path) -> Path:
    return goinfre / path.relative_to(HOME)


def move_to_goinfre(file: Path, names: CacheDirs = NAMES):
    create_goinfre_caches(names)
    link, goinfre = Path(file), to_goinfre(file)
    goinfre.mkdir(parents=True, exist_ok=True)
    try:
        if link.is_symlink() or link.is_file():
            link.unlink()
        if link.is_dir():
            move(str(link), goinfre)
            print(f"{link} -> {goinfre}")
        link.symlink_to(goinfre)
    except Exception as e:
        print(f"skipped due to {e}")


def move_all_cache_to_goinfre(names: CacheDirs):
    for f in caches(names):
        move_to_goinfre(f)


def create_goinfre_caches(names: CacheDirs):
    for f in caches(names):
        to_goinfre(f).mkdir(parents=True, exist_ok=True)


def main():
    # move_all_cache_to_goinfre(NAMES)
    create_goinfre_caches(NAMES)


if __name__ == "__main__":
    main()

"""
How To Use

python3 symlink_cache.py

configure NAMES for whatever you feel belongs in goinfre.
"""
