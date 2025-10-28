import os
from typing import List, Optional

import requests


class LinkedInSearcher:
    def __init__(self, engine: str = "duckduckgo", max_results: int = 5):
        self.engine = engine
        self.max_results = max_results
        if self.engine == "serpapi":
            if not os.getenv("SERPAPI_KEY"):
                raise ValueError("SERPAPI_KEY env var is required for serpapi engine")

    def search(self, query: str) -> List[str]:
        if self.engine == "serpapi":
            return self._search_serpapi(query)
        return self._search_duckduckgo(query)

    def _search_duckduckgo(self, query: str) -> List[str]:
        # Uses DuckDuckGo Instant Answer API as a light-weight fallback; not perfect.
        # We'll also try html endpoint for results.
        urls = []
        try:
            resp = requests.get(
                "https://duckduckgo.com/html/",
                params={"q": query},
                timeout=20,
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
                },
            )
            resp.raise_for_status()
            html = resp.text
            # Very light parsing to extract result links
            # Avoid heavy dependencies; simple heuristic
            import re

            for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"', html):
                href = m.group(1)
                # DuckDuckGo sometimes returns redirect like "/l/?kh=-1&uddg=<encoded>"
                if href.startswith("/l/?"):
                    from urllib.parse import parse_qs, urlparse, unquote

                    qs = parse_qs(urlparse(href).query)
                    uddg = qs.get("uddg", [""])[0]
                    if uddg:
                        href = unquote(uddg)
                if "linkedin.com/in" in href or "linkedin.com/pub" in href:
                    urls.append(href)
                    if len(urls) >= self.max_results:
                        break
        except Exception:
            pass
        return urls

    def _search_serpapi(self, query: str) -> List[str]:
        key = os.environ["SERPAPI_KEY"]
        params = {
            "engine": "google",
            "q": query,
            "num": self.max_results,
            "api_key": key,
        }
        try:
            resp = requests.get("https://serpapi.com/search.json", params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            urls = []
            for item in data.get("organic_results", []):
                link = item.get("link")
                if link and "linkedin.com/in" in link:
                    urls.append(link)
            return urls[: self.max_results]
        except Exception:
            return []
