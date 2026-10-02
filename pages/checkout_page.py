import re

from .base_page import BasePage


class CheckoutPage(BasePage):
    """Covers step one (info form), step two (overview) and complete page."""

    path = "/checkout-step-one.html"

    def __init__(self, page):
        super().__init__(page)
        # Step one
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.error = page.get_by_test_id("error")
        # Step two
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")
        # Complete
        self.complete_header = page.get_by_test_id("complete-header")

    def fill_info(self, first: str, last: str, postal: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()

    @staticmethod
    def _amount(text: str) -> float:
        return float(re.search(r"\$([\d.]+)", text).group(1))

    def subtotal_amount(self) -> float:
        return self._amount(self.subtotal.inner_text())

    def tax_amount(self) -> float:
        return self._amount(self.tax.inner_text())

    def total_amount(self) -> float:
        return self._amount(self.total.inner_text())

    def item_price_sum(self) -> float:
        return round(sum(float(p.lstrip("$")) for p in self.item_prices.all_inner_texts()), 2)

    def finish(self):
        self.finish_button.click()
