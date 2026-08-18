from pydantic import BaseModel
from powerchain.core.output_parsers import JsonOutputParser, ListOutputParser, PydanticOutputParser


def test_json_parser():
    parser = JsonOutputParser()
    text = '```json\n{"name": "PowerChain", "version": 1}\n```'
    data = parser.parse(text)
    assert data["name"] == "PowerChain"
    assert data["version"] == 1


def test_list_parser():
    parser = ListOutputParser()
    text = "1. First item\n2. Second item\n- Third item"
    items = parser.parse(text)
    assert len(items) == 3
    assert items[0] == "First item"


def test_pydantic_parser():
    class Person(BaseModel):
        name: str
        age: int

    parser = PydanticOutputParser(Person)
    text = '{"name": "Stanley", "age": 25}'
    person = parser.parse(text)
    assert person.name == "Stanley"
    assert person.age == 25
