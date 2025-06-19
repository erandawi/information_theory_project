import sys
from src.logging.logger  import logging
from src.components.scraper import WebScraper
from src.exception.exception import InformaitonThoeryProjectException

# testing logger

# logging.info("hi there Log message from main.py")

# testing exception

# def test_exception():
#     try:
#         a = 1 / 0  # this will raise ZeroDivisionError
#     except Exception as e:
#         raise InformaitonThoeryProjectException(e, sys)

# if __name__ == "__main__":
#     test_exception()

# testing scrapper

# if __name__ == "__main__":
#     try:
#         seed_url = "https://www.sciencedaily.com/"
#         scraper = WebScraper(seed_url, max_pages=5, delay=2)
#         scraper.crawl()
#     except InformaitonThoeryProjectException as e:
#         logging.error(e)
#     except Exception as e:
#         logging.error(f"An unexpected error occurred: {e}")