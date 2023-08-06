

from unittest.main import TestProgram
from unittest.runner import TextTestRunner

from .results import UtterlessTextTestResult


class UtterlessTestProgram(TestProgram):

    def __init__(self, *args, **kwargs):
        kwargs["testRunner"] = TextTestRunner(resultclass=UtterlessTextTestResult)
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    UtterlessTestProgram(module=None)
    pass
