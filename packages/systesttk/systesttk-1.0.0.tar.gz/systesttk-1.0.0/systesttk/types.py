
from dataclasses import dataclass
from typing import Callable, Iterator, List, Union

@dataclass(frozen=False, order=True)
class Test:
    name: str
    module: str
    method: Callable


@dataclass(frozen=False, order=True)
class TestResult:
    name: str
    time: float
    value: object


@dataclass(frozen=False, order=True)
class TestResults:
    data: List[TestResult]

    def __iter_rankings(
        self, key: Union[str, Callable[[TestResult], object]], reverse: bool = False
    ) -> Iterator[TestResult]:

        if isinstance(key, str):
            k = key
            key = lambda test: getattr(test, k)

        rankings = self.data
        rankings.sort(key=key, reverse=reverse)
        return iter(rankings)

    def iter_rankings(
        self, key: Union[str, Callable[[TestResult], object]], reverse: bool = False
    ) -> Iterator[TestResult]:
        return self.__iter_rankings(key=key, reverse=reverse)

    def rankings(
        self, key: Union[str, Callable[[TestResult], object]], reverse: bool = False
    ):
        return [e for e in self.__iter_rankings(key=key, reverse=reverse)]
