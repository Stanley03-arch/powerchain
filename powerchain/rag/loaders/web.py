from __future__ import annotations

from typing import List, Optional
from urllib.parse import urlparse

from powerchain.rag.documents import Document
from powerchain.rag.loaders.base import BaseLoader


class WebLoader(BaseLoader):
    """Load text content from a web page.

    Uses httpx + a simple HTML-to-text extraction (no heavy dependencies).
    """

    def __init__(self, url: str, timeout: float = 15.0):
        self.url = url
        self.timeout = timeout

    def load(self) -> List[Document]:
        try:
            import httpx
        except ImportError as e:
            raise ImportError("httpx is required for WebLoader") from e

        response = httpx.get(self.url, timeout=self.timeout, follow_redirects=True)
        response.raise_for_status()
        html = response.text

        text = _html_to_text(html)
        title = _extract_title(html) or self.url

        return [
            Document(
                page_content=text.strip(),
                metadata={
                    "source": self.url,
                    "title": title,
                    "domain": urlparse(self.url).netloc,
                },
            )
        ]


def _extract_title(html: str) -> Optional[str]:
    import re
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return None


def _html_to_text(html: str) -> str:
    """Very lightweight HTML to text (good enough for many pages)."""
    import re

    # Remove scripts and styles
    html = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    # Replace common block tags with newlines
    html = re.sub(r"</?(p|div|br|h[1-6]|li|tr)[^>]*>", "\n", html, flags=re.IGNORECASE)
    # Strip remaining tags
    text = re.sub(r"<[^>]+>", " ", html)
    # Collapse whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()
