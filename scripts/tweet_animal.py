import os
import sys
import json
import random
import argparse

# Safe encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    except Exception:
        pass

from tweet import post_tweet

SPECIES_JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "src", "lib", "data", "species.json")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")

# アプリのURL (環境変数 APP_URL があればそれを使い、無ければデフォルト)
APP_URL = os.getenv("APP_URL", "https://nomina-app.netlify.app")

# ハッシュタグリスト
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

def post_animal_tweet(animal_id: str = None, dry_run: bool = False, confirm: bool = True):
    species_list = load_species()
    
    # 画像が存在する動物のみにフィルタリング
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
    name_ja = animal.get("name_standard_ja", name_common)
    name_en = animal.get("name_en", "")
    desc = animal.get("description_note", "")
    img_full_path = animal.get("_full_img_path")

    # ハッシュタグリストからランダムに4つ選択
    selected_tags = random.sample(HASHTAG_POOL, min(4, len(HASHTAG_POOL)))
    # 動物名タグを追加
    animal_tag = name_common.replace(" ", "").replace("（", "").replace("）", "")
    selected_tags.append(animal_tag)
    
    hashtags_str = " ".join([f"#{tag}" for tag in selected_tags])

    # ツイート本文の生成（マスターの指定フォーマット）
    text = f"""【{name_common}（{name_en}）】
{desc}

{APP_URL}

{hashtags_str}"""

    print(f"🐾 対象動物: {name_common} (ID: {animal.get('id')})")
    post_tweet(text, img_full_path, dry_run=dry_run, confirm=confirm)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nomina! 毎日自動動物投稿スクリプト")
    parser.add_argument("--id", help="特定動物のID (例: wildebeest, quoll)", default=None)
    parser.add_argument("--dry-run", "-d", action="store_true", help="実際に投稿せずプレビューのみ表示")
    parser.add_argument("--yes", "-y", action="store_true", help="確認プロンプトをスキップして自動投稿 (定期実行用)")

    args = parser.parse_args()
    post_animal_tweet(args.id, dry_run=args.dry_run, confirm=not args.yes)
