from pydantic import BaseModel
from typing import List, Optional

class PreferencesModel(BaseModel):
    user_id: int
    preferred_hotel_types: Optional[List[str]] = []
    max_budget: Optional[float] = None