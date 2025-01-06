import asyncio
from crawler.selenium_runner import fetch_page_with_scroll
from crawler.html_parser import parse_product_urls
from utils.logger import get_logger
from config import MAX_DEPTH

logger = get_logger(__name__)

async def discover_product_urls(domains, output_file, partial_save_interval):
    """
    Discover product URLs recursively for multiple domains with partial saving.
    """
    results = {}
    visited_urls = set()
    processed_domains = 0

    async def process_page(domain, url, depth):
        if depth > MAX_DEPTH or url in visited_urls:
            return set()

        visited_urls.add(url)
        logger.info(f"Processing URL: {url} at depth {depth}")

        try:
            html_content = await asyncio.to_thread(fetch_page_with_scroll, url)
            if not html_content:
                return set()

            product_urls = set(parse_product_urls(domain, html_content))
            all_product_urls = set(product_urls)

            for product_url in product_urls:
                child_product_urls = await process_page(domain, product_url, depth + 1)
                all_product_urls.update(child_product_urls)

            return all_product_urls
        except Exception as e:
            logger.error(f"Error processing URL {url}: {e}")
            return set()

    for domain in domains:
        try:
            product_urls = await process_page(domain, domain, 1)
            results[domain] = list(product_urls)

            # Save partial results periodically
            processed_domains += 1
            if processed_domains % partial_save_interval == 0:
                save_partial_results(results, output_file)

        except Exception as e:
            logger.error(f"Error processing domain {domain}: {e}")

    return results

def save_partial_results(results, file_path):
    """
    Save partial results to a file.
    """
    try:
        with open(file_path, "a") as file:
            for domain, product_urls in results.items():
                file.write(f"{domain}:\n")
                for url in product_urls:
                    file.write(f"  {url}\n")
                file.write("\n")
        logger.info("Partial results saved.")
    except Exception as e:
        logger.error(f"Error saving partial results: {e}")
