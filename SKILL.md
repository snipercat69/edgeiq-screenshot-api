# Screenshot API — SKILL.md

## What It Is

**Screenshot API** is a developer-focused URL-to-screenshot service. Give it a URL, get back a PNG or JPEG screenshot. Think of it as the programmatic version of pressing ⌘S on a webpage — but from a server, with no browser required.

Built on Playwright's Chromium rendering engine for accurate, full-featured captures.

---

## The Product

**Screenshot API Pro** — paid micro-SaaS accessible via API key.

| | Free | Pro |
|---|---|---|
| **Price** | $0 | $19/mo |
| **Screenshots** | 100/month | 2000/month |
| **Formats** | PNG, JPEG | PNG, JPEG |
| **Dimensions** | Fixed (1280×720, 1920×1080) | Any custom size |
| **Full-page capture** | ❌ | ✅ |
| **wait_for JS selector** | ❌ | ✅ |

**Stripe:** https://buy.stripe.com/cNi00lgKv6d76w46sw7wA0t

---

## API Reference

> The CLI tool (`screenshot_api.py`) is a **reference implementation / standalone client**. A production API server (Flask/FastAPI) would run separately at a hosted endpoint.

### REST Endpoint (production server)

```
POST /v1/screenshot
Authorization: Bearer <api_key>
Content-Type: application/json
```

**Request body:**

```json
{
  "url": "https://example.com",
  "width": 1280,
  "height": 720,
  "format": "png",
  "full_page": false,
  "wait_for": null
}
```

**Response:** Binary image data (Content-Type: image/png or image/jpeg), or JSON error.

### CLI Tool

```bash
# Basic screenshot
python3 screenshot_api.py --url "https://example.com" --output screenshot.png

# JPEG format
python3 screenshot_api.py --url "https://example.com" --format jpeg --output screenshot.jpg

# Full-page capture (Pro)
python3 screenshot_api.py --url "https://example.com" --full-page --output full.png

# Custom dimensions (Pro)
python3 screenshot_api.py --url "https://example.com" --width 1920 --height 1080 --output 1080p.png

# Wait for JS selector before shot (Pro)
python3 screenshot_api.py --url "https://example.com" --wait-for "#app-loaded" --output waited.png

# With API key
python3 screenshot_api.py --url "https://example.com" --output shot.png --api-key snap_xxxxxxxxxxxx
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | *(required)* | URL to screenshot |
| `width` | int | 1280 | Viewport width in pixels |
| `height` | int | 720 | Viewport height in pixels |
| `format` | string | `png` | `png` or `jpeg` |
| `full_page` | bool | `false` | Capture entire scrollable page (Pro only) |
| `wait_for` | string | `null` | CSS/JS selector to wait for before shooting (Pro only) |

### API Key Management

```bash
# Generate a new key
python3 screenshot_api.py --generate-key

# List all keys + usage
python3 screenshot_api.py --list-keys

# Associate email with a key
python3 screenshot_api.py --api-key snap_xxxxxxxxxxxx --set-email "user@example.com"
```

Keys are stored at `~/.screenshot_api/keys.json`.

---

## Architecture Notes

- **Rendering engine:** Playwright Chromium (headless)
- **CLI client:** Python script, no server required for local use
- **Production server:** Flask/FastAPI app (separate deployment)
- **Auth:** Bearer token API keys checked against `~/.screenshot_api/keys.json`
- **Rate limiting:** Monthly counter per API key, resets each calendar month

---

## Use Cases

- Generate OG images for dynamic content
- Capture receipts/invoices automatically
- Monitor uptime with visual proof
- Build previews for link-sharing tools
- Automate visual regression testing


---

## 🔗 More from EdgeIQ Labs

**edgeiqlabs.com** — Security tools, OSINT utilities, and micro-SaaS products for developers and security professionals.

- 🛠️ **Subdomain Hunter** — Passive subdomain enumeration via Certificate Transparency
- 📸 **Screenshot API** — URL-to-screenshot API for developers
- 🔔 **uptime.check** — URL uptime monitoring with alerts
- 🛡️ **headers.check** — HTTP security headers analyzer

👉 [Visit edgeiqlabs.com →](https://edgeiqlabs.com)
