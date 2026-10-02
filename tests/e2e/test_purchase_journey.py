"""End-to-end purchase journeys, written entirely against the Page Object Model.

Each navigation method returns the next page object, so a test reads like the
user's path through the shop: login -> browse -> cart -> checkout -> complete.
"""
from decimal import Decimal

import pytest
from playwright.sync_api import expect

from data import CUSTOMER, PAYMENT_INFO, SHIPPING_INFO, OrderSummary, Products, Users
from pages import InventoryPage, LoginPage, SortOption

pytestmark = pytest.mark.e2e


@pytest.mark.smoke
def test_complete_shopping_journey(login_page: LoginPage):
    # 1. Login and browse the catalog cheapest-first.
    inventory = login_page.login(Users.STANDARD)
    prices = [p.price for p in inventory.sort_by(SortOption.PRICE_LOW_TO_HIGH).products()]
    assert prices == sorted(prices)

    # 2. Add the most expensive item from its detail page.
    detail = inventory.open_product(Products.FLEECE_JACKET)
    assert detail.product() == Products.FLEECE_JACKET
    detail.add_to_cart()
    expect(detail.card.remove_button).to_be_visible()
    detail.header.should_have_cart_count(1)

    # 3. Back on the list, the item shows as added; add two more.
    inventory = detail.back_to_products()
    expect(inventory.product(Products.FLEECE_JACKET.name).remove_button).to_be_visible()
    inventory.add_to_cart(Products.BACKPACK, Products.BIKE_LIGHT)
    inventory.header.should_have_cart_count(3)

    # 4. Review the cart, drop one item, keep shopping, add another.
    cart = inventory.open_cart()
    assert set(cart.products()) == {Products.FLEECE_JACKET, Products.BACKPACK, Products.BIKE_LIGHT}
    for item in cart.items():
        expect(item.quantity).to_have_text("1")
    cart.remove(Products.BIKE_LIGHT).header.should_have_cart_count(2)
    cart.continue_shopping().add_to_cart(Products.ONESIE)
    expected_items = {Products.FLEECE_JACKET, Products.BACKPACK, Products.ONESIE}

    # 5. Checkout: an empty form is rejected, then valid details go through.
    info = inventory.open_cart().checkout()
    info.continue_expecting_error()
    expect(info.error).to_contain_text("First Name is required")
    overview = info.fill(CUSTOMER).continue_to_overview()

    # 6. The overview lists exactly the cart contents with correct totals.
    assert set(overview.products()) == expected_items
    assert overview.summary() == OrderSummary.expected_for(expected_items)
    expect(overview.payment_info).to_have_text(PAYMENT_INFO)
    expect(overview.shipping_info).to_have_text(SHIPPING_INFO)

    # 7. Place the order; the cart is emptied.
    complete = overview.finish()
    expect(complete.complete_header).to_have_text("Thank you for your order!")
    complete.header.should_have_cart_count(0)

    # 8. Back home every product is purchasable again; logout ends the session.
    inventory = complete.back_home()
    expect(inventory.cards.get_by_role("button", name="Remove")).to_have_count(0)
    login = inventory.header.logout()
    login.page.goto(InventoryPage.path)
    expect(login.error).to_contain_text("when you are logged in")


BASKETS = {
    "single-cheapest": [Products.ONESIE],
    "same-price-pair": [Products.BOLT_TSHIRT, Products.RED_TSHIRT],
    "entire-catalog": Products.ALL,
}


@pytest.mark.parametrize("basket", BASKETS.values(), ids=BASKETS.keys())
@pytest.mark.parametrize(
    "user", [Users.STANDARD, Users.PERFORMANCE_GLITCH], ids=lambda u: u.username
)
def test_checkout_totals_per_user_and_basket(login_page: LoginPage, user, basket):
    overview = (
        login_page.login(user)
        .add_to_cart(*basket)
        .open_cart()
        .checkout()
        .fill(CUSTOMER)
        .continue_to_overview()
    )

    assert sorted(overview.products(), key=lambda p: p.name) == sorted(basket, key=lambda p: p.name)
    assert overview.summary() == OrderSummary.expected_for(basket)

    complete = overview.finish()
    expect(complete.complete_header).to_have_text("Thank you for your order!")


def test_entire_catalog_total_matches_known_value(inventory_page: InventoryPage):
    """Pins the tax formula to real numbers, independent of OrderSummary.expected_for."""
    overview = inventory_page.add_to_cart(*Products.ALL).open_cart().checkout().fill(CUSTOMER).continue_to_overview()

    assert overview.summary() == OrderSummary(Decimal("129.94"), Decimal("10.40"), Decimal("140.34"))


def test_cancel_on_info_step_returns_to_cart_with_items(inventory_page: InventoryPage):
    cart = inventory_page.add_to_cart(Products.BACKPACK, Products.ONESIE).open_cart()

    cart = cart.checkout().cancel()

    assert set(cart.products()) == {Products.BACKPACK, Products.ONESIE}


def test_cancel_on_overview_keeps_cart(inventory_page: InventoryPage):
    overview = inventory_page.add_to_cart(Products.BACKPACK).open_cart().checkout().fill(CUSTOMER).continue_to_overview()

    inventory = overview.cancel()

    inventory.header.should_have_cart_count(1)
    assert inventory.open_cart().products() == [Products.BACKPACK]


def test_cart_persists_across_reload_and_pages(inventory_page: InventoryPage):
    inventory_page.add_to_cart(Products.BACKPACK, Products.BOLT_TSHIRT)

    inventory_page.page.reload()
    inventory = InventoryPage(inventory_page.page).should_be_loaded()
    inventory.header.should_have_cart_count(2)

    detail = inventory.open_product(Products.BACKPACK)
    expect(detail.card.remove_button).to_be_visible()

    cart = detail.open_cart()
    assert set(cart.products()) == {Products.BACKPACK, Products.BOLT_TSHIRT}


def test_reset_app_state_empties_cart(inventory_page: InventoryPage):
    inventory_page.add_to_cart(Products.BACKPACK, Products.BIKE_LIGHT, Products.ONESIE)
    inventory_page.header.should_have_cart_count(3)

    inventory_page.header.reset_app_state()

    inventory_page.header.should_have_cart_count(0)
    assert inventory_page.open_cart().products() == []
