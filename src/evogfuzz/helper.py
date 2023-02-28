import os.path
import subprocess
import logging
import sys
from typing import List

from distutils.sysconfig import get_python_lib
from pathlib import Path
from tempfile import NamedTemporaryFile
from importlib import reload

from fuzzingbook import ProbabilisticGrammarFuzzer
from fuzzingbook import GrammarCoverageFuzzer

PATCH_ERROR = -3

PATCH = b"""
--- a/docs/code/GrammarCoverageFuzzer.py
+++ b/docs/code/GrammarCoverageFuzzer.py
@@ -196,6 +196,10 @@ def expansion_key(symbol: str,
     if isinstance(expansion, tuple):
         # Expansion or single derivation tree
         expansion, _ = expansion
+        
+    # Check for empty list expansion
+    if isinstance(expansion, list) and not expansion:
+        expansion = ""

     if not isinstance(expansion, str):
         # Derivation tree
--
"""


def patch():
    site_packages = get_python_lib()
    grammar_coverage_fuzzer = (
        Path(site_packages) / "fuzzingbook" / "GrammarCoverageFuzzer.py"
    )

    patch_file = NamedTemporaryFile(suffix=".patch")
    patch_file.write(PATCH)
    patch_file.seek(0)

    cmd = ["patch", str(grammar_coverage_fuzzer.absolute()), str(patch_file.name)]

    cmd_dry_run = cmd + ["--dry-run"]
    dry_run = run_cmd(cmd_dry_run)

    if b"patch detected" not in dry_run.stdout:
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if process.returncode:
            logging.error("Patching fuzzingbook.GrammarCoverageFuzzer did not work")
            sys.exit(PATCH_ERROR)

        # Reload patched modules
        reload(GrammarCoverageFuzzer)
        # Reload patched modules
        reload(ProbabilisticGrammarFuzzer)


def run_cmd(cmd: List, stdout = subprocess.PIPE, stderr = subprocess.PIPE) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            cmd, stdout=stdout, stderr=stderr
        )
    except subprocess.CalledProcessError as e:
        logging.error(e)
        logging.error(f"Can't execute command {cmd}!")
        sys.exit(PATCH_ERROR)


if __name__ == "__main__":
    sys.exit(patch())
