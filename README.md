# Saucedemo Test Automation — Playwright + pytest

Test otomatis untuk [saucedemo.com](https://www.saucedemo.com) menggunakan **Playwright (Python)** dan **pytest**, mencakup UI test dan API/HTTP test, dijalankan di **GitHub Actions**.

## Struktur

```
.
├── .github/workflows/tests.yml   # CI: job API + UI matrix (chromium/firefox/webkit)
├── conftest.py                   # Fixtures: base_url, login via cookie, api_context
├── pages/                        # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── api/test_site_api.py      # HTTP tests via APIRequestContext (tanpa browser)
│   └── ui/
│       ├── test_login.py         # login sukses/gagal, locked user, logout, akses tanpa login
│       ├── test_inventory.py     # jumlah produk, sorting, badge keranjang
│       ├── test_checkout.py      # E2E purchase + validasi form checkout
│       └── test_network.py       # monitor & mock network dari UI
├── pytest.ini
└── requirements.txt
```

## Catatan tentang API test

Saucedemo adalah SPA statis di GitHub Pages — **tidak punya REST API publik**. Jadi API test di sini menguji kontrak HTTP yang benar-benar disajikan server: status code, header (content-type, ETag, cache-control), HTML shell, `manifest.json`, aset JS/CSS, ikon, 404, dan waktu respons. Selain itu `test_network.py` menggabungkan UI + network (memantau request gagal dan memblokir gambar via `page.route`).

## Menjalankan secara lokal

```bash
python -m venv .venv
```

Aktifkan venv (`.venv\Scripts\activate` di Windows, `source .venv/bin/activate` di Linux/macOS), lalu:

```bash
pip install -r requirements.txt
```

```bash
python -m playwright install chromium
```

```bash
pytest
```

Contoh lain:

```bash
pytest -m api
```

```bash
pytest -m smoke --headed --slowmo 300
```

```bash
pytest -m ui --browser firefox -n auto --html=reports/report.html --self-contained-html
```

Jika test gagal, screenshot, video, dan trace tersimpan di `test-results/`. Buka trace dengan `playwright show-trace <file.zip>`.

## Konfigurasi (env var)

| Variabel         | Default                      |
|------------------|------------------------------|
| `BASE_URL`       | `https://www.saucedemo.com`  |
| `SAUCE_PASSWORD` | `secret_sauce`               |

## CI (GitHub Actions)

Workflow `.github/workflows/tests.yml` berjalan saat push ke `main`, pull request, manual (`workflow_dispatch`, bisa pilih marker misalnya `smoke`), dan terjadwal setiap hari.

- **api** — menjalankan `pytest -m api` tanpa install browser.
- **ui** — matrix chromium/firefox/webkit, paralel (`-n auto`) dengan 1x rerun untuk test flaky.
- Report HTML + JUnit XML di-upload sebagai artifact; screenshot/video/trace di-upload jika gagal.
