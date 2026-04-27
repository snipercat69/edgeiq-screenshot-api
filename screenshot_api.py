#!/usr/bin/env python3
"""
Screenshot API — CLI Reference Client & Standalone Tool
========================================================
A developer tool that takes a URL and returns a screenshot (PNG/JPEG).

This is the CLI / reference implementation. A production API server
(Flask/FastAPI) would run separately and expose REST endpoints.

Usage:
  python3 screenshot_api.py --url "https://example.com" --output screenshot.png
  python3 screenshot_api.py --url "https://example.com" --format jpeg --output screenshot.jpg
  python3 screenshot_api.py --url "https://example.com" --full-page --output full.png
  python3 screenshot_api.py --url "https://example.com" --wait-for "#main" --output waited.png

API Keys:
  Stored in ~/.screenshot_api/keys.json
  Generate a key: python3 screenshot_api.py --generate-key

Tiers:
  Free  — 100 screenshots/month, basic dimensions only
  Pro   — 2000 screenshots/month, full-page, custom dimensions, wait_for
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: playwright not installed.")
    print("  Install: pip install playwright && playwright install chromium")
    sys.exit(1)

from edgeiq_licensing import is_pro

# ─── Config ────────────────────────────────────────────────────────────────────

KEYS_DIR   = Path.home() / ".screenshot_api"
KEYS_FILE  = KEYS_DIR / "keys.json"
KEYS_FILE.mkdir(parents=True, exist_ok=True)

DEFAULT_WIDTH   = 1280
DEFAULT_HEIGHT  = 720
DEFAULT_FORMAT  = "png"
FREE_LIMIT      = 100       # screenshots/month
PRO_LIMIT       = 2000      # screenshots/month

# Dimensions only allowed for Pro users
ALLOWED_DIMENSIONS = {
    (1280, 720),
    (1920, 1080),
    (375, 812),   # mobile
    (414, 896),   # mobile
}

# ─── Key Management ─────────────────────────────────────────────────────────────

def load_keys() -> dict:
    if KEYS_FILE.exists():
        return json.loads(KEYS_FILE.read_text())
    return {}


def save_keys(keys: dict):
    KEYS_FILE.write_text(json.dumps(keys, indent=2))


def generate_api_key() -> str:
    """Generate a new API key and return it."""
    key = f"snap_{uuid.uuid4().hex[:24]}"
    keys = load_keys()
    keys[key] = {
        "created": datetime.utcnow().isoformat(),
        "usage": 0,
        "tier": "free",
        "email": None,
    }
    save_keys(keys)
    return key


def get_key_info(key: str) -> dict | None:
    keys = load_keys()
    return keys.get(key)


def increment_usage(key: str):
    keys = load_keys()
    if key in keys:
        keys[key]["usage"] = keys[key].get("usage", 0) + 1
        save_keys(keys)


def get_month_usage(key: str) -> int:
    info = get_key_info(key)
    if not info:
        return 0
    # Simple monthly reset based on creation month
    created = datetime.fromisoformat(info["created"])
    now = datetime.utcnow()
    if created.year == now.year and created.month == now.month:
        return info.get("usage", 0)
    return 0


def check_rate_limit(key: str) -> tuple[bool, str]:
    """Returns (allowed, message)."""
    info = get_key_info(key)
    if not info:
        return False, "Invalid API key."

    pro = is_pro()
    limit = PRO_LIMIT if pro else FREE_LIMIT
    usage = get_month_usage(key)

    if usage >= limit:
        tier = "Pro" if pro else "Free"
        return False, f"Monthly limit reached ({tier}: {limit}/month). Upgrade at https://buy.stripe.com/6oUeVf8dZ9pj8EccQU7wA0q"

    return True, f"OK ({usage + 1}/{limit} used this month)"


def validate_dimensions(width: int, height: int, pro: bool) -> bool:
    """Check if dimensions are allowed for the user's tier."""
    if pro:
        return True  # Pro can use any dimension
    return (width, height) in ALLOWED_DIMENSIONS


# ─── Screenshot Capture ────────────────────────────────────────────────────────

def capture_screenshot(
    url: str,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    format: str = DEFAULT_FORMAT,
    full_page: bool = False,
    wait_for: str | None = None,
    output: str | None = None,
    api_key: str | None = None,
) -> dict:
    """
    Capture a screenshot using Playwright.

    Returns:
        dict with keys: success (bool), path (str), message (str)
    """

    # Check API key
    if api_key:
        allowed, msg = check_rate_limit(api_key)
        if not allowed:
            return {"success": False, "path": None, "message": msg}
        pro = is_pro()
    else:
        pro = is_pro()

    # Validate dimensions
    if not validate_dimensions(width, height, pro):
        return {
            "success": False,
            "path": None,
            "message": (
                f"Custom dimensions ({width}x{height}) require Pro. "
                f"Free tier: {list(ALLOWED_DIMENSIONS)[0]} or {list(ALLOWED_DIMENSIONS)[1]}. "
                f"Upgrade: https://buy.stripe.com/6oUeVf8dZ9pj8EccQU7wA0q"
            ),
        }

    # Validate full_page for free tier
    if full_page and not pro:
        return {
            "success": False,
            "path": None,
            "message": "full_page requires Pro. Upgrade: https://buy.stripe.com/6oUeVf8dZ9pj8EccQU7wA0q",
        }

    # Validate wait_for for free tier
    if wait_for and not pro:
        return {
            "success": False,
            "path": None,
            "message": "wait_for requires Pro. Upgrade: https://buy.stripe.com/6oUeVf8dZ9pj8EccQU7wA0q",
        }

    # Determine output path
    if not output:
        ext = "jpg" if format == "jpeg" else "png"
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output = f"/tmp/screenshot_{timestamp}.{ext}"

    output_path = Path(output)
    mime_type = "image/jpeg" if format == "jpeg" else "image/png"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": width, "height": height},
                ignore_https_errors=True,
            )
            page = context.new_page()

            # Optional: wait for JS selector
            if wait_for:
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_selector(wait_for, timeout=15000)
            else:
                page.goto(url, wait_until="load", timeout=30000)

            page.screenshot(
                path=str(output_path),
                full_page=full_page,
                type=format,
            )
            browser.close()

        if api_key:
            increment_usage(api_key)

        return {
            "success": True,
            "path": str(output_path),
            "message": f"Screenshot saved to {output_path}",
        }

    except Exception as e:
        return {
            "success": False,
            "path": None,
            "message": f"Screenshot failed: {e}",
        }


# ─── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Screenshot API — Capture screenshots of any URL.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 screenshot_api.py --url "https://example.com" --output screenshot.png
  python3 screenshot_api.py --url "https://example.com" --format jpeg --output screenshot.jpg
  python3 screenshot_api.py --url "https://example.com" --full-page --output full.png
  python3 screenshot_api.py --url "https://example.com" --wait-for "#main" --output waited.png
  python3 screenshot_api.py --url "https://example.com" --width 1920 --height 1080 --output 1080p.png
  python3 screenshot_api.py --generate-key
  python3 screenshot_api.py --list-keys
        """,
    )

    parser.add_argument("--url",          help="URL to screenshot")
    parser.add_argument("--width",        type=int, default=DEFAULT_WIDTH,  help=f"Viewport width (default: {DEFAULT_WIDTH})")
    parser.add_argument("--height",       type=int, default=DEFAULT_HEIGHT, help=f"Viewport height (default: {DEFAULT_HEIGHT})")
    parser.add_argument("--format",       choices=["png", "jpeg"], default=DEFAULT_FORMAT, help=f"Output format (default: {DEFAULT_FORMAT})")
    parser.add_argument("--full-page",    action="store_true",          help="Capture full scrollable page (Pro only)")
    parser.add_argument("--wait-for",     metavar="SELECTOR",           help="Wait for a JS selector before screenshot (Pro only)")
    parser.add_argument("--output",       help="Output file path")
    parser.add_argument("--api-key",     help="API key for usage tracking")

    # Key management
    parser.add_argument("--generate-key", action="store_true", help="Generate a new API key")
    parser.add_argument("--list-keys",    action="store_true", help="List all API keys and usage")
    parser.add_argument("--set-email",    metavar="EMAIL",     help="Associate an email with an API key (use with --api-key)")

    args = parser.parse_args()

    # ── Key management commands ──────────────────────────────────────────────
    if args.generate_key:
        key = generate_api_key()
        print(f"✅ New API key generated: {key}")
        print(f"   Add this to your code: --api-key {key}")
        print(f"   Keys stored at: {KEYS_FILE}")
        return

    if args.list_keys:
        keys = load_keys()
        if not keys:
            print("No API keys found. Generate one with --generate-key")
            return
        print(f"API Keys (stored at {KEYS_FILE}):\n")
        for key, info in keys.items():
            usage = get_month_usage(key)
            print(f"  Key:   {key}")
            print(f"  Tier:  {info.get('tier', 'free')}")
            print(f"  Email: {info.get('email', 'N/A')}")
            print(f"  Usage: {usage}/month")
            print(f"  Created: {info.get('created', 'unknown')}")
            print()
        return

    if args.set_email:
        if not args.api_key:
            print("ERROR: --set-email requires --api-key")
            sys.exit(1)
        keys = load_keys()
        if args.api_key not in keys:
            print(f"ERROR: API key '{args.api_key}' not found.")
            sys.exit(1)
        keys[args.api_key]["email"] = args.set_email
        save_keys(keys)
        print(f"✅ Email '{args.set_email}' associated with key {args.api_key[:12]}...")
        return

    # ── Screenshot command ──────────────────────────────────────────────────
    if not args.url:
        parser.print_help()
        print("\n❌ Error: --url is required (or use --generate-key / --list-keys)")
        sys.exit(1)

    # Auto-detect API key from env
    api_key = args.api_key or os.environ.get("SCREENSHOT_API_KEY")

    print(f"Capturing screenshot of {args.url} ...")
    result = capture_screenshot(
        url=args.url,
        width=args.width,
        height=args.height,
        format=args.format,
        full_page=args.full_page,
        wait_for=args.wait_for,
        output=args.output,
        api_key=api_key,
    )

    if result["success"]:
        print(f"✅ {result['message']}")
        if api_key:
            info = get_key_info(api_key)
            if info:
                usage = get_month_usage(api_key)
                pro = is_pro()
                limit = PRO_LIMIT if pro else FREE_LIMIT
                print(f"   Usage: {usage}/{limit} this month ({info.get('tier', 'free')} tier)")
    else:
        print(f"❌ {result['message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
