import subprocess

from ..config import *

BREW_PATH = GOINFRE / "brew"
BREW_BIN = BREW_PATH / "bin"


def main():

    if BREW_BIN.exists():
        return

    BREW_PATH.mkdir(parents=True, exist_ok=True)
    download_cmd = ["curl -L https://github.com/Homebrew/brew/tarball/master"]
    unzip_command = [f"tar xz --strip 1 -C {BREW_PATH.absolute()}"]

    download_proc = subprocess.run(
        download_cmd,
        stdout=subprocess.PIPE,
        cwd=BREW_PATH,
        shell=True,
    )
    unzip_proc = subprocess.run(
        unzip_command,
        input=download_proc.stdout,
        # stdout=subprocess.PIPE,
        cwd=BREW_PATH,
        shell=True,
    )
    subprocess.run([f"{BREW_BIN / 'brew'}"])
    print(f"brew installed, add {BREW_BIN} to PATH`")
