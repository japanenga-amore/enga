# 演歌播放器（ENGA）

家用的演歌影片播放器。2026-10-25 完成，iPhone、Android 測試通過。

- 網址：https://japanenga-amore.github.io/enga/
- 完整備忘錄：https://claude.ai/artifact/H4e9zqadnVTvxeK4N9dex8

## 功能

- 歡迎畫面「こんにちは」→ 密碼畫面（每次打開都要輸入；離開超過 1 分鐘回來也要）→ 16 首歌單
- 有人聲（右聲道）／純伴奏（左聲道）切換，選定的聲道從兩耳播出
- 升 Key／降 Key（±6 個半音，速度不變）
- 播放／暫停、重複、全螢幕三顆大按鈕，進度條可拖拉
- 米白底色、大字，可「加入主畫面」當 App 使用

## 檔案

| 檔案 | 用途 |
| --- | --- |
| `index.html` | 整個播放器：畫面、歌名、密碼、聲道與按鈕 |
| `pitch-worklet.js` | 升降 Key 的聲音處理（舊手機會自動改用 `index.html` 內的備用方式） |
| `manifest.webmanifest`、`icons/` | 加入主畫面用的名稱與 ENGA 圖示 |

## 影片

- 放在 Cloudflare R2 的 `enga` 倉庫：`https://pub-a8f97bad0e354c668c1779fd893493fc.r2.dev/AVSEQ01.mov` ～ `AVSEQ16.mov`
- Mac 內建「編碼所選的影片檔案」壓成 480p（H.264 + AAC 立體聲）
- R2 必須設定 CORS，允許 `https://japanenga-amore.github.io` 使用 GET、HEAD，否則切換聲道會沒有聲音

## 歌單

| # | 歌名 | # | 歌名 |
| --- | --- | --- | --- |
| 1 | 紅の舟唄 | 9 | 雪國 |
| 2 | 北の旅人 | 10 | 昭和ひとり旅 |
| 3 | 大阪恋しずく | 11 | 雨の空港 |
| 4 | 思案橋ブルース | 12 | ひとり上手 |
| 5 | 黒髪 | 13 | あかね空 |
| 6 | 風姿花傳 | 14 | 好きになった人 |
| 7 | ひとりごと | 15 | 涙をありがとう |
| 8 | 秋霖 | 16 | 達者でナ |

## 修改方式

- 歌名在 `index.html` 的 `SONGS` 清單；影片網址在 `VIDEO_BASE`
- 密碼只存 SHA-256 指紋（`PASS_HASH`，內容為 `enga-salt-` + 密碼），要改密碼需重新計算
- 推送到 `main` 後，GitHub Pages 約 1–2 分鐘自動更新
