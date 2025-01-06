import asyncio
from crawler.url_discovery import discover_product_urls
from utils.logger import get_logger
from config import PARTIAL_SAVE_INTERVAL

logger = get_logger(__name__)

def load_domains_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []

def save_results_to_file(results, file_path):
    """
    Save final results to a file.
    """
    try:
        with open(file_path, "w") as file:
            for domain, product_urls in results.items():
                file.write(f"{domain}:\n")
                for url in product_urls:
                    file.write(f"  {url}\n")
                file.write("\n")
        logger.info(f"Results saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving results: {e}")

def main():
    input_file = "domains.txt"
    output_file = "output.txt"

    domains = load_domains_from_file(input_file)
    if not domains:
        logger.info("No domains found in file.")
        return

    logger.info("Starting URL discovery...")
    results = asyncio.run(discover_product_urls(domains, output_file, PARTIAL_SAVE_INTERVAL))
    save_results_to_file(results, output_file)

if __name__ == "__main__":
    main()
