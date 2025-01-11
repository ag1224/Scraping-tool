import redis
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Header
from config import AUTH_TOKEN, REDIS_HOST, REDIS_PORT
from models import ScrapeResponse, ScrapeSettings
from notifier import ConsoleNotifier
from scrapper import Scraper
from storage import JSONStorage

# Load environment variables
load_dotenv()

# Initialize Redis client
cache_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

app = FastAPI(title="Product Scraping Tool")

# ---------------------- Authentication ----------------------

API_KEY = AUTH_TOKEN

def get_api_key(api_key_header: str = Header(...)):
    # print(API_KEY, '  ', api_key_header)
    if api_key_header != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return api_key_header

# ---------------------- API Endpoint ----------------------

@app.post("/scrape", response_model=ScrapeResponse)
def scrape_products(settings: ScrapeSettings, api_key: str = Depends(get_api_key)):
    """
    Initiate scraping of products from the target website.
    - **max_pages**: Maximum number of pages to scrape (optional).
    - **proxy**: Proxy string to use for scraping (optional).
    """
    scraper = Scraper(
        storage=JSONStorage(),
        notifier=ConsoleNotifier(),
        cache_client=cache_client,
        proxy=settings.proxy
    )
    response = scraper.scrape(max_pages=settings.max_pages)
    return response

# ---------------------- Root Endpoint ----------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the Product Scraping Tool API"}

