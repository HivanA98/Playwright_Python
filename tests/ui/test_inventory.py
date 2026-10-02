import pytest
from playwright.sync_api import expect

from data import Products
from pages import InventoryPage, SortOption

pytestmark = pytest.mark.ui


def by_name(products):
    return sorted(products, key=lambda p: p.name)


@pytest.mark.smoke
def test_catalog_matches_test_data(inventory_page: InventoryPage):
    assert by_name(inventory_page.products()) == by_name(Products.ALL)


@pytest.mark.parametrize(
    "option, sort_key, reverse",
    [
        (SortOption.NAME_A_TO_Z, lambda p: p.name, False),
        (SortOption.NAME_Z_TO_A, lambda p: p.name, True),
        (SortOption.PRICE_LOW_TO_HIGH, lambda p: p.price, False),
        (SortOption.PRICE_HIGH_TO_LOW, lambda p: p.price, True),
    ],
    ids=lambda v: v.name if isinstance(v, SortOption) else "",
)
def test_sorting(inventory_page: InventoryPage, option, sort_key, reverse):
    products = inventory_page.sort_by(option).products()

    assert products == sorted(products, key=sort_key, reverse=reverse)


def test_add_and_remove_updates_cart_badge(inventory_page: InventoryPage):
    inventory_page.add_to_cart(Products.BACKPACK, Products.BIKE_LIGHT)
    inventory_page.header.should_have_cart_count(2)

    inventory_page.remove_from_cart(Products.BACKPACK)
    inventory_page.header.should_have_cart_count(1)
    expect(inventory_page.product(Products.BACKPACK.name).add_button).to_be_visible()

    inventory_page.remove_from_cart(Products.BIKE_LIGHT)
    inventory_page.header.should_have_cart_count(0)


@pytest.mark.parametrize("product", Products.ALL, ids=lambda p: p.name)
def test_product_detail_matches_inventory_card(inventory_page: InventoryPage, product):
    card = inventory_page.product(product.name).to_product()

    detail = inventory_page.open_product(product)

    assert detail.product() == card == product
    assert detail.product().description == card.description
    detail.back_to_products()
