"""
OCR Engine for Investor ScamShield.
Integrates with Tesseract OCR with resilient automatic path discovery on Windows/Linux,
image preprocessing using Pillow, and graceful fallback when OCR is unavailable
(such as in serverless cloud environments like Vercel).
"""

import os
import io
import shutil

try:
    from PIL import Image, ImageEnhance
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    pytesseract = None
    PYTESSERACT_AVAILABLE = False

COMMON_WINDOWS_PATHS = [
    os.environ.get("TESSERACT_PATH"),
    os.environ.get("TESSERACT_CMD"),
    r"C:\Users\Abhi\scoop\apps\tesseract\current\tesseract.exe",
    r"C:\Users\Abhi\scoop\shims\tesseract.exe",
    os.path.expanduser(r"~\scoop\apps\tesseract\current\tesseract.exe"),
    os.path.expanduser(r"~\scoop\shims\tesseract.exe"),
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
]

TESSDATA_CANDIDATES = [
    r"C:\Users\Abhi\scoop\apps\tesseract\current\tessdata",
    r"C:\Users\Abhi\scoop\persist\tesseract\tessdata",
    os.path.expanduser(r"~\scoop\apps\tesseract\current\tessdata"),
    r"C:\Program Files\Tesseract-OCR\tessdata",
]


def find_tesseract_binary() -> str | None:
    """Discovers tesseract binary across environment variables, standard paths, and PATH."""
    # First check environment variables
    for env_var in ("TESSERACT_PATH", "TESSERACT_CMD"):
        val = os.environ.get(env_var)
        if val and os.path.exists(val):
            return val

    # Next check system PATH (works on standard Linux/Mac/Windows)
    system_path = shutil.which("tesseract")
    if system_path:
        return system_path

    # Check common Windows locations
    for path in COMMON_WINDOWS_PATHS:
        if path and os.path.exists(path):
            return path

    return None


def is_ocr_available() -> bool:
    """Checks if Tesseract executable and required libraries are installed and reachable."""
    if not PYTESSERACT_AVAILABLE or not PILLOW_AVAILABLE:
        return False
    binary = find_tesseract_binary()
    return binary is not None


def configure_tesseract():
    """Sets pytesseract tesseract_cmd and TESSDATA_PREFIX."""
    if not PYTESSERACT_AVAILABLE:
        return False
    binary = find_tesseract_binary()
    if binary:
        pytesseract.pytesseract.tesseract_cmd = binary

        # Ensure TESSDATA_PREFIX is set to valid tessdata folder
        if not os.environ.get("TESSDATA_PREFIX") or not os.path.exists(os.environ.get("TESSDATA_PREFIX", "")):
            for td in TESSDATA_CANDIDATES:
                if os.path.exists(td):
                    os.environ["TESSDATA_PREFIX"] = td
                    break
        return True
    return False


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Applies image preprocessing to improve OCR accuracy on digital chat screenshots:
    - Convert to RGB / Grayscale
    - Enlarge small text if necessary
    - Contrast enhancement
    """
    if not PILLOW_AVAILABLE:
        return image

    # Convert RGBA / P to RGB
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Resize if small
    w, h = image.size
    if w < 1000 or h < 600:
        factor = max(2, int(1200 / max(w, 1)))
        image = image.resize((w * factor, h * factor), Image.Resampling.LANCZOS)

    # Convert to grayscale
    gray = image.convert("L")

    # Boost contrast moderately
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(1.6)

    return enhanced


def extract_text_from_image(image_input) -> dict:
    """
    Extracts text from an image (filepath, bytes, or file-like object) using Tesseract OCR.
    Handles errors gracefully without crashing or throwing unhandled exceptions.
    Provides clear bilingual fallback messages when OCR cannot run in serverless environments.
    """
    if not is_ocr_available():
        return {
            "success": False,
            "text": "",
            "configured": False,
            "error_en": "OCR text extraction is unavailable in this serverless cloud environment. Please paste or type the message text manually in the checker.",
            "error_kn": "ಕ್ಲೌಡ್ ಸರ್ವರ್‌ಲೆಸ್ ಪರಿಸರದಲ್ಲಿ OCR ಚಿತ್ರ ಓದುವಿಕೆ ಲಭ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ಸಂದೇಶದ ಪಠ್ಯವನ್ನು ನೇರವಾಗಿ ಪೇಸ್ಟ್ ಮಾಡಿ."
        }

    configured = configure_tesseract()
    if not configured:
        return {
            "success": False,
            "text": "",
            "configured": False,
            "error_en": "OCR is not configured. You can paste the message text manually.",
            "error_kn": "OCR ಕಾನ್ಫಿಗರ್ ಆಗಿಲ್ಲ. ನೀವು ಸಂದೇಶವನ್ನು ನೇರವಾಗಿ ಪೇಸ್ಟ್ ಮಾಡಬಹುದು."
        }

    try:
        # Load image into Pillow from either bytes, filepath, or file-like object
        if isinstance(image_input, (bytes, bytearray)):
            img = Image.open(io.BytesIO(image_input))
        elif isinstance(image_input, str):
            if not os.path.exists(image_input):
                return {
                    "success": False,
                    "text": "",
                    "configured": True,
                    "error_en": "Uploaded image file could not be found.",
                    "error_kn": "ಅಪ್‌ಲೋಡ್ ಮಾಡಲಾದ ಚಿತ್ರ ಕಂಡುಬಂದಿಲ್ಲ."
                }
            img = Image.open(image_input)
        elif hasattr(image_input, 'read'):
            img = Image.open(image_input)
        else:
            return {
                "success": False,
                "text": "",
                "configured": True,
                "error_en": "Invalid image format provided.",
                "error_kn": "ಅಮಾನ್ಯ ಚಿತ್ರ ಸ್ವರೂಪ."
            }

        with img:
            processed = preprocess_image(img)
            # Run pytesseract OCR with English (+ Kannada if available)
            raw_text = pytesseract.image_to_string(processed, lang="eng")
            cleaned_text = raw_text.strip()

            if not cleaned_text:
                return {
                    "success": False,
                    "text": "",
                    "configured": True,
                    "error_en": "No readable text detected in this screenshot. Please try a clearer screenshot or paste the message text manually.",
                    "error_kn": "ಈ ಸ್ಕ್ರೀನ್‌ಶಾಟ್‌ನಲ್ಲಿ ಓದಲು ಸಾಧ್ಯವಾಗುವ ಯಾವುದೇ ಪಠ್ಯ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಸ್ಪಷ್ಟವಾದ ಚಿತ್ರವನ್ನು ಪ್ರಯತ್ನಿಸಿ ಅಥವಾ ಪಠ್ಯವನ್ನು ನೇರವಾಗಿ ಪೇಸ್ಟ್ ಮಾಡಿ."
                }

            return {
                "success": True,
                "text": cleaned_text,
                "configured": True,
                "error_en": None,
                "error_kn": None
            }
    except Exception as exc:
        return {
            "success": False,
            "text": "",
            "configured": True,
            "error_en": f"Unable to read this screenshot. Please try a clearer image or paste the message text. ({str(exc)})",
            "error_kn": "ಈ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅನ್ನು ಓದಲು ಸಾಧ್ಯವಾಗುತ್ತಿಲ್ಲ. ದಯವಿಟ್ಟು ಸ್ಪಷ್ಟವಾದ ಚಿತ್ರವನ್ನು ಪ್ರಯತ್ನಿಸಿ ಅಥವಾ ಪಠ್ಯವನ್ನು ನೇರವಾಗಿ ಪೇಸ್ಟ್ ಮಾಡಿ."
        }
