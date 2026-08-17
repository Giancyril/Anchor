import re
from typing import List, Dict, Any, Optional
import httpx
from bs4 import BeautifulSoup
from langchain_core.documents import Document

class WebCrawler:
    """
    Crawls web documentation pages and XML sitemaps, extracting clean textual content.
    """
    def __init__(self, user_agent: str = "Anchor-KBCrawler/2.0"):
        self.headers = {"User-Agent": user_agent}

    def clean_html(self, html_content: str, url: str) -> Document:
        """Strips scripts, styles, headers, and footers, extracting main article text."""
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove clutter elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript"]):
            element.decompose()

        title = soup.title.string.strip() if soup.title and soup.title.string else url

        # Find main content container
        main = soup.find("main") or soup.find("article") or soup.find("body") or soup
        text = main.get_text(separator="\n", strip=True)

        # Normalize multiple newlines
        cleaned_text = re.sub(r"\n{3,}", "\n\n", text)

        return Document(
            page_content=f"# {title}\n\n{cleaned_text}",
            metadata={
                "source_url": url,
                "document_name": title,
                "format": "html",
            }
        )

    async def crawl_url(self, url: str) -> Optional[Document]:
        """Fetch and parse a single web page."""
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            try:
                res = await client.get(url, headers=self.headers)
                if res.status_code == 200:
                    return self.clean_html(res.text, url)
            except Exception:
                pass
        return None

web_crawler = WebCrawler()