from powerchain import tool, Tool


def test_tool_decorator():
    @tool
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    assert isinstance(add, Tool)
    assert add.name == "add"
    assert "Add two numbers" in add.description
    assert add.run(a=2, b=3) == 5


def test_tool_openai_schema():
    @tool
    def greet(name: str) -> str:
        """Greet someone."""
        return f"Hello {name}"

    schema = greet.to_openai_tool()
    assert schema["type"] == "function"
    assert schema["function"]["name"] == "greet"
    assert "name" in schema["function"]["parameters"]["properties"]
