"""
URL & Link Analyzer for Investor ScamShield.
Identifies links, shortened URLs, insecure connections, and suspicious characteristics.
Follows the trust rule: Never automatically label a domain fraudulent only because
it is shortened or unusual.
"""

import re
from urllib.parse import urlparse

# Common URL shorteners frequently used in unsolicited messaging
SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "ow.ly",
    "buff.ly", "rebrand.ly", "tiny.cc", "rb.gy", "shorturl.at",
    "t.me", "wa.me", "chat.whatsapp.com"
}

# Suspicious or high-risk TLDs commonly leveraged in bulk spam campaigns
UNUSUAL_TLDS = {
    ".top", ".xyz", ".click", ".loan", ".vip", ".work", ".stream",
    ".gq", ".cf", ".tk", ".ml", ".ga", ".buzz", ".cam", ".download"
}

URL_REGEX = re.compile(
    r'(?:https?://|www\.)[^\s<>"\'{}|\\^`]+|(?:[a-zA-Z0-9-]+\.)+(?:com|in|org|net|co|biz|io|xyz|top|vip|cc|ly|me)(?:/[^\s<>"\'{}|\\^`]*)?',
    re.IGNORECASE
)


def extract_urls(text: str) -> list[str]:
    """Finds all URLs and domain-like links in the text."""
    if not text:
        return []
    matches = URL_REGEX.findall(text)
    # Deduplicate while preserving order
    seen = set()
    cleaned = []
    for match in matches:
        m = match.strip('.,;!?:()"\'')
        if m and m not in seen:
            seen.add(m)
            cleaned.append(m)
    return cleaned


def analyze_url(url: str) -> dict:
    """
    Analyzes a single URL for warning signs.
    Returns details including whether it's shortened, insecure, or unusual.
    """
    normalized_url = url
    if not url.startswith("http://") and not url.startswith("https://"):
        normalized_url = "http://" + url

    try:
        parsed = urlparse(normalized_url)
        domain = (parsed.netloc or "").lower().split(":")[0]
    except Exception:
        domain = ""

    indicators = []
    is_shortened = False
    is_http_only = normalized_url.startswith("http://")
    has_unusual_tld = False
    is_direct_ip = False

    # Check for direct IP address in domain
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', domain):
        is_direct_ip = True
        indicators.append({
            "type": "IP_ADDRESS_URL",
            "title_en": "Direct IP address link detected",
            "title_kn": "ನೇರ IP ವಿಳಾಸದ ಲಿಂಕ್ ಕಂಡುಬಂದಿದೆ",
            "explanation_en": "The link uses a numeric IP address instead of a recognized domain name. Legitimate investment institutions almost always use branded domain names.",
            "explanation_kn": "ಲಿಂಕ್ ಗುರುತಿಸಲ್ಪಟ್ಟ ಡೊಮೇನ್ ಹೆಸರಿನ ಬದಲು ಸಂಖ್ಯಾತ್ಮಕ IP ವಿಳಾಸವನ್ನು ಬಳಸುತ್ತದೆ. ಅಧಿಕೃತ ಸಂಸ್ಥೆಗಳು ಅಧಿಕೃತ ಬ್ರಾಂಡ್ ಹೆಸರುಗಳನ್ನು ಬಳಸುತ್ತವೆ."
        })

    # Check for shortened URL
    for shortener in SHORTENER_DOMAINS:
        if domain == shortener or domain.endswith("." + shortener):
            is_shortened = True
            indicators.append({
                "type": "SHORTENED_URL",
                "title_en": "Shortened link detected",
                "title_kn": "ಸಂಕ್ಷಿಪ್ತ (Shortened) ಲಿಂಕ್ ಕಂಡುಬಂದಿದೆ",
                "explanation_en": "The final destination is hidden behind a shortener. Verify the destination independently before opening or entering credentials.",
                "explanation_kn": "ಅಂತಿಮ ಗಮ್ಯಸ್ಥಾನವನ್ನು ಮರೆಮಾಡಲಾಗಿದೆ. ಲಿಂಕ್ ತೆರೆಯುವ ಮೊದಲು ಅಥವಾ ವಿವರಗಳನ್ನು ನಮೂದಿಸುವ ಮೊದಲು ಗಮ್ಯಸ್ಥಾನವನ್ನು ಸ್ವತಂತ್ರವಾಗಿ ಪರಿಶೀಲಿಸಿ."
            })
            break

    # Check for unusual TLD
    for tld in UNUSUAL_TLDS:
        if domain.endswith(tld):
            has_unusual_tld = True
            indicators.append({
                "type": "UNUSUAL_DOMAIN_TLD",
                "title_en": f"Unusual domain extension ({tld}) detected",
                "title_kn": f"ಅಪರಿಚಿತ ಡೊಮೇನ್ ವಿಸ್ತರಣೆ ({tld}) ಕಂಡುಬಂದಿದೆ",
                "explanation_en": f"This link uses an unusual domain extension ({tld}). Official Indian financial institutions typically operate on .gov.in, .nic.in, or reputable .in/.com domains.",
                "explanation_kn": f"ಈ ಲಿಂಕ್ ಅಸಾಮಾನ್ಯ ಡೊಮೇನ್ ವಿಸ್ತರಣೆಯನ್ನು ({tld}) ಬಳಸುತ್ತದೆ. ಅಧಿಕೃತ ಭಾರತೀಯ ಹಣಕಾಸು ಸಂಸ್ಥೆಗಳು ಸಾಮಾನ್ಯವಾಗಿ .gov.in, .nic.in ಅಥವಾ ವಿಶ್ವಾಸಾರ್ಹ .in/.com ಡೊಮೇನ್‌ಗಳನ್ನು ಬಳಸುತ್ತವೆ."
            })
            break

    # Check for unencrypted HTTP
    if is_http_only and not is_shortened:
        indicators.append({
            "type": "INSECURE_HTTP",
            "title_en": "Unencrypted link (HTTP) detected",
            "title_kn": "ಅಸುರಕ್ಷಿತ ಲಿಂಕ್ (HTTP) ಕಂಡುಬಂದಿದೆ",
            "explanation_en": "The link does not appear to use HTTPS encryption. Financial and banking websites require HTTPS to safeguard your data.",
            "explanation_kn": "ಲಿಂಕ್ HTTPS ಎನ್‌ಕ್ರಿಪ್ಶನ್ ಬಳಸುತ್ತಿರುವಂತೆ ಕಂಡುಬರುತ್ತಿಲ್ಲ. ಬ್ಯಾಂಕಿಂಗ್ ಮತ್ತು ಹಣಕಾಸು ಜಾಲತಾಣಗಳಿಗೆ HTTPS ಕಡ್ಡಾಯವಾಗಿದೆ."
        })

    return {
        "url": url,
        "domain": domain,
        "is_shortened": is_shortened,
        "is_http_only": is_http_only,
        "has_unusual_tld": has_unusual_tld,
        "is_direct_ip": is_direct_ip,
        "indicators": indicators
    }


def analyze_all_urls(text: str) -> list[dict]:
    """Extracts and analyzes all URLs from text."""
    urls = extract_urls(text)
    return [analyze_url(u) for u in urls]
