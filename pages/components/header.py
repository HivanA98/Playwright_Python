from playwright.sync_api import Page, expect


class HeaderComponent:
    """Top bar shown on every page after login: burger menu + cart icon."""

    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.open_menu_button = page.get_by_role("button", name="Open Menu")
        self.close_menu_button = page.get_by_role("button", name="Close Menu")

    def should_have_cart_count(self, count: int, timeout: float | None = None):
        if count == 0:
            expect(self.cart_badge).to_be_hidden(timeout=timeout)
        else:
            expect(self.cart_badge).to_have_text(str(count), timeout=timeout)

    def open_cart(self):
        from pages.cart_page import CartPage

        self.cart_link.click()
        return CartPage(self.page).should_be_loaded()

    def _click_menu_item(self, test_id: str):
        self.open_menu_button.click()
        self.page.get_by_test_id(test_id).click()

    def all_items(self):
        from pages.inventory_page import InventoryPage

        self._click_menu_item("inventory-sidebar-link")
        return InventoryPage(self.page).should_be_loaded()

    def reset_app_state(self):
        self._click_menu_item("reset-sidebar-link")
        self.close_menu_button.click()

    def logout(self):
        from pages.login_page import LoginPage

        self._click_menu_item("logout-sidebar-link")
        return LoginPage(self.page).should_be_loaded()
