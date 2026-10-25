"""產生「唱歌錄音」試做版：/enga/test/
內容和原本 16 首歌單相同（同影片、同密碼），只是打開了錄音功能。
用法：python3 tools/build_test.py
"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
s = (ROOT / "index.html").read_text(encoding="utf-8")
s = s.replace('href="icons/', 'href="../icons/').replace('src="icons/', 'src="../icons/')
s = s.replace('addModule("pitch-worklet.js")', 'addModule("../pitch-worklet.js")')
flag = "const RECORD_ON = window.ENGA_RECORD_ON || false;"
assert flag in s
s = s.replace(flag, "const RECORD_ON = true;")
out = ROOT / "test"; out.mkdir(exist_ok=True)
(out / "index.html").write_text(s, encoding="utf-8")
m = (ROOT / "manifest.webmanifest").read_text(encoding="utf-8").replace('"icons/', '"../icons/')
(out / "manifest.webmanifest").write_text(m, encoding="utf-8")
print("test/index.html 已產生")
