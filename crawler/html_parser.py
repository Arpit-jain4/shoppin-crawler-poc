from bs4 import BeautifulSoup
import re
from utils.logger import get_logger
logger = get_logger(__name__)

# PRODUCT_URL_PATTERNS = [
#     # re.compile(r"https?://(?:www\.)?amazon\.in/[^/]+/dp/[A-Z0-9]{10}(?:/|\?.*)?"),  # Absolute URLs with query parameters
#     re.compile(r"/dp/[A-Z0-9]{10}(?:/|\?.*)?"),  # Relative /dp/ URLs with query parameters
#     # re.compile(r"/[^/]+/dp/[A-Z0-9]{10}(?:/|\?.*)?"),  # Relative URLs with product name
# ]

PRODUCT_URL_PATTERNS = [
    re.compile(r"/dp/[A-Za-z0-9]{10}"),
    re.compile(r".*\/dp/[A-Za-z0-9]{10}"),
    re.compile(r"/product/[A-Za-z0-9_-]+"),       # /product/<name-or-id>
    re.compile(r"/item/[A-Za-z0-9_-]+"),          # /item/<name-or-id>
    re.compile(r"/p/[A-Za-z0-9_-]+"),             # /p/<name-or-id>
    re.compile(r"/[A-Za-z0-9_-]+/dp/[A-Za-z0-9]{10}"),  # /<name>/dp/<10-char-id>
    re.compile(r".*\/ip\/[A-Za-z0-9\-]+\/\d+(?:\?.*)?"),
    re.compile(r".*\/ssp"),
    re.compile(r"^https?:\/\/www\.flipkart\.com\/[a-z0-9\-]+\/p\/[a-z0-9]+(\?[a-z0-9=&%_\-]*)?")
]

def parse_product_urls(domain, html_content):
    """
    Extract product URLs from HTML content.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    product_urls = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/"):
            href = domain + href
        if any(pattern.match(href) for pattern in PRODUCT_URL_PATTERNS):
            product_urls.add(href)

    logger.info(f"Found {len(product_urls)} product URLs.")
    return list(product_urls)

