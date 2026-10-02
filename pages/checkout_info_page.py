from playwright.sync_api import expect

from data import Customer

from .base_page import AppPage


class CheckoutInfoPage(AppPage):
    """Checkout step one: customer information form."""

    path = "/checkout-step-one.html"
    title_text = "Checkout: Your Information"

    def __init__(self, page):
        super().__init__(page)
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.cancel_button = page.get_by_test_id("cancel")
        self.error = page.get_by_test_id("error")

    def fill(self, customer: Customer) -> "CheckoutInfoPage":
        self.first_name.fill(customer.first_name)
        self.last_name.fill(customer.last_name)
        self.postal_code.fill(customer.postal_code)
        return self

    def continue_to_overview(self):
        from .checkout_overview_page import CheckoutOverviewPage

        self.continue_button.click()
        return CheckoutOverviewPage(self.page).should_be_loaded()

    def continue_expecting_error(self) -> "CheckoutInfoPage":
        self.continue_button.click()
        expect(self.error).to_be_visible()
        return self

    def cancel(self):
        from .cart_page import CartPage

        self.cancel_button.click()
        return CartPage(self.page).should_be_loaded()
