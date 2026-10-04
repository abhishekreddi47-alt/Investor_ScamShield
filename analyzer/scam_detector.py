"""
Scam Detection Engine for Investor ScamShield.
Rule-based detection using transparent regular expressions and keyword patterns.
Identifies suspicious indicators and extracts matching evidence.
"""

import re

# Comprehensive indicators specifications conforming to Hackathon guidelines
INDICATOR_RULES = [
    {
        "id": "GUARANTEED_RETURNS",
        "name_en": "Guaranteed-return language",
        "name_kn": "ಖಚಿತವಾದ ಲಾಭದ ಭರವಸೆ",
        "weight": 30,
        "explanation_en": "Promises of guaranteed or assured returns are an important warning sign. Legitimate capital market investments always involve market risk.",
        "explanation_kn": "ಖಚಿತವಾದ ಅಥವಾ ಖಾತರಿಯ ಲಾಭದ ಭರವಸೆಗಳು ಅಪಾಯದ ಮುಖ್ಯ ಸೂಚನೆಯಾಗಿದೆ. ಅಧಿಕೃತ ಷೇರು ಮಾರುಕಟ್ಟೆ ಹೂಡಿಕೆಗಳು ಯಾವಾಗಲೂ ಮಾರುಕಟ್ಟೆ ಅಪಾಯಗಳಿಗೆ ಒಳಪಟ್ಟಿರುತ್ತವೆ.",
        "patterns": [
            r'\bguaranteed\s+(?:(?:\d+%\s*)?(?:return|returns|profit|profits|income|gain|gains|growth|payout))\b',
            r'\bguaranteed\s+\d+%\b',
            r'\bassured\s+(?:(?:\d+%\s*)?(?:return|returns|profit|profits|gain|gains|income))\b',
            r'\bfixed\s+(?:return|returns|profit|profits|gain|income|payout)\b',
            r'\brisk[- ]free\s+(?:profit|profits|return|returns|investment)\b',
            r'\b100%\s*(?:safe|guaranteed|assured|risk[- ]free|profit|returns)\b',
            r'\b(?:double|triple|10x|2x|3x|5x)\s+(?:your\s+money|investment|profit|in\s+\d+\s+days)\b',
            r'\b(?:daily|weekly|monthly)\s*(?:fixed|guaranteed)\s*profit\b',
            r'\bzero\s*risk\b'
        ]
    },
    {
        "id": "PAYMENT_REQUEST",
        "name_en": "Payment request",
        "name_kn": "ಹಣ ಪಾವತಿ ವಿನಂತಿ",
        "weight": 25,
        "explanation_en": "Verify payment requests independently before transferring money. Unsolicited payment instructions often bypass authorized banking settlement channels.",
        "explanation_kn": "ಹಣ ವರ್ಗಾಯಿಸುವ ಮೊದಲು ಪಾವತಿ ವಿನಂತಿಗಳನ್ನು ಸ್ವತಂತ್ರವಾಗಿ ಪರಿಶೀಲಿಸಿ. ಪರಿಶೀಲಿಸದ ಪಾವತಿ ಸೂಚನೆಗಳು ಅಧಿಕೃತ ಬ್ಯಾಂಕಿಂಗ್ ನಿಯಮಗಳನ್ನು ಮೀರಿರಬಹುದು.",
        "patterns": [
            r'\b(?:send|transfer|pay|deposit)\s+(?:money|funds|payment|cash|rupees|amount)\b',
            r'\b(?:send|pay\s+to|transfer\s+to)\s+(?:our|this)?\s*upi\b',
            r'\bupi\s*(?:id|payment)?\s*[:=]?\s*[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b',
            r'\b(?:send|transfer|deposit|invest|pay)\s*(?:rs\.?|inr|₹)?\s*[\d,]+',
            r'\b(?:gpay|google\s*pay|phonepe|paytm)\s*(?:number|transfer|payment)?\b',
            r'\b(?:transfer|deposit|send)\s+to\s+(?:this\s+)?account\b',
            r'\bpay\s+now\b',
            r'\baccount\s+number\b',
            r'\bifsc\s*code\b'
        ]
    },
    {
        "id": "CREDENTIAL_REQUEST",
        "name_en": "Credential request",
        "name_kn": "ರಹಸ್ಯ ವಿವರಗಳ (OTP/PIN) ವಿನಂತಿ",
        "weight": 25,
        "explanation_en": "Never share OTPs, passwords, PINs or CVVs with unknown contacts. Legitimate financial institutions and advisors will never request your security credentials.",
        "explanation_kn": "ಅಪರಿಚಿತರೊಂದಿಗೆ ಎಂದಿಗೂ OTP, ಪಾಸ್‌ವರ್ಡ್, PIN ಅಥವಾ CVV ಗಳನ್ನು ಹಂಚಿಕೊಳ್ಳಬೇಡಿ. ಅಧಿಕೃತ ಹಣಕಾಸು ಸಂಸ್ಥೆಗಳು ನಿಮ್ಮ ರಹಸ್ಯ ವಿವರಗಳನ್ನು ಎಂದಿಗೂ ಕೇಳುವುದಿಲ್ಲ.",
        "patterns": [
            r'\b(?:share|send|enter|give|provide)\s*(?:your)?\s*(?:otp|one\s*time\s*password)\b',
            r'\b(?:share|send|provide|give)\s*(?:your)?\s*(?:pin|atm\s*pin|mpin|cvv|password|passcode)\b',
            r'\b(?:send|share)\s+(?:your\s+)?(?:otp|pin|password|cvv)\b',
            r'\b(?:netbanking|banking|demat|trading)\s*(?:password|login|credentials)\b',
            r'\bcard\s*(?:cvv|expiry|number)\b',
            r'\b(?:otp|one\s*time\s*password)\s+(?:and|or)\s+(?:pin|password|cvv)\b'
        ]
    },
    {
        "id": "REGULATORY_CLAIM",
        "name_en": "Regulatory claim",
        "name_kn": "ನಿಯಂತ್ರಕ ಮಂಡಳಿ ಹಕ್ಕು (SEBI / RBI)",
        "weight": 20,
        "explanation_en": "Regulatory claim detected. Verify independently using official sources. Fraudsters frequently fabricate badges, fake license numbers, and counterfeit certificates.",
        "explanation_kn": "ನಿಯಂತ್ರಕ ಮಂಡಳಿ (SEBI / RBI) ಹಕ್ಕು ಕಂಡುಬಂದಿದೆ. ಅಧಿಕೃತ ಮೂಲಗಳ ಮೂಲಕ ಸ್ವತಂತ್ರವಾಗಿ ಪರಿಶೀಲಿಸಿ. ನಕಲಿ ಪ್ರಮಾಣಪತ್ರಗಳು ಮತ್ತು ನೋಂದಣಿ ಸಂಖ್ಯೆಗಳನ್ನು ಮೋಸಗಾರರು ಬಳಸಬಹುದು.",
        "patterns": [
            r'\bsebi\b',
            r'\brbi\b',
            r'\bnsdl\b',
            r'\bcdsl\b',
            r'\b(?:sebi|rbi)\s*(?:registered|approved|certified|licensed|authorized|expert|analyst|advisor)\b',
            r'\b(?:government|govt)\s*(?:approved|backed|certified|registered)\b',
            r'\blicensed\s+(?:broker|advisor|expert)\b',
            r'\bregistered\s+(?:advisor|expert|analyst|entity)\b'
        ]
    },
    {
        "id": "REMOTE_ACCESS",
        "name_en": "Remote access request",
        "name_kn": "ರಿಮೋಟ್ ಪ್ರವೇಶ ವಿನಂತಿ (AnyDesk / TeamViewer)",
        "weight": 20,
        "explanation_en": "Do not give unknown people remote access to your device. Remote-control applications can allow attackers to observe passwords or drain banking accounts.",
        "explanation_kn": "ಅಪರಿಚಿತ ವ್ಯಕ್ತಿಗಳಿಗೆ ನಿಮ್ಮ ಮೊಬೈಲ್ ಅಥವಾ ಕಂಪ್ಯೂಟರ್‌ಗೆ ರಿಮೋಟ್ ಪ್ರವೇಶವನ್ನು ನೀಡಬೇಡಿ. ರಿಮೋಟ್ ಅಪ್ಲಿಕೇಶನ್‌ಗಳು ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ವಿವರಗಳನ್ನು ಕದಿಯಲು ಕಾರಣವಾಗಬಹುದು.",
        "patterns": [
            r'\b(?:anydesk|any\s*desk)\b',
            r'\b(?:teamviewer|team\s*viewer)\b',
            r'\bquicksupport\b',
            r'\bremote\s+(?:access|control|desktop|support)\b',
            r'\b(?:share|show)\s+(?:your)?\s*screen\b',
            r'\binstall\s+(?:app|application|software)\s+to\s+(?:help|assist|verify|invest)\b'
        ]
    },
    {
        "id": "URGENCY_PRESSURE",
        "name_en": "Urgency / pressure",
        "name_kn": "ಆತುರ / ತುರ್ತು ಒತ್ತಡ",
        "weight": 15,
        "explanation_en": "Pressure to act quickly can reduce the time available to verify a claim. High-pressure tactics are designed to trigger impulsive financial transactions.",
        "explanation_kn": "ತಕ್ಷಣ ಕ್ರಮ ಕೈಗೊಳ್ಳಲು ಒತ್ತಡ ಹೇರುವುದು ಪರಿಶೀಲನೆಗೆ ಸಮಯವನ್ನು ಕಡಿಮೆ ಮಾಡುತ್ತದೆ. ಅವಸರದಲ್ಲಿ ತಪ್ಪು ನಿರ್ಧಾರಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳುವಂತೆ ಪ್ರಚೋದಿಸಲು ಈ ತಂತ್ರ ಬಳಸಲಾಗುತ್ತದೆ.",
        "patterns": [
            r'\bact\s+now\b',
            r'\binvest\s+today\b',
            r'\b(?:only\s+)?(?:for\s+)?\d+\s*(?:hours|hrs|minutes|mins)\b',
            r'\blimited\s+time(?:\s+offer)?\b',
            r'\blast\s+chance\b',
            r'\bsend\s+immediately\b',
            r'\b(?:send|transfer|deposit|pay)[^\n.!?]{0,35}immediately\b',
            r'\bhurry\s+up\b',
            r'\boffer\s+(?:ends|expires)\b',
            r'\b(?:few|only\s*\d+)\s+slots?\s*(?:left|remaining)\b',
            r'\bdon\'?t\s+miss\s+out\b',
            r'\bimmediate\s+(?:action|transfer|joining)\b'
        ]
    },
    {
        "id": "SECRET_INSIDER_TIP",
        "name_en": "Secret / insider tip",
        "name_kn": "ರಹಸ್ಯ ಅಥವಾ ಆಂತರಿಕ ಸಲಹೆ",
        "weight": 10,
        "explanation_en": "Secret or exclusive investment claims can be used to create false trust or urgency. Trading on true insider information is illegal, and unsolicited tips are often pump-and-dump traps.",
        "explanation_kn": "ರಹಸ್ಯ ಅಥವಾ ವಿಶೇಷ ಹೂಡಿಕೆಯ ಹೇಳಿಕೆಗಳು ನಕಲಿ ನಂಬಿಕೆ ಅಥವಾ ಆತುರವನ್ನು ಸೃಷ್ಟಿಸಲು ಬಳಸಲ್ಪಡುತ್ತವೆ. ಆಂತರಿಕ ಮಾಹಿತಿ ಆಧಾರಿತ ವಹಿವಾಟು ಕಾನೂನುಬಾಹಿರವಾಗಿದೆ.",
        "patterns": [
            r'\bsecret\s+(?:[a-zA-Z]+\s+)?tip(?:s)?\b',
            r'\binsider\s+(?:[a-zA-Z]+\s+)?tip(?:s)?\b',
            r'\binsider\s+(?:info|information|leak|news)\b',
            r'\bsure[- ]shot\s+(?:profit|tip|call)\b',
            r'\bconfidential\s+opportunity\b',
            r'\bhidden\s+(?:[a-zA-Z]+\s+)?tip(?:s)?\b',
            r'\bexclusive\s+opportunity\b',
            r'\bjackpot\s+(?:call|tip|share|stock)\b',
            r'\boperator\s+(?:leak|game|call)\b'
        ]
    },
    {
        "id": "TIP_GROUP",
        "name_en": "Telegram / WhatsApp tip group",
        "name_kn": "ಟೆಲಿಗ್ರಾಮ್ / ವಾಟ್ಸಾಪ್ ಟಿಪ್ಸ್ ಗ್ರೂಪ್",
        "weight": 10,
        "explanation_en": "Investment tip groups can use social proof and repeated messages to create pressure. Coordinated admins and bots often fabricate fake testimonials of profits.",
        "explanation_kn": "ಹೂಡಿಕೆ ಟಿಪ್ಸ್ ಗ್ರೂಪ್‌ಗಳು ನಕಲಿ ಜನಪ್ರಿಯತೆ ಮತ್ತು ಪುನರಾವರ್ತಿತ ಸಂದೇಶಗಳ ಮೂಲಕ ಒತ್ತಡ ಹೇರಬಹುದು. ಗುಂಪಿನಲ್ಲಿರುವ ಇತರರು ನಕಲಿ ಲಾಭದ ಸಂದೇಶಗಳನ್ನು ಹಾಕಬಹುದು.",
        "patterns": [
            r'\btelegram\s+(?:group|channel|link|vip)\b',
            r'\bwhatsapp\s+(?:group|chat|link|community)\b',
            r'\b(?:join|join\s+our)\s+(?:[a-zA-Z]+\s+)?(?:telegram|whatsapp|channel|vip\s+group|group)\b',
            r'\b(?:stock|share|investment|crypto|forex)\s+tips?\b',
            r'\bpremium\s+(?:channel|group|calls)\b',
            r'\bt\.me/[a-zA-Z0-9_\+]+',
            r'\bchat\.whatsapp\.com/[a-zA-Z0-9_\+]+'
        ]
    }
]


def detect_indicators(text: str) -> list[dict]:
    """
    Evaluates text against scam indicators.
    Returns list of matched indicators with weight, explanation, and matched snippets.
    """
    if not text:
        return []

    detected = []

    for rule in INDICATOR_RULES:
        matched_snippets = []
        for pattern_str in rule["patterns"]:
            matches = list(re.finditer(pattern_str, text, re.IGNORECASE))
            for m in matches:
                matched_snippets.append(m.group(0).strip())

        if matched_snippets:
            # Deduplicate matched snippets
            unique_snippets = list(dict.fromkeys(matched_snippets))
            detected.append({
                "id": rule["id"],
                "name_en": rule["name_en"],
                "name_kn": rule["name_kn"],
                "weight": rule["weight"],
                "explanation_en": rule["explanation_en"],
                "explanation_kn": rule["explanation_kn"],
                "matched_snippets": unique_snippets[:5]  # limit to first 5
            })

    return detected
