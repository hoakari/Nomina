import os
import sys
import traceback
import argparse
from dotenv import load_dotenv
import tweepy

# Safe encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    except Exception:
        pass

# Load environment variables
load_dotenv()

API_KEY = os.getenv("X_API_KEY")
API_KEY_SECRET = os.getenv("X_API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")
REFRESH_TOKEN = os.getenv("X_REFRESH_TOKEN")
CLIENT_ID = os.getenv("X_CLIENT_ID")
CLIENT_SECRET = os.getenv("X_CLIENT_SECRET")

def get_twitter_clients():
    api_v1 = None
    client_v2 = None

    if API_KEY and API_KEY_SECRET and ACCESS_TOKEN and ACCESS_TOKEN_SECRET:
        print("🔑 OAuth 1.0a 認証キーを使用して接続します。")
        auth = tweepy.OAuth1UserHandler(
            API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
        )
        api_v1 = tweepy.API(auth)
        client_v2 = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_KEY_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET,
        )
    elif ACCESS_TOKEN:
        print("🔑 OAuth 2.0 アクセストークンを使用して接続します。")
        client_v2 = tweepy.Client(access_token=ACCESS_TOKEN)
    else:
        print("❌ エラー: .env / Secrets に有効な認証キーが設定されていません。")
        sys.exit(1)

    return api_v1, client_v2

def post_tweet(text: str, image_path: str = None, dry_run: bool = False, confirm: bool = True):
    print("\n================【投稿プレビュー】================")
    print(text)
    print("--------------------------------------------------")
    if image_path:
        print(f"📷 添付画像: {image_path} ({'存在します' if os.path.exists(image_path) else '❌ ファイルなし'})")
    else:
        print("📷 添付画像: なし")
    print("==================================================\n")

    if dry_run:
        print("💡 [ドライランモード] 投稿処理を行わずに終了します。")
        return None

    if confirm:
        try:
            answer = input("❓ 上記の内容で実際にX(Twitter)へ投稿しますか？ (y/N): ").strip().lower()
        except Exception:
            answer = 'n'
        if answer != 'y':
            print("🚫 投稿をキャンセルしました。")
            return None

    api_v1, client_v2 = get_twitter_clients()

    media_ids = []
    if image_path and os.path.exists(image_path):
        if api_v1:
            print(f"📷 画像をアップロード中: {image_path}")
            try:
                media = api_v1.media_upload(filename=image_path)
                media_ids.append(media.media_id)
                print(f"✅ 画像アップロード完了 (Media ID: {media.media_id})")
            except Exception as e:
                print(f"❌ 画像アップロード失敗詳細: {e}")
                traceback.print_exc()
                # If image upload fails, try text only post or raise
                raise e
        else:
            print("⚠️ 注意: OAuth 1.0a キーが揃っていないため画像なしで投稿を試みます。")

    print(f"🚀 ツイート送信中...")
    try:
        if media_ids:
            response = client_v2.create_tweet(text=text, media_ids=media_ids)
        else:
            response = client_v2.create_tweet(text=text)

        tweet_id = response.data['id']
        print(f"🎉 ツイート成功！ (Tweet ID: {tweet_id})")
        print(f"🔗 https://x.com/user/status/{tweet_id}")
        return response.data
    except Exception as e:
        print(f"❌ ツイート投稿失敗詳細: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="X (Twitter) 投稿スクリプト")
    parser.add_argument("text", help="ツイート本文")
    parser.add_argument("--image", "-i", help="添付画像ファイルパス", default=None)
    parser.add_argument("--dry-run", "-d", action="store_true", help="実際に投稿せずプレビューのみ表示")
    parser.add_argument("--yes", "-y", action="store_true", help="確認プロンプトをスキップして投稿")

    args = parser.parse_args()
    post_tweet(args.text, args.image, dry_run=args.dry_run, confirm=not args.yes)
