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
  - `uvicorn`

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

---

## Running the Application

#### Start Redis Server

Ensure that Redis is running on your machine. You can start it using:

```bash
redis-server
```

#### Run the FastAPI Application

The API will be available at `http://127.0.0.1:8000`. You can start server using:

```bash
uvicorn main:app --reload
```

---

## Usage

All requests to the `/scrape` endpoint must include the `api_key_header` header with the correct token.
#### Example Request Using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/scrape" \
     -H "api_key_header: your_static_token_here" \
     -H "Content-Type: application/json" \
     -d '{"max_pages": 5, "proxy": "http://yourproxy:port"}'
```

#### Expected Response:
```bash
{
  "scraped_count": 20,
  "updated_count": 5
}
```

This response indicates that 20 new products were scraped and 5 existing products were updated in the JSON storage.