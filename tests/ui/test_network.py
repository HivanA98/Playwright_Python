"""UI tests that observe or mock network traffic (hybrid UI + API)."""
import re

import pytest
from playwright.sync_api import expect

from data import Products
from pages import InventoryPage

pytestmark = pytest.mark.ui


def test_inventory_page_has_no_failed_requests(logged_in_page, base_url):
    failed = []

    def track(response):
        if response.url.startswith(base_url) and response.status >= 400:
            failed.append(f"{response.status} {response.url}")

    logged_in_page.on("response", track)
    inventory = InventoryPage(logged_in_page).open()
    expect(inventory.cards).to_have_count(6)

    # Deep links like /inventory.html are served through GitHub Pages' 404 SPA
    # fallback, so that one 404 is expected.
    failed = [f for f in failed if not f.endswith(InventoryPage.path)]
    assert not failed, f"Failed requests: {failed}"


def test_product_images_load(inventory_page: InventoryPage):
    expect(inventory_page.images).to_have_count(6)

    for img in inventory_page.images.all():
        img.scroll_into_view_if_needed()
        expect(img).to_have_js_property("complete", True)
        assert img.evaluate("el => el.naturalWidth > 0"), img.get_attribute("src")


def test_page_still_usable_when_images_blocked(logged_in_page):
    logged_in_page.route(re.compile(r"\.(png|jpe?g|svg|webp)$"), lambda route: route.abort())

    inventory = InventoryPage(logged_in_page).open()
    inventory.add_to_cart(Products.BACKPACK)

    expect(inventory.cards).to_have_count(6)
    inventory.header.should_have_cart_count(1)
