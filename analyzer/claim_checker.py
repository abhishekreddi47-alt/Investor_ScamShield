"""
Claim Verifier for Investor ScamShield.
Detects regulatory and government endorsement claims (SEBI, RBI, Govt, NSDL, etc.).
Reminds users not to rely on badges, registration numbers, or sender-provided proofs.
Provides links and actionable guidance for independent verification.
"""

import re

# Regulatory claim patterns with contextual regexes
REGULATORY_PATTERNS = [
    {
        "authority": "SEBI",
        "regex": re.compile(
            r'\b(?:sebi\s*(?:registered|approved|certified|licensed|authorized|expert|analyst|advisor|advisory|officer|partner|guaranteed))\b|\b(?:registered\s+with\s+sebi)\b|\b(?:sebi\s+reg(?:\.|\s*no)?\b)',
            re.IGNORECASE
        ),
        "official_source_name": "Securities and Exchange Board of India (SEBI)",
        "official_url": "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes&intmId=13",
        "official_search_instructions_en": "Visit SEBI's official portal at sebi.gov.in -> 'Recognised Intermediaries' to verify if the individual or entity is genuinely registered.",
        "official_search_instructions_kn": "sebi.gov.in ನಲ್ಲಿರುವ SEBI ಯ ಅಧಿಕೃತ ಜಾಲತಾಣಕ್ಕೆ ಭೇಟಿ ನೀಡಿ, 'Recognised Intermediaries' ವಿಭಾಗದಲ್ಲಿ ಆ ವ್ಯಕ್ತಿ ಅಥವಾ ಸಂಸ್ಥೆ ನೈಜವಾಗಿ ನೋಂದಾಯಿತವಾಗಿದೆಯೇ ಎಂದು ಪರಿಶೀಲಿಸಿ."
    },
    {
        "authority": "RBI",
        "regex": re.compile(
            r'\b(?:rbi\s*(?:approved|authorized|licensed|registered|guaranteed|backed|certified))\b|\b(?:reserve\s+bank\s+of\s+india\s*(?:approved|authorized|registered))\b',
            re.IGNORECASE
        ),
        "official_source_name": "Reserve Bank of India (RBI) Sachet Portal",
        "official_url": "https://sachet.rbi.org.in/",
        "official_search_instructions_en": "Check the RBI Sachet portal (sachet.rbi.org.in) to verify registered non-banking financial entities or report unregistered deposit-taking schemes.",
        "official_search_instructions_kn": "ನೋಂದಾಯಿತ ಹಣಕಾಸು ಸಂಸ್ಥೆಗಳನ್ನು ಪರಿಶೀಲಿಸಲು ಅಥವಾ ಅನಧಿಕೃತ ಹೂಡಿಕೆ ಯೋಜನೆಗಳನ್ನು ವರದಿ ಮಾಡಲು RBI ಸಚೇತ್ (sachet.rbi.org.in) ಪೋರ್ಟಲ್ ಅನ್ನು ಪರಿಶೀಲಿಸಿ."
    },
    {
        "authority": "GOVERNMENT",
        "regex": re.compile(
            r'\b(?:govt|government)\s*(?:approved|backed|certified|authorized|scheme|guarantee)\b|\b(?:pm\s*scheme|modi\s*scheme|national\s*investment\s*scheme)\b',
            re.IGNORECASE
        ),
        "official_source_name": "Official Government Portals (.gov.in)",
        "official_url": "https://www.india.gov.in/",
        "official_search_instructions_en": "Official government schemes are announced strictly on official .gov.in websites or national press releases, never via direct WhatsApp or Telegram messages.",
        "official_search_instructions_kn": "ಅಧಿಕೃತ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಕೇವಲ .gov.in ಜಾಲತಾಣಗಳಲ್ಲಿ ಮಾತ್ರ ಪ್ರಕಟಿಸಲಾಗುತ್ತದೆ, ನೇರ ವಾಟ್ಸಾಪ್ ಅಥವಾ ಟೆಲಿಗ್ರಾಮ್ ಸಂದೇಶಗಳ ಮೂಲಕ ಅಲ್ಲ."
    },
    {
        "authority": "DEPOSITORY",
        "regex": re.compile(
            r'\b(?:nsdl|cdsl)\s*(?:approved|authorized|certified|partner|guaranteed)\b',
            re.IGNORECASE
        ),
        "official_source_name": "NSDL / CDSL Depositories",
        "official_url": "https://nsdl.co.in/",
        "official_search_instructions_en": "Verify Depository Participant (DP) status directly via official NSDL (nsdl.co.in) or CDSL (cdslindia.com) directories.",
        "official_search_instructions_kn": "ಅಧಿಕೃತ NSDL (nsdl.co.in) ಅಥವಾ CDSL (cdslindia.com) ಮುಖಾಂತರ ಡೆಪಾಸಿಟರಿ ಪಾರ್ಟಿಸಿಪೆಂಟ್ (DP) ಸ್ಥಿತಿಯನ್ನು ನೇರವಾಗಿ ಪರಿಶೀಲಿಸಿ."
    }
]


def detect_claims(text: str) -> list[dict]:
    """
    Scans input message for regulatory and authority claims.
    Returns structured claims with authority, matched text, and official verification guidance.
    """
    if not text:
        return []

    detected = []
    seen_authorities = set()

    for item in REGULATORY_PATTERNS:
        match = item["regex"].search(text)
        if match and item["authority"] not in seen_authorities:
            seen_authorities.add(item["authority"])
            detected.append({
                "authority": item["authority"],
                "matched_text": match.group(0),
                "official_source_name": item["official_source_name"],
                "official_url": item["official_url"],
                "notice_en": "Do not rely only on the registration number, certificate screenshot, badge, or link provided in the message. Verify the claim independently using official sources.",
                "notice_kn": "ಸಂದೇಶದಲ್ಲಿ ನೀಡಲಾದ ನೋಂದಣಿ ಸಂಖ್ಯೆ, ಪ್ರಮಾಣಪತ್ರದ ಸ್ಕ್ರೀನ್‌ಶಾಟ್, ಬ್ಯಾಡ್ಜ್ ಅಥವಾ ಲಿಂಕ್ ಅನ್ನು ಮಾತ್ರ ನಂಬಬೇಡಿ. ಅಧಿಕೃತ ಮೂಲಗಳನ್ನು ಬಳಸಿಕೊಂಡು ಸ್ವತಂತ್ರವಾಗಿ ಪರಿಶೀಲಿಸಿ.",
                "official_search_instructions_en": item["official_search_instructions_en"],
                "official_search_instructions_kn": item["official_search_instructions_kn"]
            })

    return detected
