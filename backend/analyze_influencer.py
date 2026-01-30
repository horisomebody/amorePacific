import json
import os
import sys
import io  # <--- [중요] 이게 빠져서 에러가 난 겁니다!
from openai import OpenAI

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

# [디버깅] 스크립트가 시작되었는지 확인
print("🚀 [Start] analyze_influencer.py 실행 시작...")

# 1. API 키 설정: 환경변수에서 읽어오기
#    - 쉘 또는 .env(예: OPENAI_API_KEY=sk-...) 에 키를 지정
#    - OpenAI 대시보드에서 Billing(결제) 등록 및 크레딧이 있어야 정상 호출됩니다.
API_KEY = os.getenv("OPENAI_API_KEY", "")

if not API_KEY or not API_KEY.startswith("sk-"):
    print("⚠️ [Error] OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
    print("   1) OpenAI 대시보드에서 결제 수단/크레딧을 준비하고,")
    print("   2) 터미널 또는 .env 파일에 OPENAI_API_KEY=... 형태로 키를 설정하세요.")
    exit()

try:
    client = OpenAI(api_key=API_KEY)
    print("✅ [Setup] OpenAI 클라이언트 연결 성공")
except Exception as e:
    print(f"❌ [Error] OpenAI 클라이언트 설정 실패: {e}")
    exit()

def evaluate_influencer(influencer_data):
    """
    GPT-4o를 이용해 인플루언서 데이터를 분석하고 점수를 매기는 함수
    """
    print(f"   ⏳ [Process] AI 분석 요청 중... (대상: {influencer_data.get('username', 'Unknown')})")

    # 프롬프트 설정 (한국어 출력)
    system_prompt = """
    당신은 아모레퍼시픽 인플루언서 마케팅 담당자입니다.
    제공된 인플루언서 데이터를 분석하여, 브랜드 가치(클린뷰티, 럭셔리, 진정성)에 부합하는지 판단하세요.
    
    [출력 형식]
    반드시 JSON 형식으로만 응답하세요. 모든 문장은 한국어로 작성하세요.
    {
        "score": 숫자 (0-100),
        "reason": "평가 요약 한 줄 (한국어)",
        "decision": "PASS" 또는 "FAIL"
    }
    """
    
    user_content = json.dumps(influencer_data)

    try:
        # API 호출
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"}
        )

        # 결과 받기
        result_json = response.choices[0].message.content
        parsed_result = json.loads(result_json)
        print("   ✅ [Success] AI 분석 완료!")
        return parsed_result

    except Exception as e:
        print(f"   ❌ [Error] AI 분석 중 에러 발생: {e}")
        return None

def scraped_to_eval_format(data):
    """scraping.py에서 나온 한 명 분 데이터를 evaluate_influencer 형식으로 맞춤."""
    posts = data.get("recent_posts") or []
    return {
        "username": data.get("username", ""),
        "url": data.get("url", ""),
        "stats": data.get("stats", ""),
        "bio": data.get("bio", ""),
        "recent_posts": [
            {
                "caption": p.get("caption", ""),
                "image_desc": p.get("visual_desc", p.get("image_desc", "")),
                "type": p.get("type", ""),
                "link": p.get("link", ""),
            }
            for p in posts
        ],
    }


# ==========================================================
# [중요] 이 부분이 없으면 실행해도 아무 일도 안 일어납니다!
# ==========================================================
if __name__ == "__main__":
    from scraping import run_scraper

    print("\n🕷️ [Scraping] Instagram에서 인플루언서 데이터 수집 중... (브라우저가 뜰 수 있음)")
    raw_influencers = run_scraper()

    if not raw_influencers:
        print("⚠️ 수집된 데이터가 없습니다. 스크래퍼 설정(해시태그/세션)을 확인하세요.")
        exit()

    print(f"\n✅ 수집 완료: {len(raw_influencers)}명 → AI 분석 시작\n")

    results = []
    for i, one in enumerate(raw_influencers, 1):
        print(f"[{i}/{len(raw_influencers)}] @{one.get('username', '?')}")
        eval_data = scraped_to_eval_format(one)
        result = evaluate_influencer(eval_data)
        if result:
            result["username"] = one.get("username", "")
            results.append(result)

    print("\n📊 [최종 결과 출력]")
    for r in results:
        print(r)