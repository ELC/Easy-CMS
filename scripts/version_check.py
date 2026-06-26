from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

from semantic_version import Version


ROOT = Path(__file__).resolve().parent.parent

PYTHON_TO_BROWSER = {
    "studio-service": (
        ROOT / "apps" / "studio" / "service" / "pyproject.toml",
        ROOT / "apps" / "studio" / "web" / "package.json",
    ),
    "sync-server-service": (
        ROOT / "apps" / "sync-server" / "service" / "pyproject.toml",
        ROOT / "apps" / "sync-server" / "admin" / "package.json",
    ),
}

CALVER_PACKAGES = {
    "site-template": ROOT / "apps" / "site-template" / "package.json",
}

PACKAGE_ALIASES = {
    "studio-web": "studio-service",
    "sync-server-admin": "sync-server-service",
}

CALVER_PATTERN = re.compile(r"^\d{4}\.(0[1-9]|1[0-2])\.\d+$")


def read_pyproject_version(path: Path) -> Version:
    with path.open("rb") as file:
        data = tomllib.load(file)
    return Version(data["project"]["version"])


def read_package_json_version(path: Path) -> str:
    with path.open(encoding="utf-8") as file:
        data = json.load(file)
    version = data["version"]
    if not isinstance(version, str):
        raise TypeError(f"{path} version must be a string")
    return version


def check_semantic_pair(name: str, pyproject_path: Path, package_path: Path) -> list[str]:
    python_version = read_pyproject_version(pyproject_path)
    browser_version = Version(read_package_json_version(package_path))
    if python_version != browser_version:
        return [
            f"{name}: {pyproject_path} has {python_version}, "
            f"but {package_path} has {browser_version}",
        ]
    return []


def check_calver(name: str, package_path: Path) -> list[str]:
    version = read_package_json_version(package_path)
    if CALVER_PATTERN.fullmatch(version) is None:
        return [f"{name}: {package_path} version {version!r} is not YYYY.0M.MINOR"]
    return []


def selected_names(argument: str) -> list[str]:
    if argument == "":
        return [*PYTHON_TO_BROWSER, *CALVER_PACKAGES]
    return [PACKAGE_ALIASES.get(argument, argument)]


def main() -> int:
    argument = sys.argv[1] if len(sys.argv) > 1 else ""
    errors: list[str] = []

    for name in selected_names(argument):
        if name in PYTHON_TO_BROWSER:
            errors.extend(check_semantic_pair(name, *PYTHON_TO_BROWSER[name]))
        elif name in CALVER_PACKAGES:
            errors.extend(check_calver(name, CALVER_PACKAGES[name]))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
