import sys

import pytest

from impersonation import impersonate


@impersonate
class FooClass:
    arg2 = "arg2"

    def __init__(self):
        self.arg1 = "arg1"

    def method1(self):
        return self.arg1

    @classmethod
    def method2(cls):
        return cls.arg2

    @staticmethod
    def method3():
        return "arg3"


def test_impersonate_default_args_class():
    assert FooClass().method1() == "arg1"
    assert FooClass().method2() == "arg2"
    assert FooClass.method2() == "arg2"
    assert FooClass().method3() == "arg3"
    assert FooClass.method3() == "arg3"


class FooClass2:
    arg2 = "arg2"

    def __init__(self):
        self.arg1 = "arg1"

    @impersonate
    def method1(self):
        return self.arg1

    @classmethod
    @impersonate
    def method2(cls):
        return cls.arg2

    @staticmethod
    @impersonate
    def method3():
        return "arg3"


def test_impersonate_default_args_methods():
    assert FooClass2().method1() == "arg1"
    assert FooClass2().method2() == "arg2"
    assert FooClass2.method2() == "arg2"
    assert FooClass2().method3() == "arg3"
    assert FooClass2.method3() == "arg3"


class FooClass3:
    arg2 = "arg2"

    def __init__(self):
        self.arg = "arg"

    @impersonate(username="fake-user")
    def method(self):
        return self.arg


@pytest.mark.skipif("pwd" not in sys.modules, reason="requires 'pwd'")
def test_impersonate_with_args(mocker):
    with pytest.raises(KeyError) as ex:
        FooClass3().method()
    assert "name not found: 'fake-user'" in str(ex.value)

    mocker.patch("impersonation.utils.pw_pair", return_value=(0, 0))
    with pytest.raises(PermissionError) as ex:
        FooClass3().method()
    assert "Operation not permitted" in str(ex.value)
