from typing import Optional, Tuple
import requests
import re


LINKEDIN_PROFILE_RE = re.compile(r"^https?://(www\.)?linkedin\.com/(in|pub)/[^/?#]+/?")


def validate_linkedin_url(url: str, user_agent: Optional[str] = None, timeout: int = 15) -> bool:
    if not isinstance(url, str):
        return False
    url = url.strip()
    if not LINKEDIN_PROFILE_RE.match(url):
        return False

    headers = {
        "User-Agent": user_agent
        or "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
    }
    try:
        # HEAD often blocked; use GET with allow_redirects to confirm 200/OK-ish
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        # LinkedIn sometimes returns 999 for bot protection; treat as existent
        if resp.status_code in (200, 301, 302, 999):
            return True
        # Some responses redirect to authwall, which implies the profile exists
        final_url = resp.url or url
        if "linkedin.com/authwall" in final_url:
            return True
        return False
    except Exception:
        return False


def fetch_profile_latest_job(url: str, user_agent: Optional[str] = None, timeout: int = 15) -> Tuple[str, str]:
    headers = {
        "User-Agent": user_agent
        or "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if resp.status_code not in (200, 301, 302):
            return "", ""
        html = resp.text
        # Heuristic scraping without login; LinkedIn hides details behind authwall often.
        # Try to extract current role/company from OpenGraph/meta if present
        # e.g., <meta property="og:title" content="John Doe - Senior Engineer - ACME | LinkedIn">
        m = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', html)
        if m:
            content = m.group(1)
            # Pattern like "Name - Title - Company | LinkedIn"
            parts = [p.strip() for p in content.replace("| LinkedIn", "").split(" - ")]
            if len(parts) >= 3:
                # name, title, company
                return parts[-1], parts[-2]
        # Fallback: try JSON-LD
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
        if m:
            import json

            try:
                data = json.loads(m.group(1))
                # Try typical fields
                job_title = data.get("jobTitle") or ""
                works_for = data.get("worksFor")
                company = ""
                if isinstance(works_for, dict):
                    company = works_for.get("name") or ""
                elif isinstance(works_for, str):
                    company = works_for
                return company or "", job_title or ""
            except Exception:
                pass
        return "", ""
    except Exception:
        return "", ""
