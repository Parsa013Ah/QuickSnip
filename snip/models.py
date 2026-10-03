from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Snippet:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    language: str = ""
    code: str = ""
    tags: list[str] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
