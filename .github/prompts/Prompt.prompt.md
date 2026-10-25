---
name: "Forms Automation"
description: "Create or extend Behave Gherkin scenarios and Selenium page-object automation for the QA Practice Hub Forms page."
argument-hint: "Describe the form behavior or test scenario to add"
agent: "agent"
---

Create or update the Forms automation for this project based on the requested
behavior:

${input:requirement:Describe the form behavior or test scenarios to implement}

Project context:

- The target page is `https://qapracticehub.com/#forms`.
- This project uses Python, Selenium WebDriver, Behave, Gherkin, and the Page
  Object Model.
- Feature scenarios live in `features/form_submission.feature`.
- Reusable Behave steps live in `features/steps/form_steps.py`.
- Selenium locators and browser interactions belong in `pages/forms_page.py`;
  keep direct WebDriver calls out of step definitions.
- Browser and failure-screenshot hooks are in `features/environment.py`.
- Browser settings and report paths are in `utils/config.py`.
- Failed steps save screenshots under `reports/screenshots/`.

Before making changes, inspect the existing feature, step definitions, page
object, configuration, and README. Reuse existing parameterized steps and page
object methods where possible. If the requested behavior needs a new UI
interaction, implement it in the page object and expose it through a reusable
Behave step. Keep scenario language readable and use Gherkin data tables or
Scenario Outlines for variable form inputs.

After implementation:

1. Run the complete Behave suite from the `Question 4` project directory:

   ```powershell
   & "..\.venv-repaired\Scripts\python.exe" -m behave
   ```

2. If the tests pass, refresh the HTML report:

   ```powershell
   & "..\.venv-repaired\Scripts\python.exe" -m behave --format html --outfile reports\behave-report.html
   ```

3. Update the README only when scenario coverage or project usage changes.
4. Report the files changed, test results, and any failures or assumptions.
