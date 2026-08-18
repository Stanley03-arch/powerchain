from powerchain import ConversationMemory, ChatMessage, Role


def test_conversation_memory():
    mem = ConversationMemory(max_messages=4)
    mem.add_user("Hello")
    mem.add_assistant("Hi there")
    mem.add_user("How are you?")

    messages = mem.get_messages()
    assert len(messages) == 3
    assert messages[0].role == Role.USER
    assert messages[0].content == "Hello"
    assert messages[1].role == Role.ASSISTANT


def test_memory_trim():
    mem = ConversationMemory(max_messages=2)
    mem.add_user("one")
    mem.add_assistant("two")
    mem.add_user("three")
    mem.add_assistant("four")

    messages = mem.get_messages()
    assert len(messages) == 2
    assert messages[0].content == "three"
    assert messages[1].content == "four"
