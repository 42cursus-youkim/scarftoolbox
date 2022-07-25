#!/usr/bin/env python3

from sys import argv

from scarftoolbox.brew import install_brew
from scarftoolbox.cache import symlink_cache
from scarftoolbox.vscode import install_vscode


def main():
    if len(argv) < 2:
        print("Usage: ./toolbox.py <commands...>")
        exit(1)

    for command in set(argv[1:]):
        if command == "vscode":
            install_vscode.main()
        elif command == "cache":
            symlink_cache.main()
        elif command == "brew":
            install_brew.main()
        else:
            print(f"Unknown command: {command}")
            exit(1)

if __name__ == "__main__":
    main()
