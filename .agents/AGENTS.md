# Project Rules

- 今後の Git コミットメッセージはすべて日本語で記述すること (例: `feat: 〇〇機能の追加`, `fix: 〇〇の修正`, `docs: 〇〇の更新`)
- 指定がない限り日本語で応答すること
- すべての `<img>` タグにはパフォーマンスと非同期非ブロック描画のため `loading="lazy"` と `decoding="async"` 属性を付与すること
- 動物画像はすべて軽量な WebP フォーマット (`.webp`) を使用し、`species_*.json` 内の参照画像パスも `.webp` に統一すること (新規作成画像も WebP に変換して配備する)
- `species_*.json` のデータ構造設計：
  - 動物・昆虫・魚類（`mammals`, `birds`, `reptiles` 等）: `目 (Category)` ➔ `科 (Family)` ➔ `種 (Species)`
  - 農作物（`vegetables`）: `科または菌類生態 (Category)` ➔ `属または科 (Family)` ➔ `種 (Species)`（※農学・栽培・連作視点）
