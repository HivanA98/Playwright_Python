import pytest
from playwright.sync_api import expect

from pages import InventoryPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_standard_user_can_login(login_page, password):
    login_page.login("standard_user", password)

    expect(login_page.page).to_have_url("/inventory.html")
    expect(InventoryPage(login_page.page).title).to_have_text("Products")


def test_locked_out_user_sees_error(login_page, password):
    login_page.login("locked_out_user", password)

    expect(login_page.error).to_contain_text("this user has been locked out")


@pytest.mark.parametrize(
    "username, pwd, message",
    [
        ("", "", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("unknown_user", "secret_sauce", "Username and password do not match"),
    ],
    ids=["empty-form", "missing-password", "wrong-password", "unknown-user"],
)
def test_invalid_login_shows_error(login_page, username, pwd, message):
    login_page.login(username, pwd)

    expect(login_page.error).to_contain_text(message)
    expect(login_page.page).not_to_have_url("/inventory.html")


def test_protected_page_requires_login(page):
    page.goto("/inventory.html")

    expect(page.get_by_test_id("error")).to_contain_text(
        "You can only access '/inventory.html' when you are logged in"
    )


def test_logout_returns_to_login(inventory_page):
    inventory_page.logout()

    expect(inventory_page.page.get_by_test_id("login-button")).to_be_visible()
