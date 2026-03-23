"""WebWeaveX Parser - Deterministic HTML parsing."""

from bs4 import BeautifulSoup
from typing import Optional, Dict, Any, List

from .config import DEFAULT_CONFIG


class Parser:
    """HTML parser with deterministic text extraction."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        cfg = config or DEFAULT_CONFIG
        self.parse_config = cfg.get("parse", DEFAULT_CONFIG["parse"])
        self.extract_visible_text = self.parse_config.get("extract_visible_text", True)
        self.remove_scripts = self.parse_config.get("remove_scripts", True)
        self.remove_styles = self.parse_config.get("remove_styles", True)
        self.remove_comments = self.parse_config.get("remove_comments", True)
        self.remove_hidden = self.parse_config.get("remove_hidden", True)

    def parse(self, html: str, url: Optional[str] = None) -> str:
        """Parse HTML and extract visible text deterministically."""
        if not html:
            return ""

        soup = BeautifulSoup(html, "html.parser")

        if self.remove_scripts:
            for script in soup.find_all("script"):
                script.decompose()

        if self.remove_styles:
            for style in soup.find_all("style"):
                style.decompose()

        if self.remove_comments:
            for comment in soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith("<!--")):
                comment.extract()

        if self.remove_hidden:
            for tag in soup.find_all(style=True):
                if "display:none" in tag.get("style", "").lower() or "visibility:hidden" in tag.get("style", "").lower():
                    tag.decompose()

        if self.extract_visible_text:
            return self._extract_visible_text(soup)

        return soup.get_text()

    def _extract_visible_text(self, soup: BeautifulSoup) -> str:
        """Extract visible text in deterministic order."""
        skip_tags = frozenset({"script", "style", "noscript", "iframe", "svg", "head", "meta", "link"})
        text_parts: List[str] = []

        for element in soup.descendants:
            if element.name in skip_tags:
                continue
            if hasattr(element, 'name') and element.name is None:
                continue
            if isinstance(element, str):
                text = element.strip()
                if text and len(text) > 0:
                    parent = getattr(element, 'parent', None)
                    if parent and getattr(parent, 'name', None) not in skip_tags:
                        text_parts.append(text)

        result = " ".join(text_parts)
        result = result.replace("\xa0", " ")
        result = result.replace("\u200b", "")

        return result

    def extract_title(self, html: str) -> str:
        """Extract page title."""
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title")
        if title_tag:
            return title_tag.get_text().strip()
        return ""

    def extract_metadata(self, html: str) -> Dict[str, str]:
        """Extract metadata from HTML."""
        soup = BeautifulSoup(html, "html.parser")
        metadata = {}

        title_tag = soup.find("title")
        if title_tag:
            metadata["title"] = title_tag.get_text().strip()

        for meta in soup.find_all("meta"):
            name = meta.get("name") or meta.get("property", "")
            content = meta.get("content", "")
            if name and content:
                metadata[name] = content

        return metadata
