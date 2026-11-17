#!/usr/bin/env python3
"""Generates content/home.html (Gutenberg block markup) for the 7inch.rare home page.
Image placeholders {{id:KEY}} / {{url:KEY}} are resolved at deploy time to Media Library attachments."""
import json, html

def attrs(d):
    return (" " + json.dumps(d, ensure_ascii=False, separators=(",", ":"))) if d else ""

def esc(t):
    return html.escape(t, quote=False)

def group(cls, inner, tag=None, anchor=None, layout=None, extra=None):
    a = {"className": cls} if cls else {}
    if tag: a["tagName"] = tag
    if anchor: a["anchor"] = anchor
    if layout: a["layout"] = layout
    if extra: a.update(extra)
    t = tag or "div"
    idattr = f' id="{anchor}"' if anchor else ""
    dattr = ""
    if extra and "_data" in extra: pass
    return (f"<!-- wp:group{attrs(a)} -->\n<{t}{idattr} class=\"wp-block-group{(' ' + cls) if cls else ''}\">{inner}</{t}>\n<!-- /wp:group -->\n")

def para(text, cls=None, color=None):
    a = {}
    c = []
    if cls: a["className"] = cls; c.append(cls)
    if color: a["textColor"] = color; c += [f"has-{color}-color", "has-text-color"]
    cl = f' class="{" ".join(c)}"' if c else ""
    return f"<!-- wp:paragraph{attrs(a)} -->\n<p{cl}>{text}</p>\n<!-- /wp:paragraph -->\n"

def heading(text, level=2, cls=None):
    a = {}
    if level != 2: a["level"] = level
    c = ["wp-block-heading"]
    if cls: a["className"] = cls; c.append(cls)
    return f"<!-- wp:heading{attrs(a)} -->\n<h{level} class=\"{' '.join(c)}\">{text}</h{level}>\n<!-- /wp:heading -->\n"

def image(key, alt, cls=None, size="full"):
    a = {"id": "{{id:%s}}" % key, "sizeSlug": size, "linkDestination": "none"}
    c = [f"wp-block-image", f"size-{size}"]
    if cls: a["className"] = cls; c.append(cls)
    # id placeholder is numeric after resolve; keep it unquoted via marker
    aj = attrs(a).replace('"{{id:%s}}"' % key, "{{id:%s}}" % key)
    return (f"<!-- wp:image{aj} -->\n<figure class=\"{' '.join(c)}\"><img src=\"{{{{url:{key}}}}}\" alt=\"{esc(alt)}\" class=\"wp-image-{{{{id:{key}}}}}\"/></figure>\n<!-- /wp:image -->\n")

def button(label, href, kind):
    return (f"<!-- wp:button{attrs({'className': kind})} -->\n<div class=\"wp-block-button {kind}\"><a class=\"wp-block-button__link wp-element-button\" href=\"{href}\">{label}</a></div>\n<!-- /wp:button -->\n")

def buttons(items, cls="ctas"):
    return (f"<!-- wp:buttons{attrs({'className': cls})} -->\n<div class=\"wp-block-buttons {cls}\">{''.join(items)}</div>\n<!-- /wp:buttons -->\n")

# ── data ───────────────────────────────────────────────────────────
SER = {"mp": "My Philosophy", "lr": "Lowrider Anthems"}
LEAD = {"mp": 'Two sides of 90s Hip Hop &amp; R&amp;B, re-edited and pressed on 7".',
        "lr": 'Two West Coast classics, re-edited for the boulevard and cut to 7".'}
PRELEAD = "Pre-orders are open. Secure your copy before the run is pressed."

HERO = [  # id, series, n, title, status, A, B
    ("lr", 2, "Lowrider Anthems Chapter 2", "in", "So Many Tears", "Let's Play House"),
    ("mp", 8, "My Philosophy Episode 8", "in", "Step Into A World", "This One"),
    ("lr", 3, "Lowrider Anthems Chapter 3", "pre", "Hit Em Up", "Real Muthaphuckkin G's"),
    ("mp", 9, "My Philosophy Episode 9", "pre", "Fu-Gee-La", "Music Evolution (DJ Premier Remix)"),
]
CATALOGUE = [  # series, n, status
    ("lr", 3, "pre"), ("lr", 2, "in"), ("lr", 1, "in"),
    ("mp", 9, "pre"), ("mp", 8, "in"), ("mp", 7, "in"), ("mp", 6, "in"), ("mp", 5, "in"),
    ("mp", 4, "in"), ("mp", 3, "in"), ("mp", 2, "out"), ("mp", 1, "in"),
]
STATUS = {"in": "In stock", "out": "Sold out", "pre": "Pre-order"}

def title(s, n): return f"{SER[s]} {'Chapter' if s == 'lr' else 'Episode'} {n}"

# ── hero ───────────────────────────────────────────────────────────
def hero_slide(s, n, ttl, st, a, b):
    pre = st == "pre"
    badge = f"{'Pre-order' if pre else 'Out now'} · {SER[s]}"
    lead = (PRELEAD + " " if pre else "") + LEAD[s] + f" A: {esc(a)} · B: {esc(b)}"
    text = group("htext",
        para(badge, "badge", s) +
        heading(esc(ttl), 1) +
        para(lead, "lead") +
        buttons([button("Pre-order now" if pre else "View release", "#releases", "btn-fill"),
                 button("All releases", "#releases", "btn-ghost")]) +
        group("dots", ""))
    if s == "lr":
        art = group("disc", image(f"lr{n}A", "")) + image(f"lr{n}F", f"{ttl} cover", "sleeve")
    else:
        art = group("disc", image(f"mp{n}A", f"{ttl} label"))
    scene = group("scene " + s,
        (para("Pre-order", "pre") if pre else "") +
        group("float", art) + group("pod", ""))
    return group("hero-slide " + s, text + scene, extra={})

def hero():
    slides = "".join(hero_slide(*h) for h in HERO)
    return group("hero", group("wrap", group("hero-slides", slides)), tag="section", anchor="home")

# ── series ─────────────────────────────────────────────────────────
def series():
    mp = group("panel mp",
        image("mplogo", "MY PHILOSOPHY limited edition", "logo-big") +
        para("Series 01 · 90s Hip Hop &amp; R&amp;B", "eyebrow ep") +
        heading("My Philosophy", 3) +
        para("Known and lesser-known classics, one episode at a time. Small numbered runs.") +
        para("Explore My Philosophy", "go"))
    lr = group("panel lr",
        image("lr2Fs", "Lowrider Anthems Chapter 2 cover", "bgimg") +
        para("Series 02 · West Coast / G-Funk", "eyebrow el") +
        heading("Lowrider Anthems", 3) +
        para("West Coast and G-Funk only, re-edited for the boulevard. Full-colour picture sleeves.") +
        para("Explore Lowrider Anthems", "go"))
    head = group("head", group("", para("Two series", "eyebrow") + heading("Pick your side of the map.")))
    return group("band", group("wrap", head + group("series", mp + lr)), tag="section", anchor="series")

# ── catalogue ──────────────────────────────────────────────────────
def card(s, n, st):
    ttl = title(s, n)
    if s == "lr":
        art = group("art", image(f"lr{n}Fs", f"{ttl} cover", size="full"))
    else:
        art = group("art", group("v", image(f"mp{n}s", f"{ttl} label")))
    stcol = "mute" if st == "out" else s
    stcls = "st out" if st == "out" else "st"
    return group(f"card rel-{s}", art + para(SER[s], "eyebrow", s) + para(ttl, "ct") + para(STATUS[st], stcls, stcol))

def catalogue():
    filt = buttons([button("All", "#", "filter f-all is-active"),
                    button("My Philosophy", "#", "filter f-mp"),
                    button("Lowrider Anthems", "#", "filter f-lr")], "filters")
    head = group("head", group("", para("Catalogue", "eyebrow") + heading("All releases")) + filt)
    grid = group("grid", "".join(card(*c) for c in CATALOGUE))
    return group("band", group("wrap", head + grid), tag="section", anchor="releases")

# ── wholesale ──────────────────────────────────────────────────────
def trade():
    left = group("", para("For record shops &amp; distributors", "eyebrow") +
                 heading("Stock the series in your shop.") +
                 f'<!-- wp:paragraph {{"className":"lead","style":{{"spacing":{{"margin":{{"top":"var:preset|spacing|40"}}}}}}}} -->\n<p class="lead" style="margin-top:var(--wp--preset--spacing--40)">Wholesale price list, pre-order windows and shipping options on request. We ship worldwide; the buyer pays freight.</p>\n<!-- /wp:paragraph -->\n')
    nums = group("nums",
        group("num", para("50", "nb") + para("copies minimum for record shops", "nl")) +
        group("num", para("100", "nb") + para("copies minimum for distributors", "nl")))
    ctas = group("ctas-row",
        buttons([button("Request the wholesale list", "mailto:peet@7inchrare.com", "btn-fill")], "ctas") +
        para("peet@7inchrare.com", "mail"))
    return group("band", group("wrap trade", left + nums + ctas), tag="section", anchor="trade")


# ── SCF blocks ─────────────────────────────────────────────────────
import os
def scf_block(slug, group_file, overrides=None):
    g = json.load(open(os.path.join(os.path.dirname(__file__), "..", "theme", "acf-json", group_file)))
    data = {}
    for f in g["fields"]:
        if f["type"] == "repeater":
            rows = (overrides or {}).get(f["name"], [])
            data[f["name"]] = len(rows); data["_" + f["name"]] = f["key"]
            for i, row in enumerate(rows):
                for sf in f["sub_fields"]:
                    data[f"{f['name']}_{i}_{sf['name']}"] = row.get(sf["name"], "")
                    data[f"_{f['name']}_{i}_{sf['name']}"] = sf["key"]
        else:
            data[f["name"]] = (overrides or {}).get(f["name"], f.get("default_value", ""))
            data["_" + f["name"]] = f["key"]
    a = {"name": f"acf/{slug}", "data": data, "mode": "preview"}
    return f"<!-- wp:acf/{slug} {json.dumps(a, ensure_ascii=False, separators=(',', ':'))} /-->\n\n"

page = (scf_block("hero-carousel", "group_block_hero.json") +
        scf_block("series-panels", "group_block_series.json") +
        scf_block("release-catalogue", "group_block_catalogue.json") +
        scf_block("wholesale", "group_block_wholesale.json", {"stats": [
            {"number": "50", "label": "copies minimum for record shops"},
            {"number": "100", "label": "copies minimum for distributors"}]}))
open("content/home.html", "w").write(page)
print(len(page), "bytes")
