
# import sys
# sys.path.insert(1, '/Users/martineberlein/Documents/01_Uni/06_paperEMSE/git/evogfuzz-extension/evogfuzz/evogfuzzcoded')
from evogfuzzcode import external_exec as execute
# from evogfuzzcoded import external_exec as execute
from pathlib import Path

import logging


def run_java(cmd, logfile, check=True, **kwargs):
    call_java(cmd, logfile, check=check, **kwargs)


def call_java(cmd, logfile, **kwargs):
    cmd = execute.make_cmd(cmd)
    try:
        if "timeout" not in kwargs:
            kwargs["timeout"] = 3600
        # , "-XX:+HeapDumpOnOutOfMemoryError"
        execute.run(["java", "-Xss1g", "-Xmx10g"] + cmd, logfile, **kwargs)
    finally:
        # logging.info("Stopped {}".format(cmd))
        if "cwd" in kwargs:
            clear_failed_java(kwargs["cwd"])
        else:
            clear_failed_java(Path("../evogfuzzcoded"))


def clear_failed_java(cwd):
    for dump in cwd.glob("*.dmp"):
        dump.unlink()
    for dump in cwd.glob("*.phd"):
        dump.unlink()
    for dump in cwd.glob("*.trc"):
        dump.unlink()
