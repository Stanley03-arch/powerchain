"""Example of Runnable composition in PowerChain."""

from powerchain.core.runnables.base import Runnable, FunctionRunnable, Sequential


class UpperCase(Runnable):
    def invoke(self, input: str, **kwargs) -> str:
        return input.upper()


class AddExclamation(Runnable):
    def invoke(self, input: str, **kwargs) -> str:
        return input + "!"


def main():
    pipeline = UpperCase() | AddExclamation() | FunctionRunnable(lambda x: f"Result: {x}")

    print(pipeline.invoke("hello powerchain"))
    # Output: Result: HELLO POWERCHAIN!


if __name__ == "__main__":
    main()
