from data import Product

from .base_page import AppPage
from .components import ProductCard


class CartPage(AppPage):
    path = "/cart.html"
    title_text = "Your Cart"

    def __init__(self, page):
        super().__init__(page)
        self.cards = page.get_by_test_id("inventory-item")
        self.checkout_button = page.get_by_test_id("checkout")
        self.continue_shopping_button = page.get_by_test_id("continue-shopping")

    def item(self, product: Product) -> ProductCard:
        return ProductCard.named(self.cards, product.name)

    def items(self) -> list[ProductCard]:
        return ProductCard.all_in(self.cards)

    def products(self) -> list[Product]:
        return [card.to_product() for card in self.items()]

    def remove(self, *products: Product) -> "CartPage":
        for product in products:
            self.item(product).remove()
        return self

    def continue_shopping(self):
        from .inventory_page import InventoryPage

        self.continue_shopping_button.click()
        return InventoryPage(self.page).should_be_loaded()

    def checkout(self):
        from .checkout_info_page import CheckoutInfoPage

        self.checkout_button.click()
        return CheckoutInfoPage(self.page).should_be_loaded()
