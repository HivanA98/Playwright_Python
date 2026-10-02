import re

from playwright.sync_api import Page, expect

from .components import HeaderComponent


class BasePage:
    """Root of every page object.

    Conventions used by all pages:
    - Locators are attributes created in __init__ (lazy; nothing is queried yet).
    - Actions that navigate return the *next* page object, already verified
      with `should_be_loaded()`, so tests read as a fluent user journey.
    - Assertions stay in tests; page objects only expose `should_be_loaded`
      (and small `should_*` helpers) that guard navigation.
    """

    path = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(self.path)
        return self.should_be_loaded()

    def should_be_loaded(self):
        expect(self.page).to_have_url(re.compile(re.escape(self.path)))
        return self


class AppPage(BasePage):
    """A page behind login: has the header (menu + cart) and usually a title."""

    title_text: str | None = None

    def __init__(self, page: Page):
        super().__init__(page)
        self.header = HeaderComponent(page)
        self.title = page.get_by_test_id("title")

    def should_be_loaded(self):
        super().should_be_loaded()
        if self.title_text:
            expect(self.title).to_have_text(self.title_text)
        return self

    def open_cart(self):
        return self.header.open_cart()
