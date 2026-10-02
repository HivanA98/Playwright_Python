import pytest
from playwright.sync_api import expect

from pages import CartPage, CheckoutPage

pytestmark = pytest.mark.ui

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket"]


@pytest.mark.smoke
def test_end_to_end_purchase(inventory_page):
    for product in PRODUCTS:
        inventory_page.add_to_cart(product)
    inventory_page.go_to_cart()

    cart = CartPage(inventory_page.page)
    expect(cart.title).to_have_text("Your Cart")
    assert sorted(cart.names()) == sorted(PRODUCTS)
    cart.checkout()

    checkout = CheckoutPage(cart.page)
    checkout.fill_info("Ivan", "Tester", "12345")
    expect(checkout.title).to_have_text("Checkout: Overview")

    # Subtotal must equal the sum of item prices; total = subtotal + tax.
    assert checkout.subtotal_amount() == checkout.item_price_sum()
    assert checkout.total_amount() == round(checkout.subtotal_amount() + checkout.tax_amount(), 2)

    checkout.finish()
    expect(checkout.complete_header).to_have_text("Thank you for your order!")
    expect(checkout.cart_badge).to_be_hidden()


@pytest.mark.parametrize(
    "first, last, postal, message",
    [
        ("", "Tester", "12345", "First Name is required"),
        ("Ivan", "", "12345", "Last Name is required"),
        ("Ivan", "Tester", "", "Postal Code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postal-code"],
)
def test_checkout_info_validation(inventory_page, first, last, postal, message):
    inventory_page.add_to_cart("Sauce Labs Onesie")
    inventory_page.go_to_cart()
    CartPage(inventory_page.page).checkout()

    checkout = CheckoutPage(inventory_page.page)
    checkout.fill_info(first, last, postal)

    expect(checkout.error).to_contain_text(message)
