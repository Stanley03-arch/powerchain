from powerchain.core.runnables.base import Runnable, Sequential, FunctionRunnable


class Double(Runnable):
    def invoke(self, input: int, **kwargs) -> int:
        return input * 2


class AddTen(Runnable):
    def invoke(self, input: int, **kwargs) -> int:
        return input + 10


def test_sequential():
    pipeline = Double() | AddTen()
    assert pipeline.invoke(5) == 20  # (5*2)+10


def test_function_runnable():
    fn = FunctionRunnable(lambda x: x.upper())
    assert fn.invoke("hello") == "HELLO"
