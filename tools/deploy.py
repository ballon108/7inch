#!/usr/bin/env python3
"""Deploy the 7inch theme + home page to 7inchrare.com via the Novamira CLI.
usage: deploy.py media | theme | page | all"""
import base64, json, os, re, subprocess, sys, tempfile

SITE = "7inchrare.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "https://test.7inchrare.com/"

def php(code):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"code": code}, f)
    r = subprocess.run(["novamira", "--site", SITE, "run", "novamira/execute-php", "--input", "@" + f.name, "--yes", "--json"],
                       capture_output=True, text=True)
    os.unlink(f.name)
    out = json.loads(r.stdout)
    if not out.get("ok"):
        raise SystemExit(f"novamira error: {out}")
    d = out["data"]
    if not d.get("success"):
        raise SystemExit(f"php failed: {d}")
    if d.get("errors"):
        print("php notices:", d["errors"][:3])
    return d.get("return_value")

ALL = [("lr", n) for n in (1, 2, 3)] + [("mp", n) for n in range(1, 10)]

def media_keys():
    keys = {"mplogo": "assets/mp-logo.png"}
    for sr, n in ALL:
        k = f"{sr}{n}"
        keys[f"{k}A"] = f"assets/{k}A.jpg"; keys[f"{k}B"] = f"assets/{k}B.jpg"
        keys[f"{k}a"] = f"audio/{k}a.mp3"; keys[f"{k}b"] = f"audio/{k}b.mp3"
        if sr == "lr":
            keys[f"{k}Fs"] = f"assets/{k}Fs.jpg"; keys[f"{k}F"] = f"assets/{k}F.jpg"; keys[f"{k}Bk"] = f"assets/{k}Bk.jpg"
        else:
            keys[f"{k}s"] = f"assets/{k}s.jpg"
    return keys

def media():
    keys = media_keys(); items = list(keys.items()); m = {}
    for i in range(0, len(items), 6):
        batch = dict(items[i:i + 6])
        code = f"""
require_once ABSPATH.'wp-admin/includes/file.php'; require_once ABSPATH.'wp-admin/includes/media.php'; require_once ABSPATH.'wp-admin/includes/image.php';
$keys = json_decode({json.dumps(json.dumps(batch))}, true); $src = {json.dumps(SRC)}; $map = get_option('_7inch_media_map', []);
foreach ($keys as $k => $file) {{
  $ex = get_posts(['post_type'=>'attachment','post_status'=>'inherit','meta_key'=>'_7inch_key','meta_value'=>$k,'numberposts'=>1]);
  if ($ex) {{ $map[$k] = [$ex[0]->ID, wp_get_attachment_url($ex[0]->ID)]; continue; }}
  $tmp = download_url($src.$file, 120);
  if (is_wp_error($tmp)) {{ $map[$k] = 'ERR '.$tmp->get_error_message(); continue; }}
  $id = media_handle_sideload(['name'=>basename($file),'tmp_name'=>$tmp], 0, null, ['post_title'=>pathinfo($file, PATHINFO_FILENAME)]);
  if (is_wp_error($id)) {{ @unlink($tmp); $map[$k] = 'ERR '.$id->get_error_message(); continue; }}
  update_post_meta($id, '_7inch_key', $k);
  $map[$k] = [$id, wp_get_attachment_url($id)];
}}
update_option('_7inch_media_map', $map, false);
return $map;"""
        m = php(code)
    bad = {k: v for k, v in m.items() if isinstance(v, str)}
    print(f"media: {len(m) - len(bad)} ok, {len(bad)} failed", bad or "")
    return m

def theme():
    files = {}
    base = os.path.join(ROOT, "theme")
    for dp, _, fn in os.walk(base):
        for f in fn:
            p = os.path.join(dp, f); rel = os.path.relpath(p, base)
            files[rel] = base64.b64encode(open(p, "rb").read()).decode()
    code = f"""
$dir = get_theme_root().'/7inch'; wp_mkdir_p($dir);
$files = json_decode({json.dumps(json.dumps(files))}, true); $n = 0;
foreach ($files as $rel => $b64) {{ $p = $dir.'/'.$rel; wp_mkdir_p(dirname($p)); file_put_contents($p, base64_decode($b64)); $n++; }}
$rm = 0; $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS), RecursiveIteratorIterator::CHILD_FIRST);
foreach ($it as $f) {{ $rel = ltrim(substr($f->getPathname(), strlen($dir)), '/'); if ($f->isFile() && !isset($files[$rel])) {{ unlink($f->getPathname()); $rm++; }} elseif ($f->isDir()) {{ @rmdir($f->getPathname()); }} }}
wp_clean_themes_cache(); $t = wp_get_theme('7inch');
return ['written'=>$n, 'removed'=>$rm, 'exists'=>$t->exists(), 'errors'=>$t->errors() ? $t->errors()->get_error_messages() : null, 'parent'=>$t->parent() ? $t->parent()->get_stylesheet() : null];"""
    print("theme:", php(code))

def activate():
    print("activate:", php("switch_theme('7inch'); return get_stylesheet();"))


SERIES = [
 {"slug":"my-philosophy","name":"My Philosophy","accent":"mp","order":1,"eyebrow":"Series 01 · 90s Hip Hop & R&B","blurb":"Known and lesser-known classics, one episode at a time. Small numbered runs.","lead":'Two sides of 90s Hip Hop & R&B, re-edited and pressed on 7".',"cta":"Explore My Philosophy","logo":"mplogo","bg":None,
  "story_h":"The philosophy behind it","story_t":'Every episode pairs two songs that belong together: well-known classics and cuts only diggers carry in their record bag, as a limited 7" with its own label colour.'},
 {"slug":"lowrider-anthems","name":"Lowrider Anthems","accent":"lr","order":2,"eyebrow":"Series 02 · West Coast / G-Funk","blurb":"West Coast and G-Funk only, re-edited for the boulevard. Full-colour picture sleeves.","lead":'Two West Coast classics, re-edited for the boulevard and cut to 7".',"cta":"Explore Lowrider Anthems","logo":None,"bg":"lr2Fs",
  "story_h":"Built for Sunday cruising","story_t":"LOWRIDER ANTHEMS is the West Coast side of 7inch.rare: G-Funk and West Coast Hip Hop only, the soundtrack of chrome, hydraulics and slow rides down palm-lined streets."},
]
LR, MPE, MPR = "Lowrider Edit", "My PhiloSophy Edit", "Remastered Intro Edit"
# series, n, status, A, B, noteA, noteB, edition, year, hero-order
RELEASES = [
 ("lr",3,"pre","Hit Em Up","Real Muthaphuckkin G's",LR,LR,400,2026,3),("lr",2,"in","So Many Tears","Let's Play House",LR,LR,400,2026,1),("lr",1,"in","Fuck Wit Dre","Let Me Ride",LR,LR,400,2026,0),
 ("mp",9,"pre","Fu-Gee-La","Music Evolution (DJ Premier Remix)",MPE,MPE,400,2026,4),("mp",8,"in","Step Into A World","This One",MPE,MPE,400,2026,2),("mp",7,"in","Ten Crack Commandments","Money Power Respect",MPR,MPR,300,2026,0),
 ("mp",6,"in","You Know My Steez","Summertime",MPR,MPR,300,2026,0),("mp",5,"in","Winter Warz","ATLiens",MPE,MPE,300,2025,0),("mp",4,"in","If I Ruled the World (Imagine That)","I'll Be There For You (Puff Daddy Mix)",MPE,MPE,300,2025,0),
 ("mp",3,"in","Groupies","Dead Presidents II","","",100,2025,0),("mp",2,"out","U.N.I.T.Y.","The Doo-Bop Song","","",300,2025,0),("mp",1,"in","No Love","Rock & Comeen","Dubplate","Remix",300,2025,0)]

def seed():
    m = php("return get_option('_7inch_media_map');")
    def mid(k): return m[k][0] if k in m and not isinstance(m[k], str) else 0
    series = [dict(x, logo_id=mid(x["logo"]) if x["logo"] else 0, bg_id=mid(x["bg"]) if x["bg"] else 0) for x in SERIES]
    rel = []
    for i, (s, n, st, a, b, na, nb, ed, yr, fo) in enumerate(RELEASES):
        k = f"{s}{n}"
        rel.append({"series": "my-philosophy" if s == "mp" else "lowrider-anthems", "title": f"{'Lowrider Anthems Chapter' if s=='lr' else 'My Philosophy Episode'} {n}",
            "slug": f"{s}-{n:02d}", "sku": f"{s.upper()}-{n:02d}", "order": i + 1, "status": st, "a": a, "b": b, "na": na, "nb": nb, "ed": ed, "year": yr, "fo": fo,
            "price": "26.99" if s == "lr" else "19.99", "thumb": mid(f"{k}Fs") if s == "lr" else mid(f"{k}s"),
            "front": mid(f"{k}F") if s == "lr" else 0, "back": mid(f"{k}Bk") if s == "lr" else 0, "la": mid(f"{k}A"), "lb": mid(f"{k}B"), "aa": mid(f"{k}a"), "ab": mid(f"{k}b")})
    code = f"""
$series = json_decode({json.dumps(json.dumps(series))}, true); $rel = json_decode({json.dumps(json.dumps(rel))}, true); $log = [];
if (!function_exists('update_field') || !function_exists('wc_get_product')) return 'SCF/WooCommerce not loaded';
// retire the interim "release" CPT + "series" taxonomy
foreach (get_posts(['post_type'=>'release','post_status'=>'any','numberposts'=>-1]) as $p) wp_delete_post($p->ID, true);
if (!taxonomy_exists('series')) register_taxonomy('series', 'release');
foreach (get_terms(['taxonomy'=>'series','hide_empty'=>false]) as $t) wp_delete_term($t->term_id, 'series');
foreach ($series as $x) {{
  $t = term_exists($x['slug'], 'product_cat'); if (!$t) $t = wp_insert_term($x['name'], 'product_cat', ['slug'=>$x['slug']]);
  if (is_wp_error($t)) {{ $log[] = $t->get_error_message(); continue; }}
  $ref = 'product_cat_'.(is_array($t) ? $t['term_id'] : $t);
  foreach (['accent'=>'accent','order'=>'panel_order','eyebrow'=>'eyebrow','blurb'=>'blurb','lead'=>'hero_lead','cta'=>'cta','bg_id'=>'panel_image','logo_id'=>'panel_logo','story_h'=>'story_heading','story_t'=>'story_text'] as $k=>$f) {{ update_field($f, $x[$k] ?: '', $ref); }}
}}
$stock = ['in'=>'instock','out'=>'outofstock','pre'=>'onbackorder'];
foreach ($rel as $r) {{
  $id = wc_get_product_id_by_sku($r['sku']);
  $p = $id ? wc_get_product($id) : new WC_Product_Simple();
  $p->set_name($r['title']); $p->set_slug($r['slug']); $p->set_sku($r['sku']); $p->set_status('publish'); $p->set_catalog_visibility('visible');
  $p->set_regular_price($r['price']); $p->set_manage_stock(false); $p->set_stock_status($stock[$r['status']]); $p->set_menu_order($r['order']);
  $p->set_sold_individually(false); $p->set_virtual(false);
  if ($r['thumb']) $p->set_image_id($r['thumb']);
  $term = get_term_by('slug', $r['series'], 'product_cat'); $p->set_category_ids([$term->term_id]);
  $id = $p->save();
  update_field('featured', $r['fo'] ? 1 : 0, $id); update_field('hero_order', $r['fo'] ?: '', $id);
  foreach (['front'=>'cover_front','back'=>'cover_back','la'=>'label_a','lb'=>'label_b','aa'=>'audio_a','ab'=>'audio_b'] as $k=>$f) update_field($f, $r[$k] ?: '', $id);
  update_field('side_a', $r['a'], $id); update_field('side_b', $r['b'], $id); update_field('note_a', $r['na'], $id); update_field('note_b', $r['nb'], $id);
  update_field('edition', $r['ed'], $id); update_field('year', $r['year'], $id); update_field('cat_no', $r['sku'], $id); update_field('pressed_in', 'Germany', $id);
}}
$u = get_term_by('slug', 'uncategorized', 'product_cat');
return ['products'=>wp_count_posts('product')->publish, 'cats'=>wp_count_terms(['taxonomy'=>'product_cat','hide_empty'=>false]), 'log'=>$log];"""
    print("seed:", php(code))

def page(m=None):
    m = m or php("return get_option('_7inch_media_map');")
    html = open(os.path.join(ROOT, "content", "home.html")).read()
    html = re.sub(r"\{\{id:(\w+)\}\}", lambda x: str(m[x.group(1)][0]), html)
    html = re.sub(r"\{\{url:(\w+)\}\}", lambda x: m[x.group(1)][1], html)
    b64 = base64.b64encode(html.encode()).decode()
    code = f"""
$c = base64_decode({json.dumps(b64)});
$ex = get_page_by_path('home');
$arr = ['post_title'=>'Home','post_name'=>'home','post_content'=>wp_slash($c),'post_status'=>'publish','post_type'=>'page'];
if ($ex) {{ $arr['ID'] = $ex->ID; $id = wp_update_post($arr, true); }} else {{ $id = wp_insert_post($arr, true); }}
if (is_wp_error($id)) return $id->get_error_message();
update_option('show_on_front','page'); update_option('page_on_front',$id);
return ['id'=>$id,'url'=>get_permalink($id),'blocks'=>count(array_filter(parse_blocks($c), fn($b)=>$b['blockName']))];"""
    print("page:", php(code))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd == "media": media()
    elif cmd == "theme": theme()
    elif cmd == "activate": activate()
    elif cmd == "seed": seed()
    elif cmd == "page": page()
    elif cmd == "all": m = media(); theme(); seed(); page(m); activate()
