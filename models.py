from typing import Optional
from pydantic import BaseModel, Field


class ScrapeSettings(BaseModel):
    max_pages: Optional[int] = Field(None, description="Maximum number of pages to scrape")
    proxy: Optional[str] = Field(None, description="Proxy string to use for scraping")

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str

class ScrapeResponse(BaseModel):
    scraped_count: int
    updated_count: int