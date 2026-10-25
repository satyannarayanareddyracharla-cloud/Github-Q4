import re
import sys
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from behave.model import Status
from selenium.common.exceptions import WebDriverException

from utils.config import (
    BASE_URL,
    HEADLESS,
    PAGE_LOAD_TIMEOUT,
    SCREENSHOTS_DIR,
    WINDOW_SIZE,
)


def before_all(context):
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={WINDOW_SIZE}")

    context.driver = webdriver.Chrome(options=options)
    context.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    context.base_url = BASE_URL


def after_all(context):
    driver = getattr(context, "driver", None)
    if driver is not None:
        driver.quit()


def after_step(context, step):
    if step.status not in {Status.failed, Status.error}:
        return

    driver = getattr(context, "driver", None)
    if driver is None:
        print(
            "Could not capture failure screenshot: WebDriver is unavailable.",
            file=sys.stderr,
        )
        return

    scenario = getattr(context, "scenario", None)
    feature_name = getattr(getattr(scenario, "feature", None), "name", "feature")
    scenario_name = getattr(scenario, "name", "scenario")
    filename_parts = (
        _safe_filename(feature_name),
        _safe_filename(scenario_name),
        _safe_filename(step.name),
        datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
    )
    screenshot_path = SCREENSHOTS_DIR.joinpath(
        "__".join(filename_parts) + ".png"
    )

    try:
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        if not driver.save_screenshot(str(screenshot_path)):
            raise OSError("WebDriver reported that the screenshot was not saved.")
    except (OSError, WebDriverException) as error:
        print(
            f"Could not capture failure screenshot at {screenshot_path}: {error}",
            file=sys.stderr,
        )
        return

    print(f"Failure screenshot saved: {screenshot_path}")


def _safe_filename(value):
    return re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_") or "unnamed"
