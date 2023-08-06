import sys
from time import time as __time
from . import types
from typing import Callable, List


def module_tests(__module: str = "__name__", test_prefix: str = "test_"):
    __module = sys.modules.get(__module, None)
    return (
        []
        if __module is None
        else [
            types.Test(*args)
            for args in (
                (name, __module, getattr(__module, name))
                for name in dir(__module)
                if name.startswith(test_prefix)
            )
        ]
    )


def __iter_test_results(name: str, method: Callable, loops: int, **params):
    for _ in range(0, loops):
        value = None
        error = None
        start = __time()
        try:
            value = method(**params)
        except BaseException as exc:
            error = f"error:{name}.{str(exc)}".replace("\n", " ")
        time = __time() - start
        yield types.TestResultBase(time, value, error)


def __build_test_profile(test: types.Test, loops: int, **params):
    name = test.name
    method = test.method

    values = types.FreqCounter()
    errors = types.FreqCounter()
    time = types.TimeProfile()

    for result in __iter_test_results(name=name, method=method, loops=loops, **params):
        time += result.time
        error = result.error
        if error is None:
            values += result.value
        else:
            errors += error

    time.mean = time.mean / loops
    total_errors = sum(errors.freqs.values())
    success_rate = 1.0 - (total_errors / loops)

    data = types.TestData(success_rate=success_rate, errors=errors, values=values)
    profile = types.TestProfile(name=name, time=time, data=data)
    return profile


def form_test_profiles(tests: List[types.Test], loops: int, **params):
    return [__build_test_profile(test=test, loops=loops, **params) for test in tests]


def sort_test_profiles(
    profiles: List[types.TestProfile],
    getter: Callable[[types.TestProfile], object],
    reverse: bool = False,
):
    values = [(profile.name, getter(profile)) for profile in profiles]
    values.sort(key=lambda nv: nv[1], reverse=reverse)
    return values


def ranked_test_profiles_map(
    profiles: List[types.TestProfile],
    getter: Callable[[types.TestProfile], object],
    reverse: bool = False,
):
    return {
        name: value
        for (name, value) in sort_test_profiles(
            profiles=profiles, getter=getter, reverse=reverse
        )
    }


def get_test_profiles_value_map(
    profiles: List[types.TestProfile], getter: types.TestProfile2Counter
):
    freqmap = {}
    for profile in profiles:
        name = profile.name
        counter = getter(profile)
        for key, freq in counter.items():
            if not key in freqmap:
                freqmap[key] = {name: freq}
            elif not name in freqmap[key]:
                freqmap[key][name] = freq
            else:
                freqmap[key][name] += freq
    results = []
    for key, value_dist in freqmap.items():
        dist = {
            name: freq
            for (name, freq) in sorted(
                value_dist.items(), key=lambda kv: kv[1], reverse=True
            )
        }
        freq = sum(dist.values())
        freq_dist = types.FreqDist(freq=freq, dist=dist)
        error_profile = types.ValueProfile(value=key, freq_dist=freq_dist)
        results.append(error_profile)
    get_freq: types.ValueProfile2Int = lambda e: e.freq_dist.freq
    results.sort(key=get_freq, reverse=True)
    return results


def get_test_profiles_metadata(module: str, tests: list[types.Test], loops: int):
    test_names = [t.name for t in tests]
    return types.TestsProfile.Meta(
        module=str(module), loops=loops, test_names=test_names, tests=len(tests)
    )


def get_test_profiles_data(tests: List[types.Test], loops: int = 10, **params):

    profiles = form_test_profiles(tests=tests, loops=loops, **params)

    def get_times():
        get_mintime: types.TestProfile2Float = lambda p: p.time.min
        get_maxtime: types.TestProfile2Float = lambda p: p.time.max
        get_meantime: types.TestProfile2Float = lambda p: p.time.mean
        mins = ranked_test_profiles_map(profiles=profiles, getter=get_mintime)
        maxs = ranked_test_profiles_map(
            profiles=profiles, getter=get_maxtime, reverse=True
        )
        means = ranked_test_profiles_map(profiles=profiles, getter=get_meantime)
        return dict(mins=mins, maxs=maxs, means=means)

    def get_success_rate():
        getter: types.TestProfile2Float = lambda p: p.data.success_rate
        return ranked_test_profiles_map(profiles=profiles, getter=getter, reverse=True)

    def get_errors():
        getter: types.TestProfile2Counter = lambda p: p.data.errors.freqs
        return get_test_profiles_value_map(profiles=profiles, getter=getter)

    def get_values():
        getter: types.TestProfile2Counter = lambda p: p.data.values.freqs
        return get_test_profiles_value_map(profiles=profiles, getter=getter)

    success_rate = get_success_rate()
    times = get_times()
    errors = get_errors()
    values = get_values()

    return types.TestsProfile.Data(
        times=times,
        profiles=profiles,
        success_rate=success_rate,
        errors=errors,
        values=values,
    )


def get_module_tests_profile(
    module: str = "__name__", test_prefix: str = "test_", loops: int = 10, **params
):
    tests: List[types.Test] = module_tests(module, test_prefix=test_prefix)
    meta = get_test_profiles_metadata(module=module, tests=tests, loops=loops)
    data = get_test_profiles_data(tests=tests, loops=loops, **params)
    return types.TestsProfile(meta=meta, data=data)
