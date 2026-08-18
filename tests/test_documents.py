from powerchain import Document, RecursiveCharacterTextSplitter


def test_document():
    doc = Document(page_content="Hello world", metadata={"source": "test"})
    assert doc.page_content == "Hello world"
    assert doc.metadata["source"] == "test"


def test_splitter():
    splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
    text = "A" * 120
    chunks = splitter.split_text(text)
    assert len(chunks) >= 2
    assert all(len(c) <= 60 for c in chunks)  # rough upper bound
