# 🛡️ Investor ScamShield

> **“Check before you transfer money.”**  
> *A public-good investor-protection tool helping first-time and emerging digital investors identify warning signs in suspicious financial messages BEFORE they transfer money.*

---

## 📌 SANGYAN Investor Resilience Hackathon
- **Track**: **Track A: Digital Fraud & Scam Resilience**
- **Domain**: Investor Protection, Financial Safety & Fraud Resilience
- **Target Audience**: Emerging & first-time digital investors from Tier-2 & Tier-3 cities
- **Interface Support**: English & Kannada (ಕನ್ನಡ) bilingual support

---

## 📖 1. Project Overview & Problem Statement

Across India and emerging markets, millions of first-time retail investors are entering the capital markets through mobile-first brokerage apps. However, digital connectivity has also exposed first-time and Tier-2/Tier-3 investors to high-pressure digital scam campaigns operating across WhatsApp communities, Telegram channels, Instagram influencers, and SMS.

Fraudsters exploit psychological triggers:
1. **Unrealistic guaranteed return promises** (e.g., *"Guaranteed 40% return in 7 days"*).
2. **Artificial time urgency** (e.g., *"Only 2 hours left! Transfer immediately"*).
3. **Counterfeit regulatory claims** (e.g., fabricating fake SEBI/RBI certificates and fake registration IDs).
4. **Coercive payment requests** directly to personal UPI addresses or mule bank accounts.
5. **Device compromise tactics** (asking victims to install AnyDesk/TeamViewer to steal banking credentials).

### The Solution: Investor ScamShield
**Investor ScamShield** is a transparent, explainable cognitive safety brake. Before transferring funds, an investor can paste a message or upload a chat screenshot. The tool:
- Scans for **8 transparent warning indicators**
- Analyzes URLs for hidden destinations and unusual domains
- Verifies regulatory claims against official sources
- Generates a **Prototype Risk-Indicator Score** (0–100)
- Explains **WHY** each indicator was triggered in plain English and Kannada
- Provides **Safe Next Steps** and direct access to official regulatory registries (SEBI, RBI Sachet, Cybercrime Helpline 1930)

---

## 🚫 2. Ethical Guardrails & Prohibited Features

Investor ScamShield is strictly an **investor-protection public utility**.

❌ **Strictly Prohibited & Absent**:
- No stock recommendations or tips
- No buy/sell/hold trading signals
- No stock-price predictions or algorithmic trading bots
- No broker advertisements or affiliate links
- No investment commissions or paid subscriptions
- No personalized investment advice

⚖️ **Honest Communication of Uncertainty**:
- The system **never** declares: *"This person is definitely a scammer"* or *"This investment is fake."*
- Instead, it states:
  > *“Warning indicator detected. Suspicious characteristic detected. Independent verification is recommended. These indicators do not by themselves prove fraud.”*
- The score is strictly labeled:
  > *“90 / 100 Risk Indicators — This is a prototype risk-indicator score, not a probability of scam and not investment advice.”*

---

## 🏗️ 3. Architecture & Project Structure

```
Investor_ScamShield/
├── app.py                     # Flask application & REST endpoints
├── requirements.txt           # Python backend dependencies
├── README.md                  # Comprehensive project documentation
│
├── templates/                 # Jinja2 HTML templates
│   ├── index.html             # Main interactive application & checker
│   ├── safety.html            # Investor safety guide & common scam archetypes
│   └── about.html             # Mission, hackathon alignment & trust rules
│
├── static/                    # Frontend assets
│   ├── style.css              # Accessible, responsive financial-safety design system
│   ├── app.js                 # Client state, dynamic i18n, async API & UI rendering
│   └── images/
│       └── sample_scam_chat.png # Demo screenshot for 1-click OCR judge testing
│
├── analyzer/                  # Core rule-based scam detection engine
│   ├── scam_detector.py       # Indicator pattern matching & snippet extraction
│   ├── risk_engine.py         # Prototype score calculation & trust disclaimers
│   ├── url_checker.py         # Link extractor, URL shortener & domain risk checker
│   └── claim_checker.py       # Regulatory claim detection (SEBI, RBI, Govt)
│
├── ocr/                       # Optical Character Recognition
│   └── ocr_engine.py          # Tesseract OCR discovery, preprocessing & fallback
│
└── uploads/                   # Ephemeral directory for temporary OCR processing
```

---

## ⚙️ 4. Scam Detection Engine & Indicators

The detection engine uses an explainable, deterministic rule-based framework with transparent regular expressions and weights:

| Indicator | Prototype Weight | Description & Explanation |
|:---|:---:|:---|
| **Guaranteed Returns** | `+30` | Promises of guaranteed/assured returns (*"Guaranteed 40% return"*, *"risk-free profit"*). Capital market investments always involve market risk. |
| **Payment Request** | `+25` | Direct payment instructions (*"Send ₹10,000"*, *"Transfer to UPI"*, *"GPay/PhonePe"*). Unsolicited payment requests must be independently verified. |
| **Credential Request** | `+25` | Requests for OTP, PIN, password, CVV, or banking credentials. Legitimate institutions never ask for these. |
| **Regulatory Claim** | `+20` | Claims of SEBI, RBI, or Govt registration. Must be independently verified through official registries. |
| **Remote Access** | `+20` | Requests to install AnyDesk, TeamViewer, or share screens to "assist" with investment accounts. |
| **Urgency / Pressure** | `+15` | High-pressure urgency tactics (*"Act now"*, *"Only 2 hours left"*, *"Send immediately"*). |
| **Secret / Insider Tip** | `+10` | Claims of *"secret tips"*, *"insider leaks"*, or *"sure-shot jackpot calls"*. |
| **Telegram / Tip Group** | `+10` | Invitations to VIP Telegram channels or WhatsApp stock groups utilizing artificial social proof. |

### Prototype Risk Scoring:
$$\text{Score} = \min\left(\sum \text{Weights}, 100\right)$$
- **0–20**: `LOW-RISK INDICATORS`
- **21–50**: `MEDIUM-RISK INDICATORS`
- **51–100**: `HIGH-RISK INDICATORS`

---

## 🌐 5. Bilingual Interface (English & Kannada)

To empower Tier-2 and Tier-3 investors across Karnataka and regional belts, the entire interface, results, explanations, and safety steps can be toggled instantly between **English** and **Kannada (ಕನ್ನಡ)** with a single click.

Key Kannada translations:
- *"Check before you transfer money."* $\rightarrow$ **“ಹಣ ವರ್ಗಾವಣೆ ಮಾಡುವ ಮೊದಲು ಪರಿಶೀಲಿಸಿ.”**
- *"Warning indicators detected."* $\rightarrow$ **“ಅಪಾಯದ ಸೂಚನೆಗಳು ಕಂಡುಬಂದಿವೆ.”**
- *"Do not transfer money until independently verified."* $\rightarrow$ **“ಸ್ವತಂತ್ರವಾಗಿ ಪರಿಶೀಲಿಸುವವರೆಗೆ ಹಣ ವರ್ಗಾವಣೆ ಮಾಡಬೇಡಿ.”**
- *"High-Risk Indicators"* $\rightarrow$ **“ಹೆಚ್ಚು ಅಪಾಯದ ಸೂಚನೆ”**

---

## 🔒 6. Privacy by Design

Investor ScamShield is architected for zero unnecessary data collection:
1. **No Credentials Requested**: We explicitly state:
   - *We do not ask for OTPs.*
   - *We do not ask for passwords.*
   - *We do not ask for PINs.*
   - *We do not ask for CVVs.*
   - *We do not ask for banking credentials.*
2. **Transient Processing**: Uploaded screenshots are stored ephemerally in RAM or temporary storage and deleted immediately after OCR text extraction.
3. **No Surveillance**: No persistent databases, no third-party tracking pixels, and no commercial advertising scripts.

---

## 🧪 7. Test Cases & Verification Scenarios

| Test Case | Sample Message Text | Expected Result | Score & Level |
|:---|:---|:---|:---:|
| **Hackathon Judge Demo** | `🚨 SEBI REGISTERED EXPERT 🚨 Guaranteed 40% return in 7 days! Invest ₹10,000 today. Available only for 2 hours. Send payment to our UPI ID immediately. Join Telegram group for secret stock tips.` | Guaranteed Returns (+30), Payment (+25), SEBI Claim (+20), Urgency (+15), Secret Tip (+10), Telegram Group (+10) | **100 / 100**<br>`HIGH` |
| **Test 1** | `Guaranteed 50% profit today. Send ₹20,000 immediately.` | Guaranteed return (+30), Urgency (+15), Payment request (+25) | **70 / 100**<br>`HIGH` |
| **Test 2** | `SEBI registered advisor. Join our Telegram group for secret stock tips.` | Regulatory claim (+20), Secret tip (+10), Telegram group (+10) | **40 / 100**<br>`MEDIUM` |
| **Test 3** | `Install AnyDesk and share your screen so we can help with your investment account.` | Remote access request (+20) | **20 / 100**<br>`LOW` |
| **Test 4** | `Send your OTP and PIN to complete verification.` | Credential request (+25) | **25 / 100**<br>`MEDIUM` |
| **Test 5** | `Hello, here is our annual financial education newsletter explaining index funds and inflation.` | Few or no overt warning indicators | **0 / 100**<br>`LOW` |

---

## 🚀 8. Installation & Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- pip package manager

### 1. Clone or Open Project
```bash
cd Investor_Scamshield
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Install Tesseract OCR for Local Screenshot OCR
- **Windows**: Download installer from [UB-Mannheim Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) or install via Chocolatey/winget:
  ```powershell
  winget install UB-Mannheim.TesseractOCR
  ```
- **Ubuntu/Debian**:
  ```bash
  sudo apt-get install tesseract-ocr
  ```
- **Graceful Fallback**: If Tesseract is not installed on the system, the application handles it gracefully without crashing:
  > *“OCR is not configured. You can paste the message text manually.”*  
  Additionally, clicking **“Load Sample Chat Screenshot”** in the UI allows judges to test screenshot OCR with a pre-loaded chat sample.

### 4. Run the Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## ⏱️ 9. Judge Demonstration Script (1–2 Minutes)

Follow these steps for a complete hackathon demonstration:

1. **Open the Homepage (`/`)**:
   - Point out the branding: *“🛡️ Investor ScamShield”* and tagline *“Check before you transfer money.”*
   - Highlight the public-good notice: *“No stock tips. No buy/sell signals.”* and trust badges.
2. **Execute Judge Demo (1-Click)**:
   - Click the purple **“⚡ Try Judge Demo”** button in the hero section.
   - The exact test scenario loads and analyzes instantly.
3. **Inspect the Explainable Analysis Result**:
   - Notice the **HIGH-RISK INDICATORS** banner with **100 / 100 Risk Indicators**.
   - Review the prototype disclaimer: *“This is a prototype risk-indicator score, not a probability of scam and not investment advice.”*
   - Scroll through the detected warning signs showing exact matched snippets and point weights.
   - Show the **REGULATORY CLAIM DETECTED** box with a direct link to the official SEBI registry.
   - Review the **SAFE NEXT STEPS** section (Rules 1 to 6, including Helpline **1930**).
4. **Demonstrate Kannada Language Support**:
   - Click **“ಕನ್ನಡ”** in the header.
   - Observe the entire interface, score labels, explanations, and safe steps smoothly update to natural Kannada.
5. **Demonstrate Screenshot Analyzer**:
   - Click the **“📷 Upload Screenshot”** tab.
   - Click **“🖼️ Load Sample Chat Screenshot”** to view the preview.
   - Click **“Extract Text from Screenshot”** to see OCR processing.
6. **Explain Privacy Architecture**:
   - Scroll down to the **🔒 Privacy First Architecture** section highlighting the 6 privacy guarantees.
7. **Show Safety Guide (`/safety`)**:
   - Click **“Safety Tips”** to show the 6 common scam archetypes and the 60-minute **“Golden Hour”** emergency response workflow.

---

## 🔮 10. Future Scalability & Roadmap

1. **Official Registry APIs**: Direct lookup against SEBI Intermediaries Registry (`sebi.gov.in`) and RBI Sachet API to verify advisory registration numbers in real time.
2. **Local Dialect & Audio Support**: Speech-to-text input and voice playback in Kannada, Hindi, Telugu, and Tamil for rural first-time investors with low literacy.
3. **WhatsApp / SMS Forwarding Bot**: A verified WhatsApp business bot where users can simply forward suspicious messages to receive an instant ScamShield safety assessment.
4. **Mule Account Risk Feed**: Integration with the National Cyber Crime Reporting Portal (NCRP) API for known suspect UPI IDs and mule account numbers.

---

## 📜 License
Investor ScamShield is open-source public-good software developed for the **SANGYAN Investor Resilience Hackathon: Track A**.
All rights reserved under the MIT License for public investor resilience education.
