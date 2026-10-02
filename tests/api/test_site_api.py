"""HTTP-level tests for Saucedemo, using Playwright's APIRequestContext (no browser).

Saucedemo is a static SPA hosted on GitHub Pages - it has no public REST API,
so these tests verify the HTTP contract of what the server actually serves:
status codes, headers, the HTML shell, the web manifest and static assets.
"""
import re
import time

import pytest

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_homepage_returns_html(api_context):
    response = api_context.get("/")

    assert response.status == 200
    assert response.headers["content-type"].startswith("text/html")
    body = response.text()
    assert "<title>Swag Labs</title>" in body
    assert '<div id="root"></div>' in body


def test_homepage_responds_quickly(api_context):
    start = time.perf_counter()
    response = api_context.get("/")
    elapsed = time.perf_counter() - start

    assert response.ok
    assert elapsed < 3, f"Homepage took {elapsed:.2f}s"


def test_manifest_is_valid_json(api_context):
    response = api_context.get("/manifest.json")

    assert response.status == 200
    manifest = response.json()
    assert manifest["name"] == "Swag Labs"
    assert manifest["start_url"]
    assert {icon["sizes"] for icon in manifest["icons"]} >= {"192x192", "512x512"}


def test_manifest_icons_are_served(api_context):
    for icon in api_context.get("/manifest.json").json()["icons"]:
        response = api_context.get(icon["src"])
        assert response.status == 200, icon["src"]
        assert response.headers["content-type"] == icon["type"]


def test_bundled_assets_referenced_by_html_are_served(api_context):
    html = api_context.get("/").text()
    assets = re.findall(r'(?:src|href)="(/assets/[^"]+\.(?:js|css))"', html)
    assert assets, "No /assets/*.js|css referenced in index.html"

    expected_type = {"js": "javascript", "css": "text/css"}
    for asset in assets:
        response = api_context.get(asset)
        assert response.status == 200, asset
        assert expected_type[asset.rsplit(".", 1)[1]] in response.headers["content-type"]


def test_unknown_path_returns_404(api_context):
    response = api_context.get("/this-page-does-not-exist")

    assert response.status == 404


def test_head_request_has_caching_headers(api_context):
    response = api_context.head("/")

    assert response.status == 200
    assert "etag" in response.headers
    assert "max-age" in response.headers.get("cache-control", "")
