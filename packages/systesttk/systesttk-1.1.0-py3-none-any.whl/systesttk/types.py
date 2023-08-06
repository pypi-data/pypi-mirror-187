from dataclasses import dataclass, field
from typing import Callable, List, Optional
from collections import Counter, namedtuple
from . import encode


@dataclass(frozen=False, order=True)
class Test:
    name: Optional[str] = field(default=None)
    module: Optional[str] = field(default=None)
    method: Optional[Callable] = field(default=None)


@dataclass(frozen=False, order=True)
class TimeProfile:
    min: float = field(default=0.0)
    max: float = field(default=0.0)
    mean: float = field(default=0.0)

    def __iadd__(self, __t: float):
        if __t > self.max:
            self.max = __t
        elif __t < self.min:
            self.min = __t
        self.mean += __t
        return self


@dataclass(frozen=False, order=True)
class FreqCounter:
    data: list = field(default_factory=list)
    freqs: Counter = field(default_factory=Counter)

    def __getindex__(self, __value):
        value = encode.obj2str(__value)
        i = next(
            (
                i
                for (i, data) in enumerate((encode.obj2str(d) for d in self.data))
                if data == value
            ),
            None,
        )
        return i

    def __iadd__(self, __value: str):
        i = self.__getindex__(__value)
        if i is None:
            i = len(self.data)
            self.data.append(__value)
        self.freqs[i] += 1
        return self


@dataclass(frozen=False, order=True)
class FreqDist:
    freq: int = field(default=0)
    dist: Counter = field(default_factory=Counter)


@dataclass(frozen=False, order=True)
class ValueProfile:
    value: str = field(default="")
    freq_dist: FreqDist = field(default_factory=FreqDist)


@dataclass(frozen=False, order=True)
class TestData:
    success_rate: float = field(default=0.0)
    errors: FreqCounter = field(default_factory=FreqCounter)
    values: FreqCounter = field(default_factory=FreqCounter)


@dataclass(frozen=False, order=True)
class TestProfile:
    name: Optional[str] = field(default=None)
    time: TimeProfile = field(default_factory=TimeProfile)
    data: TestData = field(default_factory=TestData)


@dataclass(frozen=False, order=True)
class TestsProfile:
    @dataclass(frozen=False, order=True)
    class Meta:
        module: Optional[str] = field(default=None)
        loops: Optional[int] = field(default=None)
        tests: Optional[int] = field(default=None)
        test_names: List[str] = field(default_factory=list)

    @dataclass(frozen=False, order=True)
    class Data:
        success_rate: dict = field(default_factory=dict)
        times: dict = field(default_factory=dict)
        errors: list[ValueProfile] = field(default_factory=list)
        values: list[ValueProfile] = field(default_factory=list)
        profiles: List[TestProfile] = field(default_factory=list)

    meta: Meta = field(default_factory=Meta)
    data: Data = field(default_factory=Data)

    def json(self, indent: int = 4):
        return encode.dataclass_json(self, indent=indent)


TestResultBase = namedtuple("TestResultBase", ("time", "value", "error"))
TestProfile2Float = Callable[[TestProfile], float]
TimeProfile2Float = Callable[[TimeProfile], float]
TestProfile2Counter = Callable[[TestProfile], Counter]
ValueProfile2Int = Callable[[ValueProfile], int]
