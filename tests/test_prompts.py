from powerchain import PromptTemplate


def test_prompt_template():
    tmpl = PromptTemplate("Hello {name}, you are {age} years old.")
    result = tmpl.format(name="Stanley", age=25)
    assert result == "Hello Stanley, you are 25 years old."


def test_prompt_partial():
    tmpl = PromptTemplate("Hello {name}, welcome to {place}.")
    partial = tmpl.partial(place="Nairobi")
    result = partial.format(name="Stanley")
    assert "Nairobi" in result
    assert "Stanley" in result
