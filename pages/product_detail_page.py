from playwright.sync_api import expect

from data import Product

from .base_page import AppPage
from .components import ProductCard


class ProductDetailPage(AppPage):
    path = "/inventory-item.html"

    def __init__(self, page):
        super().__init__(page)
        self.card = ProductCard(page.get_by_test_id("inventory-item"))
        self.back_button = page.get_by_test_id("back-to-products")

    def should_be_loaded(self):
        super().should_be_loaded()
        expect(self.card.name).to_be_visible()
        return self

    def product(self) -> Product:
        return self.card.to_product()

    def add_to_cart(self) -> "ProductDetailPage":
        self.card.add_to_cart()
        return self

    def remove(self) -> "ProductDetailPage":
        self.card.remove()
        return self

    def back_to_products(self):
        from .inventory_page import InventoryPage

        self.back_button.click()
        return InventoryPage(self.page).should_be_loaded()
