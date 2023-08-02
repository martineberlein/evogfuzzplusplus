import unittest

from evogfuzz.report import FailureReport, Failure


class TestFailureReport(unittest.TestCase):
    def test_failure_report(self):
        f1 = Failure(NotImplementedError("zero division error"))
        f2 = Failure(NotImplementedError("zero division error"))
        f3 = Failure(NotImplementedError("float zero division error"))
        assert f1 == f2
        assert f1 != f3
        assert hash(f1) == hash(f2)
        assert hash(f1) != hash(f3)

        report = FailureReport()
        report.add_failure(f1, "3")
        report.add_failure(f2, "1")
        report.add_failure(f3, "4")

        failures = report.get_failures()
        assert len(failures[f1]) == 2
        assert len(failures[f2]) == 2
        assert len(failures[f3]) == 1

        assert failures[f1] == failures[f2]
        assert failures[f1] != failures[f3]


if __name__ == '__main__':
    unittest.main()
