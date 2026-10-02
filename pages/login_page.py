from playwright.sync_api import expect

from data import User

from .base_page import BasePage


class LoginPage(BasePage):
    path = "/"

    def __init__(self, page):
        super().__init__(page)
        self.username = page.get_by_test_id("username")
        self.password = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error = page.get_by_test_id("error")

    def should_be_loaded(self):
        expect(self.login_button).to_be_visible()
        return self

    def _submit(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def login(self, user: User):
        """Happy path: returns the inventory page."""
        from .inventory_page import InventoryPage

        self._submit(user.username, user.password)
        return InventoryPage(self.page).should_be_loaded()

    def login_expecting_error(self, username: str, password: str) -> "LoginPage":
        self._submit(username, password)
        expect(self.error).to_be_visible()
        return self
