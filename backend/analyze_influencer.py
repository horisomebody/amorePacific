from openai import OpenAI
import json

client = OpenAI(api_key="내_API_키")

def analyze_brand_fit(influencer_json):
    # 1. 시스템 프롬프트: AI에게 '아모레퍼시픽 마케터'라는 페르소나 부여
    system_prompt = """
    당신은 아모레퍼시픽의 인플루언서 마케팅 담당자입니다.
    주어진 인플루언서 데이터를 분석하여 우리 브랜드와의 적합성을 판단하세요.

    [아모레퍼시픽 브랜드 인재상]
    1. **Visual:** 인위적이지 않고 자연스러운 톤, 고화질, 깨끗한 배경. (선정적이거나 너무 화려하면 감점)
    2. **Content:** 단순히 '좋아요'만 외치지 않고, 제품의 성분이나 가치관(비건, 환경)에 대해 이야기하는가?
    3. **Tone:** 차분하고 전문적이거나, 밝고 건강한 에너지. (비속어, 과도한 밈 사용 금지)

    [입력 데이터]
    최근 게시물 3개의 캡션과 썸네일 정보가 주어집니다.
    """

    # 2. 사용자 프롬프트: 실제 수집한 데이터 넣기
    user_prompt = f"""
    아래 데이터를 분석해줘:
    {json.dumps(influencer_json, ensure_ascii=False)}

    결과는 반드시 다음 JSON 포맷으로 출력해:
    {{
        "total_score": 0~100점,
        "visual_vibe": "한줄 요약 (예: 자연광을 활용한 감성적인 무드)",
        "content_quality": "한줄 요약 (예: 구체적인 사용 후기를 남김)",
        "is_recommended": true/false (80점 이상이면 true),
        "reason": "추천/비추천 이유 상세 설명"
    }}
    """

    # 3. GPT-4o 호출
    response = client.chat.completions.create(
        model="gpt-4o", # 텍스트만 분석할 때 (이미지까지 보려면 gpt-4o-vision 사용 필요)
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)