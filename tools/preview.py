#!/usr/bin/env python3
"""Fetch the rendered home page (as logged-in admin via loopback) into preview/index.html — the site is in maintenance mode."""
import base64, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import deploy
path = sys.argv[1] if len(sys.argv) > 1 else "/"; out = sys.argv[2] if len(sys.argv) > 2 else "index.html"
r = deploy.php("""
$c = wp_generate_auth_cookie(1, time()+300, 'logged_in');
$r = wp_remote_get(home_url('%PATH%'), ['timeout'=>30,'redirection'=>0,'cookies'=>[new WP_Http_Cookie(['name'=>LOGGED_IN_COOKIE,'value'=>$c])]]);
if (is_wp_error($r)) return $r->get_error_message();
return ['code'=>wp_remote_retrieve_response_code($r),'b64'=>base64_encode(wp_remote_retrieve_body($r))];""".replace("%PATH%", path))
html = base64.b64decode(r["b64"]); os.makedirs("preview", exist_ok=True)
open("preview/" + out, "wb").write(html); print(r["code"], len(html), "bytes")

# ── make the local preview self-contained (module scripts + WebGL textures need CORS) ──
import re, shutil, subprocess
txt = open("preview/" + out, encoding="utf-8").read()
js = os.path.join(os.path.dirname(__file__), "..", "theme", "assets", "js", "record-viewer.js")
shutil.copy(js, "preview/record-viewer.js")
txt = re.sub(r'https://7inchrare\.com/wp-content/themes/7inch/assets/js/record-viewer\.js\?ver=\d+', '/record-viewer.js', txt)
os.makedirs("preview/img", exist_ok=True)
def mirror(m):
    url = m.group(2); name = os.path.basename(url.split("?")[0])
    dst = os.path.join("preview/img", name)
    if not os.path.exists(dst): subprocess.run(["curl", "-s", "-o", dst, url])
    return m.group(1) + '="/img/' + name + '"'
txt = re.sub(r'(data-(?:front|back|label-a|label-b))="(https://[^"]+)"', mirror, txt)
open("preview/" + out, "w", encoding="utf-8").write(txt)
