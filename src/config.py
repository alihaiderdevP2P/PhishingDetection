"""Project paths, class names, and training constants."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "phishing.csv"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

RANDOM_STATE = 42
TEST_SIZE = 0.20
CV_FOLDS = 5

TARGET_COLUMN = "label"
LABEL_NAMES = {0: "Safe", 1: "Suspicious", 2: "Phishing"}
CLASS_ORDER = [0, 1, 2]

# Ranking: phishing recall first (missed attacks), then macro F1, then accuracy.
RANK_KEYS = ("test_phishing_recall", "test_macro_f1", "test_accuracy")

URL_SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
    "buff.ly",
    "cutt.ly",
}

SUSPICIOUS_TLDS = {
    "tk",
    "ml",
    "ga",
    "cf",
    "gq",
    "xyz",
    "top",
    "click",
    "loan",
    "work",
    "rest",
    "country",
    "kim",
    "science",
}

BRAND_TOKENS = (
    "paypal",
    "apple",
    "google",
    "microsoft",
    "amazon",
    "netflix",
    "facebook",
    "instagram",
    "whatsapp",
    "bank",
    "chase",
    "wellsfargo",
    "hsbc",
    "citi",
    "outlook",
    "office365",
    "dhl",
    "fedex",
    "ups",
)

URGENCY_CUES = (
    "urgent",
    "immediately",
    "suspend",
    "suspended",
    "verify",
    "confirm",
    "limited time",
    "act now",
    "last chance",
    "expire",
    "expires",
    "locked",
    "unusual activity",
    "click here",
    "click below",
)

CREDENTIAL_CUES = (
    "password",
    "otp",
    "one-time",
    "pin",
    "ssn",
    "social security",
    "cvv",
    "card number",
    "account details",
    "login",
    "sign in",
    "credentials",
    "security code",
)

MONEY_CUES = (
    "won",
    "winner",
    "prize",
    "lottery",
    "refund",
    "wire",
    "bitcoin",
    "gift card",
    "tax refund",
    "claim",
    "million",
    "inheritance",
    "payment failed",
    "unpaid",
)

MODEL_FILES = {
    "best_model": MODELS_DIR / "best_model.joblib",
    "all_models": MODELS_DIR / "all_models.joblib",
    "metrics": REPORTS_DIR / "model_comparison.json",
    "feature_names": MODELS_DIR / "feature_names.joblib",
    "metadata": MODELS_DIR / "metadata.joblib",
}

for path in (MODELS_DIR, REPORTS_DIR, FIGURES_DIR):
    path.mkdir(parents=True, exist_ok=True)
