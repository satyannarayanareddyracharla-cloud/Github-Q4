# BDD Forms Assignment

Behave and Selenium browser tests for the Login and Registration Forms section at
`https://qapracticehub.com/#forms`.

## Project structure

```text
Question 4/
├── .github/
│   └── prompts/
│       └── Prompt.prompt.md
├── features/
│   ├── form_submission.feature
│   ├── steps/
│   │   └── form_steps.py
│   └── environment.py
├── pages/
│   └── forms_page.py
├── utils/
│   └── config.py
├── behave.ini
├── reports/
│   └── screenshots/  # PNG screenshots captured for failed steps
├── requirements.txt
└── README.md
```

## Scenarios

- Login and registration form sections are displayed.
- Valid and invalid login credentials show the expected feedback.
- Empty login username and password are rejected by required-field validation.
- The login password can be shown and hidden.
- Password recovery validates an empty username and recovers the practice
  account password for `tester`.
- Registration validates required fields and country selection, and rejects
  invalid email formats.
- Valid registration succeeds, and Clear resets the form.

The suite accepts the site's cookie banner when it appears and uses explicit
waits for dynamic page content. Headless Chrome is enabled by default.

## Setup (PowerShell)

From the project root:

```powershell
py -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
```

Chrome must be installed. Selenium Manager resolves the matching driver.

## Run

```powershell
& ".\.venv\Scripts\python.exe" -m behave
```

To create an HTML report under `reports/`:

```powershell
& ".\.venv\Scripts\python.exe" -m behave --format html --outfile reports\behave-report.html
```

When a step fails, Behave captures a browser screenshot in
`reports/screenshots/`. Each PNG filename includes the feature, scenario, failed
step, and capture timestamp.

Set `HEADLESS=false` to show the browser, or set `FORMS_BASE_URL` to override
the target page.

## Page Object Model

The Behave step definitions express business actions and assertions without
locating or manipulating web elements directly. `pages/forms_page.py` owns the
Forms page locators and Selenium interactions, while `features/environment.py`
creates and closes the browser and captures screenshots for failed steps.
Configuration such as the base URL and browser settings lives in
`utils/config.py`.

## Reusable Gherkin steps

The step definitions in `features/steps/form_steps.py` are parameterized so
scenarios can reuse the same actions and assertions with different form data:

| Step | Purpose |
| --- | --- |
| `When I open the "password recovery" form` | Open a supported form or modal |
| `When I fill the "login" form with` | Fill fields from a Gherkin data table with `field` and `value` columns |
| `When I submit the "registration" form` | Submit a supported form |
| `Then the "login" form feedback should contain "..."` | Check form feedback |
| `Then the "email" field on the "registration" form should be invalid` | Check native browser field validation |
| `When I toggle visibility of the "password" field on the "login" form` | Toggle a supported password field |
| `Then the "password" field on the "login" form should be "visible"` | Check password visibility |
| `When I clear the "registration" form` | Clear a form with a supported clear action |
| `Then all fields on the "registration" form should be empty or unselected` | Verify that a form has reset |

Supported form names are `login`, `password recovery`, and `registration`.
Field names are defined by each form and are normalized for case and spacing.
Add new UI locators and form behavior to the page object rather than putting
Selenium operations in step definitions.

The reusable VS Code Copilot prompt for adding or extending form automation is
available at `.github/prompts/Prompt.prompt.md`. Invoke it from chat with `/Forms
Automation` and describe the behavior to implement.
