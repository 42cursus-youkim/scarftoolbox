#!/usr/bin/env python3

"""
How To Use

python3 symlink_cache.py

configure NAMES for whatever you feel belongs in goinfre.
"""

import shutil
from os import environ, system
from pathlib import Path
from typing import Dict, Generator, List

"""
Constants
"""
CacheDirs = Dict[Path, List[str]]
HOME = Path(environ["HOME"])
app_support = HOME / "Library" / "Application Support"
goinfre = HOME / "goinfre" / "Cache"

"""
Configurations
"""
NAMES: CacheDirs = {
    HOME / "Library": ["Mail"],  # Evaluates to /Users/<user>/Library/Mail
    HOME: [".asdf", ".npm"],
    HOME
    / "Library"
    / "Caches": [
        "com.google.SoftwareUpdate",
        "vscode-cpptools/ipch",
        "Google/Chrome/Profile 5",
        "pip",
        "node-gyp",
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
    / "Profile 5": ["Service Worker/CacheStorage", "IndexedDB"],
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


def move_dir_to_goinfre(file: Path) -> None:
    def move_recursively(link: Path, goinfre: Path) -> None:
        goinfre.mkdir(parents=True, exist_ok=True)
        shutil.copytree(link, goinfre, dirs_exist_ok=True)
        shutil.rmtree(link)

    link, goinfre = Path(file), to_goinfre(file)
    
    if goinfre.exists():
        if goinfre.is_dir():
            return
        else:
            goinfre.unlink()
    goinfre.mkdir(parents=True)
    if link.is_symlink():
        return
    if link.is_file():
        link.unlink()
    if link.is_dir():  # Move them
        print(f"MOVE  {link}")
        move_recursively(link, goinfre)
    if not link.exists():
        print(f"LINK {goinfre}")
        link.symlink_to(goinfre)


def main():
    for f in caches(NAMES):
        move_dir_to_goinfre(f)
