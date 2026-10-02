import os

import pytest
from playwright.sync_api import Playwright, expect

from data import Users
from pages import InventoryPage, LoginPage

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")

# performance_glitch_user takes ~5s to log in; leave headroom for slow CI runners.
expect.set_options(timeout=15_000)


@pytest.fixture(scope="session")
def base_url():
    """Overrides pytest-base-url so the BASE_URL env var wins over pytest.ini."""
    return BASE_URL


@pytest.fixture(scope="session", autouse=True)
def _data_test_attribute(playwright: Playwright):
    # Saucedemo uses `data-test`, not Playwright's default `data-testid`.
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def logged_in_page(page, context, base_url):
    """Skip the login form: Saucedemo keeps the session in a plain cookie."""
    context.add_cookies([{
        "name": "session-username",
        "value": Users.STANDARD.username,
        "url": base_url,
    }])
    return page


@pytest.fixture
def inventory_page(logged_in_page) -> InventoryPage:
    return InventoryPage(logged_in_page).open()


@pytest.fixture
def api_context(playwright: Playwright, base_url):
    ctx = playwright.request.new_context(base_url=base_url)
    yield ctx
    ctx.dispose()
