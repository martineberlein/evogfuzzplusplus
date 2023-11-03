from ast import literal_eval
from typing import Type, List, Callable, Dict
from pathlib import Path
import string

from fuzzingbook.Grammars import Grammar
from evogfuzz.oracle import OracleResult
from evogfuzz.oracle_construction import construct_oracle

from subjects import TestSubject, TestSubjectFactory, load_object_dynamically


class RefactoryTestSubject(TestSubject):
    base_path: Path
    implementation_function_name: str

    def __init__(self, oracle, bug_id, solution_type: str):
        """
        Oracle allways needs to be constructed!

        :param oracle: constructed Differential Oracle
        :param bug_id: number of the implementation XYZ_N_001, XYZ_N_002 etc.
        :param solution_type: can be either 'correct', 'fail', or 'wrong'
        """
        super().__init__(oracle=oracle)
        self.bug_id = bug_id
        self.solution_type = solution_type

    @classmethod
    def harness_function(cls, input_str: str):
        raise NotImplementedError

    @classmethod
    def ground_truth(cls) -> Callable:
        solution_file_path = cls.base_path / Path("reference/reference.py")
        return load_object_dynamically(
            solution_file_path,
            cls.implementation_function_name,
        )

    def get_implementation(self) -> Callable:
        imp_dir_path = self.base_path / Path(self.solution_type)
        imp_file_path = list(imp_dir_path.absolute().glob(f"*{self.bug_id}.py"))[0]

        return load_object_dynamically(
            imp_file_path,
            self.implementation_function_name,
        )


class Question1RefactoryTestSubject(RefactoryTestSubject):
    base_path = Path("./resources/refactory/question_1/code")
    implementation_function_name = "search"
    default_grammar: Grammar = {
        "<start>": ["<input>"],
        "<input>": ["<first>, <second>"],
        "<first>": ["<integer>"],
        "<second>": ["()", "[]", "(<integer>, <integer><list>)", "[<integer><list>]"],
        "<list>": ["", ", <integer><list>"],
        "<integer>": ["<maybe_minus><one_nine><maybe_digits>"],
        "<maybe_minus>": ["", "-"],  #
        "<one_nine>": [str(num) for num in range(1, 10)],
        "<digit>": list(string.digits),
        "<maybe_digits>": ["", "<digits>"],
        "<digits>": ["<digit>", "<digit><digits>"],
    }
    default_test_inputs = ["42, (-5, 1, 3, 5, 7, 10)", "3, (1, 5, 10)"]

    @classmethod
    def harness_function(cls, input_str: str):
        # Split the string into two parts based on the first comma and a space
        arg1_str, arg2_str = input_str.split(", ", 1)

        # Convert the string parts to Python literals
        arg1 = literal_eval(arg1_str)
        arg2 = literal_eval(arg2_str)

        return arg1, arg2


class RefactoryTestSubjectFactory(TestSubjectFactory):
    def __init__(self, test_subject_type: Type[RefactoryTestSubject]):
        self.test_subject_type = test_subject_type

    def build(
        self,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
        solution_type: str = "wrong",
    ) -> List[RefactoryTestSubject]:
        subjects = []

        subject_path = Path(self.test_subject_type.base_path) / Path(solution_type)
        num_files = len(list(subject_path.absolute().glob(f"*.py")))

        for i in range(1, num_files):
            formatted_str = str(i).zfill(3)

            try:
                subject = self._build_subject(
                    formatted_str, err_def, default_oracle, solution_type
                )
                subjects.append(subject)
            except Exception as e:
                print(f"Subject {formatted_str} could not be build.")

        return subjects

    def _build_subject(
        self,
        formatted_bug_id: str,
        err_def: Dict[Exception, OracleResult] = None,
        default_oracle: OracleResult = None,
        solution_type: str = "wrong",
    ):
        reference = self.test_subject_type.ground_truth()
        subject = self.test_subject_type(
            oracle=lambda _: None, bug_id=formatted_bug_id, solution_type=solution_type
        )
        implementation = subject.get_implementation()

        error_def = err_def or {TimeoutError: OracleResult.UNDEF}
        def_oracle = default_oracle or OracleResult.BUG

        oracle = construct_oracle(
            implementation,
            reference,
            error_def,
            default_oracle_result=def_oracle,
            timeout=0.01,
            harness_function=subject.harness_function,
        )
        subject.oracle = oracle

        return subject


def main():
    sub_types = [
        Question1RefactoryTestSubject,
    ]

    factory = RefactoryTestSubjectFactory(Question1RefactoryTestSubject)
    subjects = factory.build(solution_type="fail")
    for subject in subjects:
        print(subject.bug_id)
        orc = subject.to_dict().get("oracle")
        inputs = subject.to_dict().get("initial_inputs")
        for inp in inputs:
            print(orc(inp))


def main3():
    from fuzzingbook.GrammarFuzzer import GrammarFuzzer

    fuzzer = GrammarFuzzer(Question1RefactoryTestSubject.default_grammar)
    for _ in range(30):
        print(fuzzer.fuzz())


if __name__ == "__main__":
    main()
