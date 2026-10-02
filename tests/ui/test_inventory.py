import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_inventory_lists_six_products(inventory_page):
    expect(inventory_page.items).to_have_count(6)


def test_sort_by_name_z_to_a(inventory_page):
    inventory_page.sort_by("za")

    names = inventory_page.names()
    assert names == sorted(names, reverse=True)


def test_sort_by_price_low_to_high(inventory_page):
    inventory_page.sort_by("lohi")

    prices = inventory_page.prices()
    assert prices == sorted(prices)


def test_sort_by_price_high_to_low(inventory_page):
    inventory_page.sort_by("hilo")

    prices = inventory_page.prices()
    assert prices == sorted(prices, reverse=True)


def test_add_and_remove_updates_cart_badge(inventory_page):
    inventory_page.add_to_cart("Sauce Labs Backpack")
    inventory_page.add_to_cart("Sauce Labs Bike Light")
    expect(inventory_page.cart_badge).to_have_text("2")

    inventory_page.remove_from_cart("Sauce Labs Backpack")
    expect(inventory_page.cart_badge).to_have_text("1")

    inventory_page.remove_from_cart("Sauce Labs Bike Light")
    expect(inventory_page.cart_badge).to_be_hidden()
