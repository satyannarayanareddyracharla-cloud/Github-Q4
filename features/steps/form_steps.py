from behave import given, then, when

from pages.forms_page import FormsPage


@given("the Forms page is open")
def open_forms_page(context):
    context.forms_page = FormsPage(context.driver, context.base_url)
    context.forms_page.open()


@then('I should see the "{first_section}" and "{second_section}" sections')
def verify_sections_visible(context, first_section, second_section):
    assert context.forms_page.section_is_visible(first_section)
    assert context.forms_page.section_is_visible(second_section)


@when('I open the "{form_name}" form')
def open_form(context, form_name):
    context.forms_page.open_form(form_name)


@when('I fill the "{form_name}" form with')
def fill_form(context, form_name):
    values = {row["field"]: row["value"] for row in context.table}
    context.forms_page.fill_form(form_name, values)


@when('I submit the "{form_name}" form')
def submit_form(context, form_name):
    context.forms_page.submit_form(form_name)


@then('the "{form_name}" form feedback should contain "{expected}"')
def verify_form_feedback(context, form_name, expected):
    try:
        actual = context.forms_page.form_feedback(form_name)
        assert expected in actual, (
            f"Expected {form_name!r} feedback to contain {expected!r}, "
            f"but got {actual!r}."
        )
    finally:
        context.forms_page.close_form(form_name)


@then('the "{field_name}" field on the "{form_name}" form should be invalid')
def verify_field_invalid(context, field_name, form_name):
    assert not context.forms_page.field_is_valid(form_name, field_name), (
        f"Expected {field_name!r} on {form_name!r} to be invalid."
    )


@when('I toggle visibility of the "{field_name}" field on the "{form_name}" form')
def toggle_field_visibility(context, field_name, form_name):
    context.forms_page.toggle_field_visibility(form_name, field_name)


@then('the "{field_name}" field on the "{form_name}" form should be "{visibility}"')
def verify_field_visibility(context, field_name, form_name, visibility):
    expected_visibility = visibility.lower()
    assert expected_visibility in {"visible", "hidden"}, (
        "Visibility must be either 'visible' or 'hidden'."
    )
    actual_type = context.forms_page.field_type(form_name, field_name)
    expected_type = "text" if expected_visibility == "visible" else "password"
    assert actual_type == expected_type, (
        f"Expected {field_name!r} on {form_name!r} to be {expected_visibility}, "
        f"but its input type was {actual_type!r}."
    )


@when('I clear the "{form_name}" form')
def clear_form(context, form_name):
    context.forms_page.clear_form(form_name)


@then('all fields on the "{form_name}" form should be empty or unselected')
def verify_form_is_clear(context, form_name):
    assert context.forms_page.form_fields_are_empty(form_name), (
        f"Expected every field on the {form_name!r} form to be empty or unselected."
    )
