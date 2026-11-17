#!/usr/bin/env python3
"""Generates theme/acf-json (SCF Local JSON): product + product_cat field groups and block field groups."""
import json, os
OUT = os.path.join(os.path.dirname(__file__), "..", "theme", "acf-json")
def w(name, data): open(os.path.join(OUT, name + ".json"), "w").write(json.dumps(data, indent=4, ensure_ascii=False))
def f(key, label, name, typ, **kw):
    d = {"key": "field_7i_" + key, "label": label, "name": name, "aria-label": "", "type": typ, "instructions": "", "required": 0, "conditional_logic": 0, "wrapper": {"width": "", "class": "", "id": ""}}
    d.update(kw); return d
def txt(key, label, name, default="", **kw): return f(key, label, name, "text", default_value=default, maxlength="", placeholder="", prepend="", append="", **kw)
def img(key, label, name, ins=""): return f(key, label, name, "image", instructions=ins, return_format="id", library="all", preview_size="medium", min_width=0, min_height=0, min_size=0, max_width=0, max_height=0, max_size=0, mime_types="")
def aud(key, label, name, ins=""): return f(key, label, name, "file", instructions=ins, return_format="id", library="all", min_size=0, max_size=0, mime_types="mp3,m4a,ogg,wav")
def num(key, label, name, default="", **kw): return f(key, label, name, "number", default_value=default, min="", max="", step=1, placeholder="", prepend="", append="", **kw)
def grp(key, title, fields, loc, order=0, pos="normal"):
    return {"key": "group_7i_" + key, "title": title, "fields": fields, "location": [[loc]], "menu_order": order, "position": pos, "style": "default", "label_placement": "top", "instruction_placement": "label", "hide_on_screen": "", "active": True, "description": "", "show_in_rest": 0}
def block_loc(n): return {"param": "block", "operator": "==", "value": "acf/" + n}

w("group_product", grp("product", "Release details", [
  f("p_featured", "Show in hero carousel", "featured", "true_false", message="", default_value=0, ui=1, ui_on_text="", ui_off_text=""),
  num("p_hero_order", "Hero order", "hero_order", instructions="Position in the hero carousel (1 = first).", conditional_logic=[[{"field": "field_7i_p_featured", "operator": "==", "value": "1"}]]),
  img("p_front", "Front sleeve", "cover_front", "Full-colour sleeve (Lowrider Anthems). Shown in the hero and the 3D viewer."),
  img("p_back", "Back sleeve", "cover_back", "Back of the sleeve (Lowrider Anthems), 3D viewer."),
  img("p_label_a", "Label — side A", "label_a"),
  img("p_label_b", "Label — side B", "label_b"),
  txt("p_side_a", "Side A — track", "side_a"), txt("p_note_a", "Side A — edit note", "note_a"), aud("p_audio_a", "Side A — preview", "audio_a"),
  txt("p_side_b", "Side B — track", "side_b"), txt("p_note_b", "Side B — edit note", "note_b"), aud("p_audio_b", "Side B — preview", "audio_b"),
  num("p_edition", "Edition (copies)", "edition"), num("p_year", "Year", "year"),
  txt("p_catno", "Cat. no.", "cat_no"), txt("p_made", "Pressed in", "pressed_in", "Germany"),
 ], {"param": "post_type", "operator": "==", "value": "product"}, pos="normal"))

w("group_series", grp("series", "Series details", [
  f("ser_accent", "Accent colour", "accent", "select", choices={"mp": "Orange (My Philosophy)", "lr": "Gold (Lowrider Anthems)"}, default_value="mp", return_format="value", multiple=0, allow_null=0, ui=0, ajax=0, placeholder=""),
  num("ser_order", "Order", "panel_order", 1),
  txt("ser_eyebrow", "Eyebrow", "eyebrow", instructions="e.g. Series 01 · 90s Hip Hop & R&B"),
  f("ser_blurb", "Panel text", "blurb", "textarea", default_value="", maxlength="", rows=3, placeholder="", new_lines=""),
  f("ser_lead", "Hero / product lead sentence", "hero_lead", "textarea", default_value="", maxlength="", rows=2, placeholder="", new_lines=""),
  txt("ser_cta", "Panel button label", "cta"),
  img("ser_bg", "Panel background image", "panel_image", "Full-bleed image above the text (Lowrider Anthems)."),
  img("ser_logo", "Panel logo", "panel_logo", "Centered logo on a dark panel (My Philosophy)."),
  txt("ser_story_h", "Product story — heading", "story_heading"),
  f("ser_story_t", "Product story — text", "story_text", "textarea", default_value="", maxlength="", rows=4, placeholder="", new_lines=""),
 ], {"param": "taxonomy", "operator": "==", "value": "product_cat"}))

w("group_block_hero", grp("block_hero", "Hero carousel", [
  txt("h_out", "Badge — in stock", "badge_out", "Out now"), txt("h_pre", "Badge — pre-order", "badge_pre", "Pre-order"),
  txt("h_prelead", "Pre-order lead", "pre_lead", "Pre-orders are open. Secure your copy before the run is pressed."),
  txt("h_cta_v", "Button — view", "cta_view", "View release"), txt("h_cta_p", "Button — pre-order", "cta_pre", "Pre-order now"),
  txt("h_cta_a", "Button — all releases", "cta_all", "All releases"), txt("h_cta_u", "Button link (empty = product page)", "cta_url", ""),
 ], block_loc("hero-carousel")))
w("group_block_series", grp("block_series", "Series panels", [txt("s_eyebrow", "Eyebrow", "eyebrow", "Two series"), txt("s_heading", "Heading", "heading", "Pick your side of the map.")], block_loc("series-panels")))
w("group_block_catalogue", grp("block_catalogue", "Release catalogue", [txt("c_eyebrow", "Eyebrow", "eyebrow", "Catalogue"), txt("c_heading", "Heading", "heading", "All releases"), txt("c_all", "Filter — all", "filter_all", "All")], block_loc("release-catalogue")))
w("group_block_wholesale", grp("block_wholesale", "Wholesale", [
  txt("w_eyebrow", "Eyebrow", "eyebrow", "For record shops & distributors"), txt("w_heading", "Heading", "heading", "Stock the series in your shop."),
  f("w_lead", "Lead", "lead", "textarea", rows=3, new_lines="", default_value="Wholesale price list, pre-order windows and shipping options on request. We ship worldwide; the buyer pays freight."),
  f("w_stats", "Minimum quantities", "stats", "repeater", layout="table", min=0, max=4, button_label="Add row", collapsed="", rows_per_page=20, sub_fields=[
     {"key": "field_7i_w_stat_n", "label": "Number", "name": "number", "aria-label": "", "type": "text", "instructions": "", "required": 0, "conditional_logic": 0, "wrapper": {"width": "30", "class": "", "id": ""}, "default_value": "", "maxlength": "", "placeholder": "", "prepend": "", "append": "", "parent_repeater": "field_7i_w_stats"},
     {"key": "field_7i_w_stat_l", "label": "Label", "name": "label", "aria-label": "", "type": "text", "instructions": "", "required": 0, "conditional_logic": 0, "wrapper": {"width": "70", "class": "", "id": ""}, "default_value": "", "maxlength": "", "placeholder": "", "prepend": "", "append": "", "parent_repeater": "field_7i_w_stats"}]),
  txt("w_btn", "Button label", "button_label", "Request the wholesale list"), f("w_email", "Contact e-mail", "email", "email", default_value="peet@7inchrare.com", placeholder="", prepend="", append=""),
 ], block_loc("wholesale")))
w("group_block_more", grp("block_more", "More from the series", [txt("m_eyebrow", "Eyebrow", "eyebrow", "Keep digging"), txt("m_heading", "Heading", "heading", "More from the series")], block_loc("more-from-series")))
w("group_block_tracks", grp("block_tracks", "Track list", [txt("t_play", "Play label", "play_label", "Play preview"), txt("t_pause", "Pause label", "pause_label", "Pause")], block_loc("release-tracks")))
