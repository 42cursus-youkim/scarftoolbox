#!/usr/bin/env python3

from io import BytesIO
from os import chdir, environ, getcwd, system
from pathlib import Path
from subprocess import run

import requests

from ..config import *

VSCODE_BUILD = "stable"
VSCODE_PLATFORM = "darwin-universal"
VSCODE_URL = f"https://code.visualstudio.com/sha/download?build={VSCODE_BUILD}&os={VSCODE_PLATFORM}"
VSCODE_NAME = "Visual Studio Code.app"

CODE_DIR = GOINFRE / "vscode"
CODE_ZIP_DIR = (CODE_DIR / "vscode").with_suffix(".zip")
CODE_APP_DIR = CODE_DIR / VSCODE_NAME
CODE_BIN = CODE_APP_DIR / "Contents/Resources/app/bin"
CODE_DESKTOP = HOME / "Desktop" / VSCODE_NAME


def fetch_vscode_binary() -> bytes:
    res = requests.get(VSCODE_URL, allow_redirects=True)
    if not res.ok:
        raise Exception(f"Failed to download vscode from {VSCODE_URL}")
    return res.content


def save_binary_as_zip(binary: bytes, path: Path) -> None:
    path.write_bytes(binary)


def unzip_vscode(path: Path) -> None:
    chdir(path.parent)
    print(f"cwd: {getcwd()}")
    print(f"unzipping vscode at {path}")
    system(f"ls {path}")
    if run(["unzip", path]).returncode != 0:
        raise Exception(
            f"Failed to unzip vscode at {path}. please unzip manually"
        )


LIBRARY = Path(HOME) / "Library" / "Application Support" / "Code"
EXTENSIONS = Path(HOME) / ".vscode" / "extensions"
DEPENDENCIES = [EXTENSIONS] + [
    LIBRARY / path
    for path in [
        "User/workspaceStorage",
        "Cache",
        "CachedExtensions",
        "CachedExtensionVSIXs",
        "Code Cache",
        "CachedData",
    ]
]


def mkdir_dependencies() -> None:
    for path in DEPENDENCIES:
        path.resolve().mkdir(parents=True, exist_ok=True)


def check_code_at_path() -> None:
    if CODE_BIN not in PATH:
        print(
            "Done. Add the following lines to your .zshrc or startup script:"
        )
        print(f'export PATH="$PATH:{CODE_BIN}"')


def symlink_to_desktop() -> None:
    try:
        CODE_DESKTOP.symlink_to(CODE_APP_DIR)
        print("print added symlink to desktop")
    except:
        print("could not create symlink to desktop, maybe it exists?")


def main():
    mkdir_dependencies()
    if CODE_APP_DIR.exists():
        exit(0)
    if not CODE_ZIP_DIR.exists():
        CODE_DIR.mkdir(parents=True, exist_ok=True)
        print("Fetching vscode...")
        vscode = fetch_vscode_binary()
        print("Done. Saving as zip...")
        save_binary_as_zip(vscode, CODE_ZIP_DIR)
    print("Done. Unzipping...")
    unzip_vscode(CODE_ZIP_DIR)
