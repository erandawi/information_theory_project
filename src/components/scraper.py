import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

from src.logging.logger import logging
from src.exception.exception import InformaitonThoeryProjectException

class WebScraper:
    def __init__(self, seed_url, max_pages=10, delay=5, save_dir="./data/crawled"):
        self.seed_url = seed_url
        self.max_pages = max_pages
        self.delay = delay
        self.save_dir = save_dir
        self.scraped = set()
        self.to_scrape = deque([self.seed_url])
        self.count = 0

        try:
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)
                logging.info(f"Created scraping directory: {self.save_dir}")
        except Exception as e:
            raise InformaitonThoeryProjectException("Failed to create save directory", sys)
    
    def crawl(self):
        logging.info(f"Started scraping: {self.seed_url}")

        while self.to_scrape and self.count < self.max_pages:
            url = self.to_scrape.popleft()
            if url in self.scraped:
                continue

            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')
                filename = os.path.join(self.save_dir, f"document_{self.count}.html")

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                logging.info(f"Saved: {filename}")

                self.count += 1
                self.scraped.add(url)

                for link in soup.find_all('a', href=True):
                    full_url = urljoin(url, link['href'])
                    if urlparse(full_url).netloc == urlparse(self.seed_url).netloc:
                        if full_url not in self.scraped:
                            self.to_scrape.append(full_url)
                            
            except requests.RequestException as e:
                logging.error(f"Request failed for {url}: {e}")
            except Exception as e:
                raise InformaitonThoeryProjectException(f"Error while processing {url}", sys)

            time.sleep(self.delay)

        logging.info("Scraping completed")
    
