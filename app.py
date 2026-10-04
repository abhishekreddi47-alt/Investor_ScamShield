"""
Investor ScamShield - Backend Flask Application
SANGYAN Investor Resilience Hackathon: Track A - Digital Fraud & Scam Resilience

A public-good investor-protection tool helping first-time and emerging investors,
especially from Tier-2/Tier-3 regions, recognize warning signs in suspicious financial messages
BEFORE transferring money.
"""

import os
import uuid
import tempfile
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from analyzer.scam_detector import detect_indicators
from analyzer.risk_engine import calculate_risk
from analyzer.url_checker import analyze_all_urls
from analyzer.claim_checker import detect_claims
from ocr.ocr_engine import extract_text_from_image, is_ocr_available

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static'),
    static_url_path='/static'
)

# Security & Upload Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'investor-scamshield-hackathon-2026')
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8 Megabytes maximum

# Safe upload directory using system temp directory (writable on Vercel /tmp and Windows)
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'investor_scamshield_uploads')
try:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
except Exception:
    UPLOAD_FOLDER = tempfile.gettempdir()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


SAFE_NEXT_STEPS_EN = [
    {
        "step": 1,
        "title": "Do not transfer money until the claim is independently verified.",
        "desc": "Never rush into payment under excitement or fear of missing out. Legitimate investment opportunities will not evaporate in a few hours."
    },
    {
        "step": 2,
        "title": "Never share OTPs, passwords, PINs or CVVs.",
        "desc": "No legitimate banker, SEBI advisor, or broker will ever request your login password, debit card PIN, or transaction OTP."
    },
    {
        "step": 3,
        "title": "Independently verify the person or organization using official sources.",
        "desc": "Check official registry directories like sebi.gov.in or sachet.rbi.org.in rather than trusting phone numbers or links sent in chats."
    },
    {
        "step": 4,
        "title": "Do not install remote-access applications at another person's request.",
        "desc": "Applications like AnyDesk, TeamViewer, or QuickSupport allow unauthorized parties to view and control your mobile screen and banking apps."
    },
    {
        "step": 5,
        "title": "Do not trust links or registration information supplied only by the sender.",
        "desc": "Badges, registration certificates, and ID cards can be easily fabricated with basic graphic design tools."
    },
    {
        "step": 6,
        "title": "If money has already been transferred, act immediately.",
        "desc": "Immediately dial the National Cyber Crime Helpline at 1930 or submit a formal report at cybercrime.gov.in within the golden hour to freeze transfers."
    }
]

SAFE_NEXT_STEPS_KN = [
    {
        "step": 1,
        "title": "ಸ್ವತಂತ್ರವಾಗಿ ಪರಿಶೀಲಿಸುವವರೆಗೆ ಹಣ ವರ್ಗಾವಣೆ ಮಾಡಬೇಡಿ.",
        "desc": "ಆತುರದಿಂದ ಅಥವಾ ಆಫರ್ ಮುಗಿದುಹೋಗುತ್ತದೆ ಎಂಬ ಭಯದಿಂದ ಹಣ ವರ್ಗಾವಣೆ ಮಾಡಬೇಡಿ. ಅಧಿಕೃತ ಹೂಡಿಕೆ ಅವಕಾಶಗಳು ಕೆಲವೇ ಗಂಟೆಗಳಲ್ಲಿ ಕಣ್ಮರೆಯಾಗುವುದಿಲ್ಲ."
    },
    {
        "step": 2,
        "title": "ಅಪರಿಚಿತರೊಂದಿಗೆ ಎಂದಿಗೂ OTP, ಪಾಸ್‌ವರ್ಡ್, PIN ಅಥವಾ CVV ಗಳನ್ನು ಹಂಚಿಕೊಳ್ಳಬೇಡಿ.",
        "desc": "ಯಾವುದೇ ಅಧಿಕೃತ ಬ್ಯಾಂಕರ್, SEBI ಸಲಹೆಗಾರ ಅಥವಾ ಬ್ರೋಕರ್ ನಿಮ್ಮ ಲಾಗಿನ್ ಪಾಸ್‌ವರ್ಡ್, ATM ಪಿನ್ ಅಥವಾ OTP ಯನ್ನು ಎಂದಿಗೂ ಕೇಳುವುದಿಲ್ಲ."
    },
    {
        "step": 3,
        "title": "ಅಧಿಕೃತ ಮೂಲಗಳನ್ನು ಬಳಸಿಕೊಂಡು ವ್ಯಕ್ತಿ ಅಥವಾ ಸಂಸ್ಥೆಯನ್ನು ಸ್ವತಂತ್ರವಾಗಿ ಪರಿಶೀಲಿಸಿ.",
        "desc": "ಸಂದೇಶದಲ್ಲಿ ಕಳುಹಿಸಲಾದ ಲಿಂಕ್‌ಗಳ ಬದಲು sebi.gov.in ಅಥವಾ sachet.rbi.org.in ನಂತಹ ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್‌ಗಳಲ್ಲಿ ಪರಿಶೀಲಿಸಿ."
    },
    {
        "step": 4,
        "title": "ಅಪರಿಚಿತರ ಕೋರಿಕೆಯ ಮೇರೆಗೆ ರಿಮೋಟ್ ಆಕ್ಸೆಸ್ ಅಪ್ಲಿಕೇಶನ್‌ಗಳನ್ನು ಇನ್‌ಸ್ಟಾಲ್ ಮಾಡಬೇಡಿ.",
        "desc": "AnyDesk, TeamViewer ಅಥವಾ QuickSupport ಅಪ್ಲಿಕೇಶನ್‌ಗಳು ಅಪರಿಚಿತರಿಗೆ ನಿಮ್ಮ ಫೋನ್ ಸ್ಕ್ರೀನ್ ನೋಡಲು ಮತ್ತು ಬ್ಯಾಂಕ್ ಖಾತೆ ನಿಯಂತ್ರಿಸಲು ಅವಕಾಶ ನೀಡುತ್ತವೆ."
    },
    {
        "step": 5,
        "title": "ಕಳುಹಿಸುವವರು ಮಾತ್ರ ನೀಡಿದ ಲಿಂಕ್ ಅಥವಾ ನೋಂದಣಿ ಮಾಹಿತಿಯನ್ನು ನಂಬಬೇಡಿ.",
        "desc": "ನಕಲಿ ಪ್ರಮಾಣಪತ್ರಗಳು, SEBI ಬ್ಯಾಡ್ಜ್‌ಗಳು ಮತ್ತು ಐಡಿ ಕಾರ್ಡ್‌ಗಳನ್ನು ಸುಲಭವಾಗಿ ಸೃಷ್ಟಿಸಬಹುದು."
    },
    {
        "step": 6,
        "title": "ಈಗಾಗಲೇ ಹಣ ವರ್ಗಾವಣೆ ಮಾಡಿದ್ದರೆ, ತಕ್ಷಣ ಕ್ರಮ ಕೈಗೊಳ್ಳಿ.",
        "desc": "ತಕ್ಷಣವೇ ರಾಷ್ಟ್ರೀಯ ಸೈಬರ್ ಅಪರಾಧ ಸಹಾಯವಾಣಿ 1930 ಗೆ ಕರೆ ಮಾಡಿ ಅಥವಾ cybercrime.gov.in ನಲ್ಲಿ ದೂರು ದಾಖಲಿಸಿ."
    }
]

DEMO_SCENARIOS = [
    {
        "id": "hackathon_demo",
        "title_en": "Hackathon Judge Demo (High Risk)",
        "title_kn": "ತೀರ್ಪುಗಾರರ ಡೆಮೊ (ಹೆಚ್ಚು ಅಪಾಯ)",
        "text": "🚨 SEBI REGISTERED EXPERT 🚨\n\nGuaranteed 40% return in 7 days!\n\nInvest ₹10,000 today.\n\nThis opportunity is available only for 2 hours.\n\nSend payment to our UPI ID immediately.\n\nJoin our Telegram group for secret stock tips."
    },
    {
        "id": "test_1",
        "title_en": "Test 1: Guaranteed Profit + Urgency + Payment",
        "title_kn": "ಪರೀಕ್ಷೆ 1: ಖಚಿತ ಲಾಭ + ತುರ್ತು + ಪಾವತಿ",
        "text": "Guaranteed 50% profit today. Send ₹20,000 immediately."
    },
    {
        "id": "test_2",
        "title_en": "Test 2: Regulatory Claim + Telegram + Secret Tip",
        "title_kn": "ಪರೀಕ್ಷೆ 2: SEBI ಹಕ್ಕು + ಟೆಲಿಗ್ರಾಮ್ ಗ್ರೂಪ್ + ರಹಸ್ಯ ಸಲಹೆ",
        "text": "SEBI registered advisor. Join our Telegram group for secret stock tips."
    },
    {
        "id": "test_3",
        "title_en": "Test 3: Remote Access (AnyDesk)",
        "title_kn": "ಪರೀಕ್ಷೆ 3: ರಿಮೋಟ್ ಪ್ರವೇಶ (AnyDesk)",
        "text": "Install AnyDesk and share your screen so we can help with your investment account."
    },
    {
        "id": "test_4",
        "title_en": "Test 4: Credential Request (OTP & PIN)",
        "title_kn": "ಪರೀಕ್ಷೆ 4: ರಹಸ್ಯ ವಿವರ ವಿನಂತಿ (OTP & PIN)",
        "text": "Send your OTP and PIN to complete verification."
    },
    {
        "id": "test_5",
        "title_en": "Test 5: Educational Newsletter (Benign)",
        "title_kn": "ಪರೀಕ್ಷೆ 5: ಹಣಕಾಸು ಶಿಕ್ಷಣ ಸುದ್ದಿಪತ್ರ (ಸಾಮಾನ್ಯ)",
        "text": "Hello, here is our annual financial education newsletter explaining index funds and inflation."
    }
]


@app.route('/')
def home():
    """Renders the main Investor ScamShield interactive application."""
    ocr_ready = is_ocr_available()
    return render_template('index.html', ocr_ready=ocr_ready)


@app.route('/checker')
def checker():
    """Direct route to the message checker section."""
    ocr_ready = is_ocr_available()
    return render_template('index.html', ocr_ready=ocr_ready)


@app.route('/how-it-works')
def how_it_works():
    """Direct route to the how-it-works section."""
    ocr_ready = is_ocr_available()
    return render_template('index.html', ocr_ready=ocr_ready)


@app.route('/safety')
def safety():
    """Renders the comprehensive Investor Safety Tips & Scams Guide."""
    return render_template('safety.html')


@app.route('/about')
def about():
    """Renders the About page detailing the hackathon public-good mission."""
    return render_template('about.html')


@app.route('/api/sample-scenarios', methods=['GET'])
def get_sample_scenarios():
    """Returns curated demo messages for judges and users."""
    return jsonify({
        "status": "success",
        "scenarios": DEMO_SCENARIOS
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_message():
    """
    Main scam detection endpoint.
    Accepts text message, evaluates patterns, URLs, regulatory claims,
    and returns a transparent, explainable risk-indicator score.
    """
    try:
        data = request.get_json(silent=True) or {}
        text = (data.get('text') or '').strip()
        lang = data.get('lang', 'en')
        if lang not in ('en', 'kn'):
            lang = 'en'

        if not text:
            return jsonify({
                "status": "error",
                "message_en": "Please paste a message or upload a screenshot to analyze.",
                "message_kn": "ವಿಶ್ಲೇಷಿಸಲು ದಯವಿಟ್ಟು ಸಂದೇಶವನ್ನು ಪೇಸ್ಟ್ ಮಾಡಿ ಅಥವಾ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."
            }), 400

        # Step 1: Detect rule-based warning indicators
        indicators = detect_indicators(text)

        # Step 2: Detect & analyze URLs
        urls_analysis = analyze_all_urls(text)

        # Step 3: Detect regulatory & authority claims
        claims = detect_claims(text)

        # Step 4: Calculate risk indicator score
        risk = calculate_risk(indicators, len(urls_analysis), len(claims))

        # Safe Next Steps based on language
        safe_steps = SAFE_NEXT_STEPS_KN if lang == 'kn' else SAFE_NEXT_STEPS_EN

        # Format transparent result adhering to Trust Rules
        result = {
            "status": "success",
            "lang": lang,
            "risk": risk,
            "indicators": indicators,
            "urls": urls_analysis,
            "claims": claims,
            "safe_steps": safe_steps,
            "trust_notice": {
                "en": "Warning indicators detected. These indicators do not by themselves prove fraud, but independent verification is strongly recommended.",
                "kn": "ಅಪಾಯದ ಸೂಚನೆಗಳು ಕಂಡುಬಂದಿವೆ. ಈ ಸೂಚನೆಗಳು ಕೇವಲ ವಂಚನೆಯನ್ನು ಸಾಬೀತುಪಡಿಸುವುದಿಲ್ಲ, ಆದರೆ ಸ್ವತಂತ್ರ ಪರಿಶೀಲನೆ ಅತ್ಯಗತ್ಯ."
            },
            "official_portals": [
                {
                    "name": "SEBI Intermediaries Registry",
                    "url": "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes&intmId=13",
                    "desc_en": "Official directory of SEBI-registered brokers, advisors & research analysts.",
                    "desc_kn": "SEBI ನೋಂದಾಯಿತ ಬ್ರೋಕರ್‌ಗಳು ಮತ್ತು ಸಲಹೆಗಾರರ ಅಧಿಕೃತ ಪಟ್ಟಿ."
                },
                {
                    "name": "RBI Sachet Portal",
                    "url": "https://sachet.rbi.org.in/",
                    "desc_en": "Platform to verify registered deposit entities and report unregistered finance schemes.",
                    "desc_kn": "ನೋಂದಾಯಿತ ಹಣಕಾಸು ಸಂಸ್ಥೆಗಳನ್ನು ಪರಿಶೀಲಿಸಲು ಮತ್ತು ಅಕ್ರಮ ಯೋಜನೆಗಳನ್ನು ವರದಿ ಮಾಡಲು ಪೋರ್ಟಲ್."
                },
                {
                    "name": "National Cyber Crime Portal (Helpline 1930)",
                    "url": "https://cybercrime.gov.in/",
                    "desc_en": "Official Indian Government portal for cyber financial fraud reporting.",
                    "desc_kn": "ಸೈಬರ್ ಹಣಕಾಸು ವಂಚನೆಗಳನ್ನು ವರದಿ ಮಾಡಲು ಅಧಿಕೃತ ಭಾರತ ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್."
                }
            ]
        }
        return jsonify(result)

    except Exception as exc:
        return jsonify({
            "status": "error",
            "message_en": "An unexpected error occurred while analyzing the message. Please try again.",
            "message_kn": "ಸಂದೇಶವನ್ನು ವಿಶ್ಲೇಷಿಸುವಾಗ ದೋಷ ಸಂಭವಿಸಿದೆ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
            "details": str(exc)
        }), 500


@app.route('/api/ocr', methods=['POST'])
def process_ocr():
    """
    Handles screenshot image upload, validates file type and size,
    extracts text using OCR engine in-memory, and provides graceful fallback
    if OCR is unavailable in the serverless environment.
    """
    if 'image' not in request.files:
        return jsonify({
            "status": "error",
            "message_en": "No image file provided in the request.",
            "message_kn": "ಯಾವುದೇ ಚಿತ್ರ ಕಳುಹಿಸಲಾಗಿಲ್ಲ."
        }), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({
            "status": "error",
            "message_en": "No file selected.",
            "message_kn": "ಯಾವುದೇ ಫೈಲ್ ಆಯ್ಕೆ ಮಾಡಲಾಗಿಲ್ಲ."
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "status": "error",
            "message_en": "Invalid file format. Please upload a PNG, JPG, JPEG, or WEBP image.",
            "message_kn": "ಅಮಾನ್ಯ ಫೈಲ್ ಮಾದರಿ. ದಯವಿಟ್ಟು PNG, JPG, JPEG ಅಥವಾ WEBP ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ."
        }), 400

    try:
        # Read image in-memory to prevent disk storage dependence in serverless environments
        image_bytes = file.read()
        if not image_bytes:
            return jsonify({
                "status": "error",
                "message_en": "Empty image file received.",
                "message_kn": "ಖಾಲಿ ಚಿತ್ರ ಫೈಲ್ ಸ್ವೀಕರಿಸಲಾಗಿದೆ."
            }), 400

        # Extract text via OCR
        ocr_result = extract_text_from_image(image_bytes)
        return jsonify({
            "status": "success" if ocr_result["success"] else "partial",
            "text": ocr_result["text"],
            "configured": ocr_result.get("configured", False),
            "error_en": ocr_result.get("error_en"),
            "error_kn": ocr_result.get("error_kn")
        })
    except Exception as exc:
        return jsonify({
            "status": "error",
            "message_en": f"Failed to process screenshot: {str(exc)}",
            "message_kn": "ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ."
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Graceful 404 handler for API and direct page requests."""
    if request.path.startswith('/api/'):
        return jsonify({
            "status": "error",
            "message_en": "API endpoint not found.",
            "message_kn": "API ಪುಟ ಕಂಡುಬಂದಿಲ್ಲ."
        }), 404
    return render_template('index.html', ocr_ready=is_ocr_available()), 404


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handles oversized uploads gracefully."""
    return jsonify({
        "status": "error",
        "message_en": "The uploaded screenshot exceeds the 8 MB size limit. Please upload a smaller image.",
        "message_kn": "ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ 8 MB ಮಿತಿಯನ್ನು ಮೀರಿದೆ. ದಯವಿಟ್ಟು ಸಣ್ಣ ಚಿತ್ರವನ್ನು ಬಳಸಿ."
    }), 413


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0").lower() in ("1", "true")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

