#!/usr/bin/env python3
"""Capture static previews of the library's local HTML pages and PDF covers.
Run: uv run --with playwright python scripts/generate-library-previews.py
Requires Playwright Chromium and pdftoppm. Originals are never edited.
"""
import asyncio
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import subprocess
import threading
from urllib.parse import unquote
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'assets/previews'
PDFS = {
    'engineering-mechanics.html': 'Engineering_Mechanics_Visual_Cheat_Sheet.pdf',
    '247tailorsteel-design-guide.html': '247TailorSteel_design_guide.pdf',
    'harmonic-drive-sha58a.html': 'Harmonic_Drive_SHA58A_swivel_evaluation.pdf',
}
def slug(href):
    return (href+'index' if href.endswith('/') else href).removesuffix('.html').replace('/', '-')
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

async def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    links = sorted(set(re.findall(r'<a class="page-link"[^>]*href="([^"]+)"', (ROOT/'index.html').read_text())))
    for href, pdf in PDFS.items():
        subprocess.run(['pdftoppm', '-f', '1', '-singlefile', '-scale-to', '640', '-jpeg', '-jpegopt', 'quality=80', str(ROOT/pdf), str(OUTPUT/slug(href))], check=True)
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            semaphore = asyncio.Semaphore(3)
            async def capture(href):
                if href in PDFS:
                    return
                assert (ROOT/unquote(href.split('#')[0])).exists(), href
                async with semaphore:
                    page = await browser.new_page(viewport={'width':1120, 'height':720}, device_scale_factor=.4)
                    async def local_or_static(route):
                        url = route.request.url
                        if url.startswith((origin, 'data:', 'https://cdn.jsdelivr.net/', 'https://cdnjs.cloudflare.com/', 'https://unpkg.com/', 'https://fonts.googleapis.com/', 'https://fonts.gstatic.com/')):
                            await route.continue_()
                        else:
                            await route.abort()
                    await page.route('**/*', local_or_static)
                    await page.goto(origin+'/'+href, wait_until='domcontentloaded', timeout=30000)
                    await page.wait_for_timeout(800)
                    await page.screenshot(path=str(OUTPUT/(slug(href)+'.jpg')), type='jpeg', quality=80, animations='disabled', timeout=15000)
                    await page.close()
                    print('Preview:', href, flush=True)
            await asyncio.gather(*(capture(href) for href in links))
            await browser.close()
    finally:
        server.shutdown()
    print(f'{len(links)} document previews ready.')

if __name__ == '__main__':
    asyncio.run(main())
