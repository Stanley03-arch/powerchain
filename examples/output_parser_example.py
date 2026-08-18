"""
Structured output parsing with PowerChain.

Requires OPENAI_API_KEY.
"""

from pydantic import BaseModel, Field
from powerchain import ChatOpenAI, ChatMessage, Role
from powerchain.core.output_parsers import PydanticOutputParser, JsonOutputParser, ListOutputParser


class MovieReview(BaseModel):
    title: str = Field(description="Movie title")
    rating: float = Field(description="Rating from 0 to 10")
    summary: str = Field(description="Short summary of the review")
    pros: list[str] = Field(description="List of positive points")
    cons: list[str] = Field(description="List of negative points")


def main():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # --- Pydantic parser ---
    parser = PydanticOutputParser(MovieReview)
    prompt = (
        "Write a short review of the movie Inception.\n\n"
        f"{parser.get_format_instructions()}"
    )

    response = llm.invoke([ChatMessage(role=Role.USER, content=prompt)])
    review = parser.parse(response.content)

    print("=== Pydantic Parsed ===")
    print(f"Title: {review.title}")
    print(f"Rating: {review.rating}")
    print(f"Summary: {review.summary}")
    print(f"Pros: {review.pros}")
    print(f"Cons: {review.cons}")

    # --- List parser ---
    list_parser = ListOutputParser()
    response2 = llm.invoke([
        ChatMessage(role=Role.USER, content="List 4 benefits of using PowerChain. One per line.")
    ])
    items = list_parser.parse(response2.content)
    print("\n=== List Parsed ===")
    for i, item in enumerate(items, 1):
        print(f"{i}. {item}")


if __name__ == "__main__":
    main()
