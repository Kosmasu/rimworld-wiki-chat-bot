
from datetime import datetime
from pydantic import BaseModel


class Page(BaseModel):
    url: str
    scraped_at: datetime | None = None
    content: str | None = None

class DBPage(Page):
    id: int