import time
import random
import re
from playwright.sync_api import sync_playwright
def stealth_sync(context):
    """playwright-stealth 라이브러리 내용 직접 삽입"""
    init_script = """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        Object.defineProperty(navigator, 'languages', {
            get: () => ['ko-KR', 'ko', 'en-US', 'en']
        });
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5]
        });
    """
    context.add_init_script(init_script)

# 설정 값 (실제 값으로 교체 필요)
TARGET_HASHTAG = "클린뷰티"
SESSION_ID = "80428412664%3AvXhlRZrPj78zdW%3A14%3AAYjjwyTd8vb1xbAgDLcnc5u-qSCVnWZk8JAXu_B96w" 

def run_scraper():
    # [설정 1] 여기에 크롤링에 사용하는 '내 부계정 아이디'를 적으세요 (제외 목적)
    MY_USERNAME = "genejichoong"  # 예: "test_account_123"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            locale='ko-KR'
        )
        
        stealth_sync(context)
        
        context.add_cookies([
            {'name': 'sessionid', 'value': SESSION_ID, 'domain': '.instagram.com', 'path': '/'}
        ])
        
        page = context.new_page()
        
        print(f"🚀 #{TARGET_HASHTAG} 검색 시작...")
        page.goto(f"https://www.instagram.com/explore/tags/{TARGET_HASHTAG}/", wait_until="domcontentloaded")
        time.sleep(random.uniform(3, 5))

        post_locators = page.locator('a[href^="/p/"]').all()
        unique_links = []
        for loc in post_locators[:5]: 
            link = loc.get_attribute("href")
            if link and link not in unique_links:
                unique_links.append(f"https://www.instagram.com{link}")

        print(f"✅ 수집된 게시물: {len(unique_links)}개")

        influencer_data = []
        EXCLUDE_WORDS = ['explore', 'p', 'reel', 'reels', 'stories', 'legal', 'about', 'help']

        for link in unique_links:
            try:
                print(f"➡️ 이동 중: {link}")
                page.goto(link, wait_until="domcontentloaded", timeout=15000)
                time.sleep(random.uniform(2, 3))
                
                author_username = None
                
                try:
                    # 1. <article> 태그 안을 먼저 뒤짐
                    container = page.locator("article")
                    if container.count() == 0:
                        container = page.locator("body")
                    
                    # 2. 모든 링크 가져오기
                    all_links = container.locator("a").all()
                    
                    for a_tag in all_links:
                        href = a_tag.get_attribute("href")
                        
                        if href:
                            if any(word in href for word in EXCLUDE_WORDS):
                                continue

                            match = re.search(r"^/([a-zA-Z0-9._]+)/$", href)
                            
                            if match:
                                found_id = match.group(1)
                                
                                # [핵심 수정] 내 아이디면 무시하고 다음 링크 찾기
                                if found_id == MY_USERNAME:
                                    # print(f"   (내 계정 감지됨 - 패스)")
                                    continue

                                # 3. 유효성 검사 (너무 짧거나 기능성 단어 제외)
                                if len(found_id) > 1 and found_id.lower() not in ['login', 'signup', 'home']:
                                    
                                    # [추가 검증] 링크 텍스트와 아이디가 일치하는지 확인
                                    # 작성자 링크는 보통 텍스트로 아이디가 써있음 (zeonzyoung)
                                    # 반면 내 프로필 아이콘은 텍스트가 없거나 '프로필'임
                                    try:
                                        link_text = a_tag.text_content().strip()
                                        # 텍스트가 있는데(이미지 아님), 아이디랑 전혀 다르면 의심
                                        if link_text and found_id not in link_text:
                                            # 하지만 닉네임일 수도 있으니 이건 패스하지 말고 보류
                                            pass
                                    except:
                                        pass

                                    author_username = found_id
                                    print(f"   ℹ️ 작성자 아이디 발견: {author_username}")
                                    break 
                                    
                except Exception as e:
                    print(f"   ⚠️ 링크 분석 중 에러: {e}")

                if not author_username:
                    print(f"⚠️ 작성자 아이디 추출 실패 (패스): {link}")
                    page.screenshot(path=f"fail_{int(time.time())}.png")
                    continue

                print(f"🔍 분석 중: @{author_username}")
                
                # --- 프로필 수집 로직 ---
                profile_url = f"https://www.instagram.com/{author_username}/"
                page.goto(profile_url, wait_until="domcontentloaded", timeout=15000)
                time.sleep(random.uniform(2, 4))
                
                meta_content = "정보 없음"
                try:
                    page.wait_for_selector('meta[property="og:description"]', state="attached", timeout=5000)
                    meta_content = page.locator('meta[property="og:description"]').get_attribute("content")
                except:
                    pass
                
                bio_text = "No Bio"
                try:
                    if page.locator('h1').count() > 0:
                        bio_text = "\n".join(page.locator('h1').all_text_contents())
                except:
                    pass

                data = {
                    "username": author_username,
                    "url": profile_url,
                    "stats": meta_content,
                    "bio": bio_text
                }
                influencer_data.append(data)
                print(f"   🎉 수집 성공! ({meta_content[:15]}...)")
                
            except Exception as e:
                print(f"⚠️ 에러 발생: {e}")
                continue

        browser.close()
        return influencer_data
# 실행
if __name__ == "__main__":
    results = run_scraper()
    print("\n[최종 결과]")
    for res in results:
        print(res)