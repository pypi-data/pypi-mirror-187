from dataclasses import dataclass, is_dataclass
import json
from typing import Callable, Iterator, List, Union


__encode = (
    lambda __v: {
        name: __encode(getattr(__v, name))
        for name in __v.__dataclass_fields__.keys()
    }
    if is_dataclass(__v)
    else {key: __encode(value) for key, value in __v.items()}
    if isinstance(__v, dict)
    else [__encode(value) for value in __v]
    if isinstance(__v, list) or isinstance(__v, set)
    else str(__v)
    if callable(__v)
    else __v
)

def dataclass_dict(__v):
    return __encode(__v)


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
class TestConfig:

    loops: int
    kwargs: dict


@dataclass(frozen=False, order=True)
class TimeProfile:
    min: float
    max: float
    mean: float


@dataclass(frozen=False, order=True)
class TestProfile:
    name: str
    time: TimeProfile
    value: object


@dataclass(frozen=False, order=True)
class TestProfiles:
    @dataclass(frozen=False, order=True)
    class Meta:
        module: str
        loops: int
        tests: int
        test_names: List[str]

    @dataclass(frozen=False, order=True)
    class Data:
        times: TimeProfile
        tests: List[TestProfile]

    meta: Meta
    data: Data



    def json(self,indent:int=4):
        return json.dumps(dataclass_dict(self),indent=indent)

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

    def dict(self):
        return dataclass_dict(self)

    def json(self,indent:int=4):
        return json.dumps(dataclass_dict(self),indent=indent)
