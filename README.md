# 📸 EdgeIQ Screenshot API

**URL-to-screenshot API powered by Playwright — accurate, full-featured captures.**

Give it a URL, get back a PNG or JPEG screenshot. Built on Playwright's Chromium rendering engine for accurate, JavaScript-aware captures.

[![Project Stage](https://img.shields.io/badge/Stage-Beta-blue)](https://edgeiqlabs.com)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-orange)](LICENSE)

---

## What It Does

Captures screenshots of any URL using Playwright's Chromium engine. Supports custom viewport dimensions, full-page captures, JavaScript wait selectors, and multiple output formats.

---

## Key Features

- **Playwright/Chromium rendering** — accurate, JS-aware captures
- **Custom dimensions** — any width/height combination
- **Full-page capture** — scroll and capture entire page (Pro)
- **wait_for selector** — wait for DOM element before capturing (Pro)
- **PNG/JPEG output** — flexible format options
- **Batch capture** — screenshot multiple URLs from a list

---

## Prerequisites

- Python 3.8+
- `playwright`, `pillow`
- Chromium browser installed (`playwright install chromium`)

---

## Installation

```bash
git clone https://github.com/snipercat69/edgeiq-screenshot-api.git
cd edgeiq-screenshot-api
pip install -r requirements.txt
playwright install chromium
```

---

## Quick Start

```bash
# Capture a screenshot
python3 screenshot_api.py --url "https://example.com" --output screenshot.png

# Custom dimensions
python3 screenshot_api.py --url "https://example.com" --width 1920 --height 1080 --output screenshot.png

# Full page
python3 screenshot_api.py --url "https://example.com" --full-page --output full.png

# Batch from URL list
python3 screenshot_api.py --input urls.txt --output-dir ./screenshots
```

---

## API Reference (Production Server)

```bash
POST /v1/screenshot
Authorization: Bearer <api_key>
Content-Type: application/json

{
  "url": "https://example.com",
  "width": 1280,
  "height": 720,
  "format": "png",
  "full_page": false,
  "wait_for": null
}
```

---

## Pricing

| Tier | Price | Features |
|------|-------|----------|
| **Free** | $0 | 100 screenshots/month, fixed dimensions |
| **Pro** | $19/mo | 2000 screenshots/month, any dimensions, full-page, wait_for |

---

## Integration with EdgeIQ Tools

- **[EdgeIQ Phishing Kit Detector](https://github.com/snipercat69/edgeiq-phishing-kit-detector)** — capture suspicious pages for analysis
- **[EdgeIQ Client Dashboard](https://github.com/snipercat69/edgeiq-client-dashboard)** — generate visual reports for clients

---

## Support

Open an issue at: https://github.com/snipercat69/edgeiq-screenshot-api/issues

---

*Part of EdgeIQ Labs — [edgeiqlabs.com](https://edgeiqlabs.com)*
