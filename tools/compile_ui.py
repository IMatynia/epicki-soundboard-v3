from pathlib import Path
import subprocess

ROOT = Path(__file__).parent.parent
COMPILER_COMMAND = "pyside6-uic"

def main():
    ui_designs = ROOT / "ui" / "ui_designs"
    layouts_folder = ROOT / "ui" / "layouts"

    for file in ui_designs.iterdir():
        if file.is_file() and file.name.endswith(".ui"):
            subprocess.run([COMPILER_COMMAND, "-o", layouts_folder / f"Ui_{file.stem}.py", file])


if __name__ == "__main__":
    main()