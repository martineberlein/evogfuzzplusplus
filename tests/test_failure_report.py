import unittest

from debugging_framework.report import MultipleFailureReport, Failure, SingleFailureReport


class TestFailureReport(unittest.TestCase):
    def test_single_failure_report(self):
        report = SingleFailureReport()
        report.add_failure("3")
        report.add_failure("1")
        report.add_failure("4")

        assert len(report.get_all_failing_inputs()) == 3

    def test_multi_failure_report(self):
        f1 = Failure(NotImplementedError("zero division error"))
        f2 = Failure(NotImplementedError("zero division error"))
        f3 = Failure(NotImplementedError("float zero division error"))
        assert f1 == f2
        assert f1 != f3
        assert hash(f1) == hash(f2)
        assert hash(f1) != hash(f3)

        report = MultipleFailureReport()
        report.add_failure("3", f1)
        report.add_failure("1", f2)
        report.add_failure("4", f3)

        failures = report.get_failures()
        assert len(failures[f1]) == 2
        assert len(failures[f2]) == 2
        assert len(failures[f3]) == 1

        assert failures[f1] == failures[f2]
        assert failures[f1] != failures[f3]

        f4 = Failure(AssertionError("division error"))
        failures = report.get_failures()
        assert f1 and f3 in failures.keys()
        assert f4 not in failures.keys()

        assert len(report.get_all_failing_inputs()) == 3


if __name__ == "__main__":
    unittest.main()
