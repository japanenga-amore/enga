"""產生 1～10 號歌單網址。

用法：python3 tools/build_lists.py
每組的設定寫在 tools/lists.json：
  title     歌單名稱（顯示在歌單上方與桌面圖示名稱）
  songs     歌名清單（第 1 首對應影片 AVSEQ01.mov，以此類推）
  pass_hash 密碼指紋 = sha256("enga-salt-" + 密碼)
影片放在 R2 倉庫的資料夾「<編號>/」，例如 3/AVSEQ01.mov。
根目錄 index.html 是原本的歌單，也是所有新網址的範本。
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
R2 = "https://pub-a8f97bad0e354c668c1779fd893493fc.r2.dev/"
tpl = (ROOT / "index.html").read_text(encoding="utf-8")
lists = json.loads((ROOT / "tools" / "lists.json").read_text(encoding="utf-8"))

def sub(s, old, new, count=1):
    assert s.count(old) >= count, f"找不到：{old[:50]}"
    return s.replace(old, new)

for key, cfg in lists.items():
    s = tpl
    title = cfg["title"]
    s = sub(s, "<title>演歌</title>", f"<title>{title}</title>")
    s = sub(s, 'name="apple-mobile-web-app-title" content="演歌"', f'name="apple-mobile-web-app-title" content="{title}"')
    s = sub(s, "<h2>演歌</h2>", f"<h2>{title}</h2>")
    s = s.replace('href="icons/', 'href="../icons/').replace('src="icons/', 'src="../icons/')
    s = sub(s, 'addModule("pitch-worklet.js")', 'addModule("../pitch-worklet.js")')
    s = sub(s, f'|| "{R2}";', f'|| "{R2}{key}/";')
    s = re.sub(r"const SONGS = \[.*?\];", "const SONGS = " + json.dumps(cfg["songs"], ensure_ascii=False) + ";", s, count=1, flags=re.S)
    s = re.sub(r'const PASS_HASH = "[0-9a-f]{64}";', f'const PASS_HASH = "{cfg["pass_hash"]}";', s, count=1)
    out = ROOT / key
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(s, encoding="utf-8")
    manifest = {
        "name": title, "short_name": title, "start_url": "./", "scope": "./",
        "display": "standalone", "orientation": "any",
        "background_color": "#FAF6EF", "theme_color": "#FAF6EF", "lang": "zh-Hant",
        "icons": [
            {"src": "../icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "../icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "../icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
    }
    (out / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(key, title, len(cfg["songs"]), "首")
