from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class FormsPage:
    PAGE_HEADING = (
        By.XPATH,
        "//h2[normalize-space()='Login & Registration Forms']",
    )
    COOKIE_ACCEPT = (By.ID, "cookie-accept")

    FORM_FIELDS = {
        "login": {
            "username": (By.ID, "login-username"),
            "password": (By.ID, "login-password"),
        },
        "password recovery": {
            "username": (By.ID, "forgot-username"),
        },
        "registration": {
            "first name": (By.ID, "reg-firstname"),
            "last name": (By.ID, "reg-lastname"),
            "email": (By.ID, "reg-email"),
            "country": (By.ID, "reg-country"),
        },
    }
    FORM_SUBMIT_BUTTONS = {
        "login": (By.ID, "login-submit"),
        "password recovery": (By.ID, "forgot-password-submit"),
        "registration": (By.ID, "register-submit"),
    }
    FORM_FEEDBACK = {
        "login": (By.ID, "login-message"),
        "password recovery": (By.ID, "forgot-password-message"),
        "registration": (By.ID, "register-message"),
    }
    PASSWORD_TOGGLES = {
        ("login", "password"): (By.ID, "login-password-toggle"),
    }
    FORM_CLEAR_BUTTONS = {
        "registration": (By.ID, "register-clear"),
    }
    PASSWORD_RECOVERY_RESULT = (By.ID, "forgot-password-result")
    PASSWORD_RECOVERY_MODAL = (By.ID, "forgot-password-modal")
    PASSWORD_RECOVERY_OPEN = (By.ID, "forgot-password-trigger")
    PASSWORD_RECOVERY_CLOSE = (By.ID, "forgot-password-modal-close")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("about:blank")
        self.driver.get(self.base_url)
        self.wait.until(EC.visibility_of_element_located(self.PAGE_HEADING))

        cookie_accept = self.driver.find_elements(*self.COOKIE_ACCEPT)
        if cookie_accept and cookie_accept[0].is_displayed():
            cookie_accept[0].click()

    def section_is_visible(self, title):
        return self.driver.find_element(
            By.XPATH, f"//h3[normalize-space()='{title}']"
        ).is_displayed()

    def open_form(self, form_name):
        form = self._normalize_form_name(form_name)
        if form == "password recovery":
            modal = self.driver.find_element(*self.PASSWORD_RECOVERY_MODAL)
            if not modal.is_displayed():
                self.driver.find_element(*self.PASSWORD_RECOVERY_OPEN).click()

    def fill_form(self, form_name, values):
        form = self._normalize_form_name(form_name)
        fields = self.FORM_FIELDS[form]
        for field_name, value in values.items():
            field = self._normalize_field_name(field_name)
            if field not in fields:
                raise ValueError(
                    f"Field {field_name!r} is not available on the {form!r} form."
                )

            locator = fields[field]
            if field == "country":
                Select(self.driver.find_element(*locator)).select_by_visible_text(
                    value or "Select country"
                )
            else:
                self._fill_text_field(locator, value)

    def submit_form(self, form_name):
        form = self._normalize_form_name(form_name)
        self.driver.find_element(*self.FORM_SUBMIT_BUTTONS[form]).click()

    def form_feedback(self, form_name):
        form = self._normalize_form_name(form_name)
        if form == "password recovery":
            result = self.driver.find_element(*self.PASSWORD_RECOVERY_RESULT)
            if result.is_displayed() and result.text.strip():
                return result.text.strip()
        return self._message_text(self.FORM_FEEDBACK[form])

    def field_is_valid(self, form_name, field_name):
        locator = self._field_locator(form_name, field_name)
        field = self.driver.find_element(*locator)
        return self.driver.execute_script("return arguments[0].checkValidity()", field)

    def toggle_field_visibility(self, form_name, field_name):
        form = self._normalize_form_name(form_name)
        field = self._normalize_field_name(field_name)
        toggle = self.PASSWORD_TOGGLES.get((form, field))
        if toggle is None:
            raise ValueError(
                f"Password visibility is not supported for "
                f"{field_name!r} on the {form_name!r} form."
            )
        self.driver.find_element(*toggle).click()

    def field_type(self, form_name, field_name):
        field = self.driver.find_element(*self._field_locator(form_name, field_name))
        return field.get_attribute("type")

    def clear_form(self, form_name):
        form = self._normalize_form_name(form_name)
        clear_button = self.FORM_CLEAR_BUTTONS.get(form)
        if clear_button is None:
            raise ValueError(f"Clearing the {form_name!r} form is not supported.")
        self.driver.find_element(*clear_button).click()

    def close_form(self, form_name):
        form = self._normalize_form_name(form_name)
        if form == "password recovery":
            modal = self.driver.find_element(*self.PASSWORD_RECOVERY_MODAL)
            if modal.is_displayed():
                self.driver.find_element(*self.PASSWORD_RECOVERY_CLOSE).click()

    def form_fields_are_empty(self, form_name):
        form = self._normalize_form_name(form_name)
        fields = self.FORM_FIELDS[form]
        for field_name, locator in fields.items():
            element = self.driver.find_element(*locator)
            if field_name == "country":
                if Select(element).first_selected_option.text != "Select country":
                    return False
            elif element.get_attribute("value") != "":
                return False
        return True

    def _field_locator(self, form_name, field_name):
        form = self._normalize_form_name(form_name)
        field = self._normalize_field_name(field_name)
        try:
            return self.FORM_FIELDS[form][field]
        except KeyError as error:
            raise ValueError(
                f"Field {field_name!r} is not available on the {form_name!r} form."
            ) from error

    def _message_text(self, locator):
        message = self.wait.until(EC.visibility_of_element_located(locator))
        return message.text.strip()

    def _fill_text_field(self, locator, value):
        field = self.driver.find_element(*locator)
        field.clear()
        if value:
            field.send_keys(value)

    @staticmethod
    def _normalize_form_name(form_name):
        normalized = " ".join(form_name.strip().lower().replace("-", " ").split())
        if normalized not in FormsPage.FORM_FIELDS:
            raise ValueError(f"Unknown form: {form_name!r}.")
        return normalized

    @staticmethod
    def _normalize_field_name(field_name):
        return " ".join(field_name.strip().lower().replace("_", " ").split())
