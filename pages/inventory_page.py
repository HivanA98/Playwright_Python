from enum import Enum

from data import Product

from .base_page import AppPage
from .components import ProductCard


class SortOption(str, Enum):
    NAME_A_TO_Z = "az"
    NAME_Z_TO_A = "za"
    PRICE_LOW_TO_HIGH = "lohi"
    PRICE_HIGH_TO_LOW = "hilo"


class InventoryPage(AppPage):
    path = "/inventory.html"
    title_text = "Products"

    def __init__(self, page):
        super().__init__(page)
        self.cards = page.get_by_test_id("inventory-item")
        self.images = page.locator("img.inventory_item_img")
        self.sort_select = page.get_by_test_id("product-sort-container")
        self.active_sort = page.get_by_test_id("active-option")

    def product(self, name: str) -> ProductCard:
        return ProductCard.named(self.cards, name)

    def products(self) -> list[Product]:
        return [card.to_product() for card in ProductCard.all_in(self.cards)]

    def image_sources(self) -> list[str]:
        return [img.get_attribute("src") for img in self.images.all()]

    def sort_by(self, option: SortOption) -> "InventoryPage":
        self.sort_select.select_option(option.value)
        return self

    def add_to_cart(self, *products: Product) -> "InventoryPage":
        for product in products:
            self.product(product.name).add_to_cart()
        return self

    def remove_from_cart(self, *products: Product) -> "InventoryPage":
        for product in products:
            self.product(product.name).remove()
        return self

    def open_product(self, product: Product):
        return self.product(product.name).open_details()
