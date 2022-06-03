from __future__ import annotations

from os import environ
from pathlib import Path

PATH = environ["PATH"].split(":")
HOME = Path(environ["HOME"])
GOINFRE = Path(f"/{HOME}/goinfre")
