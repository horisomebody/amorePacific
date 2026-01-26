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
SESSION_ID = "80428412664%3A08ofLaZrE0XqdP%3A28%3AAYiHOQkE8q0LUfAfgL46Ei6LNZDvJGxAlh75Ufp81A" 

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
                    continue

                print(f"🔍 분석 중: @{author_username}")
                
                # --- 프로필 수집 로직 ---
                profile_url = f"https://www.instagram.com/{author_username}/"
                page.goto(profile_url, wait_until="domcontentloaded", timeout=15000)
                time.sleep(random.uniform(2, 4))
                
                # 변수 초기화
                stats_text = "정보 없음"
                bio_text = "No Bio"
                
                try:
                    # [핵심 변경] og:description 대신 name="description"을 찾습니다.
                    # 이 태그 안에 통계와 바이오가 다 들어있습니다.
                    page.wait_for_selector('meta[name="description"]', state="attached", timeout=5000)
                    raw_content = page.locator('meta[name="description"]').get_attribute("content")
                    
                    # raw_content 예시: 
                    # "팔로워 8명, 팔로잉 77명, 게시물 92개 - 블랙체리 (@black.cherry2025)님의 Instagram 계정: '2025.08.21 인스타 시작~\n#일상 #이벤트'"
                    
                    if raw_content:
                        # 1. 통계 추출 (앞부분)
                        # " - " (하이픈)을 기준으로 앞부분이 통계입니다.
                        if " - " in raw_content:
                            stats_text = raw_content.split(" - ")[0]
                        else:
                            stats_text = raw_content

                        # 2. Bio 추출 (뒷부분)
                        # 패턴: ... Instagram 계정: '바이오내용'
                        # ": '" (콜론+공백+작은따옴표)로 나뉘어 있습니다.
                        if ": '" in raw_content:
                            # 쪼갠 뒤 마지막 부분이 바이오입니다.
                            temp_bio = raw_content.split(": '")[-1]
                            # 맨 마지막에 붙은 작은따옴표(') 하나 제거
                            bio_text = temp_bio.rstrip("'")
                        else:
                            # Bio가 없는 경우도 있으므로 처리
                            print("   ℹ️ Bio가 비어있거나 패턴이 다름")
                            
                except Exception as e:
                    print(f"   ⚠️ 정보 추출 중 에러: {e}")
                

                print(f"   📸 최근 게시물 3개(릴스 포함) 수집 시작...")
                recent_posts_data = []
                
                try:
                    # ---------------------------------------------------------
                    # STEP 1: 게시물 목록(그리드) 찾기 단계
                    # ---------------------------------------------------------
                    
                    # 1. 로딩 대기 (최대 5초)
                    # 인스타그램 프로필에서 게시물 링크는 href에 '/p/'(사진) 또는 '/reel/'(영상)이 들어감
                    try:
                        # 무작정 기다리지 말고, 실제 링크가 뜰 때까지 기다림
                        page.wait_for_selector('a[href*="/p/"], a[href*="/reel/"]', timeout=5000)
                        print("      ✅ [1단계 성공] 게시물 링크가 화면에 떴습니다.")
                    except:
                        print("      ❌ [1단계 실패] 5초를 기다려도 게시물 링크를 못 찾았습니다.")
                        # [CCTV 1] 현재 화면 찰칵! -> 범인: 로딩이 덜 됐거나, 비공개 계정이거나, 로그인 풀림
                    
                    # 2. 링크 싹 긁어오기
                    # article 태그 안에 있는지 확인하지 말고, 일단 페이지 전체에서 찾음 (범위 확장)
                    all_links = page.locator('a').all()
                    
                    post_urls = []
                    seen_urls = set()
                    
                    for link_el in all_links:
                        href = link_el.get_attribute("href")
                        if href:
                            # 게시물 패턴 확인 (/p/ 또는 /reel/)
                            if ("/p/" in href or "/reel/" in href) and "/tagged/" not in href:
                                full_url = f"https://www.instagram.com{href}"
                                if full_url not in seen_urls:
                                    post_urls.append(full_url)
                                    seen_urls.add(full_url)
                                    
                                if len(post_urls) >= 3:
                                    break
                    
                    print(f"      📊 [DEBUG] 찾아낸 링크 개수: {len(post_urls)}개")
                    
                    if len(post_urls) == 0:
                        print("      ⚠️ 링크를 하나도 못 찾았습니다. (Step 1 문제)")
                        # 여기서 끝나면 -> '인플루언서 계정에서 게시글 못 찾는 문제'

                    # ---------------------------------------------------------
                    # STEP 2: 상세 페이지 진입 단계
                    # ---------------------------------------------------------
                    for i, p_url in enumerate(post_urls):
                        try:
                            print(f"      🚀 [이동 중] {i+1}번째 게시물: {p_url}")
                            page.goto(p_url, wait_until="domcontentloaded", timeout=15000)
                            time.sleep(random.uniform(2, 3))
                            

                            post_type = "Reel" if "/reel/" in p_url else "Post"
                            post_text = "본문 없음"
                            visual_info = "이미지 없음"
                            thumbnail_url = ""

                            # A. 본문 찾기 테스트
                            try:
                                page.wait_for_selector('meta[property="og:title"]', state="attached", timeout=3000)
                                raw_title = page.locator('meta[property="og:title"]').get_attribute("content")
                                if ": '" in raw_title:
                                    post_text = raw_title.split(": '")[-1].rstrip("'")
                                else:
                                    post_text = raw_title
                                print(f"         ✅ 본문 추출 성공: {post_text[:20]}...")
                            except:
                                print(f"         ❌ 본문 추출 실패 (구조 다름)")

                            # B. 시각 정보(썸네일) 수집 (업그레이드: Meta 태그 우선 전략)
                            visual_info = "이미지 설명 없음"
                            thumbnail_url = ""
                            
                            try:
                                # [전략 1] 가장 빠른 방법: Meta 태그(og:image)에서 고화질 주소 가져오기
                                # 화면 렌더링을 기다릴 필요 없이 HTML 헤더에서 바로 추출 가능
                                try:
                                    # 메타 태그는 보통 바로 뜸. 1초만 기다려봄.
                                    page.wait_for_selector('meta[property="og:image"]', state="attached", timeout=2000)
                                    og_image = page.locator('meta[property="og:image"]').get_attribute("content")
                                    if og_image:
                                        thumbnail_url = og_image
                                        print(f"         ✅ [Meta] 고화질 썸네일 확보")
                                except:
                                    pass

                                # [전략 2] Meta 태그 실패 시, 화면 요소(Element) 뒤지기
                                if not thumbnail_url:
                                    print("         ⏳ Meta 태그 실패 -> 화면 요소 스캔 시작...")
                                    
                                    # 릴스(Video)인 경우 포스터 이미지 확인
                                    if post_type == "Reel":
                                        try:
                                            page.wait_for_selector('video', timeout=3000)
                                            poster = page.locator('video').first.get_attribute("poster")
                                            if poster:
                                                thumbnail_url = poster
                                                visual_info = "Reel Video Thumbnail"
                                                print(f"         ✅ [Element] 릴스 포스터 발견")
                                        except:
                                            pass

                                    # 일반 게시물(Post)이거나 릴스 포스터 실패 시 -> img 태그 확인
                                    if not thumbnail_url:
                                        try:
                                            # article 안의 이미지 로딩 대기
                                            page.wait_for_selector('article img', timeout=3000)
                                            
                                            # 가장 큰 이미지 찾기 (프로필 사진 제외)
                                            images = page.locator('article img').all()
                                            for img in images:
                                                src = img.get_attribute("src")
                                                alt = img.get_attribute("alt")
                                                
                                                # 주소가 있고 길이가 충분히 길면 본문 이미지로 간주
                                                if src and len(src) > 100:
                                                    thumbnail_url = src
                                                    if alt: visual_info = alt
                                                    print(f"         ✅ [Element] 본문 이미지 발견")
                                                    break
                                        except:
                                            pass

                                # https://namu.wiki/w/%EB%B3%B4%EC%A0%95 인코딩 문자 복구
                                if thumbnail_url:
                                    thumbnail_url = thumbnail_url.replace("&amp;", "&")

                                if not thumbnail_url:
                                    print("         ❌ 썸네일 추출 최종 실패")
                                    # 디버깅용: 도대체 화면이 어떻길래 못 찾았는지 찍어보기
                                    page.screenshot(path=f"fail_thumb_{i}.png")

                            except Exception as e:
                                print(f"         ⚠️ 시각 정보 로직 에러: {e}")

                            # 데이터 저장
                            recent_posts_data.append({
                                "type": post_type,
                                "link": p_url,
                                "caption": post_text[:200],
                                "visual_desc": visual_info[:200],
                                "thumbnail_url": thumbnail_url
                            })
                            
                        except Exception as e:
                            print(f"      ⚠️ 게시물 상세 에러: {e}")
                            continue
                            
                except Exception as e:
                    print(f"   ⚠️ 최근 게시물 로직 전체 에러: {e}")


                # =================================================================
                # [최종 데이터 저장] 여기가 질문하신 JSON 저장 부분입니다!
                # =================================================================
                data = {
                    "username": author_username,
                    "url": profile_url,
                    "stats": stats_text,
                    "bio": bio_text,
                    "recent_posts": recent_posts_data  # List[Dict] 형태로 저장됨
                }
                
                influencer_data.append(data)
                
                print(f"   🎉 수집 성공! (게시물 {len(recent_posts_data)}개 포함)")
                # print(f"      - 스탯: {stats_text}")
                
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