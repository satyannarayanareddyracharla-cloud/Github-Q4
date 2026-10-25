import os
from pathlib import Path


BASE_URL = os.getenv("FORMS_BASE_URL", "https://qapracticehub.com/#forms")
HEADLESS = os.getenv("HEADLESS", "true").lower() not in {"0", "false", "no"}
PAGE_LOAD_TIMEOUT = 30
WINDOW_SIZE = "1440,1000"
PROJECT_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_DIR / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
