import sys
from time import time as __time
from .types import (
    Test,
    TestResult,
    Iterator,
    List,
    TimeProfile,
    TestProfile,
    TestProfiles,
)


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


def form_test_profiles(tests: List[Test], loops: int, **kwargs):

    data: List[TestProfile] = []
    for test in tests:
        name = test.name
        method = test.method
        time_profile = TimeProfile(min=0.0, max=0.0, mean=0.0)

        for _ in range(0, loops):
            start = __time()
            try:
                value = method(**kwargs)
            except BaseException as error:
                message = f"error:{name}.{str(error)}".replace('\n',' ')
                print(message)
                break
            time = __time() - start
            if time > time_profile.max:
                time_profile.max = time
            elif time < time_profile.min:
                time_profile.min = time
            time_profile.mean += time
        time_profile.mean = time_profile.mean / loops
        test_profile = TestProfile(name=name, time=time_profile, value=value)
        data.append(test_profile)
    return data


def get_module_tests_profile(
    module: str = "__name__", test_prefix: str = "test_", loops: int = 10, **kwargs
):
    tests: List[Test] = module_tests(module=module, test_prefix=test_prefix)
    profiles = form_test_profiles(tests=tests, loops=loops, **kwargs)
    profiles.sort(key=lambda profile: profile.time.mean)
    mins = [p.time.min for p in profiles]
    maxs = [p.time.max for p in profiles]
    means = [p.time.mean for p in profiles]
    times = TimeProfile(min=min(mins), max=max(maxs), mean=sum(means) / len(means))

    meta = TestProfiles.Meta(
        module=str(module), loops=loops, test_names=[t.name for t in tests],tests=len(tests)
    )

    data = TestProfiles.Data(times=times, tests=profiles)

    return TestProfiles(meta=meta, data=data)
