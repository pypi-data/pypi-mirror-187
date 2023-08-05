import sys
from time import time as __time
from .types import Test,TestResult,Iterator,List

def module_tests(module: str = "__name__", test_prefix: str = "test_"):
    module = sys.modules.get(module, None)
    return (
        []
        if module is None
        else [
            Test(*args)
            for args in (
                (name, module, getattr(module, name))
                for name in dir(module)
                if name.startswith(test_prefix)
            )
        ]
    )


def iter_results(tests: list[Test], **kwargs) -> Iterator[TestResult]:
    for test in tests:
        name = test.name
        method = test.method
        start = __time()
        value = method(**kwargs)
        time = __time() - start
        yield TestResult(name, time, value)


def get_test_results(tests: list[Test], **kwargs) -> List[TestResult]:
    return [e for e in iter_results(tests=tests, **kwargs)]
