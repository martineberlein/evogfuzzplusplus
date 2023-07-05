import os
from pathlib import Path

patch_file_location = Path(os.path.dirname(os.path.abspath(__file__)), "GrammarCoverageFuzzer.txt")


if __name__ == "__main__":
    print(patch_file_location)