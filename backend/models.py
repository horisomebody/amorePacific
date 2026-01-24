from pydantic import BaseModel
from typing import Optional

# 인플루언서 한 명의 데이터 모양
class Influencer(BaseModel):
    id: int
    name: str
    category: str
    followers: int
    consistency_score: int
    image: str
    description: str


class RecommendationRequest(BaseModel):
    category: str
    min_score: Optional[int] = 0