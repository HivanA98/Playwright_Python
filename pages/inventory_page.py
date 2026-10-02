from .base_page import BasePage


def _slug(product_name: str) -> str:
    """'Sauce Labs Backpack' -> 'sauce-labs-backpack' (Saucedemo's data-test suffix)."""
    return product_name.lower().replace(" ", "-")


class InventoryPage(BasePage):
    path = "/inventory.html"

    def __init__(self, page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.sort_select = page.get_by_test_id("product-sort-container")

    def add_to_cart(self, product_name: str):
        self.page.get_by_test_id(f"add-to-cart-{_slug(product_name)}").click()

    def remove_from_cart(self, product_name: str):
        self.page.get_by_test_id(f"remove-{_slug(product_name)}").click()

    def sort_by(self, option: str):
        """option: 'az', 'za', 'lohi', 'hilo'."""
        self.sort_select.select_option(option)

    def names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def prices(self) -> list[float]:
        return [float(p.lstrip("$")) for p in self.item_prices.all_inner_texts()]
