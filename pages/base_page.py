from playwright.sync_api import Page


class BasePage:
    """Shared helpers for all Saucedemo pages.

    Saucedemo tags elements with `data-test`, which conftest registers as
    Playwright's test-id attribute, so `get_by_test_id` works everywhere.
    """

    path = "/"

    def __init__(self, page: Page):
        self.page = page
        self.title = page.get_by_test_id("title")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")

    def open(self):
        self.page.goto(self.path)
        return self

    def cart_count(self) -> int:
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def go_to_cart(self):
        self.cart_link.click()

    def logout(self):
        self.page.get_by_role("button", name="Open Menu").click()
        self.page.get_by_test_id("logout-sidebar-link").click()
