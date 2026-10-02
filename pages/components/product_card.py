import re

from playwright.sync_api import Locator

from data import Product, money


class ProductCard:
    """A single product block.

    Saucedemo renders products with the same `inventory-item` markup on the
    inventory list, product detail, cart and checkout overview pages, so one
    component covers all of them.
    """

    def __init__(self, root: Locator):
        self.root = root
        self.name = root.get_by_test_id("inventory-item-name")
        self.price = root.get_by_test_id("inventory-item-price")
        self.description = root.get_by_test_id("inventory-item-desc")
        self.quantity = root.get_by_test_id("item-quantity")
        self.add_button = root.get_by_role("button", name="Add to cart")
        self.remove_button = root.get_by_role("button", name="Remove")

    @classmethod
    def named(cls, cards: Locator, name: str) -> "ProductCard":
        """The card in `cards` whose product name is exactly `name`."""
        exact_name = cards.page.get_by_test_id("inventory-item-name").filter(
            has_text=re.compile(f"^{re.escape(name)}$")
        )
        return cls(cards.filter(has=exact_name))

    @classmethod
    def all_in(cls, cards: Locator) -> list["ProductCard"]:
        return [cls(card) for card in cards.all()]

    def to_product(self) -> Product:
        return Product(
            name=self.name.inner_text(),
            price=money(self.price.inner_text()),
            description=self.description.inner_text(),
        )

    def add_to_cart(self) -> "ProductCard":
        self.add_button.click()
        return self

    def remove(self) -> "ProductCard":
        self.remove_button.click()
        return self

    def open_details(self):
        from pages.product_detail_page import ProductDetailPage

        self.name.click()
        return ProductDetailPage(self.root.page).should_be_loaded()
