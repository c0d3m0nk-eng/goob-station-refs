"""
prepare-refs.py — Копирует только нужные DLLs в refs/ папку
для загрузки в goob-station-refs репозиторий.

Использование:
  python prepare-refs.py

Создаёт:
  refs/GoobBin/   — ~11 DLLs для Argus.Patch + SSCliPatch
  refs/LoaderBin/ — ~3 DLLs для SSCliPatch
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GOOB_BIN = ROOT / "Servers" / "Goob-Station" / "bin" / "Content.Client"
LOADER_BIN = ROOT / "MusyaLoader-release" / "bin_x64"

REFS_DIR = Path(__file__).resolve().parent / "refs"
GOOB_REFS = REFS_DIR / "GoobBin"
LOADER_REFS = REFS_DIR / "LoaderBin"

# Только DLLs, нужные для компиляции Argus.Patch и SSCliPatch
GOOB_DLLS = [
    # Robust — ядро
    "Robust.Shared.dll",
    "Robust.Client.dll",
    "Robust.Shared.Maths.dll",
    # Content
    "Content.Client.dll",
    "Content.Shared.dll",
    "Content.Goobstation.Maths.dll",
    # Argus.Patch зависимости
    "Microsoft.Data.Sqlite.dll",
    "SixLabors.ImageSharp.dll",
    # SSCliPatch зависимости (Roslyn REPL)
    "Serilog.dll",
    "Microsoft.CodeAnalysis.dll",
    "Microsoft.CodeAnalysis.CSharp.dll",
    "Microsoft.CodeAnalysis.Scripting.dll",
    "Microsoft.CodeAnalysis.CSharp.Scripting.dll",
]

LOADER_DLLS = [
    "0Harmony.dll",
    "Marsey.dll",
]


def copy_specific_dlls(src: Path, dst: Path, names: list[str]) -> int:
    if not src.exists():
        print(f"  [WARN] Source not found: {src}")
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for name in names:
        dll = src / name
        if dll.exists():
            shutil.copy2(dll, dst / name)
            count += 1
        else:
            print(f"  [WARN] Not found: {dll}")
    return count


def main():
    print("=== Preparing Goob-Station Refs (minimal) ===")

    # Clean existing
    if REFS_DIR.exists():
        shutil.rmtree(REFS_DIR)

    n1 = copy_specific_dlls(GOOB_BIN, GOOB_REFS, GOOB_DLLS)
    print(f"  GoobBin: {n1}/{len(GOOB_DLLS)} DLLs copied")

    n2 = copy_specific_dlls(LOADER_BIN, LOADER_REFS, LOADER_DLLS)
    print(f"  LoaderBin: {n2}/{len(LOADER_DLLS)} DLLs copied")

    total = n1 + n2
    print(f"\n  Total: {total} DLLs → {REFS_DIR}")
    print(f"\nNext steps:")
    print(f"  1. cd {REFS_DIR.parent}")
    print(f"  2. git add .")
    print(f"  3. git commit -m 'update refs'")
    print(f"  4. git push")


if __name__ == "__main__":
    main()
