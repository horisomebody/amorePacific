from data import INFLUENCERS_DB

def run_agent_logic(category: str, min_score: int):
    """
    [AI Agent Logic]
    1. 카테고리가 일치하거나 설명에 포함된 사람을 찾는다.
    2. 최소 점수(consistency_score) 이상인 사람만 남긴다.
    3. 점수가 높은 순서대로 정렬한다.
    """
    
    # 1. 검색 (Filtering)
    filtered = [
        inf for inf in INFLUENCERS_DB 
        if (category.lower() in inf["category"].lower()) or 
           (category.lower() in inf["description"].lower())
    ]
    
    # 2. 점수 커트라인 (Filtering)
    filtered = [inf for inf in filtered if inf["consistency_score"] >= min_score]
    
    # 3. 정렬 (Sorting)
    sorted_results = sorted(filtered, key=lambda x: x["consistency_score"], reverse=True)
    
    return sorted_results