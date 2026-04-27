# Screenshot API

> URL → Screenshot. No browser required.

Capture high-quality PNG/JPEG screenshots of any URL using Playwright's Chromium engine. Works as a standalone CLI tool or reference client for the hosted API.

![Screenshot API](https://img.shields.io/badge/version-1.0.0-blue) ![Python](https://img.shields.io/badge/python-3.8+-green) ![Playwright](https://img.shields.io/badge/playwright-chromium-yellow)

---

## Quick Start

### 1. Install Dependencies

```bash
pip install playwright
playwright install chromium
```

### 2. Generate an API Key

```bash
python3 screenshot_api.py --generate-key
# ✅ New API key generated: snap_xxxxxxxxxxxx
#   Add this to your code: --api-key snap_xxxxxxxxxxxx
#   Keys stored at: ~/.screenshot_api/keys.json
```

### 3. Capture a Screenshot

```bash
python3 screenshot_api.py --url "https://example.com" --output screenshot.png
# Capturing screenshot of https://example.com ...
# ✅ Screenshot saved to /tmp/screenshot_20260331_143052.png
#    Usage: 1/100 this month (free tier)
```

---

## Examples

```bash
# JPEG output
python3 screenshot_api.py --url "https://example.com" --format jpeg --output shot.jpg

# Full-page capture (Pro required)
python3 screenshot_api.py --url "https://example.com" --full-page --output full.png

# Custom viewport (Pro required)
python3 screenshot_api.py --url "https://example.com" --width 1920 --height 1080 --output 1080p.png

# Wait for element to load before shooting (Pro required)
python3 screenshot_api.py --url "https://example.com" --wait-for "#main-content" --output waited.png

# With API key for usage tracking
python3 screenshot_api.py --url "https://example.com" --output shot.png --api-key snap_xxxxxxxxxxxx
```

---

## API Key Management

```bash
# List all keys and monthly usage
python3 screenshot_api.py --list-keys

# Associate email with a key
python3 screenshot_api.py --api-key snap_xxxxxxxxxxxx --set-email "you@example.com"
```

---

## Tiers

| Feature | Free | Pro ($19/mo) |
|---------|------|-------------|
| Screenshots/mo | 100 | 2000 |
| PNG output | ✅ | ✅ |
| JPEG output | ✅ | ✅ |
| Fixed dimensions | ✅ (1280×720, 1920×1080) | ✅ (any) |
| Full-page capture | ❌ | ✅ |
| wait_for selector | ❌ | ✅ |

**Upgrade:** https://buy.stripe.com/cNi00lgKv6d76w46sw7wA0t

---

## Output

A screenshot file saved to the path you specified:

```
/tmp/screenshot_20260331_143052.png  (or .jpg for JPEG)
```

File size depends on page complexity — a typical landing page is ~200–800 KB as PNG.

---

## Requirements

- Python 3.8+
- `playwright` pip package
- `chromium` browser (installed via `playwright install chromium`)

---

## File Structure

```
screenshot-api/
├── SKILL.md              # Full skill documentation
├── README.md             # This file
├── screenshot_api.py     # CLI tool + reference client
└── edgeiq_licensing.py   # License tier checking (shared module)
```

---

## License

This tool is provided as-is. API access subject to Stripe terms.
