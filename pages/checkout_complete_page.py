from .base_page import AppPage


class CheckoutCompletePage(AppPage):
    path = "/checkout-complete.html"
    title_text = "Checkout: Complete!"

    def __init__(self, page):
        super().__init__(page)
        self.complete_header = page.get_by_test_id("complete-header")
        self.complete_text = page.get_by_test_id("complete-text")
        self.back_home_button = page.get_by_test_id("back-to-products")

    def back_home(self):
        from .inventory_page import InventoryPage

        self.back_home_button.click()
        return InventoryPage(self.page).should_be_loaded()
