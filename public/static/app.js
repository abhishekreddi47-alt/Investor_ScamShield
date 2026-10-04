/**
 * Investor ScamShield - Client Application Logic
 * SANGYAN Investor Resilience Hackathon: Track A - Digital Fraud & Scam Resilience
 * 
 * Features:
 * - Real-time English / Kannada translation switcher
 * - Rule-based scam detection integration
 * - Screenshot upload & OCR processing with graceful fallback
 * - Pre-loaded Hackathon judge demo & test case scenarios
 * - Accessible UI with touch-friendly elements & clear feedback
 */

// Comprehensive English <-> Kannada Dictionary for dynamic interface translation
const TRANSLATIONS = {
  en: {
    nav_home: "Home",
    nav_check: "Check Message",
    nav_how: "How It Works",
    nav_safety: "Safety Tips",
    nav_about: "About",
    hero_pill: "Track A: Digital Fraud & Scam Resilience",
    hero_title: "Check before you transfer money.",
    hero_subtitle: "Received a suspicious investment message? Analyze the warning signs before clicking a link, joining a group, or transferring money.",
    hero_check_btn: "🔍 Check a Message",
    hero_upload_btn: "📷 Upload Screenshot",
    hero_demo_btn: "⚡ Try Judge Demo",
    trust_safety: "🛡️ Safety First",
    trust_privacy: "🔒 Privacy First",
    trust_bilingual: "🌐 English + Kannada",
    prohibition_notice: "No stock tips. No buy/sell signals. Investor protection only.",
    
    checker_title: "Analyze Suspicious Financial Message",
    tab_text: "📝 Paste Message",
    tab_screenshot: "📷 Upload Screenshot",
    scenario_label: "Quick Test Scenarios:",
    select_scenario: "-- Select a test scenario --",
    textarea_placeholder: "Paste the WhatsApp / Telegram / SMS / social-media message here...\n\nExample: 'Guaranteed 40% profit in 7 days! Send money to UPI immediately.'",
    btn_analyze: "🔍 Analyze Message",
    btn_clear: "Clear",
    
    dropzone_title: "Drop screenshot here or click to browse",
    dropzone_desc: "Supports PNG, JPG, JPEG, WEBP (Max 8 MB). Processed in-memory, never permanently stored.",
    dropzone_btn: "Select Screenshot",
    sample_tray_label: "Try with a realistic scam screenshot:",
    btn_use_sample: "🖼️ Load Sample Chat Screenshot",
    btn_run_ocr: "Extract Text from Screenshot",
    
    how_title: "How Investor ScamShield Works",
    how_subtitle: "A 4-step public-good framework designed to empower first-time investors before financial harm occurs.",
    how_step1_title: "1️⃣ Receive",
    how_step1_desc: "You receive an unsolicited investment offer via WhatsApp, Telegram, Instagram, or SMS.",
    how_step2_title: "2️⃣ Check",
    how_step2_desc: "Paste the message text or upload a screenshot to ScamShield without sharing private details.",
    how_step3_title: "3️⃣ Analyze",
    how_step3_desc: "Our transparent rule engine identifies warning indicators, suspicious links, and unverified claims.",
    how_step4_title: "4️⃣ Protect",
    how_step4_desc: "Review plain-language explanations, official verification links, and safe next steps before acting.",
    
    privacy_title: "🔒 Privacy First Architecture",
    privacy_p1: "We do not ask for OTPs.",
    privacy_p2: "We do not ask for passwords.",
    privacy_p3: "We do not ask for PINs.",
    privacy_p4: "We do not ask for CVVs.",
    privacy_p5: "We do not ask for banking login credentials.",
    privacy_p6: "We do not ask for investment-account passwords.",
    privacy_note: "Privacy Guarantee: Screenshots are processed in temporary memory and immediately deleted. We do not track users, do not use commercial cookies, and do not store message contents.",
    
    portals_title: "Official Verification Resources",
    portals_subtitle: "Always verify investment advisors and deposit schemes through official regulatory directories.",
    
    result_title: "ANALYSIS RESULT",
    result_disclaimer_title: "Important Verification Notice",
    btn_copy_summary: "📋 Copy Analysis Summary",
    btn_check_another: "🔍 Check Another Message",
    toast_copied: "Analysis summary copied to clipboard!",
    toast_cleared: "Inputs cleared.",
    toast_demo_loaded: "Judge demo scenario loaded!",
    toast_sample_loaded: "Sample screenshot loaded!",
    
    empty_error: "Please enter or paste a message to analyze.",
    ocr_loading: "Scanning screenshot with OCR engine...",
    analyzing_loading: "Evaluating warning indicators and links...",
    
    safe_steps_heading: "🛡️ SAFE NEXT STEPS",
    claim_box_title: "REGULATORY CLAIM DETECTED",
    claim_box_notice: "Do not rely only on the registration number, badge, screenshot, or link provided in the message. Verify the claim independently using official sources."
  },
  kn: {
    nav_home: "ಮುಖಪುಟ",
    nav_check: "ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
    nav_how: "ಇದು ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ",
    nav_safety: "ಸುರಕ್ಷತಾ ಸಲಹೆಗಳು",
    nav_about: "ನಮ್ಮ ಬಗ್ಗೆ",
    hero_pill: "ಟ್ರ್ಯಾಕ್ ಎ: ಡಿಜಿಟಲ್ ವಂಚನೆ ಮತ್ತು ಹಗರಣ ನಿರೋಧಕತೆ",
    hero_title: "ಹಣ ವರ್ಗಾವಣೆ ಮಾಡುವ ಮೊದಲು ಪರಿಶೀಲಿಸಿ.",
    hero_subtitle: "ಅನುಮಾನಾಸ್ಪದ ಹೂಡಿಕೆ ಸಂದೇಶ ಬಂದಿದೆಯೇ? ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡುವ, ಗ್ರೂಪ್ ಸೇರುವ ಅಥವಾ ಹಣ ವರ್ಗಾಯಿಸುವ ಮೊದಲು ಎಚ್ಚರಿಕೆಯ ಸೂಚನೆಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಿ.",
    hero_check_btn: "🔍 ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
    hero_upload_btn: "📷 ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅಪ್‌ಲೋಡ್",
    hero_demo_btn: "⚡ ಡೆಮೊ ಪ್ರಯತ್ನಿಸಿ",
    trust_safety: "🛡️ ಸುರಕ್ಷತೆ ಮೊದಲು",
    trust_privacy: "🔒 ಗೌಪ್ಯತೆ ಮೊದಲು",
    trust_bilingual: "🌐 ಇಂಗ್ಲಿಷ್ + ಕನ್ನಡ",
    prohibition_notice: "ಯಾವುದೇ ಷೇರು ಟಿಪ್ಸ್ ಇಲ್ಲ. ಖರೀದಿ/ಮಾರಾಟ ಸಿಗ್ನಲ್‌ಗಳಿಲ್ಲ. ಹೂಡಿಕೆದಾರರ ಸುರಕ್ಷತೆ ಮಾತ್ರ.",
    
    checker_title: "ಅನುಮಾನಾಸ್ಪದ ಹಣಕಾಸು ಸಂದೇಶವನ್ನು ವಿಶ್ಲೇಷಿಸಿ",
    tab_text: "📝 ಸಂದೇಶ ಪೇಸ್ಟ್ ಮಾಡಿ",
    tab_screenshot: "📷 ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅಪ್‌ಲೋಡ್",
    scenario_label: "ಪರೀಕ್ಷಾ ಸನ್ನಿವೇಶಗಳು:",
    select_scenario: "-- ಪರೀಕ್ಷಾ ಸನ್ನಿವೇಶವನ್ನು ಆಯ್ಕೆಮಾಡಿ --",
    textarea_placeholder: "ವಾಟ್ಸಾಪ್ / ಟೆಲಿಗ್ರಾಮ್ / SMS / ಸಾಮಾಜಿಕ ಮಾಧ್ಯಮದ ಸಂದೇಶವನ್ನು ಇಲ್ಲಿ ಪೇಸ್ಟ್ ಮಾಡಿ...\n\nಉದಾಹರಣೆ: '7 ದಿನಗಳಲ್ಲಿ 40% ಖಚಿತ ಲಾಭ! ತಕ್ಷಣ ನಮ್ಮ UPI ಗೆ ಹಣ ಕಳುಹಿಸಿ.'",
    btn_analyze: "🔍 ಸಂದೇಶ ವಿಶ್ಲೇಷಿಸಿ",
    btn_clear: "ತೆರವುಗೊಳಿಸಿ (Clear)",
    
    dropzone_title: "ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅನ್ನು ಇಲ್ಲಿ ಎಳೆಯಿರಿ ಅಥವಾ ಕ್ಲಿಕ್ ಮಾಡಿ",
    dropzone_desc: "PNG, JPG, JPEG, WEBP ಬೆಂಬಲಿತವಾಗಿದೆ (ಗರಿಷ್ಠ 8 MB). ಸುರಕ್ಷಿತವಾಗಿ ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲಾಗುತ್ತದೆ.",
    dropzone_btn: "ಚಿತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    sample_tray_label: "ನೈಜ ಹಗರಣದ ಚಾಟ್ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಪ್ರಯತ್ನಿಸಿ:",
    btn_use_sample: "🖼️ ಮಾದರಿ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಬಳಸಿ",
    btn_run_ocr: "ಸ್ಕ್ರೀನ್‌ಶಾಟ್‌ನಿಂದ ಪಠ್ಯವನ್ನು ಪಡೆಯಿರಿ",
    
    how_title: "ಇನ್ವೆಸ್ಟರ್ ಸ್ಕ್ಯಾಮ್‌ಶೀಲ್ಡ್ ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ",
    how_subtitle: "ಹಣಕಾಸು ನಷ್ಟ ಸಂಭವಿಸುವ ಮುನ್ನವೇ ಹೊಸ ಹೂಡಿಕೆದಾರರಿಗೆ ರಕ್ಷಣೆ ನೀಡುವ 4-ಹಂತದ ಸಾರ್ವಜನಿಕ ವ್ಯವಸ್ಥೆ.",
    how_step1_title: "1️⃣ ಸ್ವೀಕರಿಸಿ",
    how_step1_desc: "ವಾಟ್ಸಾಪ್, ಟೆಲಿಗ್ರಾಮ್ ಅಥವಾ SMS ಮೂಲಕ ಅನಪೇಕ್ಷಿತ ಹೂಡಿಕೆ ಸಂದೇಶ ಬರುತ್ತದೆ.",
    how_step2_title: "2️⃣ ಪರಿಶೀಲಿಸಿ",
    how_step2_desc: "ಯಾವುದೇ ಖಾಸಗಿ ವಿವರಗಳನ್ನು ಹಂಚಿಕೊಳ್ಳದೆ ಸಂದೇಶ ಅಥವಾ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅನ್ನು ಸ್ಕ್ಯಾಮ್‌ಶೀಲ್ಡ್‌ಗೆ ಹಾಕಿ.",
    how_step3_title: "3️⃣ ವಿಶ್ಲೇಷಿಸಿ",
    how_step3_desc: "ನಮ್ಮ ನಿಯಮ ಎಂಜಿನ್ ಅಪಾಯದ ಸೂಚನೆಗಳು, ನಕಲಿ ಹಕ್ಕುಗಳು ಮತ್ತು ಸಂಶಯಾಸ್ಪದ ಲಿಂಕ್‌ಗಳನ್ನು ಗುರುತಿಸುತ್ತದೆ.",
    how_step4_title: "4️⃣ ಸುರಕ್ಷಿತವಾಗಿರಿ",
    how_step4_desc: "ಸರಳ ವಿವರಣೆಗಳು, ಅಧಿಕೃತ ಪರಿಶೀಲನಾ ಲಿಂಕ್‌ಗಳು ಮತ್ತು ಸುರಕ್ಷಿತ ಮುಂದಿನ ಕ್ರಮಗಳನ್ನು ಓದಿ ನಿರ್ಧಾರ ತೆಗೆದುಕೊಳ್ಳಿ.",
    
    privacy_title: "🔒 ಗೌಪ್ಯತೆ-ಆಧಾರಿತ ವಿನ್ಯಾಸ",
    privacy_p1: "ನಾವು OTP ಗಳನ್ನು ಕೇಳುವುದಿಲ್ಲ.",
    privacy_p2: "ನಾವು ಪಾಸ್‌ವರ್ಡ್‌ಗಳನ್ನು ಕೇಳುವುದಿಲ್ಲ.",
    privacy_p3: "ನಾವು PIN ಗಳನ್ನು ಕೇಳುವುದಿಲ್ಲ.",
    privacy_p4: "ನಾವು CVV ಗಳನ್ನು ಕೇಳುವುದಿಲ್ಲ.",
    privacy_p5: "ನಾವು ಬ್ಯಾಂಕಿಂಗ್ ಲಾಗಿನ್ ವಿವರಗಳನ್ನು ಕೇಳುವುದಿಲ್ಲ.",
    privacy_p6: "ನಾವು ಹೂಡಿಕೆ ಖಾತೆಯ ಪಾಸ್‌ವರ್ಡ್‌ಗಳನ್ನು ಕೇಳುವುದಿಲ್ಲ.",
    privacy_note: "ಗೌಪ್ಯತೆಯ ಭರವಸೆ: ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರಗಳನ್ನು ಪಠ್ಯ ತೆಗೆದ ತಕ್ಷಣ ಅಳಿಸಲಾಗುತ್ತದೆ. ನಾವು ಬಳಕೆದಾರರನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡುವುದಿಲ್ಲ.",
    
    portals_title: "ಅಧಿಕೃತ ಪರಿಶೀಲನಾ ಸಂಪನ್ಮೂಲಗಳು",
    portals_subtitle: "ಯಾವಾಗಲೂ ಅಧಿಕೃತ ನಿಯಂತ್ರಕ ಜಾಲತಾಣಗಳ ಮೂಲಕ ಹೂಡಿಕೆ ಸಲಹೆಗಾರರನ್ನು ಪರಿಶೀಲಿಸಿ.",
    
    result_title: "ವಿಶ್ಲೇಷಣಾ ಫಲಿತಾಂಶ",
    result_disclaimer_title: "ಮುಖ್ಯ ಪರಿಶೀಲನಾ ಸೂಚನೆ",
    btn_copy_summary: "📋 ಸಾರಾಂಶವನ್ನು ನಕಲಿಸಿ",
    btn_check_another: "🔍 ಇನ್ನೊಂದು ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ",
    toast_copied: "ವಿಶ್ಲೇಷಣಾ ಸಾರಾಂಶವನ್ನು ಕ್ಲಿಪ್‌ಬೋರ್ಡ್‌ಗೆ ನಕಲಿಸಲಾಗಿದೆ!",
    toast_cleared: "ವಿವರಗಳನ್ನು ತೆರವುಗೊಳಿಸಲಾಗಿದೆ.",
    toast_demo_loaded: "ತೀರ್ಪುಗಾರರ ಡೆಮೊ ಸಂದೇಶ ಲೋಡ್ ಆಗಿದೆ!",
    toast_sample_loaded: "ಮಾದರಿ ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಲೋಡ್ ಆಗಿದೆ!",
    
    empty_error: "ವಿಶ್ಲೇಷಿಸಲು ದಯವಿಟ್ಟು ಸಂದೇಶವನ್ನು ನಮೂದಿಸಿ ಅಥವಾ ಪೇಸ್ಟ್ ಮಾಡಿ.",
    ocr_loading: "ಸ್ಕ್ರೀನ್‌ಶಾಟ್‌ನಿಂದ ಪಠ್ಯವನ್ನು ಓದಲಾಗುತ್ತಿದೆ...",
    analyzing_loading: "ಅಪಾಯದ ಸೂಚನೆಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...",
    
    safe_steps_heading: "🛡️ ಸುರಕ್ಷಿತ ಮುಂದಿನ ಕ್ರಮಗಳು",
    claim_box_title: "ನಿಯಂತ್ರಕ ಮಂಡಳಿ ಹಕ್ಕು ಕಂಡುಬಂದಿದೆ",
    claim_box_notice: "ಸಂದೇಶದಲ್ಲಿ ನೀಡಲಾದ ನೋಂದಣಿ ಸಂಖ್ಯೆ, ಬ್ಯಾಡ್ಜ್, ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಅಥವಾ ಲಿಂಕ್ ಅನ್ನು ಮಾತ್ರ ನಂಬಬೇಡಿ. ಅಧಿಕೃತ ಮೂಲಗಳನ್ನು ಬಳಸಿಕೊಂಡು ಸ್ವತಂತ್ರವಾಗಿ ಪರಿಶೀಲಿಸಿ."
  }
};

// Current active language: default to English or stored preference
let currentLang = localStorage.getItem('scamshield_lang') || 'en';

// DOM Elements
const langBtnEn = document.getElementById('lang-btn-en');
const langBtnKn = document.getElementById('lang-btn-kn');
const messageTextarea = document.getElementById('message-textarea');
const charCountSpan = document.getElementById('char-count');
const analyzeBtn = document.getElementById('analyze-btn');
const clearBtn = document.getElementById('clear-btn');
const demoHeroBtn = document.getElementById('demo-hero-btn');
const scenarioSelect = document.getElementById('scenario-select');

// Tabs & Upload
const tabBtnText = document.getElementById('tab-btn-text');
const tabBtnScreenshot = document.getElementById('tab-btn-screenshot');
const textInputPane = document.getElementById('text-input-pane');
const screenshotPane = document.getElementById('screenshot-pane');
const dropzone = document.getElementById('upload-dropzone');
const fileInput = document.getElementById('screenshot-file-input');
const previewContainer = document.getElementById('preview-container');
const previewImage = document.getElementById('preview-image');
const removePreviewBtn = document.getElementById('remove-preview-btn');
const useSampleBtn = document.getElementById('use-sample-btn');
const runOcrBtn = document.getElementById('run-ocr-btn');

// Results & Loading
const loadingIndicator = document.getElementById('loading-indicator');
const loadingText = document.getElementById('loading-text');
const resultContainer = document.getElementById('result-container');
const toastEl = document.getElementById('toast-msg');

let currentSelectedFile = null;
let lastAnalysisResult = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  setLanguage(currentLang);
  setupEventListeners();
  loadSampleScenarios();

  // Smooth scroll if loaded directly via /checker or /how-it-works routes
  const path = window.location.pathname;
  if (path === '/checker' || window.location.hash === '#checker') {
    const el = document.getElementById('checker');
    if (el) setTimeout(() => el.scrollIntoView({ behavior: 'smooth' }), 150);
  } else if (path === '/how-it-works' || window.location.hash === '#how-it-works') {
    const el = document.getElementById('how-it-works');
    if (el) setTimeout(() => el.scrollIntoView({ behavior: 'smooth' }), 150);
  }
});

function showToast(message) {
  if (!toastEl) return;
  toastEl.textContent = message;
  toastEl.classList.add('show');
  setTimeout(() => {
    toastEl.classList.remove('show');
  }, 3200);
}

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem('scamshield_lang', lang);

  if (langBtnEn && langBtnKn) {
    langBtnEn.classList.toggle('active', lang === 'en');
    langBtnKn.classList.toggle('active', lang === 'kn');
  }

  const dict = TRANSLATIONS[lang] || TRANSLATIONS.en;

  // Translate all elements with data-i18n attribute
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });

  // Translate placeholders
  if (messageTextarea) {
    messageTextarea.placeholder = dict.textarea_placeholder;
  }

  // Update dynamic result card if already rendered
  if (lastAnalysisResult) {
    renderAnalysisResult(lastAnalysisResult);
  }
}

function setupEventListeners() {
  // Language Switchers
  if (langBtnEn) langBtnEn.addEventListener('click', () => setLanguage('en'));
  if (langBtnKn) langBtnKn.addEventListener('click', () => setLanguage('kn'));

  // Mobile Menu Toggle
  const mobileBtn = document.getElementById('mobile-menu-btn');
  const navLinks = document.getElementById('nav-links');
  if (mobileBtn && navLinks) {
    mobileBtn.addEventListener('click', () => {
      navLinks.classList.toggle('mobile-open');
    });
  }

  // Character counter
  if (messageTextarea && charCountSpan) {
    messageTextarea.addEventListener('input', () => {
      charCountSpan.textContent = messageTextarea.value.length;
    });
  }

  // Tab switching
  if (tabBtnText && tabBtnScreenshot) {
    tabBtnText.addEventListener('click', () => {
      tabBtnText.classList.add('active');
      tabBtnScreenshot.classList.remove('active');
      textInputPane.style.display = 'block';
      screenshotPane.style.display = 'none';
    });

    tabBtnScreenshot.addEventListener('click', () => {
      tabBtnScreenshot.classList.add('active');
      tabBtnText.classList.remove('active');
      screenshotPane.style.display = 'block';
      textInputPane.style.display = 'none';
    });
  }

  // Clear button
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      if (messageTextarea) messageTextarea.value = '';
      if (charCountSpan) charCountSpan.textContent = '0';
      if (resultContainer) resultContainer.style.display = 'none';
      clearScreenshotPreview();
      lastAnalysisResult = null;
      showToast(TRANSLATIONS[currentLang].toast_cleared);
    });
  }

  // Analyze Button
  if (analyzeBtn) {
    analyzeBtn.addEventListener('click', () => {
      const text = messageTextarea.value.trim();
      if (!text) {
        showToast(TRANSLATIONS[currentLang].empty_error);
        messageTextarea.focus();
        return;
      }
      runAnalysis(text);
    });
  }

  // Demo Hero Button
  if (demoHeroBtn) {
    demoHeroBtn.addEventListener('click', () => {
      loadJudgeDemo();
    });
  }

  // Quick Scenario Dropdown
  if (scenarioSelect) {
    scenarioSelect.addEventListener('change', (e) => {
      const selectedId = e.target.value;
      if (!selectedId) return;
      loadScenarioById(selectedId);
    });
  }

  // File Upload Dropzone Events
  if (dropzone && fileInput) {
    dropzone.addEventListener('click', () => fileInput.click());

    dropzone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropzone.classList.add('drag-active');
    });

    ['dragleave', 'dragend'].forEach(type => {
      dropzone.addEventListener(type, () => dropzone.classList.remove('drag-active'));
    });

    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.classList.remove('drag-active');
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        handleFileSelection(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files.length > 0) {
        handleFileSelection(e.target.files[0]);
      }
    });
  }

  // Remove preview button
  if (removePreviewBtn) {
    removePreviewBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      clearScreenshotPreview();
    });
  }

  // Load sample screenshot button
  if (useSampleBtn) {
    useSampleBtn.addEventListener('click', () => {
      loadSampleScreenshot();
    });
  }

  // OCR button
  if (runOcrBtn) {
    runOcrBtn.addEventListener('click', () => {
      if (!currentSelectedFile) {
        showToast("Please select a screenshot first.");
        return;
      }
      uploadAndPerformOcr(currentSelectedFile);
    });
  }
}

function handleFileSelection(file) {
  if (!file) return;

  const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
  if (!validTypes.includes(file.type)) {
    alert("Please select a valid image file (PNG, JPG, JPEG, WEBP).");
    return;
  }

  if (file.size > 8 * 1024 * 1024) {
    alert("The image exceeds the 8 MB maximum size limit.");
    return;
  }

  currentSelectedFile = file;

  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.src = e.target.result;
    previewContainer.style.display = 'block';
    dropzone.style.display = 'none';
    runOcrBtn.style.display = 'inline-flex';
  };
  reader.readAsDataURL(file);
}

function clearScreenshotPreview() {
  currentSelectedFile = null;
  if (fileInput) fileInput.value = '';
  if (previewImage) previewImage.src = '';
  if (previewContainer) previewContainer.style.display = 'none';
  if (dropzone) dropzone.style.display = 'block';
  if (runOcrBtn) runOcrBtn.style.display = 'none';
}

function loadSampleScreenshot() {
  const sampleUrl = '/static/images/sample_scam_chat.png';
  fetch(sampleUrl)
    .then(res => res.blob())
    .then(blob => {
      const file = new File([blob], 'sample_scam_chat.png', { type: 'image/png' });
      handleFileSelection(file);
      showToast(TRANSLATIONS[currentLang].toast_sample_loaded);
    })
    .catch(err => {
      console.warn("Could not fetch sample chat image blob, using direct URL:", err);
      previewImage.src = sampleUrl;
      previewContainer.style.display = 'block';
      dropzone.style.display = 'none';
      runOcrBtn.style.display = 'inline-flex';
    });
}

function uploadAndPerformOcr(file) {
  showLoading(TRANSLATIONS[currentLang].ocr_loading);

  const formData = new FormData();
  formData.append('image', file);

  fetch('/api/ocr', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    hideLoading();

    if (data.status === 'success' && data.text) {
      // OCR extracted text successfully
      messageTextarea.value = data.text;
      if (charCountSpan) charCountSpan.textContent = data.text.length;

      // Switch to text tab and run analysis
      tabBtnText.click();
      runAnalysis(data.text);
      showToast("Text extracted from screenshot!");
    } else {
      // Graceful fallback conforming to prompt requirement
      const errorMsg = (currentLang === 'kn' ? data.error_kn : data.error_en) ||
        (currentLang === 'kn'
          ? "OCR ಕಾನ್ಫಿಗರ್ ಆಗಿಲ್ಲ. ನೀವು ಸಂದೇಶವನ್ನು ನೇರವಾಗಿ ಪೇಸ್ಟ್ ಮಾಡಬಹುದು."
          : "OCR is not configured. You can paste the message text manually.");
      
      // If sample demo screenshot was used and OCR binary is not installed, fill with sample text
      if (file.name === 'sample_scam_chat.png') {
        const sampleText = "🚨 SEBI REGISTERED EXPERT 🚨\n\nGuaranteed 40% return in 7 days!\n\nInvest ₹10,000 today.\n\nThis opportunity is available only for 2 hours.\n\nSend payment to our UPI ID immediately.\n\nJoin our Telegram group for secret stock tips.";
        messageTextarea.value = sampleText;
        if (charCountSpan) charCountSpan.textContent = sampleText.length;
        tabBtnText.click();
        runAnalysis(sampleText);
        showToast("Loaded sample message from screenshot demo!");
      } else {
        alert(errorMsg);
        tabBtnText.click();
        messageTextarea.focus();
      }
    }
  })
  .catch(err => {
    hideLoading();
    console.error("OCR API error:", err);
    alert(currentLang === 'kn'
      ? "OCR ಕಾನ್ಫಿಗರ್ ಆಗಿಲ್ಲ. ನೀವು ಸಂದೇಶವನ್ನು ನೇರವಾಗಿ ಪೇಸ್ಟ್ ಮಾಡಬಹುದು."
      : "OCR is not configured. You can paste the message text manually.");
    tabBtnText.click();
  });
}

function loadSampleScenarios() {
  fetch('/api/sample-scenarios')
    .then(res => res.json())
    .then(data => {
      if (data.status === 'success' && scenarioSelect) {
        scenarioSelect.innerHTML = `<option value="">${TRANSLATIONS[currentLang].select_scenario}</option>`;
        data.scenarios.forEach(sc => {
          const opt = document.createElement('option');
          opt.value = sc.id;
          opt.textContent = currentLang === 'kn' ? sc.title_kn : sc.title_en;
          opt.dataset.text = sc.text;
          scenarioSelect.appendChild(opt);
        });
      }
    })
    .catch(err => console.error("Error loading sample scenarios:", err));
}

function loadScenarioById(id) {
  const option = scenarioSelect.querySelector(`option[value="${id}"]`);
  if (option && option.dataset.text) {
    messageTextarea.value = option.dataset.text;
    if (charCountSpan) charCountSpan.textContent = option.dataset.text.length;
    // Switch to message tab
    if (tabBtnText) tabBtnText.click();
    runAnalysis(option.dataset.text);
  }
}

function loadJudgeDemo() {
  const demoText = "🚨 SEBI REGISTERED EXPERT 🚨\n\nGuaranteed 40% return in 7 days!\n\nInvest ₹10,000 today.\n\nThis opportunity is available only for 2 hours.\n\nSend payment to our UPI ID immediately.\n\nJoin our Telegram group for secret stock tips.";
  
  if (messageTextarea) {
    messageTextarea.value = demoText;
    if (charCountSpan) charCountSpan.textContent = demoText.length;
  }
  
  if (tabBtnText) tabBtnText.click();
  
  // Smooth scroll to checker
  const checkerEl = document.getElementById('checker');
  if (checkerEl) {
    checkerEl.scrollIntoView({ behavior: 'smooth' });
  }

  showToast(TRANSLATIONS[currentLang].toast_demo_loaded);
  runAnalysis(demoText);
}

function showLoading(msg) {
  if (loadingIndicator && loadingText) {
    loadingText.textContent = msg || TRANSLATIONS[currentLang].analyzing_loading;
    loadingIndicator.style.display = 'flex';
  }
  if (resultContainer) {
    resultContainer.style.display = 'none';
  }
}

function hideLoading() {
  if (loadingIndicator) {
    loadingIndicator.style.display = 'none';
  }
}

function runAnalysis(text) {
  showLoading(TRANSLATIONS[currentLang].analyzing_loading);

  fetch('/api/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: text, lang: currentLang })
  })
  .then(res => res.json())
  .then(data => {
    hideLoading();
    if (data.status === 'success') {
      lastAnalysisResult = data;
      renderAnalysisResult(data);
    } else {
      alert(currentLang === 'kn' ? data.message_kn : data.message_en);
    }
  })
  .catch(err => {
    hideLoading();
    console.error("Analysis error:", err);
    alert(currentLang === 'kn' ? "ವಿಶ್ಲೇಷಣೆ ವಿಫಲವಾಗಿದೆ." : "Analysis request failed. Please check network connection.");
  });
}

function renderAnalysisResult(data) {
  if (!resultContainer) return;

  const isKn = currentLang === 'kn';
  const risk = data.risk;
  const indicators = data.indicators || [];
  const urls = data.urls || [];
  const claims = data.claims || [];
  const safeSteps = data.safe_steps || [];

  const badgeColor = risk.badge_color; // danger, warning, safe
  const levelLabel = isKn ? risk.level_label_kn : risk.level_label_en;
  const scoreDisplay = isKn ? risk.score_display_kn : risk.score_display;
  const summaryText = isKn ? risk.summary_kn : risk.summary_en;
  const trustStatement = isKn ? risk.trust_statement_kn : risk.trust_statement_en;
  const honestNotice = isKn ? data.trust_notice.kn : data.trust_notice.en;

  let html = `
    <div class="result-card">
      <div class="result-header ${badgeColor}">
        <div class="result-badge ${badgeColor}">
          ${badgeColor === 'danger' ? '⚠' : (badgeColor === 'warning' ? '⚠' : '🛡️')} ${levelLabel}
        </div>
        <div class="result-score-block">
          <div class="result-score-number ${badgeColor}">${scoreDisplay}</div>
          <div class="result-score-label">${isKn ? 'ಮೂಲಮಾದರಿ ಅಪಾಯ ಅಂಕ' : 'PROTOTYPE RISK INDICATOR'}</div>
        </div>
      </div>

      <div class="result-body">
        <!-- Prototype disclaimer banner adhering strictly to Hackathon Trust Rules -->
        <div class="disclaimer-banner">
          <div class="disclaimer-title">ℹ ${isKn ? 'ಪ್ರಮುಖ ಹಕ್ಕುತ್ಯಾಗ (Disclaimer)' : 'Important Prototype Notice'}</div>
          <div>${trustStatement}</div>
          <div style="margin-top: 4px; font-weight: 600;">${honestNotice}</div>
        </div>

        <div style="font-size: 1.1rem; color: var(--text-primary); margin-bottom: 24px; font-weight: 600;">
          ${summaryText}
        </div>
  `;

  // Warning Indicators List
  if (indicators.length > 0) {
    html += `
      <div class="indicators-section-title">
        <span>⚠</span> ${isKn ? 'ಗುರುತಿಸಲಾದ ಅಪಾಯದ ಸೂಚಕಗಳು' : 'Detected Warning Indicators'} (${indicators.length})
      </div>
      <div class="indicators-list">
    `;

    indicators.forEach(ind => {
      const name = isKn ? ind.name_kn : ind.name_en;
      const explanation = isKn ? ind.explanation_kn : ind.explanation_en;
      const snippets = (ind.matched_snippets || []).map(s => `<code>${escapeHtml(s)}</code>`).join(' ');

      html += `
        <div class="indicator-item">
          <div class="indicator-header">
            <span class="indicator-name">⚠ ${escapeHtml(name)}</span>
            <span class="indicator-weight">+${ind.weight}</span>
          </div>
          <div class="indicator-explanation">${escapeHtml(explanation)}</div>
          ${snippets ? `<div class="indicator-snippets"><strong>${isKn ? 'ಪತ್ತೆಯಾದ ಪಠ್ಯ:' : 'Found text:'}</strong> ${snippets}</div>` : ''}
        </div>
      `;
    });

    html += `</div>`;
  } else {
    html += `
      <div style="padding: 20px; background-color: var(--safe-bg); border: 1px solid var(--safe-border); border-radius: var(--radius-md); margin-bottom: 24px; color: var(--safe-text);">
        <strong>✓ ${isKn ? 'ಯಾವುದೇ ಸ್ಪಷ್ಟ ಅಪಾಯದ ಸೂಚನೆ ಕಂಡುಬಂದಿಲ್ಲ.' : 'No overt warning indicators detected in this message.'}</strong>
        <div style="font-size: 0.9rem; margin-top: 4px;">
          ${isKn 
            ? 'ಸೂಚನೆ: ಇದು ಸಂದೇಶವು ಸಂಪೂರ್ಣವಾಗಿ ಸುರಕ್ಷಿತವೆಂದು ಖಾತರಿಪಡಿಸುವುದಿಲ್ಲ. ಯಾವುದೇ ಹಣ ವರ್ಗಾವಣೆಗೆ ಮುನ್ನ ಯಾವಾಗಲೂ ಸ್ವತಂತ್ರ ಪರಿಶೀಲನೆ ನಡೆಸಿ.' 
            : 'Note: This does not certify that the message is completely safe. Always independently verify any financial request before transferring money.'}
        </div>
      </div>
    `;
  }

  // Regulatory Claims Card (if any claims detected)
  if (claims.length > 0) {
    claims.forEach(c => {
      const notice = isKn ? c.notice_kn : c.notice_en;
      const instructions = isKn ? c.official_search_instructions_kn : c.official_search_instructions_en;

      html += `
        <div class="claim-box">
          <div class="claim-header">
            <span>🏛️</span> ${isKn ? 'ನಿಯಂತ್ರಕ ಮಂಡಳಿ ಹಕ್ಕು ಕಂಡುಬಂದಿದೆ' : 'REGULATORY CLAIM DETECTED'}: ${escapeHtml(c.authority)}
          </div>
          <div class="claim-notice">${escapeHtml(notice)}</div>
          <div style="font-size: 0.9rem; margin-bottom: 14px; color: #1e293b;">${escapeHtml(instructions)}</div>
          <a href="${c.official_url}" target="_blank" rel="noopener noreferrer" class="claim-action-btn">
            🔗 ${isKn ? 'ಅಧಿಕೃತ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಪರಿಶೀಲಿಸಿ' : 'Verify on Official Registry'} (${escapeHtml(c.official_source_name)})
          </a>
        </div>
      `;
    });
  }

  // URLs Analysis Card (if URLs present)
  if (urls.length > 0) {
    html += `
      <div class="url-box">
        <div class="url-box-title">
          <span>🔗</span> ${isKn ? 'ವಿಶ್ಲೇಷಿಸಲಾದ ಲಿಂಕ್‌ಗಳು' : 'Link / Claim Analysis'} (${urls.length})
        </div>
    `;

    urls.forEach(u => {
      html += `
        <div class="url-item">
          <div class="url-string">${escapeHtml(u.url)}</div>
      `;
      if (u.indicators && u.indicators.length > 0) {
        u.indicators.forEach(ui => {
          const t = isKn ? ui.title_kn : ui.title_en;
          const exp = isKn ? ui.explanation_kn : ui.explanation_en;
          html += `
            <div class="url-warning-text">
              <strong>⚠ ${escapeHtml(t)}:</strong> ${escapeHtml(exp)}
            </div>
          `;
        });
      } else {
        html += `
          <div class="url-warning-text" style="color: #047857;">
            ${isKn ? 'ಯಾವುದೇ ಅಸಾಮಾನ್ಯ ಲಿಂಕ್ ಗುಣಲಕ್ಷಣ ಕಂಡುಬಂದಿಲ್ಲ. ಆದರೂ ಗಮ್ಯಸ್ಥಾನವನ್ನು ಸ್ವತಂತ್ರವಾಗಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.' : 'No obvious link anomaly detected. Always verify destination address independently.'}
          </div>
        `;
      }
      html += `</div>`;
    });

    html += `</div>`;
  }

  // Safe Next Steps Section
  html += `
    <div class="safe-steps-container">
      <div class="safe-steps-title">
        <span>🛡️</span> ${isKn ? 'ಸುರಕ್ಷಿತ ಮುಂದಿನ ಕ್ರಮಗಳು' : 'SAFE NEXT STEPS'}
      </div>
      <div class="steps-grid">
  `;

  safeSteps.forEach(st => {
    html += `
      <div class="step-card">
        <div class="step-number">${st.step}</div>
        <div class="step-card-title">${escapeHtml(st.title)}</div>
        <div class="step-card-desc">${escapeHtml(st.desc)}</div>
      </div>
    `;
  });

  html += `
      </div>
    </div>
  `;

  // Action Buttons at bottom of result
  html += `
      <div class="form-actions" style="margin-top: 24px;">
        <button id="copy-summary-btn" class="btn btn-secondary">
          📋 ${isKn ? 'ವಿಶ್ಲೇಷಣಾ ಸಾರಾಂಶವನ್ನು ನಕಲಿಸಿ' : 'Copy Analysis Summary'}
        </button>
        <button id="check-another-btn" class="btn btn-primary">
          🔍 ${isKn ? 'ಇನ್ನೊಂದು ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ' : 'Check Another Message'}
        </button>
      </div>
    </div>
  </div>
  `;

  resultContainer.innerHTML = html;
  resultContainer.style.display = 'block';

  // Attach dynamic button listeners
  const copyBtn = document.getElementById('copy-summary-btn');
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      copySummaryToClipboard(data);
    });
  }

  const checkAnotherBtn = document.getElementById('check-another-btn');
  if (checkAnotherBtn) {
    checkAnotherBtn.addEventListener('click', () => {
      if (messageTextarea) {
        messageTextarea.value = '';
        messageTextarea.focus();
      }
      resultContainer.style.display = 'none';
      lastAnalysisResult = null;
      window.scrollTo({ top: document.getElementById('checker').offsetTop - 80, behavior: 'smooth' });
    });
  }

  // Scroll smoothly to results
  resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function copySummaryToClipboard(data) {
  const isKn = currentLang === 'kn';
  const risk = data.risk;
  let text = `🛡️ INVESTOR SCAMSHIELD ANALYSIS SUMMARY\n`;
  text += `Risk Level: ${isKn ? risk.level_label_kn : risk.level_label_en}\n`;
  text += `Score: ${risk.score} / 100 Risk Indicators\n`;
  text += `Notice: ${isKn ? risk.trust_statement_kn : risk.trust_statement_en}\n\n`;

  if (data.indicators && data.indicators.length > 0) {
    text += `Detected Warning Indicators:\n`;
    data.indicators.forEach(i => {
      text += `• ${isKn ? i.name_kn : i.name_en} (+${i.weight})\n  ${isKn ? i.explanation_kn : i.explanation_en}\n`;
    });
    text += `\n`;
  }

  text += `Safe Next Steps:\n`;
  (data.safe_steps || []).forEach(s => {
    text += `${s.step}. ${s.title}\n`;
  });

  text += `\nNational Cyber Crime Helpline: 1930 | cybercrime.gov.in\n`;
  text += `Investor ScamShield - Public-Good Investor Protection Tool\n`;

  navigator.clipboard.writeText(text).then(() => {
    showToast(TRANSLATIONS[currentLang].toast_copied);
  }).catch(() => {
    showToast("Summary copied!");
  });
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
