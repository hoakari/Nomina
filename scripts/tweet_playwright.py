import os
import sys
import json
import time
import random
import argparse
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Safe encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    except Exception:
        pass

load_dotenv()

X_USERNAME = os.getenv("X_USERNAME")
X_PASSWORD = os.getenv("X_PASSWORD")
X_EMAIL = os.getenv("X_EMAIL")
APP_URL = os.getenv("APP_URL", "https://nomina-app.netlify.app")

SPECIES_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "lib", "data", "species.json")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")

HASHTAG_POOL = [
    "知育アプリ",
    "個人開発",
    "どうぶつずかん",
    "動物図鑑",
    "親子時間",
    "子育て"
]

def load_species():
    with open(SPECIES_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    species_list = []
    for cat in data.get("categories", []):
        for fam in cat.get("families", []):
            for sp in fam.get("species", []):
                species_list.append(sp)
    return species_list

def generate_tweet_content(animal_id: str = None):
    species_list = load_species()
    valid_animals = []
    for sp in species_list:
        img_rel_path = sp.get("image", "").lstrip("/")
        if img_rel_path:
            img_full_path = os.path.join(STATIC_DIR, img_rel_path)
            if os.path.exists(img_full_path):
                sp["_full_img_path"] = img_full_path
                valid_animals.append(sp)

    if not valid_animals:
        print("❌ エラー: 利用可能な画像付き動物が見つかりませんでした。")
        sys.exit(1)

    if animal_id:
        animal = next((sp for sp in valid_animals if sp.get("id") == animal_id), None)
        if not animal:
            print(f"❌ エラー: 動物ID '{animal_id}' (画像あり) が見つかりませんでした。")
            sys.exit(1)
    else:
        animal = random.choice(valid_animals)

    name_common = animal.get("name_common")
    name_en = animal.get("name_en", "")
    desc = animal.get("description_note", "")
    img_full_path = animal.get("_full_img_path")

    selected_tags = random.sample(HASHTAG_POOL, min(4, len(HASHTAG_POOL)))
    animal_tag = name_common.replace(" ", "").replace("（", "").replace("）", "")
    selected_tags.append(animal_tag)
    hashtags_str = " ".join([f"#{tag}" for tag in selected_tags])

    text = f"""【{name_common}（{name_en}）】
{desc}

{APP_URL}

{hashtags_str}"""

    return animal, text, img_full_path

def post_tweet_with_playwright(animal_id: str = None, dry_run: bool = False, headless: bool = True):
    animal, text, img_path = generate_tweet_content(animal_id)
    
    print(f"🐾 対象動物: {animal.get('name_common')} (ID: {animal.get('id')})")
    print("\n================【投稿プレビュー】================")
    print(text)
    print("--------------------------------------------------")
    print(f"📷 添付画像: {img_path}")
    print("==================================================\n")

    if dry_run:
        print("💡 [ドライランモード] 投稿処理を行わずに終了します。")
        return

    if not X_USERNAME or not X_PASSWORD:
        print("❌ エラー: .env / Secrets に X_USERNAME および X_PASSWORD が設定されていません。")
        sys.exit(1)

    print("🌐 Playwright でブラウザを起動しています...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        try:
            print("🔑 X (Twitter) ログイン画面にアクセス中...")
            page.goto("https://x.com/i/flow/login", wait_until="networkidle")
            page.wait_for_timeout(3000)

            # 1. ユーザー名入力
            username_input = page.wait_for_selector('input[autocomplete="username"], input[name="text"]', timeout=15000)
            username_input.fill(X_USERNAME)
            page.keyboard.press("Enter")
            page.wait_for_timeout(2000)

            # 電話番号/メール確認が求められた場合
            if page.locator('input[data-testid="ocfEnterTextTextInput"]').is_visible():
                print("📧 追加のメールアドレス認証が要求されました。入力中...")
                if X_EMAIL:
                    page.locator('input[data-testid="ocfEnterTextTextInput"]').fill(X_EMAIL)
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(2000)
                else:
                    print("⚠️ X_EMAIL が設定されていません。")

            # 2. パスワード入力
            print("🔐 パスワードを入力中...")
            password_input = page.wait_for_selector('input[name="password"]', timeout=15000)
            password_input.fill(X_PASSWORD)
            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)

            print("ログイン完了。ツイート作成画面へ遷移中...")
            page.goto("https://x.com/compose/post", wait_until="networkidle")
            page.wait_for_timeout(3000)

            # 3. ツイート本文の入力
            print("✍️ ツイート本文を入力中...")
            tweet_box = page.wait_for_selector('div[data-testid="tweetTextarea_0"]', timeout=15000)
            tweet_box.click()
            page.keyboard.insert_text(text)
            page.wait_for_timeout(1000)

            # 4. 画像の添付
            if img_path and os.path.exists(img_path):
                print(f"📷 画像を添付中: {img_path}")
                file_input = page.locator('input[data-testid="fileInput"]')
                file_input.set_input_files(img_path)
                page.wait_for_timeout(3000)

            # 5. 「ポストする」ボタンのクリック
            print("🚀 『ポストする』ボタンをクリック中...")
            post_button = page.wait_for_selector('button[data-testid="tweetButton"]', timeout=10000)
            post_button.click()
            page.wait_for_timeout(5000)

            print("🎉 Playwright による全自動投稿が正常に完了しました！")

        except Exception as e:
            print(f"❌ 投稿処理中にエラーが発生しました: {e}")
            page.screenshot(path="error_screenshot.png")
            print("📸 エラー時のスクリーンショットを error_screenshot.png に保存しました。")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nomina! Playwright 全自動X投稿スクリプト")
    parser.add_argument("--id", help="特定動物のID (例: wildebeest, quoll)", default=None)
    parser.add_argument("--dry-run", "-d", action="store_true", help="実際に投稿せずプレビューのみ表示")
    parser.add_argument("--no-headless", action="store_true", help="ブラウザ画面を表示して実行 (ローカルデバッグ用)")

    args = parser.parse_args()
    post_tweet_with_playwright(args.id, dry_run=args.dry_run, headless=not args.no_headless)
