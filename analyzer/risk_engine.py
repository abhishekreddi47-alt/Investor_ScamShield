"""
Risk-Indicator Engine for Investor ScamShield.
Calculates the aggregate risk-indicator score capped at 100.
Assigns risk levels (LOW, MEDIUM, HIGH) with strict adherence to the Trust Rules.

CRITICAL TRUST RULES:
1. Never call it a "probability of scam" or "% chance of scam".
2. Never say "This person is definitely a scammer" or "This investment is fake".
3. Always display: "[Score] / 100 Risk Indicators" and the prototype disclaimer.
"""

from typing import List, Dict, Any


def calculate_risk(indicators: List[Dict[str, Any]], url_count: int = 0, claim_count: int = 0) -> Dict[str, Any]:
    """
    Computes prototype risk-indicator score based on detected warning indicators.
    Capped strictly at 100.
    """
    raw_score = sum(ind.get("weight", 0) for ind in indicators)

    # If suspicious shortened URLs were detected, give a modest +10 indicator weight
    # without automatically declaring fraud
    # (if not already covered)
    final_score = min(raw_score, 100)

    if final_score <= 20:
        level = "LOW"
        level_label_en = "LOW-RISK INDICATORS"
        level_label_kn = "ಕಡಿಮೆ ಅಪಾಯದ ಸೂಚನೆ"
        badge_color = "safe"  # green
        summary_en = "Few or no overt warning indicators were detected in this message."
        summary_kn = "ಈ ಸಂದೇಶದಲ್ಲಿ ಕಡಿಮೆ ಅಥವಾ ಯಾವುದೇ ಸ್ಪಷ್ಟ ಅಪಾಯದ ಸೂಚನೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ."
    elif final_score <= 50:
        level = "MEDIUM"
        level_label_en = "MEDIUM-RISK INDICATORS"
        level_label_kn = "ಮಧ್ಯಮ ಅಪಾಯದ ಸೂಚನೆ"
        badge_color = "warning"  # amber
        summary_en = "Suspicious characteristics or marketing pressure detected. Independent verification is strongly recommended."
        summary_kn = "ಅನುಮಾನಾಸ್ಪದ ಲಕ್ಷಣಗಳು ಅಥವಾ ಆತುರದ ಒತ್ತಡ ಕಂಡುಬಂದಿದೆ. ಸ್ವತಂತ್ರ ಪರಿಶೀಲನೆಯನ್ನು ಬಲವಾಗಿ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ."
    else:
        level = "HIGH"
        level_label_en = "HIGH-RISK INDICATORS"
        level_label_kn = "ಹೆಚ್ಚು ಅಪಾಯದ ಸೂಚನೆ"
        badge_color = "danger"  # red
        summary_en = "Multiple high-risk warning indicators detected. Do not transfer funds or share credentials without independent official verification."
        summary_kn = "ಹಲವಾರು ಗಂಭೀರ ಅಪಾಯದ ಸೂಚನೆಗಳು ಕಂಡುಬಂದಿವೆ. ಅಧಿಕೃತ ಪರಿಶೀಲನೆ ಇಲ್ಲದೆ ಹಣ ವರ್ಗಾಯಿಸಬೇಡಿ ಅಥವಾ ರಹಸ್ಯ ವಿವರಗಳನ್ನು ಹಂಚಿಕೊಳ್ಳಬೇಡಿ."

    trust_statement_en = "This is a prototype risk-indicator score, not a probability of scam and not investment advice."
    trust_statement_kn = "ಇದು ಮೂಲಮಾದರಿಯ (prototype) ಅಪಾಯ-ಸೂಚಕ ಅಂಕವಾಗಿದೆ, ಹಗರಣದ ಸಂಭವನೀಯತೆಯಲ್ಲ ಮತ್ತು ಹೂಡಿಕೆ ಸಲಹೆಯಲ್ಲ."

    honest_uncertainty_en = "Warning indicators detected. These indicators do not by themselves prove fraud, but independent verification is strongly recommended before taking any financial action."
    honest_uncertainty_kn = "ಅಪಾಯದ ಸೂಚನೆಗಳು ಕಂಡುಬಂದಿವೆ. ಈ ಸೂಚನೆಗಳು ಕೇವಲ ವಂಚನೆಯನ್ನು ಸಾಬೀತುಪಡಿಸುವುದಿಲ್ಲ, ಆದರೆ ಯಾವುದೇ ಹಣಕಾಸು ಕ್ರಮ ಕೈಗೊಳ್ಳುವ ಮೊದಲು ಸ್ವತಂತ್ರ ಪರಿಶೀಲನೆ ಅತ್ಯಗತ್ಯ."

    return {
        "score": final_score,
        "max_score": 100,
        "score_display": f"{final_score} / 100 Risk Indicators",
        "score_display_kn": f"{final_score} / 100 ಅಪಾಯದ ಸೂಚಕಗಳು",
        "level": level,
        "level_label_en": level_label_en,
        "level_label_kn": level_label_kn,
        "badge_color": badge_color,
        "summary_en": summary_en,
        "summary_kn": summary_kn,
        "trust_statement_en": trust_statement_en,
        "trust_statement_kn": trust_statement_kn,
        "honest_uncertainty_en": honest_uncertainty_en,
        "honest_uncertainty_kn": honest_uncertainty_kn,
        "total_indicators_count": len(indicators)
    }
