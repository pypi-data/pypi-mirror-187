
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




@dataclass(frozen=False,order=True)
class TestConfig:

    loops:int
    kwargs:dict




@dataclass(frozen=False,order=True)
class TimeProfile:
    min:float
    max:float
    mean:float

@dataclass(frozen=False,order=True)
class TestProfile:
    name:str
    time:TimeProfile
    value:object

@dataclass(frozen=False,order=True)
class TestProfiles:
    @dataclass(frozen=False,order=True)
    class Meta:
        module:str
        loops:int
        tests:int
        test_names:List[str]

    @dataclass(frozen=False,order=True)
    class Data:
        times:TimeProfile
        tests:List[TestProfile]
    
    meta:Meta
    data:Data


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


        



