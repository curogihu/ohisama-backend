import random
import time
from django.core.management.base import BaseCommand
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

import csv
from pathlib import Path

def extract_talent_ids(csv_file):
    talent_ids = []
    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            talent_ids.append(row["talent_id"])
    return talent_ids


class Command(BaseCommand):
    help = "TVerから対象メンバー出演番組を取得しDBに登録"

    # def add_arguments(self, parser):
    #     parser.add_argument("talent_path", type=str, help="例: t0506ca")
    #     parser.add_argument("--max", type=int, default=10, help="最大取得件数（デフォルト10件）")

    # def _scrape_episodes(self, page, max_items):
    def _scrape_episodes(self, page):
        links = page.locator("a")
        total = links.count()

        print(links)

        self.stdout.write(self.style.WARNING(f"{total}件を処理します"))

        # for link in links:
        #     print(link)

        # for i in range(min(total, max_items)):
        #     link = links.nth(i)
        #     ps = link.locator("p")
        #     if ps.count() >= 2:
        #         title = ps.nth(0).inner_text()
        #         subtitle = ps.nth(1).inner_text()
        #         aaa = ps.nth(2).inner_text()
        #         bbb = ps.nth(3).inner_text()
        #         self.stdout.write(f"[{i+1}] {title} | {subtitle} | {aaa} | {bbb}")

        #     # アクセス過多防止
        #     if i < max_items - 1:
        #         sleep_time = random.uniform(8, 12)
        #         self.stdout.write(f"  → {sleep_time:.2f} 秒スリープ中...")
        #         time.sleep(sleep_time)

    def handle(self, *args, **options):
        # target_path = options["talent_path"]
        # max_items = options["max"]

        # csv_path = "./target_talents.csv"
        csv_path = Path(__file__).resolve().with_name("target_talents.csv")
        ids = extract_talent_ids(csv_path)

        for talent_id in ids:
            list_url = f"https://tver.jp/talents/{talent_id}/episodes"

            self.stdout.write(self.style.SUCCESS(f"アクセス中: {list_url}"))

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context()

                # 軽量化のため画像・CSS・フォントを除外
                context.route("**/*", lambda route, request: (
                    route.abort() if request.resource_type in ["image", "stylesheet", "font"] else route.continue_()
                ))

                page = context.new_page()
                try:
                    page.goto(list_url, timeout=15000)
                    page.wait_for_timeout(10000)
            #         # page.wait_for_selector("a >> p:nth-of-type(2)", timeout=10000)
                except PlaywrightTimeoutError:
                    self.stderr.write("一覧ページの読み込みに失敗しました。")
                    browser.close()
                    return

                # self._scrape_episodes(page, max_items)

                self._scrape_episodes(page)

                browser.close()
                self.stdout.write(self.style.SUCCESS("取得完了"))
