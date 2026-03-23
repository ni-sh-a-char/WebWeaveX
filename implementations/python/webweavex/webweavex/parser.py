"""HTML parser for WebWeaveX."""

from bs4 import BeautifulSoup
from typing import Dict, Any, Optional

from .config import DEFAULT_CONFIG, get_config


class Parser:
    """HTML parser that extracts visible text."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the parser."""
        cfg = config or DEFAULT_CONFIG
        self.parse_config = cfg.get("parse", DEFAULT_CONFIG.get("parse", {}))
        self.extract_visible_text = self.parse_config.get("extract_visible_text", True)
        self.remove_scripts = self.parse_config.get("remove_scripts", True)
        self.remove_styles = self.parse_config.get("remove_styles", True)
        self.remove_comments = self.parse_config.get("remove_comments", True)
        self.remove_hidden = self.parse_config.get("remove_hidden", True)

    def parse(self, html: str, url: Optional[str] = None) -> str:
        """Parse HTML and extract visible text."""
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

        if self.extract_visible_text:
            return self._extract_visible_text(soup)

        return soup.get_text()

    def extract_title(self, html: str) -> str:
        """Extract page title from HTML."""
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("title")
        if title:
            return title.get_text().strip()
        return ""

    def _extract_visible_text(self, soup: BeautifulSoup) -> str:
        """Extract visible text from parsed HTML."""
        text_parts = []

        for element in soup.descendants:
            if element.name in ("script", "style", "noscript", "iframe", "svg", "path", "img", "video", "audio", "canvas"):
                continue

            if isinstance(element, str):
                text = element.strip()
                if text:
                    parent = getattr(element, 'parent', None)
                    if parent and parent.name not in ("script", "style", "head", "meta", "link", "noscript"):
                        text_parts.append(element)

        text = " ".join(text_parts)
        text = text.replace("\xa0", " ")
        
        return text

    def extract_metadata(self, html: str, url: Optional[str] = None) -> Dict[str, Any]:
        """Extract metadata from HTML."""
        soup = BeautifulSoup(html, "html.parser")
        metadata = {}

        title = soup.find("title")
        if title:
            metadata["title"] = title.get_text().strip()

        meta_tags = soup.find_all("meta")
        for meta in meta_tags:
            name = meta.get("name") or meta.get("property", "")
            content = meta.get("content", "")
            if name and content:
                metadata[name] = content

        return metadata
