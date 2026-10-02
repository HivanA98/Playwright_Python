import pytest
from playwright.sync_api import expect

from data import Users
from pages import InventoryPage, LoginPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_standard_user_can_login(login_page: LoginPage):
    inventory = login_page.login(Users.STANDARD)

    expect(inventory.cards).to_have_count(6)


def test_locked_out_user_sees_error(login_page: LoginPage):
    login_page.login_expecting_error(Users.LOCKED_OUT.username, Users.LOCKED_OUT.password)

    expect(login_page.error).to_contain_text("this user has been locked out")


@pytest.mark.parametrize(
    "username, password, message",
    [
        ("", "", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("unknown_user", "secret_sauce", "Username and password do not match"),
    ],
    ids=["empty-form", "missing-password", "wrong-password", "unknown-user"],
)
def test_invalid_login_shows_error(login_page: LoginPage, username, password, message):
    login_page.login_expecting_error(username, password)

    expect(login_page.error).to_contain_text(message)
    expect(login_page.page).not_to_have_url(InventoryPage.path)


def test_protected_page_requires_login(page):
    page.goto(InventoryPage.path)

    login = LoginPage(page).should_be_loaded()
    expect(login.error).to_contain_text(
        "You can only access '/inventory.html' when you are logged in"
    )


def test_logout_ends_session(inventory_page: InventoryPage):
    login = inventory_page.header.logout()

    login.page.goto(InventoryPage.path)
    expect(login.error).to_contain_text("when you are logged in")
