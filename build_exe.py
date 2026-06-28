import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILD_DIR = ROOT / "build"
DIST_DIR = ROOT / "dist"

if __name__ == "__main__":
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("PyInstaller não encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    for folder in [BUILD_DIR, DIST_DIR]:
        if folder.exists():
            shutil.rmtree(folder)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--name",
        "emu_chip8",
        "--add-data",
        "roms/pong.ch8;roms",
        "main.py",
    ]

    print("Gerando executável...")
    subprocess.check_call(cmd, cwd=ROOT)
    print(f"Executável gerado em: {DIST_DIR / 'emu_chip8.exe'}")
