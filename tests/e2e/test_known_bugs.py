"""Saucedemo ships special users with deliberate bugs.

Each test asserts the *correct* behavior and is marked `xfail(strict=True)`:
- today the bug makes it fail  -> reported as XFAIL (suite stays green)
- if the bug is ever fixed     -> XPASS, which strict mode turns into a FAILURE,
  telling you to drop the marker and promote the test to a normal regression test.
"""
import pytest
from playwright.sync_api import expect

from data import CUSTOMER, Products, Users
from pages import LoginPage, SortOption

pytestmark = [pytest.mark.e2e, pytest.mark.known_bug]


def known_bug(reason: str):
    return pytest.mark.xfail(reason=reason, strict=True)


@known_bug("problem_user: sorting Z-A leaves the list unsorted")
def test_problem_user_can_sort_by_name(login_page: LoginPage):
    inventory = login_page.login(Users.PROBLEM).sort_by(SortOption.NAME_Z_TO_A)

    names = [p.name for p in inventory.products()]
    assert names == sorted(names, reverse=True)


@known_bug("problem_user: every product shows the same placeholder image")
def test_problem_user_sees_distinct_product_images(login_page: LoginPage):
    inventory = login_page.login(Users.PROBLEM)

    assert len(set(inventory.image_sources())) == len(Products.ALL)


@known_bug("problem_user: typing in Last Name overwrites First Name")
def test_problem_user_can_fill_checkout_form(login_page: LoginPage):
    info = login_page.login(Users.PROBLEM).add_to_cart(Products.BACKPACK).open_cart().checkout()

    info.fill(CUSTOMER)

    expect(info.first_name).to_have_value(CUSTOMER.first_name, timeout=2_000)
    expect(info.last_name).to_have_value(CUSTOMER.last_name, timeout=2_000)


@known_bug("some 'Add to cart' buttons do nothing for this user")
@pytest.mark.parametrize("user", [Users.PROBLEM, Users.ERROR], ids=lambda u: u.username)
def test_user_can_add_entire_catalog(login_page: LoginPage, user):
    inventory = login_page.login(user).add_to_cart(*Products.ALL)

    inventory.header.should_have_cart_count(len(Products.ALL), timeout=3_000)


@known_bug("error_user: clicking Finish does not complete the order")
def test_error_user_can_finish_checkout(login_page: LoginPage):
    overview = (
        login_page.login(Users.ERROR)
        .add_to_cart(Products.BACKPACK)
        .open_cart()
        .checkout()
        .fill(CUSTOMER)
        .continue_to_overview()
    )

    overview.finish_button.click()

    expect(overview.page).to_have_url("/checkout-complete.html", timeout=3_000)


@known_bug("visual_user: inventory shows prices that differ from the catalog")
def test_visual_user_sees_catalog_prices(login_page: LoginPage):
    inventory = login_page.login(Users.VISUAL)

    by_name = lambda products: sorted(products, key=lambda p: p.name)  # noqa: E731
    assert by_name(inventory.products()) == by_name(Products.ALL)
