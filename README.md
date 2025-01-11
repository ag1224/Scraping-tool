# Web Scraper Tool

This Web Scraper Tool automates the extraction of product data (titles, prices, and images) from an e-commerce website. The scraped data is stored locally, and product images are downloaded to a specified directory. The tool is built with **Python** using **BeautifulSoup** and supports dynamic configuration for scraping.

---

## Features

- Scrapes product titles, prices, and images from the target website.
- Downloads product images to a local directory.
- Handles dynamic or infinite pagination with configurable page limits.
- Provides robust error handling for missing data or connectivity issues.
- Outputs the scraped data in **JSON** format for easy reuse.

---

## Requirements

- Python 3.7 or higher
- Required Python libraries:
  - `beautifulsoup4`
  - `requests`
  - `fastapi`
  - `redis`
  - `python-dotenv`

To install the dependencies, run:

```bash
pip install -r requirements.txt
