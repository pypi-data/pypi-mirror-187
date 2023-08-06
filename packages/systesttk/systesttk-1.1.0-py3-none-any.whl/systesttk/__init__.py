from .util import get_module_tests_profile
if __name__ == "__main__":
    if get_module_tests_profile is None:
        print("import error")
