from pathlib import Path
import subprocess

"""
There is a problem with subprocess.run(): It uses fork(), which allocates as much memory as the parent process has. 
This quickly leads to out-of-memory situations. 

In order to prevent this, external_execute forks from within a parallel process. If setup() was not called, 
it falls back to just using subprocess.
"""

pool = None


def make_cmd(cmd):
    def clean(c):
        if isinstance(c, Path):
            return str(c.absolute())
        else:
            return c
    return [clean(c) for c in cmd]


def synchronous_run(cmd, logfile, kwargs):
    if logfile is not None:
        with open(logfile, 'a+') as log:
            log.write(" ".join(cmd))
            log.write("\n")
            log.flush()
            return subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, **kwargs)
    else:
        return subprocess.run(cmd, **kwargs)


def synchronous_check_output(cmd, kwargs):
    return subprocess.check_output(cmd, **kwargs)


def setup(procs):
    global pool
#    multiprocessing.set_start_method("forkserver")
#    pool = multiprocessing.Pool(processes=procs)


def run(cmd, logfile, **kwargs):
    cmd = make_cmd(cmd)
    global pool
    if pool is not None:
        return pool.apply(synchronous_run, (cmd, logfile, kwargs))
    else:
        return synchronous_run(cmd, logfile, kwargs)


def call(cmd, logfile, **kwargs):
    cmd = make_cmd(cmd)
    global pool
    if pool is not None:
        return run(cmd, logfile, **kwargs).returncode
    else:
        if logfile is not None:
            with open(logfile, 'a+') as log:
                log.write(" ".join(cmd))
                log.write("\n")
                log.flush()
            return subprocess.call(cmd, stdout=log, stderr=subprocess.STDOUT, **kwargs)
        else:
            return subprocess.call(cmd, **kwargs)


def check_output(cmd, **kwargs):
    cmd = make_cmd(cmd)
    global pool
    if pool is not None:
        return pool.apply(synchronous_check_output, (cmd, kwargs))
    else:
        return synchronous_check_output(cmd, kwargs)


def shutdown():
    global pool
    if pool is not None:
        pool.terminate()
        pool.join()
        pool = None
