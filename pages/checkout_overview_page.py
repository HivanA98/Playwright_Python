from data import OrderSummary, Product, money

from .base_page import AppPage
from .components import ProductCard


class CheckoutOverviewPage(AppPage):
    """Checkout step two: order review with totals."""

    path = "/checkout-step-two.html"
    title_text = "Checkout: Overview"

    def __init__(self, page):
        super().__init__(page)
        self.cards = page.get_by_test_id("inventory-item")
        self.payment_info = page.get_by_test_id("payment-info-value")
        self.shipping_info = page.get_by_test_id("shipping-info-value")
        self.subtotal_label = page.get_by_test_id("subtotal-label")
        self.tax_label = page.get_by_test_id("tax-label")
        self.total_label = page.get_by_test_id("total-label")
        self.finish_button = page.get_by_test_id("finish")
        self.cancel_button = page.get_by_test_id("cancel")

    def products(self) -> list[Product]:
        return [card.to_product() for card in ProductCard.all_in(self.cards)]

    def summary(self) -> OrderSummary:
        return OrderSummary(
            item_total=money(self.subtotal_label.inner_text()),
            tax=money(self.tax_label.inner_text()),
            total=money(self.total_label.inner_text()),
        )

    def finish(self):
        from .checkout_complete_page import CheckoutCompletePage

        self.finish_button.click()
        return CheckoutCompletePage(self.page).should_be_loaded()

    def cancel(self):
        from .inventory_page import InventoryPage

        self.cancel_button.click()
        return InventoryPage(self.page).should_be_loaded()
