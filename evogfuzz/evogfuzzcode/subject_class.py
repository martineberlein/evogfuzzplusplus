from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
import pandas
import json
import importlib
import time

# from evogfuzzcoded import helper
# from evogfuzzcoded import tools

from evogfuzzcode import helper
from evogfuzzcode import tools


class Subject(ABC):

    @abstractmethod
    def subject(self) -> str:
        """:return a name for the program under test"""
        raise AssertionError("Overwrite in subclass.")

    @abstractmethod
    def jar_location(self) -> str:
        """:return the absolute path to the subject jar"""
        raise AssertionError("Overwrite in subclass.")

    def execute_samples_dir(self, sample_dir):
        """:return a DataFrame with the execution data"""
        exception_log = Path(sample_dir).parent / "exceptions.log"
        execution_log = Path(sample_dir).parent / "execution.log"

        cmd = ["-jar", self.jar_location(),
               "--ignore-exceptions",
               "--log-exceptions", str(exception_log.absolute()), sample_dir]
        tools.call_java(cmd, execution_log)

        exceptions_data = self.read_exception_log(exception_log)
        sample_frame = self.sample_frame(sample_dir)

        joined_data = exceptions_data.set_index("file") \
            .join(sample_frame.set_index("file"), how='outer') \
            .reset_index()

        return joined_data

    def non_func_exec_samples(self, sample_dir):
        samples = helper.getAllfiles(sample_dir, self.grammar.file_extension())
        exception_log = Path(sample_dir).parent / "exceptions.log"
        execution_log = Path(sample_dir).parent / "execution.log"
        data_frame = []

        for sample in samples:
            exec_time = self.non_func_exec_sample(sample, exception_log, execution_log)
            exceptions_data = self.read_exception_log(exception_log)
            data_frame.append({
                "file": Path(sample).name,
                "subject": self.subject(),
                "exec_time": str(exec_time),
                "exception": exceptions_data['exception'].values,
                "hash": exceptions_data['hash'].values
            })

        return pandas.DataFrame.from_records(data_frame)

    def non_func_exec_sample(self, sample, exception_log, execution_log):
        t = time.process_time()
        try:
            cmd = ["-jar", self.jar_location(),
                   "--ignore-exceptions",
                   "--log-exceptions", str(exception_log.absolute()), sample]
            tools.call_java(cmd, execution_log)

            return time.process_time() - t
        except:
            return -1

    def read_exception_log(self, exception_log):
        if not exception_log.exists():
            return pandas.DataFrame(columns=["file", "hash", "exception", "location"])
        else:
            with open(exception_log, 'r') as except_in:
                exceptions = json.load(except_in)
            exceptions_data = []
            for exp in exceptions:
                stack_hash = exp["stack_hash"]
                exception_name = exp["name"]
                exception_location = exp["location"]
                for file in exp["files"]:
                    exceptions_data.append({
                        "file": Path(file).name,
                        "hash": stack_hash,
                        "exception": exception_name,
                        "location": exception_location
                    })
            exceptions_data = pandas.DataFrame.from_records(exceptions_data)
            return exceptions_data

    def sample_frame(self, samples):
        all_data = []
        samples = helper.getAllfiles(samples, "js")
        for file in samples:
            all_data.append({
                "file": Path(file).name,
                "subject": self.subject()
            })
        if 0 == len(all_data):
            return pandas.DataFrame(columns=["file", "subject"])
        return pandas.DataFrame.from_records(all_data)


def load_driver(file: Union[Path, str]) -> Subject:
    file = Path(file)
    loader = importlib.machinery.SourceFileLoader(file.name[:file.name.rfind(".")], str(file))
    driver_module = loader.load_module()
    return driver_module.create_subject()

