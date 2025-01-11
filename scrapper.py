import os
import redis
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.util.retry import Retry # type: ignore
from requests.adapters import HTTPAdapter
from models import Product, ScrapeResponse
from notifier import Notifier
from storage import Storage
from typing import Optional


class Scraper:
    BASE_URL = "https://dentalstall.com/shop"

    def __init__(self, storage: Storage, notifier: Notifier, cache_client: redis.Redis, proxy: Optional[str] = None):
        self.storage = storage
        self.notifier = notifier
        self.cache = cache_client
        self.proxies = {"http": proxy, "https": proxy} if proxy else None
        self.session = self._init_session()

    def _init_session(self) -> requests.Session:
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def scrape(self, max_pages: Optional[int] = None) -> ScrapeResponse:
        scraped_count = 0
        updated_count = 0
        existing_products = {product.product_title: product for product in self.storage.load_data()}

        for page_num in range(1, max_pages + 1 if max_pages else 10**6):
            url = f"{self.BASE_URL}/page/{page_num}"
            try:
                response = self.session.get(url, proxies=self.proxies, timeout=10)
                response.raise_for_status()
            except requests.RequestException as e:
                self.notifier.notify(f"Failed to retrieve page {page_num}: {e}")
                break # all pages are fetched
            
            print(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup)
            # with open('page_html.html', "w", encoding="utf-8") as file:
            #     file.write(response.text)
            product_cards = soup.find_all('div', class_='product-inner')
            # print(product_cards)
            
            if not product_cards:
                self.notifier.notify(f"No products found on page {page_num}. Stopping scrape.")
                break

            for card in product_cards:
                # print(card, '\n\n')
                title = card.find('h2', class_='woo-loop-product__title').get_text(strip=True)

                try:
                    price_text = card.find('span', class_='woocommerce-Price-amount').get_text(strip=True).replace('₹', '').replace(',', '')
                    price = float(price_text)
                except AttributeError:
                    price = 0.0
                except ValueError:
                    price = 0.0
                image_tag = card.find('noscript').find('img')
                image_url = image_tag['src'] if image_tag else ''

                # Caching logic
                cached_price = self.cache.get(title)
                if cached_price and float(cached_price) == price:
                    continue  # Price hasn't changed, skip updating
                self.cache.set(title, price)

                # Download image
                image_path = self._download_image(image_url, title)

                product = Product(
                    product_title=title,
                    product_price=price,
                    path_to_image=image_path
                )

                if title in existing_products:
                    existing_products[title] = product
                    updated_count += 1
                else:
                    existing_products[title] = product
                    scraped_count += 1

            # Optional: Stop if no more pages
            if max_pages and page_num >= max_pages:
                break

        self.storage.save_data(list(existing_products.values()))
        self.notifier.notify(f"Scraping completed. Scraped: {scraped_count}, Updated: {updated_count}")
        return ScrapeResponse(scraped_count=scraped_count, updated_count=updated_count)

    def _download_image(self, url: str, title: str) -> str:
        if not url:
            return ""
        try:
            response = self.session.get(url, proxies=self.proxies, timeout=10)
            response.raise_for_status()
            image_extension = url.split('.')[-1].split('?')[0]
            image_filename = f"images/{title.replace(' ', '_')}.{image_extension}"
            # check for empty filename
            if not image_filename or not os.path.dirname(image_filename):
                raise ValueError()
            os.makedirs(os.path.dirname(image_filename), exist_ok=True)
            with open(image_filename, 'wb') as f:
                f.write(response.content)
            return image_filename
        except ValueError:
            self.notifier.notify(f"Invalid or empty image filename")
            return ""
        except requests.RequestException as e:
            self.notifier.notify(f"Failed to download image for {title}: {e}")
            return ""
