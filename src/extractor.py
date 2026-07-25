import asyncio
import aiohttp
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

async def fetch_simple(session, url):
    """Fast fetch using aiohttp - works for most static sites."""
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=15)) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                # Remove scripts, styles, nav, footer clutter
                for tag in soup(['script', 'style', 'nav', 'footer', 'svg', 'img']):
                    tag.decompose()
                text = soup.get_text(separator=' ', strip=True)
                # Trim to 8000 chars to save tokens
                return text[:8000], "simple"
            else:
                logger.warning(f"HTTP {response.status} for {url}")
                return None, "failed"
    except Exception as e:
        logger.warning(f"Simple fetch failed for {url}: {e}")
        return None, "failed"

async def fetch_playwright(url):
    """Headless browser fetch for JavaScript-heavy sites."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.set_extra_http_headers(HEADERS)
            await page.goto(url, wait_until='networkidle', timeout=30000)
            # Wait a moment for dynamic content
            await page.wait_for_timeout(2000)
            content = await page.content()
            await browser.close()
            soup = BeautifulSoup(content, 'lxml')
            for tag in soup(['script', 'style', 'nav', 'footer', 'svg', 'img']):
                tag.decompose()
            text = soup.get_text(separator=' ', strip=True)
            return text[:8000], "playwright"
    except Exception as e:
        logger.warning(f"Playwright fetch failed for {url}: {e}")
        return None, "failed"

async def fetch_facility(session, facility):
    """Try simple fetch first, fall back to Playwright if needed."""
    name = facility['name']
    url = facility['url']
    logger.info(f"Fetching: {name}")

    text, method = await fetch_simple(session, url)

    # If simple fetch got very little content, try Playwright
    if not text or len(text) < 200:
        logger.info(f"Falling back to Playwright for: {name}")
        text, method = await fetch_playwright(url)

    if text:
        logger.info(f"Got {len(text)} chars via {method} for {name}")
        return {"facility": facility, "content": text, "method": method, "success": True}
    else:
        logger.warning(f"Failed to fetch: {name}")
        return {"facility": facility, "content": None, "method": "failed", "success": False}

async def fetch_all(facilities, max_concurrent=5):
    """Fetch all facilities with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)
    results = []

    async def bounded_fetch(session, facility):
        async with semaphore:
            return await fetch_facility(session, facility)

    async with aiohttp.ClientSession() as session:
        tasks = [bounded_fetch(session, f) for f in facilities]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out exceptions
    clean = []
    for r in results:
        if isinstance(r, Exception):
            logger.error(f"Task exception: {r}")
        else:
            clean.append(r)
    return clean
