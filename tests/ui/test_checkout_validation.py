import pytest
from playwright.sync_api import expect

from data import Customer, Products
from pages import InventoryPage

pytestmark = pytest.mark.ui


@pytest.mark.parametrize(
    "customer, message",
    [
        (Customer("", "Tester", "12345"), "First Name is required"),
        (Customer("Ivan", "", "12345"), "Last Name is required"),
        (Customer("Ivan", "Tester", ""), "Postal Code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postal-code"],
)
def test_checkout_info_validation(inventory_page: InventoryPage, customer, message):
    info = inventory_page.add_to_cart(Products.ONESIE).open_cart().checkout()

    info.fill(customer).continue_expecting_error()

    expect(info.error).to_contain_text(message)
