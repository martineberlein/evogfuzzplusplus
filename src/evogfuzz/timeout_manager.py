import signal


class ManageTimeout:
    def __init__(self, timeout: float):
        self.timeout = timeout

    def __enter__(self):
        self.old_handler = signal.signal(signal.SIGALRM, self.alarm_handler)
        self.set_alarm(self.timeout)

    def __exit__(self, exc_type, exc_value, traceback):
        self.cancel_alarm()
        signal.signal(signal.SIGALRM, self.old_handler)  # Restore old signal handler

    @staticmethod
    def alarm_handler(signum, frame):
        raise TimeoutError("Function call timed out")

    @staticmethod
    def set_alarm(seconds: float):
        signal.setitimer(signal.ITIMER_REAL, seconds)

    @staticmethod
    def cancel_alarm():
        signal.setitimer(signal.ITIMER_REAL, 0)
