import random
import time
from playwright.sync_api import sync_playwright
# from playwright import page

def scrape_tver_episodes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://tver.jp/talents/t05c523/episodes", timeout=60000)
        print('started')
        page.wait_for_timeout(10000)
        print('finished waiting')
        # <a>タグの中に<p>が2つ以上あるものだけを対象にする（エピソードカードの特徴）
        page.wait_for_selector("a >> p:nth-of-type(2)")

        # 対象となる<a>タグ一覧を取得
        episode_links = page.locator("a").filter(
            has=page.locator("p:nth-of-type(2)")
        )

        count = episode_links.count()
        for i in range(count):
            link = episode_links.nth(i)
            ps = link.locator("p")
            if ps.count() >= 2:
                title = ps.nth(0).inner_text()
                subtitle = ps.nth(1).inner_text()
                print(f"[{i+1}] タイトル: {title}")
                print(f"     サブタイトル・放送情報: {subtitle}")
                print("-" * 50)

                if i != count - 1:
                    sleep_sec = random.uniform(8, 12)
                    print(f"→ {sleep_sec:.2f} 秒スリープ中...\n")
                    # time.sleep(sleep_sec)
                    page.wait_for_timeout(10000);

        browser.close()

if __name__ == "__main__":
    scrape_tver_episodes()